import hashlib

from aurora_platform.modules.crawler.ingestion.normalizer import NormalizedDoc


def compute_id(doc: NormalizedDoc) -> str:
    base = (doc.meta.title or "") + "|" + doc.markdown
    return hashlib.sha256(base.encode("utf-8")).hexdigest()
