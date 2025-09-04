from .auth_router import router as auth_router
from .etp_router import router as etp_router
from .knowledge_router import router as knowledge_router
from .profiling_router import router as profiling_router
from .two_factor_router import router as two_factor_router

__all__ = ['auth_router', 'two_factor_router', 'knowledge_router', 'profiling_router', 'etp_router']


# NOTE: merged imports/__all__ with merge_candidates version
