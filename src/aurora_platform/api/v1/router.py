from fastapi import APIRouter
from .endpoints import auth_router, two_factor_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router.router, prefix="/v1/auth", tags=["auth"])
api_v1_router.include_router(two_factor_router.router, prefix="/v1/2fa", tags=["2fa"])

# Add other v1 routers here as the application grows
