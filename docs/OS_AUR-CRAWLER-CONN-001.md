# Ordem de Serviço: AUR-CRAWLER-CONN-001

Título: Conector piloto para o Banco de Preços (TCE-RN)

Agente Designado: Arquiteto de Agentes (GPT-5)

Fonte da Verdade: /docs/CODICE_AURORA.md

Resumo: Esta OS descreve, fase a fase, a implementação de um conector piloto para a API do TCE-RN. Inclui os contratos de dados (Pydantic), o cliente HTTP com retentativas e paginação, um pipeline de ingestão que normaliza e empurra os registos para o endpoint de ingestão e testes unitários que validam a normalização sem depender da API externa.

## Fase 1 — Estrutura e Contratos de Dados

Diretório: `backend/app/connectors/tce_rn/`

Criar `schemas.py` com modelos Pydantic canónicos para despesas (empenho/liquidação/pagamento). O modelo visa capturar campos essenciais e servir como contrato para downstream.

Arquivo: `backend/app/connectors/tce_rn/schemas.py` (fornecido)

Critério de aceite:

- Modelos Pydantic validados com testes unitários.

## Fase 2 — Implementação do Cliente da API

Diretriz: Implementar `client.py` com:

- `TceRnClient` que encapsula `httpx.Client` e lógica de paginação.
- Retentativas com backoff exponencial (usa `tenacity` quando disponível, ou fallback interno).
- Tratamento de erros e logs.

Arquivo: `backend/app/connectors/tce_rn/client.py` (fornecido)

Critério de aceite:

- Métodos documentados e testáveis (sem necessidade de conexão real).

## Fase 3 — Integração com Pipeline de Ingestão

Diretriz: Implementar `pipeline.py` que usa `TceRnClient` para extrair lotes, normalizar via `schemas.py` e, opcionalmente, enviar para um endpoint `/ingest` (parametrizável).

Arquivo: `backend/app/connectors/tce_rn/pipeline.py` (fornecido)

Critério de aceite:

- Função `run_pipeline` que retorna lista de registros normalizados e pode postar para `ingest_url` se fornecido.

## Fase 4 — Testes de Integração e Evals

Diretriz: Fornecer `tests/test_connector_tce_rn.py` com testes que:

- Verifiquem a normalização de entradas de exemplo.
- Validem comportamento de paginação/consumo sem chamar a API real (mock do `TceRnClient`).
- Sugerir um `eval` simples que mede taxa de sucesso na normalização em um lote de 100 registos sintéticos.

Arquivo: `backend/app/connectors/tce_rn/tests/test_connector_tce_rn.py` (fornecido)

Critério de aceite:

- Testes passam em CI sem rede (mocks locais).

---

### Observações de Segurança e Governança

- Nunca enviar dados sensíveis para serviços externos durante POC; usar dados anonimizados ou sintéticos.
- Logar metadados de execução no Córtex (ver /backend/app/core/cortex_logger.py) ao finalizar cada batch.

---

Arquivos adicionados (implementação técnica entregue):

- `backend/app/connectors/tce_rn/schemas.py`
- `backend/app/connectors/tce_rn/client.py`
- `backend/app/connectors/tce_rn/pipeline.py`
- `backend/app/connectors/tce_rn/tests/test_connector_tce_rn.py`

Execução: O Executor (Copilot) pode agora aplicar estes arquivos; testes locais cobrem normalização. Para integração real com a API do TCE-RN, configure variáveis de ambiente (BASE_URL, API_KEY se necessário) e execute `run_pipeline(..., ingest_url=...)`.

---

CONCLUSÃO DA ORDEM DE SERVIÇO

- Status: FINALIZADA
- Data: 2025-08-22
- Responsável: Rodrigo C. Winhaski
- Observações: Ações realizadas (resumo): merge direto via API (HTTP 204), branch rd/20250820-004-docparser-testing-shortcut deletada (HTTP 204).

---
