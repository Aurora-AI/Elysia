from __future__ import annotations

import hashlib
import importlib
import os
from typing import Any

from .client import TCERNClient
from .config import AURORA_INGEST_TOKEN, AURORA_INGEST_URL
from .schemas import ExpenseRecord, IngestEnvelope, RawApiExpense

# Use a local proxy for httpx so tests can monkeypatch `pipe_mod.httpx.Client`
# without mutating the global httpx module.
_real_httpx = importlib.import_module("httpx")


class _HttpxProxy:
    # annotate Client to please static type checkers; runtime assignment below is valid
    Client: type


httpx = _HttpxProxy()
httpx.Client = _real_httpx.Client  # type: ignore[attr-defined]


def _cnpj_digits(cnpj: str | None) -> str | None:
    if not cnpj:
        return None
    return "".join(ch for ch in cnpj if ch.isdigit())


def _deterministic_id(raw: RawApiExpense) -> str:
    """
    Determinístico entre execuções (evita o hash aleatório do Python).
    Usa campos-chave; se houver id_registro, prioriza.
    """
    if raw.id_registro:
        return raw.id_registro
    key = "|".join(
        [
            raw.orgao or "",
            raw.unidade or "",
            (raw.fornecedor_cnpj or ""),
            raw.empenho_numero or "",
            raw.competencia or "",
        ]
    )
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()
    return f"tce-rn-{h}"


def normalize(raw: RawApiExpense) -> ExpenseRecord:
    return ExpenseRecord(
        record_id=_deterministic_id(raw),
        orgao=raw.orgao,
        unidade=raw.unidade,
        fornecedor_nome=raw.fornecedor_nome,
        fornecedor_cnpj=_cnpj_digits(raw.fornecedor_cnpj),
        empenho_numero=raw.empenho_numero,
        empenho_data=raw.empenho_data,
        licitacao_modalidade=raw.licitacao_modalidade,
        objeto=raw.objeto,
        processo=raw.processo,
        classificacao_despesa=raw.classificacao_despesa,
        natureza_despesa=raw.natureza_despesa,
        funcao=raw.funcao,
        subfuncao=raw.subfuncao,
        programa=raw.programa,
        acao=raw.acao,
        valor_empenhado=raw.valor_empenhado,
        valor_liquidado=raw.valor_liquidado,
        valor_pago=raw.valor_pago,
        competencia=raw.competencia,
        municipio=raw.municipio,
        uf=raw.uf,
        fonte_dados=raw.fonte_dados or "api_tce_rn",
    )


def _post_ingest(payload: IngestEnvelope) -> dict[str, Any]:
    ingest_url = AURORA_INGEST_URL or os.getenv("AURORA_INGEST_URL")
    ingest_token = AURORA_INGEST_TOKEN or os.getenv("AURORA_INGEST_TOKEN")
    if not ingest_url:
        raise RuntimeError("AURORA_INGEST_URL not configured")

    with httpx.Client(timeout=60) as client:
        r = client.post(
            ingest_url,
            json=payload.model_dump(mode="json"),
            headers={
                "Authorization": f"Bearer {ingest_token}",
                "Content-Type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()


def run(
    date_from: str | None = None,
    date_to: str | None = None,
    page_size: int | None = None,
    max_pages: int | None = None,
    batch_size: int = 500,
) -> dict[str, Any]:
    """
    Extrai, normaliza e envia registros ao Aurora DocParser++ em lotes.
    """
    client = TCERNClient()
    total = 0
    batch: list[ExpenseRecord] = []
    try:
        for raw in client.iter_expenses(
            date_from=date_from, date_to=date_to, page_size=page_size or 100, max_pages=max_pages
        ):
            rec = normalize(raw)
            batch.append(rec)
            if len(batch) >= batch_size:
                _post_ingest(IngestEnvelope(items=batch))
                total += len(batch)
                batch.clear()
        if batch:
            _post_ingest(IngestEnvelope(items=batch))
            total += len(batch)
    finally:
        client.close()

    return {
        "ok": True,
        "ingested": total,
        "date_from": date_from,
        "date_to": date_to,
    }
