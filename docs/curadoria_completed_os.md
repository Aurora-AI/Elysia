# Curadoria — Ordens de Serviço Concluídas

Documento de curadoria que regista as Ordens de Serviço (OS) concluídas e artefatos associados.

Gerado automaticamente em 2025-08-15.

## OS concluídas

- AUR-GOV-002 — Córtex Operacional (DB + init script + logger)
  - Status: Concluída
  - Artefactos: `scripts/init_cortex_db.py`, `db/cortex.db`, `backend/app/core/cortex_logger.py`
  - Notas: Schema atualizado, smoke test de inserção executado.

- AUR-GOV-003 — Harden Córtex (commit metadata + testes)
  - Status: Concluída
  - Artefactos: Atualizações em `backend/app/core/cortex_logger.py`, testes em `backend/app/core/tests`
  - Notas: SQL sync e `_verify_table_schema` adicionados; testes locais verdes.

- AUR-CRAWLER-FIX-002 — CI e E2E do Crawler (matrix extras + fallback)
  - Status: Concluída
  - Artefactos: `.github/workflows/crawler-tests.yml`, `tests/crawler/` (fixtures e e2e)
  - Notas: Workflow criado com matrix para extras; testes locais executados com `TESTING=1`.

- AUR-CRAWLER-CONN-001 — Conector piloto TCE-RN
  - Status: Concluída (scaffold + testes locais)
  - Artefactos: `backend/app/connectors/tce_rn/` contendo `schemas.py`, `client.py`, `pipeline.py`, `tests/test_connector_tce_rn.py` e `README.md`.
  - Notas: Testes unitários do conector passaram localmente com mocks; pronto para PR/integração.

- AUR-TECH-UPGRADE-002 — Inspeção e Plano de Refatoração (LangGraph)
  - Status: Concluída (inspeção e plano entregue)
  - Artefactos: `analysis/impact_map.md`, `analysis/langgraph_refactoring_plan.md`
  - Notas: Plano por ficheiro com estimativas de esforço para upgrade para LangGraph v0.6.5.

- Processamento GPS Comercial — Documento de Pesquisa (docx → Markdown)
  - Status: Concluído
  - Artefactos: `docs/research/gps_comercial/` (3 markdowns gerados)


## Observações
- Alguns artefatos adicionais (ex.: estudo MIT e alterações no Códice) foram gerados em workspace, ver `docs/library/mit_westerman_transformation_strategy.md` e `docs/reports/MIT_Westerman_integration_360.md` — podem requerer commit/PR separado.
- Recomenda-se abrir PRs para os commits locais pendentes e executar os workflows no GitHub para validação completa.

*Curadoria realizada automaticamente pelo agente executor em 2025-08-15.*
