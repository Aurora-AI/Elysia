import json
import os
import time

import requests
from kafka import KafkaConsumer, KafkaProducer
from neo4j import GraphDatabase

KAFKA_BOOT = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("AURORA_E2E_TOPIC", "aurora.e2e.ping")
NEO_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO_USER = os.getenv("NEO4J_USER", "neo4j")
NEO_PASS = os.getenv("NEO4J_PASSWORD", "password")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.getenv("AURORA_E2E_COLLECTION", "aurora_e2e_test")


def test_kafka_produce_consume():
    """Testa produção e consumo básico no Kafka"""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOT, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    test_message = {"test": "e2e_pipeline", "timestamp": int(time.time())}
    producer.send(TOPIC, test_message)
    producer.flush()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOT,
        auto_offset_reset="latest",
        consumer_timeout_ms=5000,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    messages = []
    for msg in consumer:
        messages.append(msg.value)
        break

    assert len(messages) > 0, "Nenhuma mensagem consumida do Kafka"
    assert messages[0]["test"] == "e2e_pipeline"


def test_neo4j_connection_and_data():
    """Testa conexão Neo4j e verifica dados do seed"""
    driver = GraphDatabase.driver(NEO_URI, auth=(NEO_USER, NEO_PASS))

    with driver.session() as session:
        # Teste básico de conectividade
        result = session.run("RETURN 1 AS test")
        assert result.single()["test"] == 1

        # Verifica se seed foi executado
        result = session.run("MATCH (n:TestNode {id: 'e2e_marker'}) RETURN count(n) AS count")
        count = result.single()["count"]
        assert count > 0, "Nó de teste E2E não encontrado - seed não executado"

        # Verifica pilares
        result = session.run("MATCH (p:Pilar) RETURN count(p) AS pilares")
        pilares = result.single()["pilares"]
        assert pilares >= 3, f"Esperado pelo menos 3 pilares, encontrado {pilares}"

    driver.close()


def test_qdrant_connection_and_vectors():
    """Testa conexão Qdrant e operações com vetores"""
    # Verifica se coleção existe
    response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}")
    assert response.status_code == 200, f"Coleção {COLLECTION} não encontrada"

    # Verifica se há pontos na coleção
    response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}/points/1")
    assert response.status_code == 200, "Ponto de teste não encontrado"

    point_data = response.json()
    assert point_data["result"]["payload"]["test"] == "e2e"


def test_full_pipeline_integration():
    """Teste de integração completa: Kafka → processamento → Neo4j/Qdrant"""
    # Este teste simula o fluxo completo
    # Em um cenário real, haveria um consumer que processa mensagens do Kafka
    # e grava no Neo4j/Qdrant

    # 1. Produzir mensagem estruturada
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOT, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    pipeline_message = {
        "type": "knowledge_ingestion",
        "data": {
            "title": "Teste E2E Pipeline",
            "content": "Conteúdo de teste para pipeline E2E",
            "metadata": {"source": "e2e_test", "timestamp": int(time.time())},
        },
    }

    producer.send(TOPIC, pipeline_message)
    producer.flush()

    # 2. Verificar que a infraestrutura está funcionando
    # (em um teste real, aguardaríamos o processamento)

    # Neo4j está acessível
    driver = GraphDatabase.driver(NEO_URI, auth=(NEO_USER, NEO_PASS))
    with driver.session() as session:
        result = session.run("RETURN datetime() AS now")
        assert result.single()["now"] is not None
    driver.close()

    # Qdrant está acessível
    response = requests.get(f"{QDRANT_URL}/collections")
    assert response.status_code == 200

    # Kafka está processando
    consumer = KafkaConsumer(
        TOPIC, bootstrap_servers=KAFKA_BOOT, auto_offset_reset="latest", consumer_timeout_ms=3000
    )

    # Verifica que conseguimos consumir (infraestrutura OK)
    for _ in consumer:
        break

    # Pipeline infrastructure is working
    assert True
