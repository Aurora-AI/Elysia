from fastapi.testclient import TestClient

from aurora_platform.ingest.router import app

client = TestClient(app)


def test_ingest_and_get_chunks():
    resp = client.post(
        "/ingest", json={"source_url": "http://example.com/doc2"})
    assert resp.status_code == 200
    data = resp.json()
    doc_id = data["doc_id"]
    assert data["chunks_count"] >= 1

    # GET chunks
    resp2 = client.get(f"/chunks/{doc_id}")
    assert resp2.status_code == 200
    lst = resp2.json()
    assert isinstance(lst, list)
    assert len(lst) >= 1
