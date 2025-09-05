# Elysia Bridge — Aurora

A ponte `elysia-bridge` expõe a Memória Ativa (RAG/Qdrant) da Aurora como tools HTTP consumíveis pela Elysia.

## Endpoints

- `POST /bridge/elysia/search` → { query, top_k } → resultados de `query_memory`.
- `GET /bridge/elysia/doc/{doc_id}` → retorna Documento Macro (payload em `docs_macro`).
- `POST /bridge/elysia/ingest` → (opcional) enfileira uma URL no Crawler.

## Como usar na Elysia (tool HTTP)

Configure uma tool HTTP apontando para o serviço da Aurora (ex.: `http://aurora-api:8000/bridge/elysia/search`).

**Request:**

```json
{ "query": "pergunta do usuário", "top_k": 3 }
```

**Response (exemplo):**

```json
{
  "query": "pergunta do usuário",
  "results": [
    {
      "doc_id": "d1",
      "metadata": { "uri": "..." },
      "score": 0.91,
      "text": "..."
    }
  ]
}
```

## Smoke test

Com o servidor FastAPI da Aurora rodando em `localhost:8000`:

```bash
make bridge-test
```
