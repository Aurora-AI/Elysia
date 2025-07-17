# src/aurora_platform/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.aurora_platform.api.v1.endpoints import auth_router, knowledge_router, mentor_router, profiling_router, converse_router, browser_router
from src.aurora_platform.api.routers import etp_router
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação. Carrega o KnowledgeBaseService
    na inicialização e o mantém disponível no estado da aplicação.
    """
    print("INFO: Iniciando aplicação... Pré-carregando KnowledgeBaseService.")
    app.state.kb_service = KnowledgeBaseService()
    print("INFO: KnowledgeBaseService carregado e pronto.")
    
    yield
    
    print("INFO: Encerrando aplicação...")

# Passa a função lifespan para a instância principal do FastAPI
app = FastAPI(
    title="Aurora-Core AIOS",
    description="O Kernel do Sistema Operacional de IA da Aurora.",
    version="0.1.0",
    lifespan=lifespan
)

# Adiciona o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Inclui os roteadores na aplicação principal da API
app.include_router(auth_router.router)
app.include_router(converse_router.router)
app.include_router(mentor_router.router)
app.include_router(knowledge_router.router)
app.include_router(profiling_router.router, prefix="/v1/profiling", tags=["Agent Profiling"])

app.include_router(etp_router.router, prefix="/v1", tags=["ETP Generator"])
app.include_router(browser_router.router, prefix="/v1", tags=["Browser Engine"])

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar a saúde da API."""
    return {"message": "Bem-vindo ao Aurora-Core AIOS. O sistema está operacional."}