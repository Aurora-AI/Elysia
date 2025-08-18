from __future__ import annotations
from typing import Dict, Any, List
import yaml, hashlib, os

REQUIRED_ROOT_KEYS = ["mission_id", "objective", "topics", "entities"]
ALLOWED_OBJECTIVES = {"licitacoes", "estrutura_setorial", "legislacao", "ppp", "contatos"}

def _sha256_bytes(b: bytes) -> str:
    import hashlib as _h
    return _h.sha256(b).hexdigest()

def load_mission(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    raw = open(path, "rb").read()
    data = yaml.safe_load(raw) or {}
    # validações mínimas
    for k in REQUIRED_ROOT_KEYS:
        if k not in data:
            raise ValueError(f"mission missing required key: {k}")
    if data["objective"] not in ALLOWED_OBJECTIVES:
        raise ValueError(f"objective must be one of {sorted(ALLOWED_OBJECTIVES)}")
    if not isinstance(data["topics"], list) or not all(isinstance(t, str) and t.strip() for t in data["topics"]):
        raise ValueError("topics must be a non-empty list[str]")
    if not isinstance(data["entities"], list) or not data["entities"]:
        raise ValueError("entities must be a non-empty list")

    # normalizações
    data.setdefault("constraints", {})
    c = data["constraints"]
    c.setdefault("max_pages", 300)
    c.setdefault("per_host_cap", 80)
    c.setdefault("require_topic_match", True)
    c.setdefault("allow_non_official", False)
    c.setdefault("allowed_suffixes", [".rn.gov.br", ".gov.br"])

    # seeds/hosts opcionais
    data.setdefault("seeds", [])
    data.setdefault("hosts", [])

    # hash da missão p/ manifest
    data["_mission_hash"] = _sha256_bytes(raw)
    return data
