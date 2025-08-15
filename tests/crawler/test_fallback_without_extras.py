from __future__ import annotations
import importlib.util
import pytest
from aurora_platform.modules.crawler.loaders.pdf_loader import PDFLoader
from aurora_platform.modules.crawler.loaders.docx_loader import DocxLoader


def _has_any_pdf_backend():
    return any(importlib.util.find_spec(m) is not None for m in ("unstructured", "pdfplumber", "pypdf"))


def _has_any_docx_backend():
    return any(importlib.util.find_spec(m) is not None for m in ("docx", "mammoth"))


@pytest.mark.skipif(_has_any_pdf_backend(), reason="run only when pdf backends are absent")
def test_pdf_loader_no_backends(tmp_path):
    doc = PDFLoader().load(source="nonexistent.pdf")
    assert "engine" in doc["metadata"]
    assert isinstance(doc["text"], str)


@pytest.mark.skipif(_has_any_docx_backend(), reason="run only when docx backends are absent")
def test_docx_loader_no_backends(tmp_path):
    doc = DocxLoader().load(source="nonexistent.docx")
    assert "engine" in doc["metadata"]
    assert isinstance(doc["text"], str)
