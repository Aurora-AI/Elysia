from fastapi import FastAPI
from aurora_platform.api.kg_endpoints import router as kg_router

app = FastAPI(
    title="Aurora Platform API",
    description="API unificada para Kafka + Knowledge Graph",
    version="2.0.0"
)

app.include_router(kg_router)

@app.get("/")
async def root():
    return {"message": "Aurora Platform API - Kafka + KG RAG 2.0", "version": "2.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "aurora-platform"}
