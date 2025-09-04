from fastapi.testclient import TestClient
from aurora_platform.api.server import app

def test_bridge_search_unit(monkeypatch):
    # Simula a Memória Ativa para não depender do Qdrant
    def fake_query_memory(query: str, top_k: int = 3):
        return [{"doc_id": "d1", "snippet": "hello world", "score": 0.99}]
    
    # Patch direto na função importada
    import aurora_platform.bridge.elysia_bridge as bridge_module
    monkeypatch.setattr(bridge_module, "query_memory", fake_query_memory)

    client = TestClient(app)
    r = client.post("/bridge/elysia/search", json={"query": "hello", "top_k": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "hello"
    assert isinstance(body["results"], list) and body["results"]