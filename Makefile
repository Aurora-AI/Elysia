tag:

.PHONY: guard lint lint-fix type test ci-local e2e precommit

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

ci-local: guard lint type test
