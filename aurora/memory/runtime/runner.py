"""Helpers to build an ADK Runner with injected Memory Service."""

from __future__ import annotations

from typing import Any

try:
    from google.adk.runners import Runner  # type: ignore
except Exception:  # pragma: no cover - optional runtime
    Runner = None  # type: ignore


def build_runner(agent: Any, session_service: Any, memory_service: Any, app_name: str) -> Any:
    """Return a Runner configured with memory_service injected.

    Raises RuntimeError if Runner class is unavailable.
    """
    if Runner is None:
        raise RuntimeError("google-adk runners not available: install the ADK packages")
    return Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
        memory_service=memory_service,
    )
