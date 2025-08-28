"""FastAPI router for the ingest MVP.

Provides POST /ingest and GET /chunks/{doc_id} endpoints.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi import Body
# fastapi.responses.JSONResponse not used in this minimal router
from typing import List

from .models import IngestRequest, IngestResult, Chunk
from .docling_pipeline import run_pipeline

app = FastAPI(title="aurora.ingest")

# simple in-memory store for chunks to serve GET /chunks in the MVP
_CHUNKS_STORE: dict[str, List[Chunk]] = {}


@app.post("/ingest", response_model=IngestResult)
async def ingest(req: IngestRequest = Body(...)) -> IngestResult:
    try:
        doc_id, count = run_pipeline(
            source_url=req.source_url, file_b64=req.file_b64)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # load chunks from index fallback file to memory so GET /chunks works in MVP
    # naive load: read /tmp/aurora_ingest/aurora_docs.jsonl and filter by doc_id
    from pathlib import Path
    import json
    path = Path('/tmp/aurora_ingest/aurora_docs.jsonl')
    chunks = []
    if path.exists():
        with path.open('r', encoding='utf-8') as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get('doc_id') == doc_id:
                    chunks.append(
                        Chunk(**{k: v for k, v in rec.items() if k in Chunk.__fields__}))
    _CHUNKS_STORE[doc_id] = chunks
    return IngestResult(doc_id=doc_id, chunks_count=count)


@app.get("/chunks/{doc_id}", response_model=List[Chunk])
async def get_chunks(doc_id: str):
    lst = _CHUNKS_STORE.get(doc_id)
    if lst is None:
        raise HTTPException(status_code=404, detail="doc_id not found")
    return lst
