from __future__ import annotations
from typing import Optional
from io import BytesIO

try:
    from pypdf import PdfReader  # type: ignore
except Exception:
    PdfReader = None  # type: ignore


def pdf_to_text(data: bytes) -> Optional[str]:
    if PdfReader is None:
        return None
    try:
        reader = PdfReader(BytesIO(data))
        chunks = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            if txt.strip():
                chunks.append(txt)
        return "\n\n".join(chunks) if chunks else None
    except Exception:
        return None
