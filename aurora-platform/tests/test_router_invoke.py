from fastapi.testclient import TestClient

from src.router.router_service import app

client = TestClient(app)


def test_capabilities_list():
    res = client.get("/capabilities")
    assert res.status_code == 200
    j = res.json()
    caps = [c["id"] for c in j.get("capabilities", [])]
    assert "datajud.search_by_process_number" in caps


def test_invoke_datajud_success(monkeypatch):
    # monkeypatch do conector interno para não depender de rede/SDK
    from src.connectors import datajud_connector

    def fake(numero_processo: str):
        return {"status": "ok", "numero_processo": numero_processo, "from": "fake"}

    monkeypatch.setattr(datajud_connector,
                        "search_by_process_number", fake, raising=True)

    payload = {
        "capability_id": "datajud.search_by_process_number",
        "payload": {"numero_processo": "0000000-00.0000.0.00.0000"},
        "timeout_ms": 3000,
    }
    res = client.post("/invoke", json=payload)
    assert res.status_code == 200, res.text
    j = res.json()
    assert j["capability_id"] == payload["capability_id"]
    assert j["result"]["status"] == "ok"
    assert j["result"]["numero_processo"].endswith("0000")


def test_invoke_missing_field():
    payload = {
        "capability_id": "datajud.search_by_process_number",
        "payload": {},
    }
    res = client.post("/invoke", json=payload)
    assert res.status_code == 400
    assert "Campos obrigatórios" in res.text


def test_invoke_unknown_capability():
    res = client.post(
        "/invoke", json={"capability_id": "foo.bar", "payload": {}})
    assert res.status_code == 404
