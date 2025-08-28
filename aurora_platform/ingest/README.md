# Aurora Ingest (MVP1)

- POST /ingest: aceita PDF/HTML (base64) ou URL, extrai markdown, chunk, indexa (Qdrant/mock)
- GET /chunks/{doc_id}: retorna chunks
- (Opcional) POST /ingest/search: busca híbrida (BM25+vetor)

Rodar local: `make ingest-api-run`
