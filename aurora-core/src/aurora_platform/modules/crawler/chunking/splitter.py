from __future__ import annotations
from typing import List, Dict, Any


def split_markdown(md: str, chunk_size: int = 800, overlap: int = 100) -> List[Dict[str, Any]]:
    # Use langchain splitter if available, else fallback to naive splitter
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=overlap)
        return [{"text": c} for c in splitter.split_text(md)]
    except Exception:
        chunks = []
        start = 0
        n = len(md)
        while start < n:
            end = min(n, start + chunk_size)
            chunk = md[start:end]
            chunks.append({"text": chunk})
            start = end - overlap if end < n else end
            if start < 0:
                start = 0
        return chunks
