from __future__ import annotations
from typing import Optional
from pypdf import PdfReader
from io import BytesIO

def pdf_to_text(data: bytes) -> Optional[str]:
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
