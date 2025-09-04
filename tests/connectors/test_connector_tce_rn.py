from __future__ import annotations

from typing import cast

import httpx
import pytest

from backend.app.connectors.tce_rn.pipeline import normalize
from backend.app.connectors.tce_rn.schemas import RawApiExpense


class MockTransport(httpx.BaseTransport):
    """
    Simula:
      - GET /expenses (duas páginas)
      - POST /ingest (aceita)
    """

    def __init__(self):
        self.calls = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.calls.append((request.method, str(request.url)))
        url = str(request.url)
        if url.endswith("/ingest"):
            return httpx.Response(200, json={"status": "accepted"})

        if "/expenses" in url:
            q = dict(request.url.params)
            page = int(q.get("page", "1"))
            if page == 1:
                data = {
                    "items": [
                        {
                            "orgao": "SEFAZ",
                            "fornecedor_nome": "ACME",
                            "fornecedor_cnpj": "12.345.678/0001-90",
                            "empenho_numero": "E1",
                            "valor_empenhado": 100.0,
                            "id_registro": "R1",
                        },
                        {
                            "orgao": "SESA",
                            "fornecedor_nome": "BETA",
                            "fornecedor_cnpj": "98.765.432/0001-10",
                            "empenho_numero": "E2",
                            "valor_empenhado": 200.0,
                            "id_registro": "R2",
                        },
                    ],
                    "page": 1,
                    "total_pages": 2,
                    "total": 4,
                }
            else:
                data = {
                    "items": [
                        {
                            "orgao": "SEED",
                            "fornecedor_nome": "GAMMA",
                            "fornecedor_cnpj": "11.111.111/0001-11",
                            "empenho_numero": "E3",
                            "valor_empenhado": 300.0,
                            "id_registro": "R3",
                        },
                        {
                            "orgao": "SEPLAN",
                            "fornecedor_nome": "DELTA",
                            "fornecedor_cnpj": "22.222.222/0001-22",
                            "empenho_numero": "E4",
                            "valor_empenhado": 400.0,
                            "id_registro": "R4",
                        },
                    ],
                    "page": 2,
                    "total_pages": 2,
                    "total": 4,
                }
            return httpx.Response(200, json=data)

        return httpx.Response(404, json={"error": "not found"})


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    # configura variáveis necessárias para os módulos
    monkeypatch.setenv("TCE_RN_BASE_URL", "https://mock.tce.rn")
    monkeypatch.setenv("AURORA_INGEST_URL", "https://aurora-docparser/ingest")
    monkeypatch.setenv("AURORA_INGEST_TOKEN", "test-token")


def test_normalize_cnpj_digits():
    raw = RawApiExpense(fornecedor_cnpj="12.345.678/0001-90", id_registro="R1")
    rec = normalize(raw)
    assert rec.fornecedor_cnpj == "12345678000190"


def test_client_pagination(monkeypatch):
    # Força o client do conector a usar o MockTransport
    transport = MockTransport()
    import backend.app.connectors.tce_rn.client as c

    def _client(*a, **k):
        return httpx.Client(transport=transport, base_url="https://mock.tce.rn")

    c._build_client = _client  # patcha a fábrica de client
    cli = c.TCERNClient()
    got = list(cli.iter_expenses(page_size=2))
    cli.close()
    assert len(got) == 4
    assert got[0].orgao == "SEFAZ"
    assert got[-1].orgao == "SEPLAN"


def test_pipeline_run(monkeypatch):
    # patches: fonte (/expenses) e destino (/ingest)
    transport = MockTransport()

    import backend.app.connectors.tce_rn.client as client_mod
    import backend.app.connectors.tce_rn.pipeline as pipe_mod

    def _client_source(*a, **k):
        return httpx.Client(transport=transport, base_url="https://mock.tce.rn")

    def _client_sink(*a, **k):
        return httpx.Client(transport=transport)

    client_mod._build_client = _client_source
    pipe_mod.httpx.Client = cast(type, _client_sink)

    res = pipe_mod.run(page_size=2)
    assert res["ok"] is True
    assert res["ingested"] == 4
