import os
import pytest
from aurora_platform.modules.crawler.models.events import CrawlRequest
from aurora_platform.modules.crawler.pipeline.orchestrator import run_single_crawl

@pytest.mark.skipif(
    os.getenv("ENABLE_NET_TESTS") != "1",
    reason="Teste de rede desabilitado. Defina ENABLE_NET_TESTS=1 para executar.",
)
def test_orchestrator_example_net():
    # smoke test com Playwright real
    req = CrawlRequest(url="https://example.com")
    res, html = run_single_crawl(req)
    assert res.status in (200, 999)  # 999 indica robots disallow
    assert isinstance(res.body_text, str)
    assert isinstance(res.links, list)