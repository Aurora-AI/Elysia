import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from aurora_platform.main import app

# Set testing environment
os.environ["TESTING"] = "1"


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session using in-memory SQLite"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client
