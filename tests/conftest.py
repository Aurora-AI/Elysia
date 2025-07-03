import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from aurora_platform.main import app
from aurora_platform.db.database import get_session
from aurora_platform.db.models.user_model import User
from aurora_platform.core.security import get_password_hash

# Set testing environment
os.environ["TESTING"] = "1"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user