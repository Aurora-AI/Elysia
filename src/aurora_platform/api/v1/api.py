# src/aurora_platform/api/v1/api.py

from fastapi import APIRouter
from .endpoints import auth_router, users_router, knowledge_router, two_factor_router

api_router = APIRouter()

# Inclui todos os roteadores da aplicação
api_router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router.router, prefix="/users", tags=["Users"])
api_router.include_router(two_factor_router.router, prefix="/2fa", tags=["Two-Factor Authentication"])
api_router.include_router(knowledge_router.router) # O prefixo já está no roteador