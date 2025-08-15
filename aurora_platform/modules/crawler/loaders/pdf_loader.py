from __future__ import annotations
from typing import List
from ..types import LoadedDocument

# Optional backends
try:
    from unstructured.partition.pdf import partition_pdf  # type: ignore
    _HAS_UNSTRUCTURED = True
except Exception:
    _HAS_UNSTRUCTURED = False

try:
    import pdfplumber  # type: ignore
    _HAS_PDFPLUMBER = True
except Exception:
    _HAS_PDFPLUMBER = False

try:
    from pypdf import PdfReader  # type: ignore
    _HAS_PYPDF = True
except Exception:
    _HAS_PYPDF = False


class PDFLoader:
    def load(self, *, source: str, content_type: str | None = None) -> LoadedDocument:
        # 1) unstructured
        if _HAS_UNSTRUCTURED:
            parts = partition_pdf(filename=source)
            text = "\n".join(
                [getattr(p, "get", lambda k, d="": "")("text", "") for p in parts])
            return {"text": text, "metadata": {"source": source, "content_type": "application/pdf", "engine": "unstructured"}}

        # 2) pdfplumber
        if _HAS_PDFPLUMBER:
            pages: List[str] = []
            with pdfplumber.open(source) as pdf:
                for p in pdf.pages:
                    pages.append(p.extract_text() or "")
            return {"text": "\n".join(pages), "metadata": {"source": source, "content_type": "application/pdf", "engine": "pdfplumber"}}

        # 3) pypdf
        if _HAS_PYPDF:
            reader = PdfReader(source)
            pages = [p.extract_text() or "" for p in reader.pages]
            return {"text": "\n".join(pages), "metadata": {"source": source, "content_type": "application/pdf", "engine": "pypdf"}}

        # fallback
        return {"text": "", "metadata": {"source": source, "content_type": "application/pdf", "engine": "noop", "warning": "no pdf backends installed"}}
