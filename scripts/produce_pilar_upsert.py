import json
import os

from confluent_kafka import Producer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "PILAR_UPSERT")

p = Producer({"bootstrap.servers": BOOTSTRAP})

payload = {
    "entity_type": "Pilar",
    "slug": "antropologia",
    "name": "Antropologia",
    "fonte": "DeepSeek/DeepResearch",
    "metadata": {"descricao": "Base cultural e contexto organizacional"},
    "ts": "2025-08-19T18:00:00Z",
}


def delivery(err, msg):
    if err:
        print(f"❌ delivery failed: {err}")
    else:
        print(f"✅ delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")


p.produce(TOPIC, json.dumps(payload).encode("utf-8"), callback=delivery)
p.flush()
