from __future__ import annotations

import os

from sentence_transformers import CrossEncoder

from .hybrid import Hit


class CrossEncoderReranker:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or os.getenv(
            "RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
        self.model = CrossEncoder(self.model_name)

    def rerank(self, query: str, hits: list[Hit], top_k: int = 10) -> list[Hit]:
        if not hits:
            return []
        pairs = [[query, h.payload["chunk_text"]] for h in hits]
        scores = self.model.predict(pairs)  # maior = melhor
        scored = list(zip(hits, scores, strict=False))
        scored.sort(key=lambda x: float(x[1]), reverse=True)
        out: list[Hit] = []
        for h, sc in scored[:top_k]:
            out.append(
                Hit(id=h.id, score=float(sc), payload=h.payload, source="rerank")
            )
        return out
