"""LangGraph adapter shim for Aurora.

This shim provides a stable interface (`generate`, `generate_async`) that
wraps a real `langgraph` client when available, or a lightweight fallback
implementation when not installed. The goal is to centralize LangGraph
compatibility work for the v0.6.5 upgrade.
"""
from __future__ import annotations

import importlib.util
from typing import Any, Dict, Optional


class LangGraphAdapter:
    """Adapter shim that normalizes LangGraph interactions.

    Methods:
        generate(prompt) -> dict
        generate_async(prompt) -> dict

    If the `langgraph` package is present, the adapter will try to use it;
    otherwise it returns a deterministic shim response useful for tests.
    """

    def __init__(self, client: Optional[Any] = None):
        self._client = client
        if self._client is None:
            spec = importlib.util.find_spec("langgraph")
            self._has_langgraph = spec is not None
            if self._has_langgraph:
                # Import lazily; exact API may vary across versions.
                import langgraph as _lg  # type: ignore

                # Try common client entrypoints; adapt as necessary in future.
                if hasattr(_lg, "Client"):
                    try:
                        self._client = _lg.Client()
                    except Exception:
                        self._client = None
                else:
                    self._client = None
            else:
                self._client = None
                self._has_langgraph = False

    def generate(self, prompt: str) -> Dict[str, Any]:
        """Synchronous generate wrapper.

        Returns a dict with at least a `text` key and optional metadata.
        """
        if self._client is not None:
            # Best-effort call; actual LangGraph client API may differ.
            try:
                # Prefer a `run` method if it exists.
                if hasattr(self._client, "run"):
                    out = self._client.run(prompt)
                    return {"text": str(out), "shim": False}
                # Fallback to a generic call
                out = self._client(prompt)
                return {"text": str(out), "shim": False}
            except Exception as e:
                return {"text": f"<langgraph-error: {e}>", "shim": False}

        # Fallback deterministic shim for testability
        return {"text": prompt, "shim": True, "run_id": None}

    async def generate_async(self, prompt: str) -> Dict[str, Any]:
        """Async wrapper; may call an async client method if available.

        For environments without LangGraph installed, returns the same shim
        deterministically.
        """
        if self._client is not None:
            try:
                if hasattr(self._client, "run_async"):
                    out = await self._client.run_async(prompt)  # type: ignore
                    return {"text": str(out), "shim": False}
                if hasattr(self._client, "run"):
                    # call sync run in executor if needed
                    out = self._client.run(prompt)
                    return {"text": str(out), "shim": False}
            except Exception as e:
                return {"text": f"<langgraph-error: {e}>", "shim": False}

        return {"text": prompt, "shim": True, "run_id": None}
