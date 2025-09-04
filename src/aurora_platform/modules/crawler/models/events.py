from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, HttpUrl, Field
import time

class CrawlRequest(BaseModel):
    url: HttpUrl
    source: str = "manual"  # ou "seed", "api"
    depth: int = 0          # profundidade futura
    ts: int = Field(default_factory=lambda: int(time.time()))

class CrawlResult(BaseModel):
    url: HttpUrl
    status: int
    body_text: str
    links: List[str] = []
    meta: Dict[str, Any] = {}
    ts: int = Field(default_factory=lambda: int(time.time()))