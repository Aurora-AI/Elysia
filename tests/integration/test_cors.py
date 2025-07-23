import pytest
import requests

BASE_URL = "http://localhost:8001"


@pytest.mark.integration
def test_cors_blocked_origin():
    headers = {"Origin": "http://malicioso.com"}
    r = requests.get(f"{BASE_URL}/health", headers=headers)
    assert r.headers.get("access-control-allow-origin") is None


@pytest.mark.integration
def test_cors_allowed_origin():
    import os

    allowed = os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")[0]
    headers = {"Origin": allowed}
    r = requests.get(f"{BASE_URL}/health", headers=headers)
    assert r.headers.get("access-control-allow-origin") == allowed
