import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType
from src.memory.embeddings import embedding_dim  # import absoluto e estável


def get_client() -> QdrantClient:
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY") or None
    return QdrantClient(url=url, api_key=api_key)


def ensure_collection(client: QdrantClient, name: str, size: int):
    existing = [c.name for c in client.get_collections().collections]
    if name not in existing:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )
        client.create_payload_index(
            name, field_name="text", field_schema=PayloadSchemaType.TEXT)
        client.create_payload_index(
            name, field_name="title", field_schema=PayloadSchemaType.TEXT)
        client.create_payload_index(
            name, field_name="source", field_schema=PayloadSchemaType.KEYWORD)


def main():
    dim = embedding_dim()
    client = get_client()
    for coll in ["cases_raw", "cases_norm", "cases_chunks"]:
        ensure_collection(client, coll, size=dim)
    print("OK: collections cases_raw, cases_norm, cases_chunks prontas.")


if __name__ == "__main__":
    main()
