"""Minimal Docling pipeline skeleton.

This implementation keeps external dependencies minimal and provides placeholders
for embedding and Qdrant indexing so tests can run with mocks.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from typing import Iterable, List, Tuple, Optional

from .models import Chunk


def _make_doc_id(source: str) -> str:
    return hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]


def load_from_url(url: str) -> str:
    # Placeholder: in real implementation use httpx / requests and docling
    return f"Loaded content from {url}"


def load_from_b64(b64: str) -> str:
    # Placeholder: decode and detect mime
    # b64 is expected to be a base64 string; tests will pass a short placeholder.
    return f"decoded-{len(b64)}"


def to_markdown(text: str) -> str:
    # Placeholder normalization
    return text


def chunk_text(md: str, doc_id: str, max_chars: int = 1000) -> List[Chunk]:
    chunks: List[Chunk] = []
    words = md.split()
    cur = []
    order = 0
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > max_chars:
            txt = " ".join(cur)
            chunks.append(Chunk(id=str(uuid.uuid4()),
                          doc_id=doc_id, order=order, text=txt))
            order += 1
            cur = []
    if cur:
        txt = " ".join(cur)
        chunks.append(Chunk(id=str(uuid.uuid4()),
                      doc_id=doc_id, order=order, text=txt))
    return chunks


def embed_chunks(chunks: Iterable[Chunk]) -> List[List[float]]:
    # Placeholder deterministic vector based on text hash (for tests/mocks)
    vectors = []
    for c in chunks:
        h = int(hashlib.sha1(c.text.encode("utf-8")).hexdigest()[:8], 16)
        # simple pseudo-vector
        vectors.append([(h % 1000) / 1000.0])
    return vectors


# Simple file-based index fallback for local testing
_INDEX_DIR = os.environ.get("AURORA_INGEST_INDEX_DIR", "/tmp/aurora_ingest")


def index_qdrant(chunks: Iterable[Chunk], vectors: List[List[float]], collection: str = "aurora_docs") -> None:
    os.makedirs(_INDEX_DIR, exist_ok=True)
    path = os.path.join(_INDEX_DIR, f"{collection}.jsonl")
    with open(path, "a", encoding="utf-8") as fh:
        for c, v in zip(chunks, vectors):
            rec = {"id": c.id, "doc_id": c.doc_id,
                   "order": c.order, "text": c.text, "vector": v}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def run_pipeline(source_url: Optional[str] = None, file_b64: Optional[str] = None) -> Tuple[str, int]:
    assert source_url or file_b64, "provide source_url or file_b64"
    if source_url:
        raw = load_from_url(source_url)
    else:
        # mypy-safe: file_b64 is not None here because of the assertion
        raw = load_from_b64(file_b64)  # type: ignore[arg-type]
    md = to_markdown(raw)
    doc_id = _make_doc_id(raw)
    chunks = chunk_text(md, doc_id)
    vectors = embed_chunks(chunks)
    index_qdrant(chunks, vectors)
    return doc_id, len(chunks)
