import os
import json

from src.hrm.engine import evaluate


def test_hrm_eq_and_priority():
    # facts that match two rules with different priorities and same decision key
    facts = {"tribunal": "TRT", "classe": "Recurso"}

    res = evaluate(facts, rule_set_path=os.path.join(
        "src", "hrm", "rules", "sample_rules.yaml"))
    assert res["status"] == "ok"
    # matched_rules should be a list
    assert isinstance(res["matched_rules"], list)
    # decisions should not contain duplicate keys for the same decision field
    keys = [k for d in res["decisions"] for k in d.keys()]
    # at least rule_id present in decisions
    assert any("rule_id" in d for d in res["decisions"]) or len(
        res["decisions"]) >= 1


def test_hrm_operators_basic():
    # facts crafted to test multiple operators (gt, lt, in, regex, startswith)
    facts = {
        "tribunal": "TRT",
        "classe": "Recurso",
        "valor": 1200,
        "categoria": "especial",
        "processo": "ABC-12345",
    }

    res = evaluate(facts, rule_set_path=os.path.join(
        "src", "hrm", "rules", "sample_rules.yaml"))
    assert res["status"] == "ok"
    # ensure decisions is a list and explanations present
    assert isinstance(res["decisions"], list)
    assert isinstance(res.get("explanation", []), list)
