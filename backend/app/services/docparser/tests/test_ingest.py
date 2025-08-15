from fastapi.testclient import TestClient


def test_ingest_with_url_local():
    from backend.app.services.docparser.main import app

    client = TestClient(app)
    resp = client.post("/ingest/url", json={"url": "http://example.com/test.pdf"})
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert isinstance(data["texto_markdown"], str)
    assert isinstance(data["tabelas"], list)
    assert isinstance(data["imagens"], list)
    assert isinstance(data["metadados"], dict)
    assert isinstance(data["proveniencia"], dict)
    assert isinstance(data["custo"], dict)
    assert "hash_conteudo" in data["metadados"]
