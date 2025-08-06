import pytest
import requests

BASE_URL = "http://localhost:8001"


@pytest.mark.integration
def test_rate_limiting_exceeded():
    for i in range(105):
        r = requests.get(f"{BASE_URL}/health")
        if i >= 100:
            assert r.status_code == 429
            assert "Rate limit exceeded" in r.text


@pytest.mark.integration
def test_rate_limiting_reset():
    import time

    for i in range(100):
        requests.get(f"{BASE_URL}/health")
    time.sleep(61)
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
