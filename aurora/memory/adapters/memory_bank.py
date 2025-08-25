"""Factory for Vertex AI Memory Bank service adapter.

This module provides a small factory that returns a memory_service compatible
with the ADK/Vertex interfaces used in the OS. It wraps import errors and
documents where to find the relevant classes.
"""
from __future__ import annotations

import os
from typing import Any, Optional

try:
    # The ADK package namespaces may differ; the doc references google.adk.memory
    from google.adk.memory import VertexAiMemoryBankService  # type: ignore
except Exception:  # pragma: no cover - optional runtime
    VertexAiMemoryBankService = None  # type: ignore


def create_memory_service(project: Optional[str] = None, location: Optional[str] = None, agent_engine_id: Optional[str] = None) -> Any:
    """Create a Vertex AI Memory Bank service instance.

    Args:
        project: GCP project id (falls back to env GOOGLE_CLOUD_PROJECT)
        location: GCP region (falls back to env GOOGLE_CLOUD_LOCATION)
        agent_engine_id: Agent Engine id used by the Memory Bank integration

    Returns:
        An instance of VertexAiMemoryBankService (or raises RuntimeError if SDK is missing).
    """
    project = project or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = location or os.getenv("GOOGLE_CLOUD_LOCATION")
    agent_engine_id = agent_engine_id or os.getenv("AGENT_ENGINE_ID")

    if VertexAiMemoryBankService is None:
        raise RuntimeError(
            "google-adk MemoryBank SDK not available: install the ADK packages")

    return VertexAiMemoryBankService(
        project=project,
        location=location,
        agent_engine_id=agent_engine_id,
    )
