from __future__ import annotations

import os

from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASSWORD", "password")


def upsert_page(tx, url: str, status: int):
    tx.run(
        "MERGE (p:Page {url:$url}) " "SET p.status=$status, p.updatedAt=timestamp()",
        url=url,
        status=status,
    )


def upsert_link(tx, src: str, dst: str):
    tx.run(
        "MERGE (a:Page {url:$src}) " "MERGE (b:Page {url:$dst}) " "MERGE (a)-[:LINKS_TO]->(b)",
        src=src,
        dst=dst,
    )


def save_crawl(url: str, status: int, links: list[str]) -> None:
    drv = GraphDatabase.driver(URI, auth=(USER, PASS))
    with drv.session() as s:
        s.write_transaction(upsert_page, url, status)
        for link in links:
            s.write_transaction(upsert_link, url, link)
    drv.close()
