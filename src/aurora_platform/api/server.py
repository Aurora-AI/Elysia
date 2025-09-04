from __future__ import annotations
from fastapi import FastAPI
from aurora_platform.modules.rag.api.memory_api import router as memory_router
from aurora_platform.bridge.elysia_bridge import router as elysia_bridge_router

app = FastAPI(title="Aurora Platform API")

app.include_router(memory_router, prefix="/api/v1/memory")
app.include_router(elysia_bridge_router)

@app.get("/")
def root():
    return {"message": "Aurora Platform API"}