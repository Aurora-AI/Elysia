# Estrutura de Diretórios do Projeto Aurora

Esta é a estrutura de diretórios padrão para o `Aurora-Core`. Ela garante a separação de responsabilidades e a manutenibilidade do projeto.

aurora-core/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── ARCHITECTURE_SUMMARY.md
│   ├── CONVENTIONAL_COMMITS_EXAMPLES.md
│   └── PULL_REQUEST_CHECKLIST.md
├── src/
│   └── aurora_platform/
│       ├── api/
│       │   └── v1/
│       │       └── endpoints/
│       ├── core/
│       ├── clients/
│       │   ├── adapters/
│       │   └── factories/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       │   └── browser_automation/
│       └── db/
│           └── migrations/
│
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── alembic.ini
├── pyproject.toml
└── README.md
