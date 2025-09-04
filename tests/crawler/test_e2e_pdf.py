from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from aurora_platform.modules.crawler.pipeline import run_ingestion


def _has_pdf():
    return any(importlib.util.find_spec(m) is not None for m in ("unstructured", "pdfplumber", "pypdf"))


@pytest.mark.skipif(not _has_pdf(), reason="pdf backends not installed")
def test_e2e_pdf(tmp_path):
    p = Path("tests/crawler/fixtures/sample.pdf")
    if not p.exists():
        if importlib.util.find_spec("reportlab") is not None:
            subprocess.run(
                [sys.executable, "tests/crawler/fixtures/make_sample_pdf.py"], check=True)
    assert p.exists(), "sample.pdf missing (commit a small test pdf or enable reportlab)"
    rec = run_ingestion(content=str(p.read_text(
        encoding='utf-8')), media_type="pdf", source=str(p))
    assert rec["id"]
    assert rec["chunks"]
