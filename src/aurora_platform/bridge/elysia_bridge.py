from __future__ import annotations
import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from aurora_platform.modules.rag.pipeline.rag_pipeline import query_memory
from aurora_platform.modules.crawler.producers.enqueue import enqueue_crawl

router = APIRouter(prefix="/bridge/elysia", tags=["elysia-bridge"])

class AskBody(BaseModel):
    query: str
    top_k: int = 3

@router.get("/health")
def health():
    return {"ok": True}

@router.post("/search")
def elysia_search(b: AskBody):
    # Encaminha para a Memória Ativa (RAG/Qdrant)
    results = query_memory(b.query, top_k=b.top_k)
    return {"query": b.query, "results": results}

@router.get("/doc/{doc_id}")
def get_doc(doc_id: str):
    # Busca Documento Macro na coleção docs_macro (payload contém doc_id/url/text/meta)
    cli = QdrantClient(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=30.0,
    )
    r = cli.scroll(
        collection_name="docs_macro",
        scroll_filter=qm.Filter(
            must=[qm.FieldCondition(key="doc_id", match=qm.MatchValue(value=doc_id))]
        ),
        limit=1,
        with_payload=True,
    )
    if not r or not r[0]:
        raise HTTPException(status_code=404, detail="doc not found")
    return r[0][0].payload

# Opcional (Fase 2): permitir que a Elysia solicite ingestão de novas URLs
class IngestBody(BaseModel):
    url: str
    source: Optional[str] = "elysia"

@router.post("/ingest")
def elysia_ingest(b: IngestBody):
    enqueue_crawl(b.url, source=b.source or "elysia")
    return {"enqueued": True, "url": b.url, "source": b.source or "elysia"}