"""Simple DOCX -> JSON normalizer.

Provides a small CLI and library functions to extract text from a .docx file
and convert it into a normalized JSON structure. Uses python-docx if
available; otherwise falls back to a minimal zip/Xml text extractor.

This is intentionally lightweight: it extracts paragraphs and classifies
blocks as headings when the paragraph is short and mostly uppercase.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def extract_text_from_docx(path: str) -> str:
    """Return the full textual content from a .docx file as plain text.

    Tries to use python-docx (Document). If not available, falls back to
    reading word/document.xml and extracting <w:t> text nodes.
    """
    try:
        from docx import Document  # type: ignore

        doc = Document(path)
        paras = [p.text for p in doc.paragraphs if p.text is not None]
        return "\n\n".join(paras)
    except Exception:
        # Minimal fallback: unzip document and extract text nodes
        try:
            import zipfile
            from xml.etree import ElementTree as ET

            with zipfile.ZipFile(path) as zf:
                with zf.open("word/document.xml") as f:
                    tree = ET.parse(f)
                    # Namespace-agnostic findall for text nodes
                    texts = tree.findall('.//')
                    parts: list[str] = []
                    for elem in texts:
                        if elem.tag.endswith('}t') or elem.tag == 't':
                            if elem.text:
                                parts.append(elem.text)
                    return "\n\n".join(parts)
        except Exception:
            raise SystemExit(
                "Failed to extract text from DOCX; install python-docx or provide a valid .docx file")


def normalize_text_to_json(text: str) -> dict[str, list[dict[str, str]]]:
    """Normalize plaintext into a JSON-friendly structure.

    Produces {'blocks': [{'type': 'heading'|'paragraph', 'text': '...'}, ...]}
    Basic heuristic: a paragraph that is short (< 80 chars) and mostly
    uppercase will be tagged as a heading.
    """
    blocks: list[dict[str, str]] = []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paragraphs:
        is_short = len(p) < 80
        letters = re.sub(r"[^A-Za-z]+", "", p)
        is_upper = letters and letters.upper() == letters
        if is_short and is_upper:
            blocks.append({"type": "heading", "text": p})
        else:
            blocks.append({"type": "paragraph", "text": p})
    return {"blocks": blocks}


def docx_to_json_file(in_path: str, out_path: str | None = None) -> str:
    text = extract_text_from_docx(in_path)
    obj = normalize_text_to_json(text)
    out = out_path or (Path(in_path).with_suffix('.json').as_posix())
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return out


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: docx_to_json.py <input.docx> [output.json]")
        return 2
    inp = argv[1]
    out = argv[2] if len(argv) > 2 else None
    res = docx_to_json_file(inp, out)
    print(f"Wrote: {res}")
    return 0


if __name__ == '__main__':
    raise SystemExit(_main(sys.argv))
