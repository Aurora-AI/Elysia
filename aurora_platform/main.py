# src/aurora_platform/main.py - Versão Corrigida para Aurora-Core



import logging
import os
from contextlib import asynccontextmanager

import firebase_admin
import sentry_sdk
from fastapi import FastAPI, status
from firebase_admin import credentials
from aurora_platform.core.config import settings
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.api.v1.endpoints import auth_router, knowledge_router, debug_router
from aurora_platform.api.v1.routers import system_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa o Sentry ANTES de criar o app FastAPI
if getattr(settings, "SENTRY_DSN", None):
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        environment=getattr(settings, "ENVIRONMENT", "development"),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "google-credentials.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar Firebase Admin SDK: {e}")
        raise RuntimeError(f"Falha na inicialização do Firebase: {e}")
    logger.info("Iniciando Aurora-Core AIOS...")
    app.state.kb_service = KnowledgeBaseService()
    yield
    logger.info("Encerrando Aurora-Core AIOS...")

app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", "Aurora Platform API"),
    version=getattr(settings, "PROJECT_VERSION", "1.0.0"),
    lifespan=lifespan
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

app.include_router(
    knowledge_router, prefix="/api/v1/knowledge", tags=["Knowledge Base"]
)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    debug_router.router,
    prefix="/api/v1/debug",
    tags=["Debug"]
)
app.include_router(system_router.router, prefix="/v1/system", tags=["System"])
