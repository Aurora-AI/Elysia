from __future__ import annotations
import os, hashlib, time
from typing import List
from aurora_platform.modules.rag.models.rag_models import DocumentMacro, ChunkResult
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

QURL = os.getenv("QDRANT_URL", "http://localhost:6333")
QKEY = os.getenv("QDRANT_API_KEY")
COLL_DOCS = "docs_macro"
COLL_CHUNKS = "chunks_on_demand"
DIM = int(os.getenv("RAG_EMBED_DIM", "384"))

def _hash_embed(text: str, dim: int = DIM) -> List[float]:
    h = hashlib.sha256(text.encode()).digest()
    return [((h[i % len(h)]/255.0)-0.5)*2 for i in range(dim)]

def ensure_collections(cli: QdrantClient) -> None:
    if not cli.collection_exists(COLL_DOCS):
        cli.recreate_collection(COLL_DOCS, vectors_config=qm.VectorParams(size=DIM, distance=qm.Distance.COSINE))
    if not cli.collection_exists(COLL_CHUNKS):
        cli.recreate_collection(COLL_CHUNKS, vectors_config=qm.VectorParams(size=DIM, distance=qm.Distance.COSINE))

def ingest_document(doc: DocumentMacro) -> None:
    cli = QdrantClient(url=QURL, api_key=QKEY, timeout=30.0)
    ensure_collections(cli)
    vec = _hash_embed(doc.text)
    cli.upsert(
        collection_name=COLL_DOCS,
        points=[qm.PointStruct(id=doc.doc_id, vector=vec, payload=doc.model_dump())]
    )

def chunk_on_demand(doc: DocumentMacro, size: int = 500) -> List[ChunkResult]:
    words = doc.text.split()
    chunks, out = [], []
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        chunk_id = f"{doc.doc_id}_c{i//size}"
        out.append(ChunkResult(doc_id=doc.doc_id, chunk_id=chunk_id, text=chunk, meta=doc.meta))
    cli = QdrantClient(url=QURL, api_key=QKEY, timeout=30.0)
    ensure_collections(cli)
    for c in out:
        vec = _hash_embed(c.text)
        cli.upsert(
            collection_name=COLL_CHUNKS,
            points=[qm.PointStruct(id=c.chunk_id, vector=vec, payload=c.model_dump())]
        )
    return out

def query_memory(query: str, top_k: int = 3) -> List[dict]:
    cli = QdrantClient(url=QURL, api_key=QKEY, timeout=30.0)
    ensure_collections(cli)
    qvec = _hash_embed(query)
    # fase 1 — busca em documentos
    res_doc = cli.search(COLL_DOCS, query_vector=qvec, limit=3)
    if not res_doc:
        return []
    results = []
    for hit in res_doc:
        doc = DocumentMacro(**hit.payload)
        # fase 2 — chunk sob demanda
        chunks = chunk_on_demand(doc)
        res_chunk = cli.search(COLL_CHUNKS, query_vector=qvec, limit=top_k)
        for ch in res_chunk:
            results.append(ch.payload)
    return results