Aurora Crawler module

Purpose

This module contains loaders and pipeline code to ingest documents (HTML, PDF, DOCX, URLs) into Aurora's ingestion pipeline. It's designed to work with optional extras (pdf/docx parsers) and fall back when those extras are not installed.

Structure

- `loaders/` — Loaders for different media types (html, pdf, docx, url).
- `pipeline.py` — Orchestration that normalizes and sends content to the ingestion API.
- `cli.py` — Tiny CLI for local ingestion testing.
- `types.py` — Shared types and protocols for loaders.

Quick start

Run the CLI for a local file:

```bash
python -m aurora_platform.modules.crawler.cli --path ./somefile.html
```

Run tests (in repo root):

```bash
TESTING=1 PYTHONPATH=$(pwd) pytest -q tests/crawler
```

Notes

- Loaders use guarded imports for optional dependencies (unstructured, pdfplumber, python-docx). If extras are not installed, fallback loaders or error messages are used.
- The pipeline is tested under `TESTING=1` to avoid talking to production services.
