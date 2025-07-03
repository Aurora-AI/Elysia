from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .api.v1.router import api_v1_router
from .core.config import settings
from .db.database import create_db_and_tables
from .middleware.rate_limiter import RateLimitMiddleware
from .middleware.security_headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    print("INFO:     Aurora Platform iniciando...")
    create_db_and_tables()
    yield
    print("INFO:     Aurora Platform encerrando...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API central para a plataforma Aurora, gerenciando CRM, integrações e serviços de IA.",
    lifespan=lifespan,
)

# Security Middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Trusted Host Middleware
if settings.HTTPS_ONLY:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "testserver", "*.aurora.local"]
    )

# Include routers
app.include_router(api_v1_router, prefix="/api")


@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "Bem-vindo à Aurora Platform",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs",
    }
