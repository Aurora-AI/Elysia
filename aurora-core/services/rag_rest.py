from __future__ import annotations

import hashlib
import logging
import os
import uuid

from fastapi import Depends, FastAPI, Form, Header, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

from aurora_platform.modules.rag.indexer.qdrant_indexer import QdrantIndexer
from aurora_platform.modules.rag.search.hybrid import Hit, HybridSearchService
from aurora_platform.modules.rag.search.reranker import CrossEncoderReranker

log = logging.getLogger("rag-api")
app = FastAPI(title="Aurora RAG API", version="1.0")

# --- Segurança simples por API-Key ---


def api_key_guard(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("RAG_API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="invalid api key")


# --- Prometheus ---
Instrumentator().instrument(app).expose(app, endpoint="/rag/metrics")

# --- Modelos ---


class QueryRequest(BaseModel):
    query: str
    top_k: int = 10
    use_hybrid: bool = bool(int(os.getenv("HYBRID_SEARCH", "1")))
    use_rerank: bool = bool(int(os.getenv("RERANK", "0")))


class QueryHit(BaseModel):
    id: str
    score: float
    title: str | None
    chunk_index: int | None
    source_type: str | None
    url: str | None
    text_preview: str
    source: str


class QueryResponse(BaseModel):
    hits: list[QueryHit]


# --- Helpers ---


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _to_hit(h: Hit) -> QueryHit:
    p = h.payload
    return QueryHit(
        id=h.id,
        score=h.score,
        title=p.get("title"),
        chunk_index=p.get("chunk_index"),
        source_type=p.get("source_type"),
        url=p.get("url"),
        text_preview=(p.get("chunk_text") or "")[:400],
        source=h.source,
    )


# --- Endpoints ---


@app.post(
    "/rag/query", response_model=QueryResponse, dependencies=[Depends(api_key_guard)]
)
def rag_query(req: QueryRequest):
    coll = os.getenv("QDRANT_COLLECTION", "aurora_docs@v1")
    svc = HybridSearchService(coll)
    hits = svc.query(
        req.query,
        k_vec=max(10, req.top_k),
        k_lex=max(10, req.top_k),
        k_out=req.top_k,
        enable_lex=req.use_hybrid,
    )
    if req.use_rerank:
        rr = CrossEncoderReranker()
        hits = rr.rerank(req.query, hits, top_k=req.top_k)
    return QueryResponse(hits=[_to_hit(h) for h in hits])


@app.post("/rag/ingest", dependencies=[Depends(api_key_guard)])
def rag_ingest(
    text: str = Form(...),
    title: str = Form(default=""),
    url: str = Form(default=""),
    source_type: str = Form(default="manual"),
):
    """Ingesta 1 'chunk' simples direto (atalho para demos/testes)."""
    idx = QdrantIndexer.from_env()
    rec = {
        "source_id": str(uuid.uuid4()),
        "source_type": source_type,
        "title": title or None,
        "lang": None,
        "authors": None,
        "published_at": None,
        "url": url or None,
        "canonical_id": _sha256((title or "") + text),
        "chunk_id": f"{(title or 'doc')}-0000",
        "chunk_index": 0,
        "chunk_text": text,
        "tokens_est": len(text.split()),
    }
    idx.upsert_record(rec)
    return {"status": "ok", "canonical_id": rec["canonical_id"]}


@app.get("/rag/health", response_class=PlainTextResponse)
def rag_health():
    # confere Qdrant
    from qdrant_client import QdrantClient

    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    coll = os.getenv("QDRANT_COLLECTION", "aurora_docs@v1")
    try:
        c = QdrantClient(url=url)
        c.get_collection(coll)
        qdrant_ok = True
    except Exception:
        qdrant_ok = False
    # opcional: kafka
    kafka_ok = bool(os.getenv("KAFKA_BOOTSTRAP"))
    # lexical arquivo
    import pathlib

    lf = pathlib.Path("artifacts/lexical") / f"{coll}.jsonl"
    lexical_ok = lf.exists()
    return f"qdrant={qdrant_ok} kafka_cfg={'yes' if kafka_ok else 'no'} lexical={'yes' if lexical_ok else 'no'}"
