from __future__ import annotations
import os
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from aurora_platform.modules.crawler.producers.enqueue import enqueue_crawl

app = FastAPI(title="Aurora Crawler API")

class EnqueueBody(BaseModel):
    url: HttpUrl
    source: str = "api"

@app.post("/crawl")
def crawl(b: EnqueueBody):
    enqueue_crawl(str(b.url), source=b.source)
    return {"enqueued": True, "url": str(b.url)}