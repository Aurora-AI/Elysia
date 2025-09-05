# ![Aurora CI/CD](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/aurora-ci-cd.yml/badge.svg)

# Aurora Knowledge Base

## Status

[![CI](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/ci.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/ci.yml)
[![Actionlint](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/actionlint.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/actionlint.yml)
[![Docker Presence](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/docker-presence.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/docker-presence.yml)
[![KG Seed Smoke](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml)
[![PR Housekeeping](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml)

## Workflows

| Workflow        | Descrição                                              | Status                                                                                                                                                                                                   |
| --------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI              | Lint, type-check e testes (matrix 3.11/3.12 + Qdrant). | [![CI](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/ci.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/ci.yml)                                        |
| Actionlint      | Validação estática dos workflows.                      | [![Actionlint](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/actionlint.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/actionlint.yml)                |
| Docker Presence | Garante disponibilidade básica do docker CLI.          | [![Docker Presence](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/docker-presence.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/docker-presence.yml) |
| KG Seed Smoke   | Valida o seed dos Pilares em Neo4j efêmero.            | [![KG Seed Smoke](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml)       |
| PR Housekeeping | Auto-atribui o autor em cada PR.                       | [![PR Housekeeping](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml) |

## Contribuição

### Hooks locais

Instale o pre-commit rápido (não versionado):

```bash
bash scripts/install-hooks.sh
```

Bypass consciente: `export SKIP_EXEMPLO=1` ou inclua `[skip-exemplo-check]` na mensagem do commit.
