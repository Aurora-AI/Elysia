SHELL := /usr/bin/env bash

# Helper: carrega .env e .env.aura se existirem (sem falhar)
define with_dotenv
set -a; \
[ -f .env ] && . ./.env; \
[ -f .env.aura ] && . ./.env.aura; \
set +a;
endef

.PHONY: help
help:
	@echo "Alvos:"
	@echo "  neo4j-seed                 - Aplica seed dos pilares (script Aura-aware via HTTP)"
	@echo "  neo4j-seed-cypher          - Aplica seed via cypher-shell (tools/neo4j_seed_constraints.cypher)"
	@echo "  neo4j-check                - Lista pilares no banco"
	@echo "  neo4j-check-pillars        - Verifica pilares (driver Python, sem cypher-shell)"
	@echo "  neo4j-check-pillars-venv   - Mesmo check garantindo 'neo4j' instalado"
	@echo "  neo4j-check-pillars-strict - Check strict (obriga índices; override via env)"
	@echo "  env-example                - Copia .env.aura.example -> .env.aura (se ausente)"
	@echo "  pr-aura-kg-seed            - Abre PR da branch aura/kg-seed -> main (gh cli)"
	@echo "  install/lock/test          - Helpers Poetry"
	@echo "  lint/format/clean          - Qualidade de código"
	@echo "  release-*                  - Helpers de release (GitHub CLI)"

# ----------------------------
# Dev helpers
# ----------------------------
.PHONY: env-example
env-example:
	@if [ ! -f .env.aura ]; then cp .env.aura.example .env.aura; echo "[env] .env.aura criado."; else echo "[env] .env.aura já existe — ok."; fi

# ----------------------------
# Neo4j
# ----------------------------

# Seed via script HTTP (usa AURA_NEO4J_HTTP_URL/NEO4J_URL)
.PHONY: neo4j-seed
neo4j-seed:
	@{ $(with_dotenv) \
	NEO4J_USER="$${AURA_NEO4J_USERNAME:-$${NEO4J_USERNAME:-neo4j}}" \
	NEO4J_PASSWORD="$${AURA_NEO4J_PASSWORD:-$${NEO4J_PASSWORD:-neo4j}}" \
	NEO4J_URL="$${AURA_NEO4J_HTTP_URL:-$${NEO4J_URL:-http://localhost:7474}}" \
	bash tools/neo4j_seed_constraints.sh; }

# Seed via cypher-shell usando o arquivo .cypher
.PHONY: neo4j-seed-cypher
neo4j-seed-cypher:
	@{ $(with_dotenv) cypher-shell \
		-u "$${AURA_NEO4J_USERNAME:-$${NEO4J_USERNAME:-neo4j}}" \
		-p "$${AURA_NEO4J_PASSWORD:-$${NEO4J_PASSWORD:-neo4j}}" \
		-a "$${AURA_NEO4J_URI:-$${NEO4J_URI:-bolt://localhost:7687}}" \
		-f ./tools/neo4j_seed_constraints.cypher; }

# Consulta simples para conferir nós de pilares (seeds)
.PHONY: neo4j-check
neo4j-check:
	@{ $(with_dotenv) cypher-shell \
		-u "$${AURA_NEO4J_USERNAME:-$${NEO4J_USERNAME:-neo4j}}" \
		-p "$${AURA_NEO4J_PASSWORD:-$${NEO4J_PASSWORD:-neo4j}}" \
		-a "$${AURA_NEO4J_URI:-$${NEO4J_URI:-bolt://localhost:7687}}" \
		'MATCH (p:Pillar) RETURN p.key, p.name ORDER BY p.key'; }

# ----------------------------
# Pillars Check (fallback Python sem cypher-shell)
# ----------------------------

# Variáveis esperadas (vêm do .env/.env.aura):
# AURA_NEO4J_URI / AURA_NEO4J_USERNAME / AURA_NEO4J_PASSWORD
# (ou legados NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD)

.PHONY: neo4j-check-pillars
neo4j-check-pillars: ## Verifica conectividade, constraints e sanidade do Neo4j (driver Python)
	@{ $(with_dotenv) python3 tools/neo4j_check_pillars.py; }

.PHONY: neo4j-check-pillars-venv
neo4j-check-pillars-venv: ## Mesmo check, garantindo 'neo4j' instalado no ambiente atual
	@echo ">> Ensuring 'neo4j' driver is installed…"
	@python3 -c "import importlib,sys; sys.exit(0 if importlib.util.find_spec('neo4j') else 1)" || pip install 'neo4j>=5.22.0'
	@$(MAKE) neo4j-check-pillars

.PHONY: neo4j-check-pillars-strict
neo4j-check-pillars-strict: ## Checagem strict (obriga índices, override via env)
	@{ $(with_dotenv) NEO4J_CHECK_STRICT=true NEO4J_MIN_INDEXES=0 python3 tools/neo4j_check_pillars.py --strict; }

# ----------------------------
# PR helper
# ----------------------------

.PHONY: pr-aura-kg-seed
pr-aura-kg-seed:
	@branch=aura/kg-seed; \
	msg="KG Seed: aliases AURA, Makefile dotenv, tasks.json e .env.aura.example"; \
	git checkout -B $$branch; \
	git add .; \
	git commit -m "$$msg" || true; \
	git push -u origin $$branch; \
	gh pr create --title "$$msg" --body "Esta PR adiciona:\n- Suporte a aliases AURA_NEO4J_*\n- Makefile com carregamento .env/.env.aura\n- .vscode/tasks.json para seed/check\n- .env.aura.example\n- Seed idempotente dos pilares\n\nTestes: seed local e verificação via cypher-shell." --base main --head $$branch || true; \
	echo "[pr] PR criada (ou já existente)."

# ----------------------------
# Poetry / Qualidade
# ----------------------------

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

# ----------------------------
# Release helpers (GitHub CLI)
# ----------------------------
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
