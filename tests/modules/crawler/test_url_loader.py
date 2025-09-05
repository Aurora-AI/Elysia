# /tests/modules/crawler/test_url_loader.py
import os

import pytest
from aurora_platform.modules.crawler.loaders.url_loader import fetch_body_text, fetch_html_dom

# Para rodar no CI, é necessário instalar o browser do Playwright:
#   python -m pip install playwright
#   python -m playwright install --with-deps chromium
# Este teste é marcado como "integration" e pode ser pulado sem ENABLE_NET_TESTS=1

requires_net = pytest.mark.skipif(
    os.getenv("ENABLE_NET_TESTS") != "1",
    reason="Teste de rede desabilitado. Defina ENABLE_NET_TESTS=1 para executar.",
)


@requires_net
def test_fetch_html_dom_example():
    res = fetch_html_dom("https://example.com", timeout_ms=20000, headless=True)
    assert res.status == 200
    assert "<title>Example Domain</title>" in res.html


@requires_net
def test_fetch_body_text_example():
    txt = fetch_body_text("https://example.com", timeout_ms=20000, headless=True)
    assert "Example Domain" in txt
