from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class CrawlRequest(BaseModel):
    url: HttpUrl
    source: str = "manual"  # ou "seed", "api"
    depth: int = 0  # profundidade futura
    ts: int = Field(default_factory=lambda: int(time.time()))


class CrawlResult(BaseModel):
    url: HttpUrl
    status: int
    body_text: str
    links: list[str] = []
    meta: dict[str, Any] = {}
    ts: int = Field(default_factory=lambda: int(time.time()))
