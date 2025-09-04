import os
from typing import Any

from fastapi import FastAPI, Query
from pydantic import BaseModel
from qdrant_client import QdrantClient
from rank_bm25 import BM25Okapi

# qdrant models are not required directly here
from src.memory.embeddings import encode_one

app = FastAPI(title="Aurora Memory Search (Hybrid)")


def qdr():
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY") or None
    return QdrantClient(url=url, api_key=api_key)


ALPHA = float(os.getenv("HYBRID_ALPHA", "0.5"))


class SearchResult(BaseModel):
    id: str
    score: float
    payload: dict[str, Any]


def vector_search(client: QdrantClient, query: str, k: int = 50):
    vec = encode_one(query).tolist()
    res = client.search(
        collection_name="cases_chunks",
        query_vector=vec,
        limit=k,
        with_payload=True,
        with_vectors=False
    )
    # Retorna (id, score, payload, text) para uso no BM25 local
    out = []
    for p in res:
        pid = str(p.id)
        score = float(p.score or 0.0)
        payload = p.payload or {}
        text = payload.get("text", "")
        out.append((pid, score, payload, text))
    return out


def bm25_scores(candidates: list[tuple], query: str):
    texts = [t[3] for t in candidates]
    if not texts:
        return []
    tokenized = [t.split() for t in texts]
    bm25 = BM25Okapi(tokenized)
    qtok = query.split()
    scores = bm25.get_scores(qtok)
    mx = max(scores) if scores else 1.0
    return [(float(s) / float(mx)) if mx > 0 else 0.0 for s in scores]


@app.get("/search", response_model=list[SearchResult])
def search(query: str = Query(...), k: int = Query(10, ge=1, le=100), alpha: float | None = Query(None)):
    client = qdr()
    cand = vector_search(client, query, k=max(k, 50))
    if not cand:
        return []
    bm = bm25_scores(cand, query)
    a = ALPHA if alpha is None else float(alpha)
    max_vec = max([c[1] for c in cand]) or 1.0

    blended = []
    for i, (pid, vscore, payload, _text) in enumerate(cand):
        v_norm = float(vscore) / float(max_vec)
        l_norm = bm[i] if i < len(bm) else 0.0
        final = a * v_norm + (1.0 - a) * l_norm
        blended.append((pid, final, payload))

    blended.sort(key=lambda x: x[1], reverse=True)
    top = blended[:k]
    return [SearchResult(id=pid, score=float(score), payload=payload) for pid, score, payload in top]


@app.get("/healthz")
def healthz():
    return {"ok": True}
