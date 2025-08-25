# ![Aurora CI/CD](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/aurora-ci-cd.yml/badge.svg)
# Aurora Knowledge Base

## Status

[![KG Seed Smoke](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml)
[![PR Housekeeping](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml)

## Workflows

| Workflow          | Descrição                                                   | Status |
|-------------------|-------------------------------------------------------------|--------|
| KG Seed Smoke     | Valida o seed dos Pilares em um Neo4j efêmero (CI smoke).   | [![KG Seed Smoke](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/kg-seed-smoke.yml) |
| PR Housekeeping   | Auto-atribui o autor em cada Pull Request aberta/atualizada.| [![PR Housekeeping](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml/badge.svg)](https://github.com/Aurora-AI/Aurora-Plataform/actions/workflows/pr-housekeeping.yml) |

## Contribuição

### Hooks locais
Instale o pre-commit rápido (não versionado):

```bash
bash scripts/install-hooks.sh
```

Bypass consciente: `export SKIP_EXEMPLO=1` ou inclua `[skip-exemplo-check]` na mensagem do commit.
