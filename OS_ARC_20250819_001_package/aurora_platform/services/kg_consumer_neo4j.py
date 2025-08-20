from confluent_kafka import Consumer, KafkaException
from py2neo import Graph
import json, hashlib

BOOTSTRAP = "localhost:9092"
BATCH_SIZE = 500
POLL_TIMEOUT = 1.0

graph = Graph("bolt://localhost:7687", auth=("neo4j","password"))

MERGE_ENTITIES = """
UNWIND $rows AS r
MERGE (e:Entity {id: r.entity_id})
SET e.entity_type = r.entity_type
SET e += r.properties
"""
MERGE_RELATIONS = """
UNWIND $rows AS r
MATCH (a:Entity {id:r.from_id}), (b:Entity {id:r.to_id})
MERGE (a)-[rel:REL {id:r.relation_id}]->(b)
SET rel.type = r.rel_type
SET rel += r.properties
"""

def event_hash(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def run():
    consumer = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": "kg-writer",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "max.poll.interval.ms": 300000
    })
    consumer.subscribe(["eventos.kg.entidades-extraidas","eventos.kg.relacoes-extraidas"])

    entities, relations = [], []
    try:
        while True:
            msg = consumer.poll(POLL_TIMEOUT)
            if msg is None:
                if entities or relations:
                    flush_batches(consumer, entities, relations)
                    entities.clear(); relations.clear()
                continue
            if msg.error():
                raise KafkaException(msg.error())

            payload = msg.value()
            if isinstance(payload, (bytes, bytearray)):
                payload = json.loads(payload)
            payload["_hash"] = event_hash(payload)

            if msg.topic() == "eventos.kg.entidades-extraidas":
                entities.append(payload)
            else:
                relations.append(payload)

            if (len(entities) + len(relations)) >= BATCH_SIZE:
                flush_batches(consumer, entities, relations)
                entities.clear(); relations.clear()
    finally:
        consumer.close()

def flush_batches(consumer, entities, relations):
    tx = graph.begin()
    if entities:
        tx.run(MERGE_ENTITIES, rows=entities)
    if relations:
        tx.run(MERGE_RELATIONS, rows=relations)
    tx.commit()
    consumer.commit(asynchronous=False)

if __name__ == "__main__":
    run()
