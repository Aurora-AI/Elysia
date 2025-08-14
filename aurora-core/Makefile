.PHONY: kafka indexer-consumer ingest index e2e test api

kafka:
	docker compose up -d redpanda

indexer-consumer:
	poetry run python -m aurora_platform.modules.rag.indexer.rag_indexer_consumer

ingest:
	poetry run python -m aurora_platform.modules.crawler.pipeline --src $(SRC) --emit-kafka

index:
	poetry run python -m aurora_platform.modules.crawler.pipeline --src $(SRC) --index

e2e: kafka
	$(MAKE) -s indexer-consumer & sleep 3
	$(MAKE) -s ingest SRC=$(SRC)

api:
	poetry run uvicorn aurora_platform.services.rag_rest:app --host 0.0.0.0 --port 8080 --reload

test:
	poetry run pytest -q
