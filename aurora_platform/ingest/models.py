from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    source_url: Optional[str] = None
    file_b64: Optional[str] = None
    mime: Optional[str] = None


class Chunk(BaseModel):
    id: str
    doc_id: str
    order: int
    text: str
    section: Optional[str] = None
    page: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestResult(BaseModel):
    doc_id: str
    chunks_count: int
