__all__ = ["auth_router", "two_factor_router", "knowledge_router", "profiling_router"]

from .auth_router import router as auth_router
from .knowledge_router import router as knowledge_router
from .profiling_router import router as profiling_router
from .two_factor_router import router as two_factor_router

# TODO: Reativar na integração do Crawler
# from . import ingestion_router
