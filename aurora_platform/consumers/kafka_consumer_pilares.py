import json
import os
import time
from typing import Any, Dict, Optional

from confluent_kafka import Consumer, KafkaError, Producer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# DB sync helper
from aurora_platform.core.db_legacy import SessionLocal
from aurora_platform.models import (
    PilarAntropologia, PilarPsicologia, PilarVendas, PilarEstatistica
)

# ========= helpers =========

TOPIC = os.getenv("KAFKA_TOPIC_PILARES", "pilares.upsert")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
GROUP_ID = os.getenv("KAFKA_GROUP_PILARES", "consumer-pilares-v1")

DLQ_TOPIC = os.getenv("CONSUMER_DLQ_TOPIC", "pilares.dlq")
MAX_RETRIES = int(os.getenv("CONSUMER_MAX_RETRIES", "5"))
RETRY_BASE_MS = int(os.getenv("CONSUMER_RETRY_BASE_MS", "500"))

SKIP_NEO4J = os.getenv("SKIP_NEO4J", "true").lower() == "true"
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

try:
    from neo4j import GraphDatabase   # opcional
    HAS_NEO4J = True
except Exception:
    HAS_NEO4J = False


def get_model_for(pilar: str):
    p = (pilar or "").lower()
    if p == "antropologia":
        return PilarAntropologia
    if p == "psicologia":
        return PilarPsicologia
    if p == "vendas":
        return PilarVendas
    if p == "estatistica":
        return PilarEstatistica
    raise ValueError(f"Pilar inválido: {pilar}")

# ========= persistência =========


def upsert_pilar(db: Session, payload: Dict[str, Any]) -> None:
    pilar = payload["pilar"]
    Model = get_model_for(pilar)

    # chave natural: pilar_id
    obj = db.query(Model).filter(Model.pilar_id ==
                                 payload["pilar_id"]).one_or_none()
    if obj is None:
        obj = Model(pilar_id=payload["pilar_id"])
        db.add(obj)

    # mapeamento campos básicos (ajuste conforme seus models)
    obj.titulo = payload.get("titulo")
    obj.descricao = payload.get("descricao")
    obj.fonte = payload.get("fonte")
    obj.referencia_url = payload.get("referencia_url")
    obj.versao = payload.get("versao", 1)
    obj.extra = payload.get("extra")  # se o modelo tiver JSONB

    db.commit()


def ensure_neo4j_nodes(payload: Dict[str, Any], driver) -> None:
    if SKIP_NEO4J or not HAS_NEO4J:
        return
    with driver.session() as session:
        session.execute_write(_merge_pilar_node, payload)


def _merge_pilar_node(tx, payload: Dict[str, Any]):
    cypher = """
    MERGE (p:Pilar {id:$pilar_id})
    SET p.name = $pilar,
        p.titulo = $titulo,
        p.fonte = $fonte,
        p.ref = $referencia_url,
        p.versao = $versao
    """
    tx.run(cypher, **{
        "pilar_id": payload["pilar_id"],
        "pilar": payload["pilar"],
        "titulo": payload.get("titulo"),
        "fonte": payload.get("fonte"),
        "referencia_url": payload.get("referencia_url"),
        "versao": payload.get("versao", 1),
    })


def build_dlq_producer() -> Optional[Producer]:
    try:
        return Producer({"bootstrap.servers": BOOTSTRAP})
    except Exception:
        return None


def send_to_dlq(p: Optional[Producer], msg, reason: str):
    if p is None:
        print(f"[DLQ][DROP] {reason} key={msg.key()}")
        return
    try:
        p.produce(
            topic=DLQ_TOPIC,
            key=msg.key(),
            value=json.dumps({
                "reason": reason,
                "payload": json.loads(msg.value().decode("utf-8")) if msg.value() else None
            }).encode("utf-8"),
            headers=[("dlq_reason", reason.encode("utf-8"))]
        )
        p.flush(5)
    except Exception as e:
        print(f"[DLQ][ERROR] {e}")


def run():
    consumer = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "max.poll.interval.ms": 900000
    })
    consumer.subscribe([TOPIC])

    dlq_producer = build_dlq_producer()

    neo_driver = None
    if not SKIP_NEO4J and HAS_NEO4J:
        from neo4j import GraphDatabase
        neo_driver = GraphDatabase.driver(
            NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

    print(
        f"[START] Consuming {TOPIC} @ {BOOTSTRAP} (group={GROUP_ID}) | SKIP_NEO4J={SKIP_NEO4J}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"[KAFKA][ERROR] {msg.error()}")
                continue

            key = msg.key().decode("utf-8") if msg.key() else None
            raw = msg.value().decode("utf-8") if msg.value() else "{}"

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                send_to_dlq(dlq_producer, msg, "json_decode_error")
                consumer.commit(message=msg, asynchronous=False)
                continue

            # backoff simples
            attempt = 0
            while True:
                try:
                    with SessionLocal() as db:
                        upsert_pilar(db, payload)
                    if neo_driver:
                        ensure_neo4j_nodes(payload, neo_driver)
                    consumer.commit(message=msg, asynchronous=False)
                    if attempt > 0:
                        print(f"[OK][RETRY={attempt}] key={key}")
                    break
                except (IntegrityError, Exception) as e:
                    attempt += 1
                    if attempt > MAX_RETRIES:
                        print(f"[DLQ][MAX_RETRIES] key={key} err={e}")
                        send_to_dlq(dlq_producer, msg,
                                    f"processing_error:{type(e).__name__}")
                        consumer.commit(message=msg, asynchronous=False)
                        break
                    sleep_ms = RETRY_BASE_MS * (2 ** (attempt - 1))
                    print(
                        f"[RETRY {attempt}/{MAX_RETRIES}] key={key} in {sleep_ms}ms err={e}")
                    time.sleep(sleep_ms / 1000.0)

    except KeyboardInterrupt:
        print("[STOP] interrupted by user")
    finally:
        consumer.close()
        if neo_driver:
            neo_driver.close()


if __name__ == "__main__":
    run()
