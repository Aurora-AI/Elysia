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

---

## Limpeza do Banco de Dados ChromaDB

Para remover o banco de dados e diretórios antigos do ChromaDB:

1. Exclua o arquivo `chroma.sqlite3` na raiz do projeto (ou onde estiver localizado).
2. Exclua a pasta `chroma_db` (ou qualquer pasta de dados do ChromaDB).
3. Reinicie o servidor ChromaDB. Um novo banco limpo será criado automaticamente.

---

## Ambiente com Docker Compose

Agora é possível subir todo o ambiente Aurora + ChromaDB + Redis com um único comando usando Docker Compose.

### Subindo o ambiente

1. Certifique-se de ter o Docker e o Docker Compose instalados.
2. Execute na raiz do projeto:
   ```bash
   docker compose up --build
   ```
   Isso irá:
   - Subir o ChromaDB na porta 8000
   - Subir o Redis na porta 6379
   - Subir o Aurora-Core na porta 8080

3. Para parar os serviços:
   ```bash
   docker compose down
   ```

### Observações
- O volume `./chroma_db` é persistente, então os dados do ChromaDB não serão perdidos entre reinicializações.
- O volume `redis_data` é persistente, então os dados do Redis não serão perdidos entre reinicializações.
- Para limpar o banco do ChromaDB, basta apagar a pasta `chroma_db` na raiz do projeto.
- Para limpar o banco do Redis, basta remover o volume Docker `redis_data` com:
  ```bash
  docker volume rm aurora-core_redis_data
  ```

---

## Solução de Problemas: Erro KeyError '_type' com ChromaDB

Se ao iniciar o Aurora ocorrer erro 500 do ChromaDB com `KeyError: '_type'`, siga estes passos para corrigir incompatibilidade de versões entre ChromaDB e Pydantic (para ChromaDB >= 0.5.x):

1. **Verifique a versão do ChromaDB no projeto:**
   ```bash
   poetry show chromadb
   ```
   E do servidor (se for externo):
   ```bash
   curl http://localhost:8000/version
   ```

2. **Garanta que cliente e servidor ChromaDB usam a mesma versão.**  
   Recomenda-se usar `chromadb@0.5.20` ou superior (compatível com Pydantic V2):

   ```bash
   poetry add chromadb@0.5.20
   ```

3. **Force o uso do Pydantic V2 no `pyproject.toml`:**
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
