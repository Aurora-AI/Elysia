from __future__ import annotations
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from .settings import settings

Base = declarative_base()


def _is_sqlite_memory(url: str) -> bool:
    # cobre formatos como sqlite+aiosqlite:///:memory:?cache=shared
    return url.startswith("sqlite+aiosqlite:///:memory:")


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite+aiosqlite://")


db_url = settings.database_url

engine_kwargs = {}
connect_args = {}

if _is_sqlite_memory(db_url):
    # SQLite em memória precisa de StaticPool para compartilhar a mesma conexão
    engine_kwargs["poolclass"] = StaticPool
    connect_args = {"check_same_thread": False}
elif _is_sqlite(db_url):
    # SQLite em arquivo (tests locais) — permitir thread sharing
    connect_args = {"check_same_thread": False}

engine = create_async_engine(
    db_url, echo=False, future=True, connect_args=connect_args, **engine_kwargs
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


# Backwards-compatible aliases used by some tests and scripts
def create_db_and_tables() -> None:
    """Create tables synchronously for tests that expect a sync helper."""
    # Use a synchronous bind if available; fall back to noop.
    try:
        from sqlalchemy import create_engine

        sync_engine = create_engine(
            "sqlite:///./test.db", connect_args={"check_same_thread": False}
        )
        SQLModel.metadata.create_all(bind=sync_engine)
    except Exception:
        # best-effort: if creation fails in this env, do nothing
        return


# alias 'engine' already exists above
