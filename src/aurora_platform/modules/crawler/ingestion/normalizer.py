from __future__ import annotations

from dataclasses import dataclass

from aurora_platform.modules.crawler.ingestion.metadata import CanonicalMetadata


@dataclass
class NormalizedDoc:
    markdown: str
    meta: CanonicalMetadata


def to_markdown(bundle_content: str, meta: CanonicalMetadata) -> NormalizedDoc:
    # Minimal normalization to Markdown; placeholders for title/headers
    md = bundle_content.strip()
    if not md:
        md = "(empty)"
    return NormalizedDoc(markdown=md, meta=meta)
