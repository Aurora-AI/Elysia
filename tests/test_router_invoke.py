import json
from fastapi.testclient import TestClient
import subprocess

from src.router.router_service import app

client = TestClient(app)


class DummyCompleted:
    def __init__(self, stdout, stderr=""):
        self.stdout = stdout
        self.stderr = stderr


def test_capabilities_list():
    r = client.get("/capabilities")
    assert r.status_code == 200
    j = r.json()
    assert "capabilities" in j


def test_invoke_missing_capability():
    r = client.post(
        "/invoke", json={"capability_id": "not.exist", "input": {}})
    assert r.status_code == 404


def test_invoke_datajud_monkeypatch(monkeypatch):
    # simulate subprocess.run returning a JSON payload
    expected = {"hits": [{"_id": "1", "_source": {"numeroProcesso": "0001"}}]}

    def fake_run(cmd, capture_output, text, check, timeout):
        return DummyCompleted(stdout=json.dumps(expected))

    monkeypatch.setattr(subprocess, "run", fake_run)

    payload = {"capability_id": "datajud.search_by_process_number",
               "input": {"numero_processo": "0000993-58.2022.5.09.0014"}}
    r = client.post("/invoke", json=payload)
    assert r.status_code == 200
    assert r.json() == expected
