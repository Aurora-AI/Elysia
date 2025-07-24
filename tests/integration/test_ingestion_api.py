from fastapi.testclient import TestClient
from src.aurora_platform.main import app

client = TestClient(app)

def test_start_ingestion_pipeline_success():
    response = client.post("/api/v1/ingest", json={"source_dir": "/tmp/test_data"})
    assert response.status_code == 202
    assert response.json()["message"] == "Processo de ingestão iniciado com sucesso."