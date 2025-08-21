from fastapi.testclient import TestClient
from src.router.router_service import app

client = TestClient(app)


def test_decision_capability_listed():
    r = client.get("/capabilities")
    assert r.status_code == 200
    ids = [c["id"] for c in r.json().get("capabilities", [])]
    assert "decision.evaluate_case" in ids


def test_decision_invoke_mem_to_hrm(monkeypatch):
    # monkeypatch do fetch_context para não depender de Qdrant nos testes
    from src.orchestration import decision_flow

    fake_ctx = [
        {"tribunal": "TRT", "classe": "Recurso",
            "numero_processo": "0000000-00.0000.0.00.0000"},
        {"tribunal": "TRT", "classe": "Recurso"},
        {"tribunal": "TRT"},
    ]
    monkeypatch.setattr(decision_flow, "fetch_context",
                        lambda **kw: fake_ctx, raising=True)

    payload = {
        "capability_id": "decision.evaluate_case",
        "payload": {
            "numero_processo": "0000000-00.0000.0.00.0000",
            "extra_facts": {"assunto": "Execução"},
            "top_k": 3
        },
        "timeout_ms": 2000
    }
    r = client.post("/invoke", json=payload)
    assert r.status_code == 200, r.text
    j = r.json()
    assert j["capability_id"] == "decision.evaluate_case"
    res = j["result"]
    assert res["status"] == "ok"
    assert res["facts"]["tribunal"] == "TRT"
    # HRM deve conter decisões conforme sample_rules
    assert res["hrm"]["status"] == "ok"
    assert isinstance(res["hrm"]["decisions"], list) and len(
        res["hrm"]["decisions"]) >= 1
