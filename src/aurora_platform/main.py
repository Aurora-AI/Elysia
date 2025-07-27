# src/aurora_platform/main.py - Versão Corrigida para Aurora-Core

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
import logging

# Importa apenas os roteadores que existem no Aurora-Core
# Importa apenas os roteadores que existem no Aurora-Core
from aurora_platform.api.v1.endpoints import (
    knowledge_router,
    auth_router
)
# Importa as configurações do local correto no Core
from aurora_platform.core.config import settings
from aurora_platform.services.knowledge_service import KnowledgeBaseService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de startup e shutdown
    logger.info("Iniciando Aurora-Core AIOS...")
    app.state.kb_service = KnowledgeBaseService()
    yield
    logger.info("Encerrando Aurora-Core AIOS...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Endpoint de verificação de saúde
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

# Inclui os roteadores do Core
app.include_router(
    knowledge_router.router, prefix="/api/v1/knowledge", tags=["Knowledge Base"]
)
app.include_router(
    auth_router.router, prefix="/api/v1/auth", tags=["Authentication"]
)
