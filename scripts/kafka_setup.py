#!/usr/bin/env python3
"""
Script para configurar tópicos Kafka e registrar schemas
"""
import os

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.schema_registry import SchemaRegistryClient

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")

# Configuração de tópicos
TOPICS = [
    {"name": "crawler.raw_docs", "partitions": 3, "replication": 1, "retention": "24h"},
    {"name": "crawler.cleaned_docs", "partitions": 3, "replication": 1, "retention": "7d"},
    {"name": "kg.entity.upsert", "partitions": 6, "replication": 1, "cleanup": "compact"},
    {"name": "kg.relation.upsert", "partitions": 6, "replication": 1, "cleanup": "compact"},
    {"name": "kg.deprecations", "partitions": 3, "replication": 1, "retention": "30d"},
    {"name": "index.embed", "partitions": 3, "replication": 1, "retention": "1h"},
    {"name": "index.upsert", "partitions": 6, "replication": 1, "retention": "7d"},
    {"name": "rag.querylog", "partitions": 3, "replication": 1, "retention": "30d"},
    {"name": "rag.answerlog", "partitions": 3, "replication": 1, "retention": "30d"},
]

def create_topics():
    """Cria tópicos Kafka"""
    admin = AdminClient({"bootstrap.servers": BOOTSTRAP})

    new_topics = []
    for topic_config in TOPICS:
        config = {}
        if "retention" in topic_config:
            config["retention.ms"] = str(parse_retention(topic_config["retention"]))
        if "cleanup" in topic_config:
            config["cleanup.policy"] = topic_config["cleanup"]

        new_topics.append(NewTopic(
            topic=topic_config["name"],
            num_partitions=topic_config["partitions"],
            replication_factor=topic_config["replication"],
            config=config
        ))

    futures = admin.create_topics(new_topics)
    for topic, future in futures.items():
        try:
            future.result()
            print(f"✅ Tópico criado: {topic}")
        except Exception as e:
            print(f"❌ Erro ao criar {topic}: {e}")

def parse_retention(retention_str):
    """Converte string de retenção para ms"""
    if retention_str.endswith("h"):
        return int(retention_str[:-1]) * 3600 * 1000
    elif retention_str.endswith("d"):
        return int(retention_str[:-1]) * 24 * 3600 * 1000
    return int(retention_str)

def register_schemas():
    """Registra schemas no Schema Registry"""
    client = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

    schemas = [
        ("kg_entity_upsert", "aurora_platform/events/schemas/kg_entity_upsert.json"),
        ("kg_relation_upsert", "aurora_platform/events/schemas/kg_relation_upsert.json"),
    ]

    for subject, schema_file in schemas:
        try:
            with open(schema_file) as f:
                schema_str = f.read()

            client.register_schema(subject, {"type": "JSON", "schema": schema_str})
            print(f"✅ Schema registrado: {subject}")
        except Exception as e:
            print(f"❌ Erro ao registrar {subject}: {e}")

if __name__ == "__main__":
    print("🚀 Configurando Kafka + Schema Registry...")
    create_topics()
    register_schemas()
    print("✅ Setup completo!")
