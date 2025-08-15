from __future__ import annotations
from typing import List, Dict, Any
from dataclasses import dataclass
from rank_bm25 import BM25Okapi
import pathlib
import json
import re

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_]+")


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or "")]


@dataclass
class BM25Hit:
    id: str
    score: float
    payload: Dict[str, Any]


class LexicalBM25:
    """BM25 carregado a partir do JSONL lexical salvo pelo indexador."""

    def __init__(self, collection: str):
        self.collection = collection
        self.path = pathlib.Path("artifacts/lexical") / f"{collection}.jsonl"
        self._docs: List[str] = []
        self._ids: List[str] = []
        self._payloads: List[Dict[str, Any]] = []
        self._bm25: BM25Okapi | None = None

    def _load(self):
        if self._bm25 is not None:
            return
        self._docs, self._ids, self._payloads = [], [], []
        if not self.path.exists():
            self._bm25 = BM25Okapi([[]])  # vazio (evita falha)
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                self._ids.append(obj["id"])
                self._docs.append(obj["text"])
                self._payloads.append(obj["meta"])
        tokenized_corpus = [tokenize(d) for d in self._docs]
        self._bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, top_k: int = 10) -> List[BM25Hit]:
        self._load()
        if not self._docs:
            return []
        toks = tokenize(query)
        scores = self._bm25.get_scores(toks)
        pairs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        hits: List[BM25Hit] = []
        for idx, sc in pairs:
            hits.append(
                BM25Hit(id=self._ids[idx], score=float(sc), payload=self._payloads[idx])
            )
        return hits
