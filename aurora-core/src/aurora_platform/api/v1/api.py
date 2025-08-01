# src/aurora_platform/api/v1/api.py

from fastapi import APIRouter

from .endpoints import (
    auth_router,
    knowledge_router,
    profiling_router,
    two_factor_router,
)

api_router = APIRouter()

# Inclui todos os roteadores com seus respectivos prefixos e tags
api_router.include_router(knowledge_router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(
    two_factor_router, prefix="/2fa", tags=["Two-Factor Authentication"]
)
api_router.include_router(profiling_router, prefix="/profiling", tags=["Profiling"])
