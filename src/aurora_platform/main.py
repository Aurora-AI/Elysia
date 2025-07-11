from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from aurora_platform.api.v1.api import api_router
from aurora_platform.services.knowledge_service import KnowledgeBaseService

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO: Iniciando aplicação... Pré-carregando KnowledgeBaseService.")
    app.state.kb_service = KnowledgeBaseService()
    print("INFO: KnowledgeBaseService carregado e pronto.")
    yield
    print("INFO: Encerrando aplicação...")

app = FastAPI(title="Aurora Core", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Aurora Core"}