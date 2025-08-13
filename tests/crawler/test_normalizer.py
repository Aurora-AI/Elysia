from aurora_platform.modules.crawler.ingestion.metadata import CanonicalMetadata
from aurora_platform.modules.crawler.ingestion.normalizer import to_markdown


def test_to_markdown_basic():
    meta = CanonicalMetadata(source="demo")
    nd = to_markdown("Hello world", meta)
    assert nd.markdown == "Hello world"
    assert nd.meta.source == "demo"
