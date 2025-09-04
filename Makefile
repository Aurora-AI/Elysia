tag:

.PHONY: guard lint lint-fix type test ci-local e2e precommit audit-crawler-rag

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

ci-local: guard lint type test
