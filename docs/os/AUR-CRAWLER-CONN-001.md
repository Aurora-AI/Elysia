# Ordem de Serviço — AUR-CRAWLER-CONN-001
**Título:** Conector Piloto — API TCE‑RN (Banco de Preços / Despesas)
**Origem:** AUR-ARCH-CRAWLER-001 (Arquiteto de Agentes – GPT‑5)
**Agente Designado:** Executor (GitHub Copilot Chat no VSCode)
**Fonte da Verdade:** `/docs/CODICE_AURORA.md` (vivo)
**Objetivo:** Implementar um conector robusto e testado para a API do TCE‑RN, normalizar os dados no modelo canónico Aurora e entregar ao Aurora DocParser++ via `/ingest`.

## 0) Pré‑requisitos
- Python 3.11+; Poetry/pip.
- Dependências: `httpx`, `tenacity`, `pydantic>=2`, `pytest`.
- Variáveis de ambiente:
  - `TCE_RN_BASE_URL` (ex.: `https://api.tce.rn.gov.br`)
  - `TCE_RN_API_KEY` (opcional)
  - `TCE_RN_EXPENSES_PATH` (default `/expenses`; ajuste para `/despesas` etc.)
  - `CONNECTOR_DEFAULT_PAGE_SIZE` (default `100`)
  - `AURORA_INGEST_URL` (ex.: `https://aurora-docparser/ingest`)
  - `AURORA_INGEST_TOKEN` (Bearer)

## 1) Estrutura

```
/backend/app/connectors/tce_rn/__init__.py
/backend/app/connectors/tce_rn/config.py
/backend/app/connectors/tce_rn/schemas.py
/backend/app/connectors/tce_rn/client.py
/backend/app/connectors/tce_rn/pipeline.py
/tests/connectors/test_connector_tce_rn.py
```

## 2) Critérios de Aceite
- Estrutura criada nos caminhos exatos.
- Testes verdes em `tests/connectors/test_connector_tce_rn.py`.
- `run()` retorna `{"ok": true, "ingested": N, ...}`.
- Normalização e ID canónico determinístico; robustez (timeout, retries).

## 3) Observações
- `TCE_RN_EXPENSES_PATH` parametrizado.
- Cursor (`next`) suportado além de `page/total_pages`.
- Envelope de ingestão: `connector="tce_rn"`, `schema="expense_v1"`.

## Comandos rápidos

```bash
# criar diretórios
mkdir -p docs/os backend/app/connectors/tce_rn tests/connectors

# dependências
poetry add httpx tenacity pydantic pytest

# rodar testes do conector
PYTHONPATH=. TESTING=1 poetry run pytest -q tests/connectors/test_connector_tce_rn.py
```


---
CONCLUSÃO DA ORDEM DE SERVIÇO
- Status: FINALIZADA
- Data: 2025-08-22
- Responsável: Rodrigo C. Winhaski
- Observações: Ações realizadas (resumo): merge direto via API (HTTP 204), branch rd/20250820-004-docparser-testing-shortcut deletada (HTTP 204).
---
