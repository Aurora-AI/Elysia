import os
import pytest
import sys
import importlib
sys.path.append("./src")
from aurora_platform.services.knowledge_service import KnowledgeService

class DummyEmbeddingModel:
    def embed_documents(self, docs):
        return [[0.1]*1536 for _ in docs]
    def embed_query(self, query):
        return [0.1]*1536

def test_knowledge_service_add_and_retrieve(monkeypatch):
    qdrant_url = os.getenv("QDRANT_URL") or ""
    qdrant_api_key = os.getenv("QDRANT_API_KEY") or ""
    os.environ["QDRANT_URL"] = qdrant_url
    os.environ["QDRANT_API_KEY"] = qdrant_api_key
    service = KnowledgeService(DummyEmbeddingModel())
    docs = [{"content": "test doc", "metadata": {"source": "unit"}}]
    assert service.add_knowledge(docs) is True
    results = service.retrieve_knowledge("test doc", k=1)
    assert isinstance(results, list)
    assert any("test doc" in r["content"] for r in results)

def test_knowledge_service_healthcheck():
    service = KnowledgeService(DummyEmbeddingModel())
    assert service.healthcheck() is True
