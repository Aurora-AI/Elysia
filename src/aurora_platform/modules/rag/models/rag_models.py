from __future__ import annotations
from typing import Dict, Any, List
from pydantic import BaseModel, HttpUrl
import time

class DocumentMacro(BaseModel):
    doc_id: str
    url: HttpUrl
    text: str
    meta: Dict[str, Any] = {}
    ts: int = int(time.time())

class ChunkResult(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    meta: Dict[str, Any] = {}