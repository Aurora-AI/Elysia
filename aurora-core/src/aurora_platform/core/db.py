
from __future__ import annotations
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing import AsyncGenerator
import os


def create_db_and_tables_sync() -> None:

    # aurora-core/src/aurora_platform/core/db.py


    # URL do banco via env; fallback para SQLite assíncrono local
    # Exemplos:
    #   sqlite+aiosqlite:///./aurora.db
    #   postgresql+asyncpg://user:pass@localhost:5432/aurora
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///./aurora.db")

# Engine assíncrono (SQLAlchemy 2.x)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # mude para True se quiser logs SQL
    pool_pre_ping=True,  # detecta conexões “mortas”
    future=True,
)

# Session factory (assíncrona)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def init_db() -> None:
    """
    Cria as tabelas definidas no metadata do SQLModel.
    Use apenas em ambientes controlados (dev/test).
    Em prod, prefira migrations (Alembic).
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency padrão (FastAPI) / gerador de sessão para testes.
    """
    async with AsyncSessionLocal() as session:
        yield session
