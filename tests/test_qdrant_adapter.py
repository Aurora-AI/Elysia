import os
import pytest
from src.aurora_platform.clients.adapters.qdrant_adapter import QdrantAdapter

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = "test_aurora_knowledge"

@pytest.fixture(scope="module")
def adapter():
    return QdrantAdapter(url=QDRANT_URL, api_key=QDRANT_API_KEY, collection_name=COLLECTION)

def test_healthcheck(adapter):
    assert adapter.healthcheck() is True

def test_collection_created(adapter):
    collections = adapter.client.get_collections().collections
    assert any(c.name == COLLECTION for c in collections)

def test_add_and_search(adapter):
    ids = ["id1", "id2"]
    embeddings = [[0.1]*1536, [0.2]*1536]
    metadatas = [{"content": "doc1"}, {"content": "doc2"}]
    adapter.add_embeddings(ids, embeddings, metadatas)
    results = adapter.search([0.1]*1536, k=2)
    assert len(results) >= 1
    assert any(r["payload"].get("content") == "doc1" for r in results)
