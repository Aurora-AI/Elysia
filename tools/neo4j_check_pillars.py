#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j Pillars Check (fallback sem cypher-shell)
Autor: Projeto Aurora

Funções:
- Verifica conectividade via Bolt
- Confere constraints essenciais
- Executa sanity checks (labels mínimos e quantidade de índices)

Saída: JSON no stdout
Exit codes:
  0 = OK
  1 = Falha de conexão / credenciais / variáveis ausentes
  2 = Constraints essenciais ausentes
  3 = Sanity checks falharam ou erro em runtime

Observações:
- Respeita variáveis padrão e aliases AURA_*:
  NEO4J_URI / AURA_NEO4J_URI
  NEO4J_USER / AURA_NEO4J_USER
  NEO4J_PASSWORD / AURA_NEO4J_PASSWORD
- Dependência: neo4j>=5.22.0
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

# --- Utilidades de ENV -----------------------------------------------------


def env(name: str, default: str | None = None) -> str:
    """
    Lê a variável de ambiente priorizando AURA_*.
    """
    return os.getenv(name) or os.getenv(f"AURA_{name}") or (default if default is not None else "")


def bool_env(name: str, default: bool = False) -> bool:
    v = env(name, "")
    if v == "":
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}


# --- Dependência do driver Neo4j -------------------------------------------

try:
    from neo4j import GraphDatabase, basic_auth  # type: ignore
except Exception as e:  # pragma: no cover
    # Não conseguimos nem importar o driver → erro de runtime (3).
    print(
        json.dumps(
            {
                "status": "error",
                "stage": "import",
                "error": f"Falha ao importar 'neo4j': {e}",
                "hint": "Instale com: pip install 'neo4j>=5.22.0'",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    sys.exit(3)

# --- Defaults ajustáveis ----------------------------------------------------

DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "neo4j"

# Labels e constraints mínimos esperados — ajuste conforme seu domínio
EXPECTED_LABELS = ["Entity", "Relation"]

EXPECTED_CONSTRAINTS = [
    # UNIQUE CONSTRAINT em (Entity.id)
    {"type": "UNIQUE", "label": "Entity", "properties": [
        "id"], "name_hint": "entity_id_unique"},
    # UNIQUE CONSTRAINT em (Relation.id)
    {"type": "UNIQUE", "label": "Relation", "properties": [
        "id"], "name_hint": "relation_id_unique"},
]

# Sanity mínima: pelo menos 1 índice existente no banco (pode ser qualquer)
MIN_INDEX_COUNT = 1


# --- Driver / Sessão --------------------------------------------------------


def get_driver():
    uri = env("NEO4J_URI", DEFAULT_URI)
    user = env("NEO4J_USER", DEFAULT_USER)
    pwd = env("NEO4J_PASSWORD", DEFAULT_PASSWORD)

    if not uri or not user or not pwd:
        emit_error(
            stage="connectivity",
            error="Variáveis NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD não configuradas.",
            code=1,
        )

    # Pool básico; para ambientes CI, o default é suficiente
    driver = GraphDatabase.driver(uri, auth=basic_auth(user, pwd))
    return driver


def check_connectivity(driver) -> Tuple[bool, str]:
    """
    Verifica conectividade (handshake + query leve de versão).
    Retorna (ok, info_versao_ou_erro)
    """
    try:
        driver.verify_connectivity()
        with driver.session() as s:
            rec = s.run(
                "CALL dbms.components() YIELD name, versions RETURN name, versions"
            ).single()
            version = rec["versions"][0] if rec and rec.get(
                "versions") else "unknown"
        return True, version
    except Exception as e:
        return False, str(e)


# --- Coletas e verificações -------------------------------------------------


def list_constraints(session) -> List[Dict[str, Any]]:
    """
    SHOW CONSTRAINTS (Neo4j 5+) retorna linhas com:
    name, type, entityType, labelsOrTypes, properties, ownedIndex, ...
    """
    result = session.run("SHOW CONSTRAINTS")
    return [r.data() for r in result]


def list_indexes(session) -> List[Dict[str, Any]]:
    result = session.run("SHOW INDEXES")
    return [r.data() for r in result]


def constraint_matches(row: Dict[str, Any], exp: Dict[str, Any]) -> bool:
    typ = (row.get("type") or "").upper()
    labels = row.get("labelsOrTypes") or []
    props = row.get("properties") or []
    return typ == exp["type"] and exp["label"] in labels and all(p in props for p in exp["properties"])


def check_expected_constraints(session) -> Dict[str, Any]:
    have = list_constraints(session)
    missing = []
    for exp in EXPECTED_CONSTRAINTS:
        if not any(constraint_matches(row, exp) for row in have):
            missing.append(exp)
    return {"found_count": len(have), "expected": EXPECTED_CONSTRAINTS, "missing": missing}


def labels_count(session, labels: List[str]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for lbl in labels:
        rec = session.run(f"MATCH (n:`{lbl}`) RETURN count(n) AS c").single()
        out[lbl] = int(rec["c"]) if rec and rec.get("c") is not None else 0
    return out


def do_sanity_checks(session) -> Dict[str, Any]:
    idx = list_indexes(session)
    lbl_counts = labels_count(session, EXPECTED_LABELS)
    return {"indexes_count": len(idx), "labels": lbl_counts}


# --- Emissão estruturada ----------------------------------------------------


def emit_and_exit(payload: Dict[str, Any], code: int) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def emit_error(stage: str, error: str, code: int = 3, extra: Dict[str, Any] | None = None) -> None:
    payload: Dict[str, Any] = {
        "status": "error", "stage": stage, "error": error}
    if extra:
        payload.update(extra)
    emit_and_exit(payload, code)


# --- Main -------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Neo4j Pillars Check (fallback sem cypher-shell) — Projeto Aurora"
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exige ao menos 1 índice (além das constraints) e checa labels mínimos > 0.",
    )
    p.add_argument(
        "--min-indexes",
        type=int,
        default=MIN_INDEX_COUNT,
        help=f"Mínimo de índices exigidos no sanity check (default: {MIN_INDEX_COUNT}).",
    )
    p.add_argument(
        "--require-label",
        action="append",
        default=[],
        help="Label adicional a exigir no sanity (pode repetir a flag várias vezes).",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    # Permite acrescentar labels via CLI ou ENV (AURA_EXTRA_LABELS="Foo,Bar")
    extra_labels_env = [x.strip() for x in env("EXTRA_LABELS", env(
        "AURA_EXTRA_LABELS", "")).split(",") if x.strip()]
    required_labels = list(dict.fromkeys(
        EXPECTED_LABELS + args.require_label + extra_labels_env))  # unique, keep order

    strict_mode = args.strict or bool_env("NEO4J_CHECK_STRICT", False)
    min_indexes = max(0, int(env("NEO4J_MIN_INDEXES", str(args.min_indexes))))

    driver = get_driver()

    ok, info = check_connectivity(driver)
    if not ok:
        emit_error(stage="connectivity", error=info, code=1)

    output: Dict[str, Any] = {"status": "ok", "neo4j_version": info}

    try:
        with driver.session() as session:
            # Constraints
            constraints_info = check_expected_constraints(session)
            output["constraints"] = constraints_info

            # Sanity
            sanity = do_sanity_checks(session)
            # Recalcula labels usando a lista final (com extras)
            sanity["labels"] = labels_count(session, required_labels)
            output["sanity"] = sanity
            output["config"] = {
                "strict": strict_mode,
                "min_indexes": min_indexes,
                "required_labels": required_labels,
            }

            # Avaliação
            if constraints_info["missing"]:
                output["status"] = "warn"
                output["note"] = "Constraints essenciais ausentes."
                emit_and_exit(output, 2)

            if strict_mode:
                # Índices mínimos
                if sanity["indexes_count"] < min_indexes:
                    output["status"] = "warn"
                    output["note"] = f"Menos índices do que o mínimo exigido ({sanity['indexes_count']} < {min_indexes})."
                    emit_and_exit(output, 3)

                # Labels com pelo menos 1 nó (sanidade de dados mínima)
                missing_label_data = [lbl for lbl,
                                      c in sanity["labels"].items() if c == 0]
                if missing_label_data:
                    output["status"] = "warn"
                    output["note"] = f"Labels sem dados: {missing_label_data}"
                    emit_and_exit(output, 3)
            else:
                # Modo não-estrito: apenas alerta suave se não houver nenhum índice
                if sanity["indexes_count"] < 1:
                    output["status"] = "warn"
                    output["note"] = "Nenhum índice encontrado (pode impactar performance)."
                    emit_and_exit(output, 3)

            # Tudo OK
            emit_and_exit(output, 0)

    except SystemExit:
        raise
    except Exception as e:
        emit_error(stage="runtime", error=str(e), code=3)
    finally:
        driver.close()


if __name__ == "__main__":
    sys.exit(main())
