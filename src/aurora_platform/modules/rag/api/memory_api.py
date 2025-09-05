from __future__ import annotations

from aurora_platform.modules.rag.pipeline.rag_pipeline import query_memory
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AskBody(BaseModel):
    query: str
    top_k: int = 3


@router.post("/ask")
def ask(b: AskBody):
    results = query_memory(b.query, top_k=b.top_k)
    return {"query": b.query, "results": results}
