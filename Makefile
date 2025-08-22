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

# ===============================
# Release helpers (GitHub CLI)
# ===============================
VERSION ?= 0.0.0
PREV_TAG ?= $(shell git describe --abbrev=0 --tags 2>/dev/null || echo "v0.0.0")
RELEASE_TITLE ?= "Aurora Platform v$(VERSION)"
RELEASE_NOTES_TMP := /tmp/RELEASE_NOTES_$(VERSION).md
RELEASE_TEMPLATE := .github/release_body_template.md

.PHONY: release-notes
release-notes:
	@echo ">> Gerando corpo de release a partir do template"
	@test -f $(RELEASE_TEMPLATE) || (echo "Template não encontrado: $(RELEASE_TEMPLATE)"; exit 1)
	@sed -e 's/{{VERSION}}/$(VERSION)/g' -e 's/{{PREV_TAG}}/$(PREV_TAG)/g' $(RELEASE_TEMPLATE) > $(RELEASE_NOTES_TMP)
	@echo ">> Preview:"
	@head -n 20 $(RELEASE_NOTES_TMP) || true

.PHONY: tag
tag:
	@if [ -z "$(VERSION)" ]; then echo "Use: make tag VERSION=x.y.z"; exit 1; fi
	@git tag -a v$(VERSION) -m "Release v$(VERSION)"
	@git push origin v$(VERSION)

.PHONY: release
release: release-notes
	@if [ -z "$(VERSION)" ]; then echo "Use: make release VERSION=x.y.z"; exit 1; fi
	@echo ">> Criando release v$(VERSION) com notas"
	@gh release create v$(VERSION) --title $(RELEASE_TITLE) --notes-file $(RELEASE_NOTES_TMP)

.PHONY: release-auto
release-auto:
	@if [ -z "$(VERSION)" ]; then echo "Use: make release-auto VERSION=x.y.z"; exit 1; fi
	@gh release create v$(VERSION) --title "Aurora Platform v$(VERSION)" --generate-notes
