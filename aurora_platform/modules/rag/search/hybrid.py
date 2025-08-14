from __future__ import annotations
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import os

from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint, Filter
from fastembed import TextEmbedding
from .lexical_bm25 import LexicalBM25


@dataclass
class Hit:
    id: str
    score: float
    payload: Dict[str, Any]
    source: str  # "vec" | "bm25" | "rerank"


def rrf_fuse(vec_hits: List[Hit], lex_hits: List[Hit], k0: int = 60, top_k: int = 10) -> List[Hit]:
    # rank maps
    def rank_map(hs: List[Hit]) -> Dict[str, int]:
        return {h.id: i for i, h in enumerate(hs)}

    rv = rank_map(vec_hits)
    rl = rank_map(lex_hits)
    ids = set(rv.keys()) | set(rl.keys())
    fused: List[Tuple[str, float]] = []
    for pid in ids:
        r1 = rv.get(pid, 10**6)
        r2 = rl.get(pid, 10**6)
        score = 1.0 / (k0 + r1) + 1.0 / (k0 + r2)
        fused.append((pid, score))
    fused.sort(key=lambda x: x[1], reverse=True)
    # materializa
    plook: Dict[str, Hit] = {h.id: h for h in (vec_hits + lex_hits)}
    out: List[Hit] = []
    for pid, sc in fused[:top_k]:
        base = plook[pid]
        out.append(Hit(id=pid, score=float(sc),
                   payload=base.payload, source="hybrid"))
    return out


class VectorSearch:
    def __init__(self, collection: str, qdrant_url: str, embed_model: str):
        self.collection = collection
        self.client = QdrantClient(url=qdrant_url)
        self.embedder = TextEmbedding(model_name=embed_model)

    def search(self, query: str, top_k: int = 10) -> List[Hit]:
        vec = list(self.embedder.embed([query]))[0]
        pts: List[ScoredPoint] = self.client.search(
            collection_name=self.collection,
            query_vector=vec,
            limit=top_k
        )
        hits: List[Hit] = []
        for p in pts:
            hits.append(Hit(id=str(p.id), score=float(
                p.score), payload=p.payload, source="vec"))
        return hits


class HybridSearchService:
    def __init__(self, collection: str):
        self.collection = collection
        self.vec = VectorSearch(
            collection, os.getenv("QDRANT_URL", "http://localhost:6333"),
            os.getenv("EMBEDDINGS_MODEL", "BAAI/bge-small-en-v1.5")
        )
        self.lex = LexicalBM25(collection)

    def query(self, q: str, k_vec: int = 20, k_lex: int = 20, k_out: int = 10, enable_lex: bool = True) -> List[Hit]:
        vec_hits = self.vec.search(q, top_k=k_vec)
        if enable_lex:
            lex_raw = self.lex.search(q, top_k=k_lex)
            lex_hits = [Hit(id=h.id, score=h.score,
                            payload=h.payload, source="bm25") for h in lex_raw]
            return rrf_fuse(vec_hits, lex_hits, top_k=k_out)
        return vec_hits[:k_out]
