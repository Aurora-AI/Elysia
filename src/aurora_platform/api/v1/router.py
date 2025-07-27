from fastapi import APIRouter
from .endpoints import (
    auth_router,
    two_factor_router,
    knowledge_router,
    profiling_router,
)

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_v1_router.include_router(two_factor_router, prefix="/v1/2fa", tags=["2fa"])
api_v1_router.include_router(knowledge_router)
api_v1_router.include_router(
    profiling_router, prefix="/v1/profiling", tags=["Agent Profiling"]
)

# Add other v1 routers here as the application grows
