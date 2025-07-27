# Placeholder for Vector Store interaction logic
# This could involve using libraries like ChromaDB, FAISS, etc.

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import Dict, Any


class VectorStore:
    def __init__(self, path: str = "./chroma_db"):
        # Initialize ChromaDB client
        # Persistent client stores data on disk in the specified path
        self.client = chromadb.PersistentClient(
            path=path,
            settings=ChromaSettings(
                anonymized_telemetry=False
            ),  # Optional: disable telemetry
        )
        self.collection = None  # To be set or created

    def get_or_create_collection(self, name: str = "aurora_collection"):
        try:
            self.collection = self.client.get_collection(name=name)
            print(f"Collection '{name}' retrieved.")
        except Exception:  # chromadb.errors.CollectionNotFoundException - more specific error handling is better
            self.collection = self.client.create_collection(name=name)
            print(f"Collection '{name}' created.")
        return self.collection

    def add_documents(
        self,
        documents: list[str],
        metadatas: list[Dict[str, Any]] | None = None,
        ids: list[str] | None = None,
    ):
        if not self.collection:
            print("Collection not initialized. Call get_or_create_collection first.")
            return
        if not ids:
            ids = [f"doc_{i}" for i in range(len(documents))]  # Simple ID generation
        if metadatas is None:
            metadatas = [{} for _ in documents]

        # TODO: Revisar lógica de adição de documentos durante a Sprint de Unificação
        # self.collection.add(documents=[doc_text], metadatas=[metadata], ids=[doc_id])  # type: ignore
        print(f"Added {len(documents)} documents to the collection.")

    def query(self, query_texts: list[str], n_results: int = 5):
        if not self.collection:
            print("Collection not initialized. Call get_or_create_collection first.")
            return None
        results = self.collection.query(query_texts=query_texts, n_results=n_results)
        return results


# Example usage (optional, for testing)
if __name__ == "__main__":
    vector_store = VectorStore(path="./test_chroma_db")  # Use a test path
    collection = vector_store.get_or_create_collection("test_collection")

    if collection:
        # Add some documents
        vector_store.add_documents(
            documents=[
                "Aurora is a platform for AI development.",
                "It uses FastAPI for its API.",
                "SQLModel is used for database interactions.",
                "Large Language Models are a key component.",
            ],
            metadatas=[
                {"source": "doc1"},
                {"source": "doc2"},
                {"source": "doc3"},
                {"source": "doc4"},
            ],
            ids=["id1", "id2", "id3", "id4"],
        )

        # Query the collection
        query_results = vector_store.query(query_texts=["What is Aurora?"], n_results=2)
        print("\nQuery Results:")
        if query_results:
            documents = query_results.get("documents", [])
            if documents:
                for i, docs in enumerate(documents):
                    print(f"Query {i+1}:")
                    for doc in docs:
                        print(f"  - {doc}")

        # Clean up test database (optional)
        try:
            vector_store.client.delete_collection("test_collection")
            print("\nTest collection deleted.")
            import shutil

            shutil.rmtree("./test_chroma_db")  # Remove the test directory
            print("Test ChromaDB directory removed.")
        except Exception as e:
            print(f"Error during cleanup: {e}")
