from __future__ import annotations

from dataclasses import dataclass
import os
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """
    Configurações centrais da Aurora.
    - ENV: dev|staging|prod (AURORA_ENV)
    - DB_URL: string de conexão SQLAlchemy (DATABASE_URL)
    - DB_ECHO: echo SQLAlchemy (DB_ECHO=true/1 habilita)
    - TESTING: flag automática se em pytest
    """
    ENV: str = os.getenv("AURORA_ENV", "dev")
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aurora.db")
    DB_ECHO: bool = os.getenv("DB_ECHO", "0").lower() in {"1", "true", "yes"}
    TESTING: bool = bool(os.getenv("PYTEST_CURRENT_TEST"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna Settings memoizado (barato e estável durante o processo)."""
    return Settings()


__all__ = ["Settings", "get_settings"]
