import os
import pytest
from fastapi.testclient import TestClient
from aurora_platform.api.server import app
from aurora_platform.modules.rag.models.rag_models import DocumentMacro
from aurora_platform.modules.rag.pipeline.rag_pipeline import ingest_document

qdrant_enabled = os.getenv("ENABLE_QDRANT_TESTS") == "1"

@pytest.mark.skipif(not qdrant_enabled, reason="ENABLE_QDRANT_TESTS != 1")
def test_bridge_search_integration(tmp_path):
    # Ingesta um doc macro no Qdrant, depois consulta via bridge
    doc = DocumentMacro(doc_id="bridge-doc-1", url="https://mem://bridge-doc", text="Aurora Elysia integration test")
    ingest_document(doc)

    client = TestClient(app)
    r = client.post("/bridge/elysia/search", json={"query": "integration", "top_k": 3})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["results"], list)