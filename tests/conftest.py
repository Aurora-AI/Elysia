import os
import sys
import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from aurora_platform.core.db import Base, engine, SessionLocal

# Ensure aurora-core/src is on sys.path for imports
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SRC = os.path.join(REPO, "aurora-core", "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


@pytest.fixture(scope="session")
def event_loop():
    # Permite escopo de sessão para async tests
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def _create_test_schema():
    # Cria o schema do SQLAlchemy em memória (sem alembic) para os testes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Limpa ao final da sessão de testes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
