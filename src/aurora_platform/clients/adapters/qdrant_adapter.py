from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging

class QdrantAdapter:
    def __init__(self, host: str = "qdrant", port: int = 6333, collection_name: str = "aurora_knowledge"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self):
        """Cria a coleção se não existir com configurações otimizadas"""
        try:
            if not self.client.collection_exists(collection_name=self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Tamanho compatível com embeddings OpenAI
                        distance=models.Distance.COSINE
                    ),
                    optimizers_config=models.OptimizersConfigDiff(
                        indexing_threshold=0,
                        memmap_threshold=2000
                    )
                )
        except Exception as e:
            logging.error(f"Erro ao criar coleção Qdrant: {e}")
            raise

    def add_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ):
        """Adiciona embeddings à coleção com resiliência"""
        try:
            points = [
                models.PointStruct(
                    id=idx,
                    vector=embedding,
                    payload=metadata or {}
                )
                for idx, embedding, metadata in zip(ids, embeddings, metadatas or [{}]*len(ids))
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )
        except Exception as e:
            logging.error(f"Erro ao adicionar embeddings: {e}")
            # Implementar lógica de retry ou fallback aqui

    def search(
        self,
        query_embedding: List[float],
        k: int = 5,
        **filters
    ) -> List[Dict[str, Any]]:
        """Busca similares com filtragem avançada"""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=models.Filter(**filters) if filters else None,
                limit=k
            )

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in search_result
            ]
        except Exception as e:
            logging.error(f"Erro na busca Qdrant: {e}")
            return []
