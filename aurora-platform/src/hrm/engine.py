from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml


@dataclass
class Rule:
    id: str
    when: Dict[str, Any] | None
    then: Dict[str, Any] | None
    priority: int = 0


@dataclass
class RuleSet:
    version: str
    domain: str
    rules: List[Rule]


def load_rules(path: str) -> RuleSet:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    rules = []
    for r in data.get("rules", []):
        rules.append(
            Rule(
                id=r.get("id"),
                when=r.get("when") or {},
                then=r.get("then") or {},
                priority=int(r.get("priority") or 0),
            )
        )
    return RuleSet(
        version=str(data.get("version", "1.0")),
        domain=str(data.get("domain", "generic")),
        rules=rules,
    )


def _to_number(v: Any) -> Optional[float]:
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.replace(",", "."))
        except Exception:
            return None
    return None


def _as_iterable(x: Any) -> List[Any]:
    if x is None:
        return []
    if isinstance(x, (list, tuple, set)):
        return list(x)
    return [x]


def _meets_op(value: Any, cond: Any) -> bool:
    """
    cond pode ser escalar (eq implícito) ou dict com operadores.
    Operadores suportados: eq, ne, gt, gte, lt, lte, in, nin, regex, startswith, endswith, contains
    """
    if not isinstance(cond, dict):
        return value == cond

    for op, expected in cond.items():
        if op == "eq":
            if not (value == expected):
                return False
        elif op == "ne":
            if not (value != expected):
                return False
        elif op in ("gt", "gte", "lt", "lte"):
            lv = _to_number(value)
            rv = _to_number(expected)
            if lv is None or rv is None:
                return False
            if op == "gt" and not (lv > rv):
                return False
            if op == "gte" and not (lv >= rv):
                return False
            if op == "lt" and not (lv < rv):
                return False
            if op == "lte" and not (lv <= rv):
                return False
        elif op == "in":
            if value not in _as_iterable(expected):
                return False
        elif op == "nin":
            if value in _as_iterable(expected):
                return False
        elif op == "regex":
            if not isinstance(value, str) or re.search(str(expected), value) is None:
                return False
        elif op == "startswith":
            if not (isinstance(value, str) and str(value).startswith(str(expected))):
                return False
        elif op == "endswith":
            if not (isinstance(value, str) and str(value).endswith(str(expected))):
                return False
        elif op == "contains":
            seq = expected if isinstance(
                expected, (list, tuple, set)) else [expected]
            if isinstance(value, str):
                # para string, contains: expected como substring
                if not all(str(e) in value for e in seq):
                    return False
            else:
                if not all(e in _as_iterable(value) for e in seq):
                    return False
        else:
            # operador desconhecido => falha
            return False
    return True


def _matches(facts: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
    for key, cond in (conditions or {}).items():
        if not _meets_op(facts.get(key), cond):
            return False
    return True


def evaluate(facts: Dict[str, Any], rule_set_path: str | None = None) -> Dict[str, Any]:
    path = rule_set_path or os.getenv(
        "HRM_DEFAULT_RULESET", "src/hrm/rules/sample_rules.yaml")
    rs: RuleSet = load_rules(path)

    ordered = sorted(rs.rules, key=lambda r: int(
        getattr(r, "priority", 0) or 0), reverse=True)

    matched: List[Tuple[str, Dict[str, Any], Dict[str, Any], int]] = []
    for r in ordered:
        if _matches(facts, r.when or {}):
            matched.append(
                (r.id, r.when or {}, r.then or {}, int(r.priority or 0)))

    decisions: List[Dict[str, Any]] = []
    explanations: List[Dict[str, Any]] = []
    decided_keys: set[str] = set()

    for rid, when, then, prio in matched:
        decided = {}
        for k, v in (then or {}).items():
            if k not in decided_keys:
                decided[k] = v
                decided_keys.add(k)
        if decided:
            decisions.append({"rule_id": rid, "priority": prio, **decided})
        explanations.append({"rule": rid, "priority": prio,
                            "why": "conditions matched", "conditions": when})

    return {
        "status": "ok",
        "domain": rs.domain,
        "matched_rules": [rid for rid, *_ in matched],
        "decisions": decisions,
        "explanation": explanations,
        "facts_echo": facts,
        "ruleset_version": rs.version,
        "ruleset_path": path,
    }


