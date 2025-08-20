# Blueprint de Treinamento Cognitivo — KG + RAG 2.0

Arquitetura (3 camadas):

1. Ingestão
   - ETL: normalização, extração de metadados, chunking.
2. Knowledge Graph (KG)
   - Neo4j para relações semânticas e entidades canônicas.
3. RAG 2.0
   - Vetor store (Qdrant) + indexação por metadados + re-ranker.

Roadmap de implementação
- Fase 1: pipelines de ingestão e indexação (3 meses)
- Fase 2: KG linking e sincronização (2 meses)
- Fase 3: RAG refinements e UI (2 meses)

Observações técnicas
- Usar embeddings compartilháveis e versionadas.
- Garantir idempotência dos consumers Kafka.
