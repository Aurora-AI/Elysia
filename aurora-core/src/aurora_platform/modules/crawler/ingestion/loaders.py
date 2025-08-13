from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentBundle:
    content: str
    media_type: str  # "pdf" | "html" | "youtube" | "text"
    raw_path: Optional[str] = None


class DoclingLoader:
    """Loads PDFs using Docling when available; falls back to PyMuPDF if not.
    Avoids hard dependency on Docling.
    """

    AVAILABLE = False
    try:  # soft import
        import docling  # type: ignore

        AVAILABLE = True
    except Exception:  # pragma: no cover
        pass

    @staticmethod
    def load(path: str) -> DocumentBundle:
        if DoclingLoader.AVAILABLE:
            # Placeholder: integrate docling if present
            # For now, read binary and return placeholder content
            return DocumentBundle(content=f"[docling] {path}", media_type="pdf", raw_path=path)
        # fallback: PyMuPDF
        try:
            try:
                import fitz  # type: ignore[import-not-found]
            except Exception:
                fitz = None  # type: ignore[assignment]
            if fitz is None:
                raise RuntimeError(
                    "PyMuPDF (fitz) não está disponível. Instale para habilitar PDF loader.")
            text = []
            with fitz.open(path) as doc:
                for page in doc:
                    text.append(page.get_text())
            return DocumentBundle(content="\n".join(text), media_type="pdf", raw_path=path)
        except Exception as e:  # pragma: no cover
            raise FileNotFoundError(f"Unable to load PDF: {path}: {e}")


class HTMLLoader:
    @staticmethod
    def load_from_string(html: str) -> DocumentBundle:
        # very simple tag stripper without new deps
        import re
        text = re.sub(r"<[^>]+>", " ", html)
        return DocumentBundle(content=" ".join(text.split()), media_type="html")

    @staticmethod
    def load_from_file(path: str) -> DocumentBundle:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLLoader.load_from_string(html)


class YouTubeTranscriptLoader:
    @staticmethod
    def load_transcript_text(text: str) -> DocumentBundle:
        return DocumentBundle(content=text, media_type="youtube")
