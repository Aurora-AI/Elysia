from confluent_kafka import SerializingProducer
import json
import os
import time

# Configuration
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TESTING = os.getenv("TESTING", "0") == "1"


def _delivery_report(err, msg):
    """Callback para confirmação de entrega"""
    if err:
        print(
            f"ERRO ao entregar {msg.topic()}[{msg.partition()}]@{msg.offset()}: {err}")


if TESTING:
    # Testing mode: avoid network calls to Schema Registry / Kafka. Use in-memory/no-op producer.
    class _FakeProducer:
        def __init__(self):
            self._messages = []

        def produce(self, topic, key=None, value=None, on_delivery=None, **_kwargs):
            # store message for inspection if needed; keep behavior synchronous
            self._messages.append((topic, key, value))
            if on_delivery:
                try:
                    on_delivery(None, type(
                        "M", (), {"topic": lambda: topic, "partition": lambda: 0, "offset": lambda: 0}))
                except Exception:
                    pass

        def flush(self, timeout=None):
            return

    # simple JSON serializers that return bytes
    def _json_serializer(value, ctx=None):
        return json.dumps(value).encode("utf-8")

    producer = _FakeProducer()

    def send_entity_upsert(payload: dict):
        producer.produce(topic="kg.entity.upsert", key=payload.get(
            "entity_id"), value=payload, on_delivery=_delivery_report)
        producer.flush()

    def send_relation_upsert(payload: dict):
        producer.produce(topic="kg.relation.upsert",
                         key=payload.get("relation_id"), value=payload)
        producer.flush()

    def send_raw_doc(doc_id: str, content: str, metadata: dict = None):
        payload = {
            "doc_id": doc_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": int(time.time() * 1000)
        }
        producer.produce(topic="crawler.raw_docs", key=doc_id,
                         value=json.dumps(payload))
        producer.flush()

else:
    # Normal mode: use Schema Registry and JSONSerializer
    from confluent_kafka.schema_registry import SchemaRegistryClient
    from confluent_kafka.schema_registry.json_schema import JSONSerializer

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
        "value.serializer": entity_serializer,
        "acks": "all",
        "retries": 3
    })

    def send_entity_upsert(payload: dict):
        producer.produce(topic="kg.entity.upsert",
                         key=payload["entity_id"], value=payload, on_delivery=_delivery_report)
        producer.flush()

    def send_relation_upsert(payload: dict):
        producer_rel = SerializingProducer({
            "bootstrap.servers": BOOTSTRAP,
            "value.serializer": relation_serializer
        })
        producer_rel.produce(topic="kg.relation.upsert",
                             key=payload["relation_id"], value=payload)
        producer_rel.flush()

    def send_raw_doc(doc_id: str, content: str, metadata: dict = None):
        payload = {
            "doc_id": doc_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": int(time.time() * 1000)
        }
        producer.produce(topic="crawler.raw_docs", key=doc_id,
                         value=json.dumps(payload))
        producer.flush()
