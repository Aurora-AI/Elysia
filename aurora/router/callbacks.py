"""
Callbacks do AuroraRouter para integração com Memory Bank (Fase 1).
"""
from typing import Any

from aurora.memory.adk_client import autosave_to_memory, search_memory


def preload_memory(scope: dict[str, str]) -> list[dict[str, Any]]:
    """Recupera memórias no início da sessão"""
    return search_memory("contexto inicial", scope=scope)


def post_turn_autosave(conversation: list[dict[str, Any]], scope: dict[str, str]) -> None:
    """Callback após cada interação para salvar memória"""
    autosave_to_memory(conversation, scope=scope)
