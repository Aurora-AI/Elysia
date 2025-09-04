from __future__ import annotations
import time, os, hashlib
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

QURL = os.getenv("QDRANT_URL", "http://localhost:6333")
QKEY = os.getenv("QDRANT_API_KEY")
COLL = os.getenv("CRAWLER_QDRANT_COLLECTION", "crawl_pages")
DIM = int(os.getenv("CRAWLER_EMBED_DIM", "384"))

def _hash_embed(text: str, dim: int = DIM) -> list[float]:
    if not text: return [0.0] * dim
    h = hashlib.sha256(text.encode()).digest()
    return [((h[i % len(h)]/255.0)-0.5)*2 for i in range(dim)]

def ensure() -> QdrantClient:
    cli = QdrantClient(url=QURL, api_key=QKEY, timeout=30.0)
    if not cli.collection_exists(COLL):
        cli.recreate_collection(COLL, vectors_config=qm.VectorParams(size=DIM, distance=qm.Distance.COSINE))
    return cli

def upsert_page_vector(url: str, text: str, meta: dict) -> None:
    cli = ensure()
    vec = _hash_embed(text)
    cli.upsert(
        collection_name=COLL,
        points=[qm.PointStruct(id=url, vector=vec, payload={"url": url, "meta": meta, "ts": int(time.time())})]
    )