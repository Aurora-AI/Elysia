# src/aurora_platform/api/v1/api.py

from fastapi import APIRouter
from .endpoints import knowledge_router, auth_router, two_factor_router, users_router

api_router = APIRouter()

# Inclui todos os roteadores com seus respectivos prefixos e tags
api_router.include_router(knowledge_router.router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(two_factor_router.router, prefix="/2fa", tags=["Two-Factor Authentication"])
api_router.include_router(users_router.router, prefix="/users", tags=["Users"])