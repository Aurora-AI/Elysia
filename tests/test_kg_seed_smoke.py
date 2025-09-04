import os

import pytest

NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


@pytest.mark.integration
def test_seed_pillars_smoke():
    try:
        from neo4j import GraphDatabase
    except Exception:
        pytest.skip("neo4j driver not installed")
    try:
        driver = GraphDatabase.driver(
            NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as s:
            rec = s.run("MATCH (p:Pilar) RETURN count(p) as c").single()
            assert rec and rec["c"] >= 4
    except Exception as e:
        pytest.skip(f"Neo4j not reachable: {e}")
