from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel, HttpUrl


class DocumentMacro(BaseModel):
    doc_id: str
    url: HttpUrl
    text: str
    meta: dict[str, Any] = {}
    ts: int = int(time.time())


class ChunkResult(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    meta: dict[str, Any] = {}
