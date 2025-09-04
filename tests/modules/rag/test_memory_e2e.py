import pytest
import os
from aurora_platform.modules.rag.pipeline.rag_pipeline import query_memory
from aurora_platform.modules.crawler.producers.enqueue import enqueue_crawl

@pytest.mark.skipif(os.getenv("ENABLE_E2E_TESTS") != "1", reason="E2E desabilitado")
def test_e2e_memory_flow():
    enqueue_crawl("https://example.com", "seed")
    results = query_memory("Example Domain")
    assert isinstance(results, list)