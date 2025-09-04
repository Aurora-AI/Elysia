from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonicalMetadata:
    source: str
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    language: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    tags: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
