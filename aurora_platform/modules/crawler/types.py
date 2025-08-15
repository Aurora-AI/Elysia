from __future__ import annotations
from typing import TypedDict, Dict, Any, Protocol


class LoadedDocument(TypedDict):
    text: str
    metadata: Dict[str, Any]


class LoaderProtocol(Protocol):
    def load(self, *, source: str, content_type: str |
             None = None) -> LoadedDocument: ...
