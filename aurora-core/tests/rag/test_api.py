import os
from fastapi.testclient import TestClient
from aurora_platform.services.rag_rest import app


def test_health_smoke():
    client = TestClient(app)
    r = client.get("/rag/health")
    assert r.status_code == 200


def test_query_without_key_is_401(monkeypatch):
    client = TestClient(app)
    monkeypatch.setenv("RAG_API_KEY", "abc")
    r = client.post("/rag/query", json={"query": "teste"})
    assert r.status_code == 401


def test_ingest_mocked_indexer(monkeypatch):
    client = TestClient(app)
    monkeypatch.setenv("RAG_API_KEY", "abc")
    from aurora_platform.modules.rag.indexer import qdrant_indexer as qi
    def fake_upsert(rec): pass
    monkeypatch.setattr(qi.QdrantIndexer, "from_env", classmethod(lambda cls: type(
        "X", (object,), {"upsert_record": staticmethod(fake_upsert)})()))
    r = client.post("/rag/ingest", headers={"X-API-Key": "abc"},
                    data={"text": "texto de teste", "title": "demo", "url": ""})
    assert r.status_code == 200
