# src/aurora_platform/api/v1/api.py

from fastapi import APIRouter

from .endpoints.auth_router import router as auth_router
from .endpoints.etp_router import router as etp_router
from .endpoints.knowledge_router import router as knowledge_router
from .endpoints.profiling_router import router as profiling_router
from .endpoints.two_factor_router import router as two_factor_router

api_router = APIRouter()

# Inclui todos os roteadores com seus respectivos prefixos e tags
api_router.include_router(knowledge_router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(
    two_factor_router, prefix="/2fa", tags=["Two-Factor Authentication"]
)
api_router.include_router(profiling_router, prefix="/profiling", tags=["Profiling"])
api_router.include_router(etp_router, prefix="/etp", tags=["ETP"])
