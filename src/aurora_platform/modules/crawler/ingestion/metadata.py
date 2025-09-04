from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class CanonicalMetadata:
    source: str
    title: Optional[str] = None
    authors: list[str] = field(default_factory=list)
    language: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
