from __future__ import annotations
import importlib.util
import subprocess
import sys
from pathlib import Path
import pytest
from aurora_platform.modules.crawler.pipeline import run_ingestion


def _has_docx():
    return importlib.util.find_spec("docx") is not None or importlib.util.find_spec("mammoth") is not None


@pytest.mark.skipif(not _has_docx(), reason="docx backends not installed")
def test_e2e_docx(tmp_path):
    # gera o fixture se necessário
    p = Path("tests/crawler/fixtures/sample.docx")
    if not p.exists() and importlib.util.find_spec("docx") is not None:
        subprocess.run(
            [sys.executable, "tests/crawler/fixtures/make_sample_docx.py"], check=True)
    assert p.exists(), "sample.docx missing"
    # Use the DocxLoader to obtain text content (avoid reading binary .docx as text)
    from aurora_platform.modules.crawler.loaders.docx_loader import DocxLoader

    doc = DocxLoader().load(source=str(p))
    rec = run_ingestion(content=doc["text"], media_type="docx", source=str(p))
    assert rec["id"]
    assert rec["chunks"]
