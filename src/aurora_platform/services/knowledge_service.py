from aurora_platform.clients.adapters.qdrant_adapter import QdrantAdapter
from typing import List, Dict, Any
import numpy as np
import logging

from typing import Optional

class KnowledgeService:
    def __init__(self, embedding_model, persist_dir: Optional[str] = None):
        self.embedding_model = embedding_model
        self.vector_db = QdrantAdapter()
        logging.info("KnowledgeService usando Qdrant como backend vetorial")

    def add_knowledge(self, documents: List[Dict[str, Any]]):
        """Processa e armazena documentos com resiliência aprimorada"""
        try:
            # Extrai metadados e conteúdo
            contents = [doc["content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            # Gera embeddings
            embeddings = self.embedding_model.embed_documents(contents)
            # Gera IDs únicos
            ids = [f"doc_{hash(content)}" for content in contents]
            # Armazena no Qdrant
            self.vector_db.add_embeddings(ids, embeddings, metadatas)
            return True
        except Exception as e:
            logging.error(f"Falha ao adicionar conhecimento: {e}")
            # Implementar estratégia de fallback aqui
            return False

    def retrieve_knowledge(
        self,
        query: str,
        k: int = 5,
        **filters
    ) -> List[Dict[str, Any]]:
        """Recupera conhecimento relevante com filtragem avançada"""
        try:
            # Gera embedding da consulta
            query_embedding = self.embedding_model.embed_query(query)
            # Busca no Qdrant
            results = self.vector_db.search(query_embedding, k=k, **filters)
            return [
                {
                    "content": result["payload"].get("content", ""),
                    "metadata": result["payload"],
                    "score": result["score"]
                }
                for result in results
            ]
        except Exception as e:
            logging.error(f"Falha na recuperação de conhecimento: {e}")
            return []
