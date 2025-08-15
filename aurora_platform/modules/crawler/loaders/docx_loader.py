from __future__ import annotations
from ..types import LoadedDocument

try:
    import docx  # type: ignore
    _HAS_DOCPY = True
except Exception:
    _HAS_DOCPY = False

try:
    import mammoth  # type: ignore
    _HAS_MAMMOTH = True
except Exception:
    _HAS_MAMMOTH = False


class DocxLoader:
    def load(self, *, source: str, content_type: str | None = None) -> LoadedDocument:
        if _HAS_DOCPY:
            document = docx.Document(source)
            text = "\n".join(p.text for p in document.paragraphs)
            return {"text": text, "metadata": {"source": source, "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "engine": "python-docx"}}

        if _HAS_MAMMOTH:
            with open(source, "rb") as f:
                result = mammoth.convert_to_markdown(f)
            return {"text": result.value, "metadata": {"source": source, "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "engine": "mammoth"}}

        return {"text": "", "metadata": {"source": source, "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "engine": "noop", "warning": "no docx backends installed"}}
