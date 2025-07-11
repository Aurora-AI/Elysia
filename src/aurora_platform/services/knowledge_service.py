import logging
import re
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KnowledgeService")

class KnowledgeBaseService:
    def __init__(self, host: str = "localhost", port: int = 8000, collection_name: str = "aurora_docs", main_model_name: str = 'all-MiniLM-L6-v2'):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function  # type: ignore
        )
        logger.info(f"KnowledgeService conectado ao servidor Chroma em {host}:{port}.")

    def add_document(self, document_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        if metadata is None:
            metadata = {}
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[document_id]
        )
        logger.info(f"Documento '{document_id}' ingerido/atualizado com sucesso.")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(query_texts=[query], n_results=top_k)
        formatted = []
        if results and results.get("ids") and results.get("ids") and len(results["ids"]) > 0:
            ids = results["ids"][0] if results.get("ids") and results["ids"] and len(results["ids"]) > 0 else []
            distances = results["distances"][0] if results.get("distances") and results["distances"] and len(results["distances"]) > 0 else []
            documents = results["documents"][0] if results.get("documents") and results["documents"] and len(results["documents"]) > 0 else []
            metadatas = results["metadatas"][0] if results.get("metadatas") and results["metadatas"] and len(results["metadatas"]) > 0 else []
            
            for i in range(len(ids)):
                formatted.append({
                    "id": ids[i],
                    "distance": distances[i] if i < len(distances) else None,
                    "text": documents[i] if i < len(documents) else None,
                    "metadata": metadatas[i] if i < len(metadatas) else None
                })
        return formatted