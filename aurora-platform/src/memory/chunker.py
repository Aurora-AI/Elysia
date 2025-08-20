from typing import List
import re

# Chunking simples por parágrafos com janela deslizante


def split_into_chunks(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    if not text:
        return []
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks: List[str] = []
    buf = ""
    for p in paras:
        if not buf:
            buf = p
        elif len(buf) + 2 + len(p) <= max_chars:
            buf = buf + "\n\n" + p
        else:
            chunks.append(buf)
            # overlap em chars
            if overlap > 0 and len(buf) > overlap:
                buf = buf[-overlap:] + "\n\n" + p
            else:
                buf = p
    if buf:
        chunks.append(buf)
    return chunks
