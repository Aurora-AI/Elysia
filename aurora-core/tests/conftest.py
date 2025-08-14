from aurora_platform.main import app
from fastapi.testclient import TestClient
import os
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Set testing environment
os.environ["TESTING"] = "1"


@pytest.fixture(scope="session", autouse=True)
def _bootstrap_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield

    # Optionally: SQLModel.metadata.drop_all(engine)


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
