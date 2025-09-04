# /src/aurora_platform/modules/rag/pipeline.py
from __future__ import annotations

import hashlib
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

# Requer: pip install qdrant-client
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels


# =========================
# Embeddings (plugável)
# =========================
def _hash_embedding(text: str, dim: int = 384) -> list[float]:
    """
    Embedding determinístico leve (placeholder).
    Substitua por um provedor real (ex.: Sentence Transformers, OpenAI, etc.).
    """
    if not text:
        return [0.0] * dim
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # expandir determinísticamente
    vals = []
    for i in range(dim):
        b = h[i % len(h)]
        vals.append(((b / 255.0) - 0.5) * 2.0)  # [-1, 1]
    return vals


# =========================
# Chunking
# =========================
def simple_chunk(text: str, *, max_chars: int = 800, overlap: int = 100) -> list[str]:
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        if end == n:
            break
        start = end - overlap
        if start < 0:
            start = 0
    return [c for c in chunks if c]


# =========================
# Dados & Retornos
# =========================
@dataclass
class DocRecord:
    doc_id: str
    text: str
    metadata: dict[str, Any]


@dataclass
class SearchHit:
    doc_id: str
    score: float
    text: str
    metadata: dict[str, Any]


@dataclass
class RAGResult:
    query: str
    doc_hits: list[SearchHit]
    chunk_hits: list[SearchHit]


# =========================
# Pipeline RAG 2.0
# =========================
class QdrantRAGPipeline:
    def __init__(
        self,
        *,
        qdrant_url: str = "http://localhost:6333",
        api_key: str | None = None,
        collection_docs: str = "docs",
        collection_chunks: str = "chunks_on_demand",
        vector_size: int = 384,
        distance: qmodels.Distance = qmodels.Distance.COSINE,
        embedder: Callable[[str], list[float]] = _hash_embedding,
        default_topk_docs: int = 3,
        default_topk_chunks: int = 6,
        chunk_max_chars: int = 800,
        chunk_overlap: int = 100,
        cache_ttl_sec: int = 7 * 24 * 3600,
    ) -> None:
        self.client = QdrantClient(url=qdrant_url, api_key=api_key, timeout=30.0)
        self.collection_docs = collection_docs
        self.collection_chunks = collection_chunks
        self.vector_size = vector_size
        self.distance = distance
        self.embed = embedder
        self.topk_docs = default_topk_docs
        self.topk_chunks = default_topk_chunks
        self.chunk_max_chars = chunk_max_chars
        self.chunk_overlap = chunk_overlap
        self.cache_ttl_sec = cache_ttl_sec

        self._ensure_collections()

    # ---------- Collections ----------
    def _ensure_collections(self) -> None:
        for name in (self.collection_docs, self.collection_chunks):
            if not self.client.collection_exists(name):
                self.client.recreate_collection(
                    collection_name=name,
                    vectors_config=qmodels.VectorParams(
                        size=self.vector_size,
                        distance=self.distance,
                    ),
                )

    # ---------- Indexação ----------
    def index_document(self, record: DocRecord) -> None:
        vec = self.embed(record.text)
        payload = {
            "doc_id": record.doc_id,
            "metadata": record.metadata,
            "is_chunk": False,
            "ts": int(time.time()),
        }
        self.client.upsert(
            collection_name=self.collection_docs,
            points=[
                qmodels.PointStruct(
                    id=record.doc_id,
                    vector=vec,
                    payload=payload,
                )
            ],
        )

    # ---------- Busca (Etapa 1: DOC) ----------
    def _search_docs(self, query: str, top_k: int | None = None) -> list[SearchHit]:
        vec = self.embed(query)
        k = top_k or self.topk_docs
        out = self.client.search(
            collection_name=self.collection_docs,
            query_vector=vec,
            limit=k,
            with_payload=True,
            with_vectors=False,
        )
        hits: list[SearchHit] = []
        for r in out:
            payload = r.payload or {}
            doc_id = str(payload.get("doc_id") or r.id)
            text = ""  # não armazenamos o texto original aqui (somente vetor + metadados)
            hits.append(
                SearchHit(
                    doc_id=doc_id,
                    score=float(r.score),
                    text=text,
                    metadata=payload.get("metadata") or {},
                )
            )
        return hits

    # ---------- Chunk on Demand ----------
    def _ensure_chunks_cached(
        self, doc_id: str, full_text: str, parent_meta: dict[str, Any]
    ) -> None:
        """Gera (caso necessário) e armazena chunks do doc na collection de chunks."""
        now = int(time.time())
        # Existe pelo menos 1 chunk recente?
        existing = self.client.scroll(
            collection_name=self.collection_chunks,
            scroll_filter=qmodels.Filter(
                must=[qmodels.FieldCondition(key="doc_id", match=qmodels.MatchValue(value=doc_id))]
            ),
            limit=1,
            with_payload=True,
        )
        if existing and existing[0]:
            payload = existing[0][0].payload or {}
            ts = int(payload.get("ts") or 0)
            if now - ts < self.cache_ttl_sec:
                return  # cache válido

        # (Re)criar chunks
        chunks = simple_chunk(full_text, max_chars=self.chunk_max_chars, overlap=self.chunk_overlap)
        points: list[qmodels.PointStruct] = []
        for i, ch in enumerate(chunks):
            vec = self.embed(ch)
            payload = {
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}::ch{i:04d}",
                "parent_meta": parent_meta,
                "is_chunk": True,
                "ts": now,
                "len": len(ch),
            }
            points.append(
                qmodels.PointStruct(
                    id=payload["chunk_id"],
                    vector=vec,
                    payload=payload,
                )
            )
        if points:
            self.client.upsert(collection_name=self.collection_chunks, points=points)

    # ---------- Busca (Etapa 2: CHUNKS dos DOCs candidatos) ----------
    def _search_chunks_for_docs(
        self, query: str, doc_ids: list[str], top_k: int | None = None
    ) -> list[SearchHit]:
        if not doc_ids:
            return []
        vec = self.embed(query)
        k = top_k or self.topk_chunks
        # Filtrar por doc_id ∈ doc_ids
        filt = qmodels.Filter(
            must=[qmodels.FieldCondition(key="doc_id", match=qmodels.MatchAny(any=doc_ids))]
        )
        out = self.client.search(
            collection_name=self.collection_chunks,
            query_vector=vec,
            limit=k,
            with_payload=True,
            with_vectors=False,
            query_filter=filt,
        )
        hits: list[SearchHit] = []
        for r in out:
            payload = r.payload or {}
            hits.append(
                SearchHit(
                    doc_id=str(payload.get("doc_id")),
                    score=float(r.score),
                    text=payload.get("text") or "",  # opcional: guardar o texto no payload
                    metadata={
                        "chunk_id": payload.get("chunk_id"),
                        "len": payload.get("len"),
                        "parent_meta": payload.get("parent_meta") or {},
                    },
                )
            )
        return hits

    # ---------- API Pública ----------
    def search(
        self,
        query: str,
        *,
        get_full_text_fn: Callable[[str], str],  # função para recuperar o corpo do doc por doc_id
        get_doc_meta_fn: Callable[[str], dict[str, Any]] | None = None,
        top_k_docs: int | None = None,
        top_k_chunks: int | None = None,
    ) -> RAGResult:
        doc_hits = self._search_docs(query, top_k=top_k_docs)
        doc_ids = [h.doc_id for h in doc_hits]

        # Garantir chunks sob demanda para cada doc candidato
        for doc_id in doc_ids:
            full_text = get_full_text_fn(doc_id)
            parent_meta = (get_doc_meta_fn(doc_id) if get_doc_meta_fn else {}) or {}
            self._ensure_chunks_cached(doc_id, full_text, parent_meta)

        chunk_hits = self._search_chunks_for_docs(query, doc_ids, top_k=top_k_chunks)
        return RAGResult(query=query, doc_hits=doc_hits, chunk_hits=chunk_hits)
