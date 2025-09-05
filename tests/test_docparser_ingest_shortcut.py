from fastapi.testclient import TestClient


def test_ingest_example_url_uses_fixture(monkeypatch):
    # Force TESTING mode so the ingest_by_url shortcut returns the local fixture
    monkeypatch.setenv("TESTING", "1")

    from backend.app.services.docparser.main import app

    client = TestClient(app)
    resp = client.post("/ingest/url", json={"url": "http://example.com/test.pdf"})
    assert resp.status_code == 200, resp.text
    data = resp.json()

    # response uses Portuguese keys (metadados) as the service defines
    assert "metadados" in data
    assert data["metadados"].get("hash_conteudo")
    assert data["metadados"].get("fonte", "").endswith(".pdf")
