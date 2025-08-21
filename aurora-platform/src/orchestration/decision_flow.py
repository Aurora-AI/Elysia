from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Sequence
from collections import Counter

from qdrant_client import QdrantClient
from src.memory.embeddings import encode_one
from src.hrm.engine import evaluate as hrm_evaluate

_TOPK = int(os.getenv("DECISION_TOPK", "5"))


def _qdr() -> QdrantClient:
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY") or None
    return QdrantClient(url=url, api_key=api_key)


def _vector_candidates(client: QdrantClient, query_vec: List[float], limit: int = 32):
    res = client.search(
        collection_name="cases_chunks",
        query_vector=query_vec,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    out = []
    for p in res:
        out.append(p.payload or {})
    return out


def fetch_context(query: str | None = None, numero_processo: str | None = None, top_k: int | None = None) -> List[Dict[str, Any]]:
    """Busca contexto na Memória (Qdrant). Usa vetor por consulta textual; se informado numero_processo, filtra por payload."""
    client = _qdr()
    k = top_k or _TOPK

    qtext = query or numero_processo
    if not qtext:
        return []

    vec = encode_one(qtext).tolist()
    cand = _vector_candidates(client, vec, limit=max(k, 24))

    if numero_processo:
        cand = [c for c in cand if (
            c.get("numero_processo") or "") == numero_processo]

    return cand[:k]


def _majority(values: Sequence[Optional[str]]) -> Optional[str]:
    vals = [v for v in values if isinstance(v, str) and v]
    if not vals:
        return None
    c = Counter(vals).most_common(1)
    return c[0][0] if c else None


def derive_facts(context: List[Dict[str, Any]], extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Heurística simples: agrega metadados dominantes do contexto."""
    tribunais: List[Optional[str]] = [
        (c.get("tribunal") or c.get("jurisdicao")) for c in context
    ]
    classes: List[Optional[str]] = [c.get("classe") for c in context]
    assunto: List[Optional[str]] = [c.get("assunto") for c in context]

    facts = {
        "tribunal": _majority(tribunais),
        "classe": _majority(classes),
        "assunto": _majority(assunto),
    }
    if extra:
        facts.update({k: v for k, v in extra.items() if v is not None})
    return {k: v for k, v in facts.items() if v is not None}


def evaluate_case(
    numero_processo: str | None = None,
    query: str | None = None,
    extra_facts: Dict[str, Any] | None = None,
    top_k: int | None = None,
    rule_set_path: str | None = None,
) -> Dict[str, Any]:
    """Orquestra: Memória → fatos → HRM."""
    ctx = fetch_context(
        query=query, numero_processo=numero_processo, top_k=top_k)
    facts = derive_facts(ctx, extra=extra_facts)
    result = hrm_evaluate(facts=facts, rule_set_path=rule_set_path)
    return {
        "status": "ok",
        "input": {"numero_processo": numero_processo, "query": query, "extra_facts": extra_facts, "top_k": top_k},
        "facts": facts,
        "hrm": result,
        "context_sample": ctx[:3],
    }
