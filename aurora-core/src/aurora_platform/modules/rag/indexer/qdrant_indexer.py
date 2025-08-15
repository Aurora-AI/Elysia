import os
import logging
import json
import pathlib
from typing import Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

LEXICAL_DIR = pathlib.Path("artifacts/lexical")
LEXICAL_DIR.mkdir(parents=True, exist_ok=True)


class QdrantIndexer:
    def __init__(self, client: QdrantClient, collection: str, embedder: TextEmbedding):
        self.client = client
        self.collection = collection
        self.embedder = embedder
        self._ensure_collection()

    @classmethod
    def from_env(cls):
        url = os.getenv("QDRANT_URL", "http://localhost:6333")
        col = os.getenv("QDRANT_COLLECTION", "aurora_docs@v1")
        client = QdrantClient(url=url)
        embedder = TextEmbedding(
            model_name=os.getenv("EMBEDDINGS_MODEL", "BAAI/bge-small-en-v1.5")
        )
        return cls(client, col, embedder)

    def _ensure_collection(self):
        dim = self.embedder.get_sentence_embedding_dimension()
        try:
            self.client.get_collection(self.collection)
        except Exception:
            self.client.recreate_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
            logging.info(f"Criada coleção {self.collection} (dim={dim})")

    def upsert_record(self, rec: Dict[str, Any]):
        text = rec["chunk_text"]
        vec = list(self.embedder.embed([text]))[0]
        point = PointStruct(
            id=rec["canonical_id"] + f":{rec['chunk_index']}", vector=vec, payload=rec
        )
        self.client.upsert(collection_name=self.collection, points=[point])
        # 🔹 Persistência lexical simples para BM25:
        lf = LEXICAL_DIR / f"{self.collection}.jsonl"
        with lf.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"id": point.id, "text": text, "meta": rec}, ensure_ascii=False
                )
                + "\n"
            )
