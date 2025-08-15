from __future__ import annotations
import httpx
from tempfile import NamedTemporaryFile
from pathlib import Path
from ..types import LoadedDocument


class URLLoader:
    def load(self, *, source: str, content_type: str | None = None, timeout: float = 10.0) -> LoadedDocument:
        with httpx.Client(timeout=timeout) as client:
            r = client.get(source, follow_redirects=True)
            r.raise_for_status()
            ct = content_type or r.headers.get("content-type", "")
            ct_low = ct.split(";")[0].lower()
            if "pdf" in ct_low or source.lower().endswith(".pdf"):
                with NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
                    tf.write(r.content)
                    tmp_path = tf.name
                from .pdf_loader import PDFLoader

                return PDFLoader().load(source=tmp_path)
            if "officedocument" in ct_low or "word" in ct_low or source.lower().endswith(".docx"):
                with NamedTemporaryFile(suffix=".docx", delete=False) as tf:
                    tf.write(r.content)
                    tmp_path = tf.name
                from .docx_loader import DocxLoader

                return DocxLoader().load(source=tmp_path)
            # default: treat as HTML/text
            return {"text": r.text, "metadata": {"source": source, "content_type": ct or "text/html", "engine": "httpx"}}
