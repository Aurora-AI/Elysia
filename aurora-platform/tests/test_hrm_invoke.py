from fastapi.testclient import TestClient
from src.router.router_service import app

client = TestClient(app)


def test_hrm_capability_listed():
    res = client.get("/capabilities")
    assert res.status_code == 200
    caps = [c["id"] for c in res.json().get("capabilities", [])]
    assert "hrm.evaluate" in caps


def test_hrm_invoke_success_with_sample_rules():
    payload = {
        "capability_id": "hrm.evaluate",
        "payload": {
            "facts": {"tribunal": "TRT", "classe": "Recurso"}
        },
        "timeout_ms": 2000
    }
    res = client.post("/invoke", json=payload)
    assert res.status_code == 200, res.text
    j = res.json()
    assert j["capability_id"] == "hrm.evaluate"
    r = j["result"]
    assert r["status"] == "ok"
    decisions = r["decisions"]
    assert isinstance(decisions, list) and len(decisions) >= 1
    assert "rule_id" in decisions[0]
    assert "base_legal" in decisions[0] or "prazo_dias" in decisions[0]


def test_hrm_invoke_missing_facts():
    res = client.post(
        "/invoke", json={"capability_id": "hrm.evaluate", "payload": {}})
    assert res.status_code == 400
    assert "Campos obrigat" in res.text
