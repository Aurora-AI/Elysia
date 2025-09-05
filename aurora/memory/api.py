from __future__ import annotations

from typing import Any


async def autosave_session_to_memory(memory_service: Any, session_obj: Any) -> None:
    """Extract facts from session and store them in the Memory Bank.

    This function delegates to the memory_service implementation (ADK/Vertex).
    """
    # In ADK, this is often a sync call; we support either.
    fn = getattr(memory_service, "add_session_to_memory", None) or getattr(
        memory_service, "save", None
    )
    if fn is None:
        raise RuntimeError("memory_service does not implement add_session_to_memory/save")
    res = fn(session_obj)
    if hasattr(res, "__await__"):
        await res


async def search_memory(
    memory_service: Any, app_name: str, user_id: str, query: str, team_id: str | None = None
) -> list[dict[str, Any]]:
    """Search memories scoped by user_id (and optionally team_id).

    Returns a list of memory records (dict-like).
    """
    scoped_app = f"{app_name}::team={team_id}" if team_id else app_name
    fn = getattr(memory_service, "search_memory", None) or getattr(memory_service, "query", None)
    if fn is None:
        raise RuntimeError("memory_service does not implement search_memory/query")
    res = fn(app_name=scoped_app, user_id=user_id, query=query)
    if hasattr(res, "__await__"):
        res = await res
    return list(res or [])
