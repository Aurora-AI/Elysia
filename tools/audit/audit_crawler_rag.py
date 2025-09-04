#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "artifacts" / "audit_crawler_rag.json"
MD = ROOT / "artifacts" / "audit_crawler_rag.md"
REPORT.parent.mkdir(parents=True, exist_ok=True)

# Heurísticas
PLAYWRIGHT_IMPORTS = (
    "from playwright.sync_api import",
    "from playwright.async_api import",
    "import playwright",
)
NON_DOM_IMPORTS = ("requests", "httpx", "urllib", "aiohttp", "selenium")  # selenium ≠ nosso alvo
HTML_PARSERS = ("bs4", "BeautifulSoup", "lxml", "selectolax")
RAG_PIPELINE_HINTS = ("pipeline", "retriever", "chunk", "embed", "qdrant", "faiss", "chromadb")
QDRANT_IMPORTS = ("import qdrant_client", "from qdrant_client", "QdrantClient")
KAFKA_IMPORTS = ("from kafka import", "import confluent_kafka", "from confluent_kafka import")
NEO4J_IMPORTS = ("from neo4j import", "import neo4j")
TEST_HINTS = ("tests/modules/crawler", "tests/modules/rag", "tests/e2e")

PATHS = {
    "crawler_loader": "src/aurora_platform/modules/crawler/loaders/url_loader.py",
    "rag_pipeline": "src/aurora_platform/modules/rag/pipeline.py",
    "rag_store": "src/aurora_platform/modules/rag/store.py",
    "rag_config": "src/aurora_platform/modules/rag/config.py",
    "e2e_test": "tests/e2e/test_kafka_to_kg.py",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def file_exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def scan_imports(code: str, needles: tuple[str, ...]) -> bool:
    return any(n in code for n in needles)


def grep(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def summarize_file(rel: str) -> dict[str, Any]:
    p = ROOT / rel
    info: dict[str, Any] = {"path": rel, "exists": p.exists()}
    if not p.exists():
        return info
    code = read_text(p)
    info["lines"] = len(code.splitlines())
    info["imports_playwright"] = scan_imports(code, PLAYWRIGHT_IMPORTS)
    info["imports_non_dom_http"] = scan_imports(code, NON_DOM_IMPORTS)
    info["imports_html_parsers"] = scan_imports(code, HTML_PARSERS)
    info["contains_chunk_terms"] = "chunk" in code.lower()
    info["imports_qdrant"] = scan_imports(code, QDRANT_IMPORTS)
    info["imports_kafka"] = scan_imports(code, KAFKA_IMPORTS)
    info["imports_neo4j"] = scan_imports(code, NEO4J_IMPORTS)
    # Heurística Chunk-on-Demand (pipeline): buscar 2 estágios (doc -> chunk)
    info["has_two_stage_query"] = all(
        key in code.lower() for key in ("top", "doc", "chunk")
    ) or grep(r"(two[-\s]?stage|stage\s*1|stage\s*2)", code)
    # Coleção Qdrant sugerida
    info["mentions_chunks_collection"] = grep(r"chunks?_on_demand|e2e_temp|chunks", code)
    return info


def check_tests_present() -> dict[str, Any]:
    out: dict[str, Any] = {"paths": {}, "any": False}
    for hint in TEST_HINTS:
        p = ROOT / hint
        out["paths"][hint] = p.exists()
        out["any"] = out["any"] or p.exists()
    return out


def docker_compose_services() -> dict[str, Any]:
    f = ROOT / "docker-compose.yml"
    info = {"exists": f.exists(), "mentions": {}}
    if not f.exists():
        return info
    text = read_text(f)
    for key in ["neo4j", "kafka", "qdrant", "postgres", "zookeeper"]:
        info["mentions"][key] = key in text.lower()
    return info


def collect() -> dict[str, Any]:
    data: dict[str, Any] = {"paths": {}, "tests": {}, "compose": {}, "summary": {}}
    for k, v in PATHS.items():
        data["paths"][k] = summarize_file(v)
    data["tests"] = check_tests_present()
    data["compose"] = docker_compose_services()

    # Resumo decisório
    crawler = data["paths"]["crawler_loader"]
    rag = data["paths"]["rag_pipeline"]

    crawler_ready = crawler.get("exists") and crawler.get("imports_playwright")
    rag_two_stage = rag.get("exists") and rag.get("has_two_stage_query")
    rag_qdrant = rag.get("imports_qdrant")

    data["summary"] = {
        "crawler_uses_playwright": bool(crawler_ready),
        "crawler_uses_non_dom_http": bool(crawler.get("imports_non_dom_http")),
        "crawler_needs_refactor": bool(crawler.get("exists")) and not crawler_ready,
        "rag_has_two_stage_query": bool(rag_two_stage),
        "rag_uses_qdrant": bool(rag_qdrant),
        "rag_mentions_chunks_collection": bool(rag.get("mentions_chunks_collection")),
        "tests_present": data["tests"]["any"],
        "compose_has_core_services": all(
            data["compose"]["mentions"].get(s, False) for s in ("neo4j", "kafka", "qdrant")
        ),
    }
    return data


def to_markdown(data: dict[str, Any]) -> str:
    s = ["# Auditoria Crawler & RAG — Relatório\n"]
    # Crawler
    c = data["paths"]["crawler_loader"]
    s += [
        "## Crawler (url_loader.py)\n",
        f"- Arquivo: `{c['path']}` — **{'OK' if c.get('exists') else 'MISSING'}**\n",
        f"- Playwright importado: **{c.get('imports_playwright')}**\n",
        f"- HTTP não-DOM (requests/httpx/etc.): **{c.get('imports_non_dom_http')}**\n",
        f"- Parsers HTML (bs4/lxml/etc.): **{c.get('imports_html_parsers')}**\n",
        f"- Necessita refator DOM: **{data['summary']['crawler_needs_refactor']}**\n",
    ]
    # RAG
    r = data["paths"]["rag_pipeline"]
    s += [
        "\n## RAG (pipeline.py)\n",
        f"- Arquivo: `{r['path']}` — **{'OK' if r.get('exists') else 'MISSING'}**\n",
        f"- Qdrant importado: **{r.get('imports_qdrant')}**\n",
        f"- Heurística 2 etapas (doc→chunk): **{data['summary']['rag_has_two_stage_query']}**\n",
        f"- Menção a coleção de chunks: **{data['summary']['rag_mentions_chunks_collection']}**\n",
    ]
    # Infra/Testes
    s += [
        "\n## Infra & Testes\n",
        f"- docker-compose.yml: **{'OK' if data['compose']['exists'] else 'MISSING'}**\n",
        f"- Compose serviços (neo4j/kafka/qdrant/postgres/zookeeper): {json.dumps(data['compose'].get('mentions', {}), ensure_ascii=False)}\n",
        f"- Pastas de testes presentes: {json.dumps(data['tests']['paths'], ensure_ascii=False)}\n",
    ]
    # Resumo
    s += [
        "\n## Resumo Executável\n",
        f"- Crawler usa Playwright: **{data['summary']['crawler_uses_playwright']}**\n",
        f"- RAG em 2 etapas + Qdrant: **{data['summary']['rag_has_two_stage_query']}** / **{data['summary']['rag_uses_qdrant']}**\n",
        f"- Compose com core (neo4j+kafka+qdrant): **{data['summary']['compose_has_core_services']}**\n",
        f"- Testes existem: **{data['summary']['tests_present']}**\n",
    ]
    return "".join(s)


def main():
    data = collect()
    REPORT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    MD.write_text(to_markdown(data), encoding="utf-8")
    print(f"[OK] Relatórios salvos em:\n- {REPORT}\n- {MD}")


if __name__ == "__main__":
    main()
