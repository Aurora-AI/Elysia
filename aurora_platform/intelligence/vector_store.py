
# Vector Store implementation using Qdrant

from typing import Any, Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue


class VectorStore:
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = "aurora_collection", vector_size: int = 384):
        """
        Inicializa o cliente Qdrant e garante a existência da coleção.
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Garante que a coleção existe no Qdrant.
        """
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size, distance=Distance.COSINE)
            )
            print(f"Collection '{self.collection_name}' created.")
        else:
            print(f"Collection '{self.collection_name}' exists.")

    def add_documents(
        self,
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ):
        """
        Adiciona documentos e seus vetores à coleção Qdrant.
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        if metadatas is None:
            metadatas = [{} for _ in documents]
        points = [
            PointStruct(
                id=ids[i],
                vector=embeddings[i],
                payload={"text": documents[i], **metadatas[i]}
            )
            for i in range(len(documents))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)
        print(
            f"Added {len(documents)} documents to the collection '{self.collection_name}'.")

    def query(self, embedding: List[float], n_results: int = 5, filter_metadata: Optional[Dict[str, Any]] = None):
        """
        Realiza busca vetorial na coleção Qdrant.
        """
        qdrant_filter = None
        if filter_metadata:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_metadata.items()
                ]
            )
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=n_results,
            query_filter=qdrant_filter
        )
        return results
