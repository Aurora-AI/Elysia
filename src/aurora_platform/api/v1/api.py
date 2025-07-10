# src/aurora_platform/api/v1/api.py

from fastapi import APIRouter

# Importando os roteadores existentes
from aurora_platform.api.v1.endpoints.auth_router import router as auth_api_router
from aurora_platform.api.v1.endpoints.users_router import router as users_api_router

# --- ADIÇÃO 1: Importe o novo roteador de conhecimento ---
from aurora_platform.api.v1.knowledge_router import router as knowledge_api_router

api_router = APIRouter()

# Incluindo os roteadores existentes
api_router.include_router(auth_api_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_api_router, prefix="/users", tags=["Users"])

# --- ADIÇÃO 2: Inclua o roteador de conhecimento na API principal ---
api_router.include_router(knowledge_api_router)