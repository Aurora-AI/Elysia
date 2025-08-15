from __future__ import annotations

from typing import Any, Dict, Iterator, Optional

import httpx
try:
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
except Exception:  # pragma: no cover - fallback when tenacity not installed
    def retry(*args, **kwargs):
        def _decorator(f):
            return f

        return _decorator

    def retry_if_exception_type(*args, **kwargs):
        return None

    def stop_after_attempt(*args, **kwargs):
        return None

    def wait_exponential(*args, **kwargs):
        return None

from .config import (
    HTTP_TIMEOUT,
    MAX_RETRIES,
    PAGE_SIZE,
    TCE_RN_API_KEY,
    TCE_RN_BASE_URL,
    TCE_RN_EXPENSES_PATH,
)
from .schemas import RawApiExpense


class ApiError(Exception):
    pass


def _headers() -> Dict[str, str]:
    h = {"Accept": "application/json"}
    if TCE_RN_API_KEY:
        h["Authorization"] = f"Bearer {TCE_RN_API_KEY}"
    return h


def _build_client() -> httpx.Client:
    return httpx.Client(base_url=TCE_RN_BASE_URL, timeout=HTTP_TIMEOUT, headers=_headers())


@retry(
    reraise=True,
    retry=retry_if_exception_type((httpx.HTTPError, ApiError)),
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
)
def _request(client: httpx.Client, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    r = client.get(url, params=params)
    if r.status_code >= 500:
        raise ApiError(f"Server error {r.status_code}")
    r.raise_for_status()
    return r.json()


class TCERNClient:
    """
    Cliente de alto nível para a API do TCE-RN.
    O caminho do recurso é configurável por `TCE_RN_EXPENSES_PATH`.
    """

    def __init__(self, client: Optional[httpx.Client] = None):
        self._client = client or _build_client()

    def iter_expenses(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page_size: int = PAGE_SIZE,
        max_pages: Optional[int] = None,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> Iterator[RawApiExpense]:
        """
        Itera registros paginados. Funciona com:
        - paginação por `page`/`page_size` + `total_pages`/`total`
        - OU cursor `next` quando não há metadados de página.
        """
        params = dict(extra_params or {})
        if date_from:
            params["data_inicial"] = date_from
        if date_to:
            params["data_final"] = date_to

        page = 1
        fetched_pages = 0

        while True:
            params.update({"page": page, "page_size": page_size})
            data = _request(
                self._client, url=TCE_RN_EXPENSES_PATH, params=params)
            items = data.get("items") or data.get("data") or []
            for it in items:
                yield RawApiExpense.model_validate(it)

            total_pages = data.get("total_pages")
            if total_pages is None:
                total = data.get("total")
                if total is None:
                    next_token = data.get("next")
                    if next_token:
                        params["cursor"] = next_token
                        page += 1
                        continue
                    break
                else:
                    total_pages = (total + page_size - 1) // page_size

            page += 1
            fetched_pages += 1
            if (max_pages and fetched_pages >= max_pages) or (total_pages and page > total_pages):
                break

    def close(self) -> None:
        self._client.close()
