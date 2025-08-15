TCE-RN Connector

Purpose

This package implements a small connector that extracts expense records from a TCE-RN style API, normalizes them into a canonical expense schema, and optionally posts them to Aurora's ingestion endpoint.

Files

- `schemas.py` — Pydantic models for raw and canonical records.
- `client.py` — HTTP client with pagination and retry logic.
- `pipeline.py` — Normalization and batch ingestion orchestration.
- `tests/` — Unit tests that run without external network calls.

Quick start

1. Run unit tests (recommended):

```bash
TESTING=1 PYTHONPATH=$(pwd) pytest -q backend/app/connectors/tce_rn/tests
```

2. To run the pipeline against a real API (for integration only):

- Configure `backend/app/connectors/tce_rn/config.py` (BASE URL, API keys, AURORA_INGEST_URL/TOKEN).
- Call `backend.app.connectors.tce_rn.pipeline.run(...)` from a script or task.

Notes

- Tests are designed to avoid real HTTP calls (they monkeypatch the client and post functions).
- Keep sensitive credentials out of the repository and use environment variables.
