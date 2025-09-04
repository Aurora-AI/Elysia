"""Seed minimal KG nodes and constraints into Neo4j.

Usage:
  export NEO4J_URL=bolt://localhost:7687
  export NEO4J_USER=neo4j
  export NEO4J_PASSWORD=password
  python scripts/neo4j_seed.py

This script is idempotent and will create uniqueness constraints and four Pilar nodes.
"""
from __future__ import annotations

import os

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover - optional dependency
    raise SystemExit("neo4j-driver is required: pip install neo4j")


NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


def _constraints(tx):
    # Create uniqueness constraint on Pilar.id (if not exists)
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pilar) REQUIRE (p.id) IS UNIQUE")


def _create_pilar(tx, pilar_id: str, name: str, titulo: str, descricao: str):
    cypher = """
    MERGE (p:Pilar {id:$id})
    ON CREATE SET p.name = $name, p.titulo = $titulo, p.descricao = $descricao
    ON MATCH SET p.name = $name
    RETURN p
    """
    tx.run(cypher, id=pilar_id, name=name, titulo=titulo, descricao=descricao)


def seed(pilares: list[dict]):
    driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            session.execute_write(_constraints)
            for p in pilares:
                session.execute_write(_create_pilar, p["id"], p["name"], p.get(
                    "titulo", ""), p.get("descricao", ""))
    finally:
        driver.close()


DEFAULT_PILARES = [
    {"id": "ANTROPOLOGIA", "name": "antropologia",
        "titulo": "Antropologia", "descricao": "Pilar antropologia"},
    {"id": "PSICOLOGIA", "name": "psicologia",
        "titulo": "Psicologia", "descricao": "Pilar psicologia"},
    {"id": "VENDAS", "name": "vendas",
        "titulo": "Vendas", "descricao": "Pilar vendas"},
    {"id": "ESTATISTICA", "name": "estatistica",
        "titulo": "Estatística", "descricao": "Pilar estatística"},
]


if __name__ == "__main__":
    print(f"Connecting to Neo4j at {NEO4J_URL} as {NEO4J_USER}")
    seed(DEFAULT_PILARES)
    print("Seed completed")
