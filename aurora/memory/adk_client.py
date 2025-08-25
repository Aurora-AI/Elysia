"""
Integração Aurora com Google ADK Memory Bank (Fase 1).
Suporta search_memory e autosave_to_memory.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform import VertexAi
except Exception:  # pragma: no cover - optional runtime dependency
    aiplatform = None  # type: ignore
    VertexAi = None  # type: ignore

# Configurações do ambiente (usando .env/.env.aura)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "aurora-dev")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MEMORY_BANK_ID = os.getenv("VERTEX_MEMORY_BANK_ID", "aurora-mem-dev")


def get_memory_client() -> Any:
    """Retorna cliente do Memory Bank (ou raise se driver ausente)."""
    if aiplatform is None or VertexAi is None:
        raise RuntimeError(
            "google-cloud-aiplatform is required: pip install google-cloud-aiplatform")
    VertexAi.init(project=PROJECT_ID, location=LOCATION)
    # Note: MemoryBank is used as an illustrative API surface; adapt if SDK differs.
    return aiplatform.MemoryBank(resource_name=MEMORY_BANK_ID)


def search_memory(query: str, scope: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Busca memórias relevantes no Memory Bank.
    :param query: Texto da consulta
    :param scope: Dicionário de escopo (ex: {"user_id": "u123"})
    """
    client = get_memory_client()
    results = client.query(query=query, scope=scope)
    # Normalize to plain dicts for upstream usage
    return [dict(r) for r in results]


def autosave_to_memory(conversation: List[Dict[str, Any]], scope: Dict[str, str]) -> None:
    """
    Salva conversação resumida no Memory Bank.
    :param conversation: Lista de turns {"role": "user/assistant", "content": "..."}
    :param scope: Escopo (user_id, team_id, etc.)
    """
    client = get_memory_client()
    client.save(conversation=conversation, scope=scope)
    print(f"[MemoryBank] Autosave realizado para escopo {scope}")
