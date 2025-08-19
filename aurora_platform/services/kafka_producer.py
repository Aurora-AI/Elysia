from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import json
import os
import time

SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

schema_registry = SchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

# Load schemas
with open("aurora_platform/events/schemas/kg_entity_upsert.json") as f:
    entity_schema_str = f.read()

with open("aurora_platform/events/schemas/kg_relation_upsert.json") as f:
    relation_schema_str = f.read()

entity_serializer = JSONSerializer(entity_schema_str, schema_registry)
relation_serializer = JSONSerializer(relation_schema_str, schema_registry)

producer = SerializingProducer({
    "bootstrap.servers": BOOTSTRAP,
    "value.serializer": entity_serializer
})

def send_entity_upsert(payload: dict):
    """Envia evento de upsert de entidade com chave = entity_id"""
    producer.produce(topic="kg.entity.upsert", key=payload["entity_id"], value=payload)
    producer.flush()

def send_relation_upsert(payload: dict):
    """Envia evento de upsert de relação com chave = relation_id"""
    producer_rel = SerializingProducer({
        "bootstrap.servers": BOOTSTRAP,
        "value.serializer": relation_serializer
    })
    producer_rel.produce(topic="kg.relation.upsert", key=payload["relation_id"], value=payload)
    producer_rel.flush()

def send_raw_doc(doc_id: str, content: str, metadata: dict = None):
    """Envia documento bruto do crawler"""
    payload = {
        "doc_id": doc_id,
        "content": content,
        "metadata": metadata or {},
        "timestamp": int(time.time() * 1000)
    }
    producer.produce(topic="crawler.raw_docs", key=doc_id, value=json.dumps(payload))
    producer.flush()
