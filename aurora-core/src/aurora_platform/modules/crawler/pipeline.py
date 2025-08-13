from __future__ import annotations
import json
import os
from typing import Dict, Any
from aurora_platform.modules.crawler.ingestion.metadata import CanonicalMetadata
from aurora_platform.modules.crawler.ingestion.normalizer import to_markdown
from aurora_platform.modules.crawler.ingestion.dedupe import compute_id
from aurora_platform.modules.crawler.chunking.splitter import split_markdown
from aurora_platform.modules.crawler.chunking import policies as chunk_policies


def run_ingestion(content: str, media_type: str, source: str, tags: Dict[str, Any] | None = None) -> Dict[str, Any]:
    meta = CanonicalMetadata(source=source, tags=tags or {}, raw={
                             "media_type": media_type})
    normalized = to_markdown(content, meta)
    canonical_id = compute_id(normalized)
    policy = chunk_policies.for_source(media_type)
    chunks = split_markdown(
        normalized.markdown, chunk_size=policy["size"], overlap=policy["overlap"])
    for idx, ch in enumerate(chunks):
        ch["id"] = f"{canonical_id}::{idx}"
        ch["source"] = media_type
    record = {
        "id": canonical_id,
        "source": source,
        "meta": normalized.meta.__dict__,
        "content_markdown": normalized.markdown,
        "chunks": chunks,
    }
    return record


def save_record(record: Dict[str, Any], out_dir: str = "artifacts/ingested") -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{record['id']}.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path
