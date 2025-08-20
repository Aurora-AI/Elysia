import json
import os
import signal
import sys
import time
from typing import List, Dict, Optional

from confluent_kafka import Consumer, KafkaException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aurora_platform.consumers.config import (
    KAFKA_BOOTSTRAP, KAFKA_GROUP_ID, KAFKA_TOPIC,
    DATABASE_URL, NEO4J_URI, NEO4J_USER, NEO4J_PASS,
    POLL_TIMEOUT_S, BATCH_SIZE, LOG_EVERY_N
)
from aurora_platform.db.repo_pilares import upsert_pilar_basico

# --- Flags de operação ---
SKIP_NEO4J = os.getenv("SKIP_NEO4J", "false").lower() in {"1", "true", "yes"}
STARTUP_MAX_RETRIES = int(os.getenv("STARTUP_MAX_RETRIES", "20"))
STARTUP_BACKOFF_SEC = float(os.getenv("STARTUP_BACKOFF_SEC", "1.5"))

# --- Estado de parada ---
_stop = False


def _sig_handler(sig, frame):
    global _stop
    _stop = True


signal.signal(signal.SIGINT, _sig_handler)
signal.signal(signal.SIGTERM, _sig_handler)

# --- Neo4j lazy import (só se não pular) ---
Neo4jClient = None


def _import_neo4j_client():
    global Neo4jClient
    if Neo4jClient is None:
        from aurora_platform.graph.neo4j_client import Neo4jClient as _C
        Neo4jClient = _C
    return Neo4jClient


def _retry(fn, what: str, max_retries: int, base_sleep: float):
    """Retry com backoff exponencial simples."""
    attempt = 0
    last_err: Optional[Exception] = None
    while attempt < max_retries and not _stop:
        try:
            return fn()
        except Exception as e:
            last_err = e
            sleep_s = base_sleep * (2 ** attempt)
            print(
                f"[startup] {what} indisponível (tentativa {attempt+1}/{max_retries}): {e}. Retry em {sleep_s:.1f}s…", file=sys.stderr)
            time.sleep(sleep_s)
            attempt += 1
    if last_err:
        raise last_err


def _build_consumer() -> Consumer:
    def _mk():
        c = Consumer({
            "bootstrap.servers": KAFKA_BOOTSTRAP,
            "group.id": KAFKA_GROUP_ID,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "max.poll.interval.ms": 300000
        })
        # sanity: lista tópicos (não obrigatório, mas força handshake)
        md = c.list_topics(timeout=3.0)
        _ = md.topics
        return c
    return _retry(_mk, "Kafka", STARTUP_MAX_RETRIES, STARTUP_BACKOFF_SEC)


def _build_db_session():
    def _mk():
        engine = create_engine(DATABASE_URL, future=True)
        # teste de conexão leve
        with engine.connect() as _:
            pass
        return sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return _retry(_mk, "Postgres", STARTUP_MAX_RETRIES, STARTUP_BACKOFF_SEC)


def _build_neo_client():
    if SKIP_NEO4J:
        return None

    def _mk():
        C = _import_neo4j_client()
        neo = C(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
        neo.ensure_constraints()
        return neo
    return _retry(_mk, "Neo4j", STARTUP_MAX_RETRIES, STARTUP_BACKOFF_SEC)


def handle_pilar(db_sess, neo, msg_value: Dict):
    if msg_value.get("entity_type") != "Pilar":
        return

    for r in ("slug", "name"):
        if r not in msg_value:
            raise ValueError(f"Mensagem inválida: falta campo '{r}'")

    # 1) Postgres
    upsert_pilar_basico(db_sess, msg_value)

    # 2) Neo4j (opcional)
    if neo is not None:
        neo.upsert_pilar(msg_value)


def _flush(events: List[Dict], Session, neo):
    db = Session()
    try:
        for e in events:
            handle_pilar(db, neo, e)
        db.commit()
    except Exception as ex:
        db.rollback()
        print(f"[Consumer] erro no batch: {ex}", file=sys.stderr)
        raise
    finally:
        db.close()


def run():
    consumer = _build_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    Session = _build_db_session()
    neo = _build_neo_client()

    buffered: List[Dict] = []
    processed = 0
    try:
        print(f"[Consumer] iniciado. SKIP_NEO4J={SKIP_NEO4J}")
        while not _stop:
            msg = consumer.poll(POLL_TIMEOUT_S)
            if msg is None:
                if buffered:
                    _flush(buffered, Session, neo)
                    consumer.commit(asynchronous=False)
                    processed += len(buffered)
                    print(
                        f"[Consumer] flushed lote: {processed} mensagens processadas")
                    buffered.clear()
                continue
            if msg.error():
                raise KafkaException(msg.error())

            val = msg.value()
            if isinstance(val, (bytes, bytearray)):
                val = json.loads(val.decode("utf-8"))
            elif isinstance(val, str):
                val = json.loads(val)

            buffered.append(val)
            if len(buffered) >= BATCH_SIZE:
                _flush(buffered, Session, neo)
                consumer.commit(asynchronous=False)
                processed += len(buffered)
                if processed % LOG_EVERY_N == 0:
                    print(f"[Consumer] processados={processed}")
                buffered.clear()
    finally:
        try:
            if neo is not None:
                neo.close()
        except Exception:
            pass
        consumer.close()


if __name__ == "__main__":
    run()
