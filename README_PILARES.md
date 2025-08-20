Entrega RD-20250819-001 - Fundação Cognitiva Aurora

Como usar:

1. Subir a stack de dependências (Postgres, Kafka, Neo4j):
   docker compose -f docker-compose.pilares.yml up -d

2. Rodar ingest:
   python scripts/ingest_pilares.py

3. Validar:
   python scripts/validate_ingest.py

4. Rodar API de pilares (exemplo):
   uvicorn aurora_platform.api.kg_endpoints_pilares:router --reload
