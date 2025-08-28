# OS-AUR-MVP1-DOC-QDR-001 — Pipeline Docling → Qdrant (ingestão + busca híbrida

**Agente Executor:** Copilot Chat  
**Branch:** `feat/mvp1-docling-ingest`  
**Objetivo:** Ingerir PDFs/HTML com Docling, extrair Markdown/Chunks, gerar embeddings e indexar no Qdrant; expor API mínima e testes.

---

## Escopo
1. **Pipeline de ingestão** (`aurora_platform/ingest/docling_pipeline.py`)
   - `load(input)` → detecta PDF/HTML
   - `to_markdown(doc)` → normalização
   - `chunk_text(md)` → particiona por heading/tamanho
   - `embed_chunks(chunks)` → placeholder (trocar por embedding oficial depois)
   - `index_qdrant(chunks, vectors)` → upsert em `aurora_docs` (ou mock/local)
2. **Modelos Pydantic** (`aurora_platform/ingest/models.py`)
   - `IngestRequest`, `Chunk`, `IngestResult`
3. **API FastAPI** (`aurora_platform/ingest/router.py`)
   - `POST /ingest` (arquivo base64 ou URL) → `IngestResult`
   - `GET /chunks/{doc_id}` → lista de `Chunk`
   - (Opcional) `POST /ingest/search` → busca híbrida (BM25 + vetorial) em `aurora_docs`
4. **Testes** (`tests/ingest/…`)
   - Pipeline básico e endpoints
5. **DX/CI**
   - Makefile: `ingest-api-run`
   - Workflow: `.github/workflows/mvp1-ingest.yml` rodando testes

## Critérios de Encerramento
- [ ] `POST /ingest` aceita PDF/HTML e indexa chunks.  
- [ ] `GET /chunks/:doc_id` retorna chunks.  
- [ ] (Se aplicado) `POST /ingest/search` retorna resultados consistentes.  
- [ ] Testes `tests/ingest/**` passam no CI.  
- [ ] `make ingest-api-run` funciona localmente.

## Notas de Implementação
- **Qdrant**: no CI, preferir mock ou compose dedicado; localmente, permitir `QDRANT_URL`/`QDRANT_API_KEY`.  
- **Embeddings**: placeholder agora; trocar pelo pipeline homogêneo de Memória Ativa.  
- **Roteiro futuro**: integrar promoção para Neo4j após “score” de confiança.

---
