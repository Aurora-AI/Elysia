from __future__ import annotations

import os
from typing import Any

# reaproveita as classes do loader
from src.hrm.hrm_loader import RuleSet, load_rules


def _matches(facts: dict[str, Any], conditions: dict[str, Any]) -> bool:
    """
    Casamento simples por igualdade rasa (chave -> valor).
    Futuras extensões: operadores (> < in regex), caminhos nested (a.b.c).
    """
    for k, v in (conditions or {}).items():
        if facts.get(k) != v:
            return False
    return True


def _explain(rule_id: str, conditions: dict[str, Any]) -> dict[str, Any]:
    return {
        "rule": rule_id,
        "why": "all 'when' conditions matched",
        "conditions": conditions or {},
    }


def evaluate(
    facts: dict[str, Any],
    rule_set_path: str | None = None,
) -> dict[str, Any]:
    """
    Avalia um RuleSet YAML sobre 'facts' e retorna decisão + justificativas.
    - facts: dicionário de fatos de entrada.
    - rule_set_path: caminho do arquivo YAML; se None, usa HRM_DEFAULT_RULESET.
    """
    rules_path = rule_set_path or os.getenv(
        "HRM_DEFAULT_RULESET", "src/hrm/rules/sample_rules.yaml")

    # If the rules_path is not found as given, try resolving relative to this package
    if not os.path.exists(rules_path):
        pkg_root = os.path.dirname(__file__)
        alt = os.path.join(pkg_root, "rules", os.path.basename(rules_path))
        if os.path.exists(alt):
            rules_path = alt

    rs: RuleSet = load_rules(rules_path)

    matched: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for r in rs.rules:
        if _matches(facts, r.when or {}):
            matched.append((r.id, r.when or {}, r.then or {}))

    # decisões: apenas agrega os 'then' das regras casadas; não resolve conflitos.
    # (Evolução: resolver conflitos por prioridade/precedência.)
    decisions: list[dict[str, Any]] = []
    explanations: list[dict[str, Any]] = []
    for rid, when, then in matched:
        decisions.append({"rule_id": rid, **then})
        explanations.append(_explain(rid, when))

    return {
        "status": "ok",
        "domain": rs.domain,
        "matched_rules": [rid for rid, _, _ in matched],
        "decisions": decisions,
        "explanation": explanations,
        "facts_echo": facts,
        "ruleset_version": rs.version,
        "ruleset_path": rules_path,
    }
