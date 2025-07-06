import os
import pytest
from fastapi.testclient import TestClient

from src.aurora_platform.main import app

# Set testing environment
os.environ["TESTING"] = "1"

@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client