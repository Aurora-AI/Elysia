from fastapi import APIRouter
from .endpoints import auth_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])

# Add other v1 routers here as the application grows
