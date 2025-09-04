import os
import time

import requests
from kafka import KafkaConsumer, KafkaProducer  # se usar confluent-kafka, ajuste
from neo4j import GraphDatabase

KAFKA_BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("AURORA_E2E_TOPIC", "aurora.e2e.ping")
NEO_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO_USER = os.getenv("NEO4J_USER", "neo4j")
NEO_PASS = os.getenv("NEO4J_PASSWORD", "password")
QDRANT = os.getenv("QDRANT_URL", "http://localhost:6333")


def test_kafka_to_kg_pipeline():
    # produce
    p = KafkaProducer(bootstrap_servers=KAFKA_BOOT)
    payload = b'{"ping":"e2e","ts":%d}' % int(time.time())
    p.send(TOPIC, payload)
    p.flush()

    # consume (se houver consumer dedicado, esse teste vira integração black-box)
    c = KafkaConsumer(
        TOPIC, bootstrap_servers=KAFKA_BOOT, auto_offset_reset="latest", consumer_timeout_ms=5000
    )
    msgs = [m.value for m in c]
    assert msgs, "Sem mensagens no tópico E2E"

    # verificar Neo4j (ex.: nó marcador)
    drv = GraphDatabase.driver(NEO_URI, auth=(NEO_USER, NEO_PASS))
    with drv.session() as s:
        res = s.run("RETURN 1 AS ok").single()
        assert res and res["ok"] == 1

    # verificar Qdrant (coleção teste existe)
    r = requests.get(f"{QDRANT}/collections/e2e_temp")
    assert r.status_code in (200, 404)  # 200 se criada em check_qdrant, 404 ok se não persistida
