# tests/conftest.py
import os
import pytest
import requests

def qdrant_is_ready(url: str) -> bool:
    try:
        r = requests.get(f"{url.rstrip('/')}/ready", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    enable = os.getenv("ENABLE_QDRANT_TESTS") == "1"
    qurl = os.getenv("QDRANT_URL", "http://localhost:6333")
    if not enable or not qdrant_is_ready(qurl):
        skip = pytest.mark.skip(reason="Qdrant indisponível ou ENABLE_QDRANT_TESTS != 1")
        for item in items:
            # Heurística simples: pula testes da pasta rag
            if "tests/modules/rag" in str(item.fspath):
                item.add_marker(skip)