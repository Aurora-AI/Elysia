import os
from typing import Optional


def env_str(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Read env var, but be tolerant when running tests (TESTING=1).

    This allows pytest collection to import modules that expect env vars
    while test fixtures or the test runner set them later.
    """
    val = os.getenv(name, default)
    testing = os.getenv("TESTING")
    if required and not val and not testing:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


TCE_RN_BASE_URL = env_str("TCE_RN_BASE_URL", required=True)
TCE_RN_API_KEY = env_str("TCE_RN_API_KEY", required=False)
TCE_RN_EXPENSES_PATH = env_str(
    "TCE_RN_EXPENSES_PATH", "/expenses") or "/expenses"

PAGE_SIZE = int(env_str("CONNECTOR_DEFAULT_PAGE_SIZE", "100") or "100")
HTTP_TIMEOUT = int(env_str("CONNECTOR_HTTP_TIMEOUT", "30") or "30")
MAX_RETRIES = int(env_str("CONNECTOR_MAX_RETRIES", "5") or "5")

AURORA_INGEST_URL = env_str("AURORA_INGEST_URL", required=True)
AURORA_INGEST_TOKEN = env_str("AURORA_INGEST_TOKEN", required=True)
