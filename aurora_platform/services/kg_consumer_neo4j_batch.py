from confluent_kafka import Consumer, KafkaException
from py2neo import Graph
import json
import os
import time
import hashlib

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
BATCH_SIZE = int(os.getenv("KG_BATCH_SIZE", "500"))
POLL_TIMEOUT = float(os.getenv("KG_POLL_TIMEOUT", "1.0"))

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

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
    """Gera hash do evento para controle de idempotência"""
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def flush_batches(consumer, entities, relations):
    """Aplica lotes no Neo4j com transação"""
    start_time = time.time()
    tx = graph.begin()
    try:
        if entities:
            tx.run(MERGE_ENTITIES, rows=entities)
            print(f"Batch entities: {len(entities)}")
        if relations:
            tx.run(MERGE_RELATIONS, rows=relations)
            print(f"Batch relations: {len(relations)}")
        tx.commit()
        consumer.commit(asynchronous=False)
        elapsed = (time.time() - start_time) * 1000
        print(f"Batch committed in {elapsed:.1f}ms")
    except Exception as e:
        tx.rollback()
        print(f"Batch failed: {e}")
        raise

def run_consumer():
    """Loop principal do consumer com processamento em lote"""
    consumer = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": "kg-writer-batch",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "max.poll.interval.ms": 300000
    })
    consumer.subscribe(["kg.entity.upsert", "kg.relation.upsert"])

    entities, relations = [], []
    processed = 0

    print(f"Starting KG batch consumer (batch_size={BATCH_SIZE})...")

    try:
        while True:
            msg = consumer.poll(POLL_TIMEOUT)
            if msg is None:
                if entities or relations:
                    flush_batches(consumer, entities, relations)
                    processed += len(entities) + len(relations)
                    entities.clear()
                    relations.clear()
                continue

            if msg.error():
                raise KafkaException(msg.error())

            v = json.loads(msg.value()) if isinstance(msg.value(), (bytes, bytearray)) else msg.value()
            v["_hash"] = event_hash(v)

            if msg.topic() == "kg.entity.upsert":
                entities.append(v)
            else:
                relations.append(v)

            if (len(entities) + len(relations)) >= BATCH_SIZE:
                flush_batches(consumer, entities, relations)
                processed += len(entities) + len(relations)
                print(f"Total processed: {processed}")
                entities.clear()
                relations.clear()

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_consumer()
