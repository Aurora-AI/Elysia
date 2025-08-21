```python
from fastapi.testclient import TestClient
from src.router.router_service import app
from src.connectors import datajud_connector

client = TestClient(app)


def test_capabilities_list():
    r = client.get("/capabilities")
    assert r.status_code == 200
    j = r.json()
    assert "capabilities" in j
    ids = [c["id"] for c in j["capabilities"]]
    assert "datajud.search_by_process_number" in ids


def test_invoke_missing_capability():
    r = client.post("/invoke", json={"capability_id": "not.exist", "payload": {}})
    assert r.status_code == 404


def test_invoke_datajud_monkeypatch(monkeypatch):
    # monkeypatch do conector interno (sem subprocess)
    def fake(numero_processo: str):
        return {"status": "ok", "numero_processo": numero_processo, "from": "fake"}

    monkeypatch.setattr(
        datajud_connector, "search_by_process_number", fake, raising=True
    )

    payload = {
        "capability_id": "datajud.search_by_process_number",
        "payload": {"numero_processo": "0000993-58.2022.5.09.0014"},
    }
    r = client.post("/invoke", json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body, dict)
    assert body.get("capability_id") == "datajud.search_by_process_number"
    res = body.get("result") or {}
    assert res.get("status") == "ok"
    assert res.get("numero_processo") == payload["payload"]["numero_processo"]
```
