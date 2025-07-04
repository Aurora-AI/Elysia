# src/aurora_platform/services/knowledge_service.py
import chromadb
from chromadb.utils import embedding_functions

class KnowledgeBaseService:
    def __init__(self, path: str = "aurora_knowledge_base"):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="aurora_documents",
            embedding_function=self.embedding_function,  # type: ignore
            metadata={"hnsw:space": "cosine"}
        )
        print("Serviço da Base de Conhecimento inicializado.")

    def add_document(self, doc_text: str, doc_id: str, metadata: dict):
        self.collection.add(documents=[doc_text], metadatas=[metadata], ids=[doc_id])

    def search(self, query_text: str, n_results: int = 3) -> list:
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        if results and 'documents' in results:
            return results.get('documents', [[]])[0]  # type: ignore
        return []