from neo4j import GraphDatabase
from typing import Dict


class Neo4jClient:
    def __init__(self, uri: str, user: str, pwd: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        self._driver.close()

    def ensure_constraints(self):
        cyphers = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pilar) REQUIRE p.slug IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pilar) REQUIRE p.name IS UNIQUE"
        ]
        with self._driver.session() as s:
            for c in cyphers:
                s.run(c)

    def upsert_pilar(self, payload: Dict):
        """
        payload: { slug, name, fonte?, metadata? }
        """
        cy = """
        MERGE (p:Pilar {slug: $slug})
        SET  p.name = $name,
             p.fonte = coalesce($fonte, p.fonte),
             p.updated_at = datetime(),
             p += coalesce($metadata, {})
        RETURN p.slug AS slug
        """
        with self._driver.session() as s:
            s.run(cy, **{
                "slug": payload["slug"],
                "name": payload["name"],
                "fonte": payload.get("fonte"),
                "metadata": payload.get("metadata", {})
            })
