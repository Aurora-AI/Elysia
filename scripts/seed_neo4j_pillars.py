import os
from typing import List, Dict
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test")

PILARES: List[Dict] = [
    {"name": "Antropologia", "slug": "antropologia",
        "fonte": "DeepSeek/DeepResearch"},
    {"name": "Psicologia",   "slug": "psicologia",
        "fonte": "DeepSeek/DeepResearch"},
    {"name": "Vendas",       "slug": "vendas",
        "fonte": "DeepSeek/DeepResearch"},
    {"name": "Estatística",  "slug": "estatistica",
        "fonte": "DeepSeek/DeepResearch"},
]

CONSTRAINTS = [
    # Neo4j 5+ syntax
    "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pilar) REQUIRE p.slug IS UNIQUE",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pilar) REQUIRE p.name IS UNIQUE"
]

MERGE_PILAR = """
MERGE (p:Pilar {slug: $slug})
SET p.name = $name,
    p.fonte = $fonte,
    p.updated_at = datetime()
RETURN p.slug AS slug
"""

# Relacionamentos "convergência" básicos (opcional, seguro repetir: MERGE)
REL_EDGES = [
    ("antropologia", "vendas",       "INFLUENCES"),
    ("psicologia",   "vendas",       "SUPPORTS"),
    ("estatistica",  "vendas",       "SUPPORTS"),
    ("antropologia", "psicologia",   "CONTEXTS"),
]

MERGE_REL = """
MATCH (a:Pilar {slug: $from}), (b:Pilar {slug: $to})
MERGE (a)-[r:%s]->(b)
ON CREATE SET r.created_at = datetime()
ON MATCH  SET r.updated_at = datetime()
RETURN type(r) AS rel
"""


def run():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as sess:
        # constraints
        for c in CONSTRAINTS:
            sess.run(c)
        # pillars
        for p in PILARES:
            sess.run(MERGE_PILAR, **p)
        # relations
        for f, t, rel in REL_EDGES:
            sess.run(MERGE_REL % rel, **{"from": f, "to": t})
    driver.close()
    print("✅ Neo4j seed concluído: pilares + constraints + relações básicas.")


if __name__ == "__main__":
    run()
