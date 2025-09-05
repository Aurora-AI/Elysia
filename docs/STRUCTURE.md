# Estrutura de Diretórios do Projeto Aurora

Esta é a estrutura de diretórios padrão para o `Aurora-Core`. Ela garante a separação de responsabilidades e a manutenibilidade do projeto.

aurora-core/
├── .github/
│ └── workflows/
│ └── ci.yml
├── docs/
│ ├── ARCHITECTURE_SUMMARY.md
│ ├── CONVENTIONAL_COMMITS_EXAMPLES.md
│ └── PULL_REQUEST_CHECKLIST.md
├── src/
│ └── aurora_platform/
│ ├── api/
│ │ └── v1/
│ │ └── endpoints/
│ ├── core/
│ ├── clients/
│ │ ├── adapters/
│ │ └── factories/
│ ├── models/
│ ├── schemas/
│ ├── services/

# TODO: Reativar/substituir na integração do Crawler.

# │ │ └── browser_automation/

│ └── db/
│ └── migrations/
│
├── tests/
│ ├── unit/
│ └── integration/
├── .gitignore
├── alembic.ini
├── pyproject.toml
└── README.md

---

```toml
[tool.poetry.dependencies]
chromadb = "^0.5.20"
pydantic = "^2.0.0"
```

4. **Sincronize e reinstale as dependências:**

   ```bash
   poetry lock --no-update
   poetry install
   ```

5. **Reinicie o servidor ChromaDB e o Aurora:**

   ```bash
   poetry run uvicorn src.aurora_platform.main:app --reload --port 8080
   ```

6. **Se necessário, limpe os dados antigos do ChromaDB** (veja instruções acima).

> **Importante:** Sempre mantenha as versões do ChromaDB e do Pydantic compatíveis para evitar erros de serialização.
