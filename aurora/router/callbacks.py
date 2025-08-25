"""
Callbacks do AuroraRouter para integração com Memory Bank (Fase 1).
"""
from typing import Dict, Any, List
from aurora.memory.adk_client import search_memory, autosave_to_memory


def preload_memory(scope: Dict[str, str]) -> List[Dict[str, Any]]:
    """Recupera memórias no início da sessão"""
    return search_memory("contexto inicial", scope=scope)


def post_turn_autosave(conversation: List[Dict[str, Any]], scope: Dict[str, str]) -> None:
    """Callback após cada interação para salvar memória"""
    autosave_to_memory(conversation, scope=scope)
