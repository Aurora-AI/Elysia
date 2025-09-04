tag:

.PHONY: guard lint lint-fix type test ci-local e2e precommit audit-crawler-rag qdrant-up qdrant-wait rag-test crawler-test

python := python

guard:
	@$(python) tools/check_duplicate_packages.py

lint:
	@ruff check .
	@ruff format --check .

lint-fix:
	@ruff check . --fix
	@ruff format .

type:
	@pyright

test:
	@pytest -q --maxfail=1 --disable-warnings --cov=aurora_platform --cov-report=term-missing

precommit:
	@pre-commit run --all-files || true

audit-crawler-rag:
	@python tools/audit/audit_crawler_rag.py

qdrant-up:
	@docker compose up -d qdrant

qdrant-wait:
	@bash -lc 'for i in {1..60}; do curl -fsS http://localhost:6333/ready && exit 0 || sleep 1; done; exit 1'

rag-test: qdrant-up qdrant-wait
	@export ENABLE_QDRANT_TESTS=1 && pytest -q tests/modules/rag/test_pipeline_chunk_on_demand.py

crawler-test:
	@export ENABLE_NET_TESTS=1 && pytest -q tests/modules/crawler/test_url_loader.py

ci-local: guard lint type test
