.PHONY: install lock test test-verbose lint format clean

install:
	@poetry install --no-interaction

lock:
	@poetry lock --no-update

test:
	@echo ">> Running tests in Poetry venv"
	@poetry run pytest --disable-warnings -q

test-verbose:
	@poetry run pytest -vv

lint:
	@poetry run flake8

format:
	@poetry run ruff check --fix .
	@poetry run black .

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
