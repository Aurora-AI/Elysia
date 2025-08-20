from confluent_kafka import Consumer
from py2neo import Graph
import json
import os

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP,
    "group.id": "kg-writer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True
})
consumer.subscribe(["kg.entity.upsert", "kg.relation.upsert"])

MERGE_ENTITY = """
MERGE (e:Entity {id:$entity_id})
SET e += $properties, e.entity_type=$entity_type
"""

MERGE_REL = """
MATCH (a:Entity {id:$from_id}), (b:Entity {id:$to_id})
MERGE (a)-[r:REL {id:$relation_id, type:$rel_type}]->(b)
SET r += $properties
"""

def handle_entity(msg):
    """Processa evento de entidade e aplica no Neo4j"""
    v = json.loads(msg.value()) if isinstance(msg.value(), str) else msg.value()
    graph.run(MERGE_ENTITY, **{
        "entity_id": v["entity_id"],
        "entity_type": v["entity_type"],
        "properties": v.get("properties", {})
    })
    print(f"Entity upserted: {v['entity_id']}")

def handle_relation(msg):
    """Processa evento de relação e aplica no Neo4j"""
    v = json.loads(msg.value()) if isinstance(msg.value(), str) else msg.value()
    graph.run(MERGE_REL, **{
        "relation_id": v["relation_id"],
        "from_id": v["from_id"],
        "to_id": v["to_id"],
        "rel_type": v["rel_type"],
        "properties": v.get("properties", {})
    })
    print(f"Relation upserted: {v['relation_id']}")

def run_consumer():
    """Loop principal do consumer"""
    print("Starting KG consumer...")
    while True:
        msg = consumer.poll(1.0)
        if not msg:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        if msg.topic() == "kg.entity.upsert":
            handle_entity(msg)
        elif msg.topic() == "kg.relation.upsert":
            handle_relation(msg)

if __name__ == "__main__":
    run_consumer()
