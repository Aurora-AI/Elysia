DocParser++ service

Purpose

This service provides document parsing logic used by the ingestion pipeline. It attempts to parse with the primary Docling parser and falls back to a simpler OCR-based approach when needed.

Key modules

- `pipeline.py` — `process_document_pipeline(filename, content)` orchestrates parsing and returns an `IngestResponse`.
- `parsers/docling_parser.py` — Primary parser (currently simulated).
- `parsers/fallback_parser.py` — Fallback parser (currently simulated).

Running locally

Run unit tests from the repository root:

```bash
TESTING=1 PYTHONPATH=$(pwd) pytest -q backend/app/services/docparser/tests
```

Integration

- The parsing pipeline is synchronous; if we later plug real async parsers, update `pipeline.process_document_pipeline` to call them appropriately.

Notes

- Replace simulated implementations in `parsers/` with production integration for Docling or other parsing libraries.
