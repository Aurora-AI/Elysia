import logging
import os
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models


class QdrantAdapter:
    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
        host: str = "qdrant",
        port: int = 6333,
        collection_name: str = "aurora_knowledge",
    ):
        # Permite inicialização por URL/API_KEY (Qdrant Cloud) ou host/port (local)
        url = url or os.getenv("QDRANT_URL")
        api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.collection_name = collection_name
        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(host=host, port=port)
        self._ensure_collection()

    def healthcheck(self) -> bool:
        try:
            status = self.client.get_collections()
            return True if status else False
        except Exception as e:
            logging.error(f"Qdrant healthcheck failed: {e}")
            return False

    def _ensure_collection(self):
        """Cria a coleção se não existir com configurações otimizadas"""
        try:
            if not self.client.collection_exists(collection_name=self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Tamanho compatível com embeddings OpenAI
                        distance=models.Distance.COSINE,
                    ),
                    optimizers_config=models.OptimizersConfigDiff(
                        indexing_threshold=0, memmap_threshold=2000
                    ),
                )
        except Exception as e:
            logging.error(f"Erro ao criar coleção Qdrant: {e}")
            raise

    def add_embeddings(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]] | None = None,
    ):
        """Adiciona embeddings à coleção com resiliência"""
        try:
            points = [
                models.PointStruct(id=idx, vector=embedding, payload=metadata or {})
                for idx, embedding, metadata in zip(
                    ids, embeddings, metadatas or [{}] * len(ids), strict=False
                )
            ]

            self.client.upsert(
                collection_name=self.collection_name, points=points, wait=True
            )
        except Exception as e:
            logging.error(f"Erro ao adicionar embeddings: {e}")
            # Implementar lógica de retry ou fallback aqui

    def search(
        self, query_embedding: list[float], k: int = 5, **filters
    ) -> list[dict[str, Any]]:
        """Busca similares com filtragem avançada"""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=models.Filter(**filters) if filters else None,
                limit=k,
            )

            return [
                {"id": result.id, "score": result.score, "payload": result.payload}
                for result in search_result
            ]
        except Exception as e:
            logging.error(f"Erro na busca Qdrant: {e}")
            return []
