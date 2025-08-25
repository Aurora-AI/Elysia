#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed dos Pilares no Neo4j (idempotente).
- Suporta env aliases: AURA_NEO4J_* e NEO4J_* (fallback).
- Lê arquivo Cypher e executa em transação única.
"""
from __future__ import annotations

import os
import sys
import pathlib
from typing import Tuple

try:
    from neo4j import GraphDatabase, basic_auth
except Exception:  # pragma: no cover - optional runtime dependency
    raise SystemExit("neo4j-driver is required: pip install neo4j")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CYPHER = ROOT / "seeds" / "seed_pillars.cypher"


def getenv_alias(key_aura: str, key_std: str, default: str | None = None) -> str | None:
    v = os.getenv(key_aura)
    if v is not None and v != "":
        return v
    v = os.getenv(key_std)
    if v is not None and v != "":
        return v
    return default


def resolve_creds() -> Tuple[str, str, str]:
    uri = getenv_alias("AURA_NEO4J_URI", "NEO4J_URI", "bolt://localhost:7687")
    user = getenv_alias("AURA_NEO4J_USERNAME", "NEO4J_USERNAME", getenv_alias(
        "AURA_NEO4J_USER", "NEO4J_USER", "neo4j"))
    pwd = getenv_alias("AURA_NEO4J_PASSWORD", "NEO4J_PASSWORD", "neo4j")
    return uri, user, pwd


def load_cypher(path: pathlib.Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo Cypher não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def main(cypher_file: str | None = None) -> int:
    cypher_path = pathlib.Path(cypher_file) if cypher_file else DEFAULT_CYPHER
    stmt = load_cypher(cypher_path)

    uri, user, pwd = resolve_creds()
    print(f"[seed] Conectando em {uri} como '{user}'...")
    try:
        # TLS automático: se o esquema tiver "+s" (neo4j+s:// ou bolt+s://),
        # o driver habilita criptografia; local (bolt://) segue sem TLS.
        secure = uri.startswith(("neo4j+s://", "bolt+s://"))
        if secure:
            driver = GraphDatabase.driver(uri, auth=basic_auth(user, pwd))
        else:
            driver = GraphDatabase.driver(
                uri, auth=basic_auth(user, pwd), encrypted=False)
    except Exception as e:
        print(f"[seed] Falha ao inicializar driver: {e}", file=sys.stderr)
        return 2

    try:
        with driver.session() as session:
            def run_tx(tx):
                tx.run(stmt)
            session.execute_write(run_tx)
            print("[seed] Seed aplicado com sucesso (idempotente).")
    except Exception as e:
        print(f"[seed] ERRO executando seed: {e}", file=sys.stderr)
        return 3
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    cypher_arg = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(main(cypher_arg))
