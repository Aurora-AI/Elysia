.PHONY: venv install schema ingest-trf1 ingest-trt9 ingest-dir search api router hrm-test test-router

PYTHON := python
PIP := pip

venv:
	$(PYTHON) -m venv .venv

install:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	$(PIP) install -U pip; \
	$(PIP) install -r requirements.txt

schema:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.memory.qdrant_schema

ingest-trf1:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.memory.ingest_to_qdrant --input ./data/datajud/trf1

ingest-trt9:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.memory.ingest_to_qdrant --input ./data/datajud/trt9

ingest-dir:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.memory.ingest_to_qdrant --input "$$DIR"

search:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.memory.search_local

api:
	. .venv/Scripts/activate 2>/dev/null || . . .venv/bin/activate; \
	PYTHONPATH=. uvicorn src.memory.search_local:app --host 0.0.0.0 --port 8089 --reload

router:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. uvicorn src.router.router_service:app --host 0.0.0.0 --port 8090 --reload

hrm-test:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. python -m src.hrm.hrm_loader --rules src/hrm/rules/sample_rules.yaml

test-router:
	. .venv/Scripts/activate 2>/dev/null || . .venv/bin/activate; \
	PYTHONPATH=. pytest -q aurora-platform/tests/test_router_invoke.py
