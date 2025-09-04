# /src/aurora_platform/modules/crawler/loaders/url_loader.py
from __future__ import annotations

import contextlib
from dataclasses import dataclass

# Requer: pip install playwright
# E (uma vez): python -m playwright install --with-deps chromium
from playwright.sync_api import Browser, Page, sync_playwright
from playwright.sync_api import TimeoutError as PWTimeoutError

DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class DOMFetchResult:
    url: str
    status: int
    html: str


def _launch_browser(headless: bool = True) -> tuple[contextlib.ExitStack, Browser]:
    stack = contextlib.ExitStack()
    p = stack.enter_context(sync_playwright())
    browser = stack.enter_context(p.chromium.launch(headless=headless))
    return stack, browser


def fetch_html_dom(
    url: str,
    *,
    wait_until: str = "networkidle",
    wait_selector: str | None = None,
    timeout_ms: int = 15000,
    headless: bool = True,
    user_agent: str = DEFAULT_UA,
) -> DOMFetchResult:
    """
    Navega até a URL com Chromium headless (Playwright), espera o carregamento JS e retorna HTML.
    - wait_until: 'domcontentloaded' | 'networkidle'
    - wait_selector: CSS opcional para garantir que um elemento-chave apareceu
    """
    stack, browser = _launch_browser(headless=headless)
    try:
        context = browser.new_context(user_agent=user_agent, ignore_https_errors=True)
        page: Page = context.new_page()
        resp = page.goto(url, wait_until=wait_until, timeout=timeout_ms)
        if wait_selector:
            page.wait_for_selector(wait_selector, timeout=timeout_ms)

        status = resp.status if resp else 0
        html = page.content()
        context.close()
        return DOMFetchResult(url=url, status=status, html=html)

    except PWTimeoutError:
        # Re-tentativa simples com uma espera menos agressiva
        try:
            context = browser.new_context(user_agent=user_agent, ignore_https_errors=True)
            page = context.new_page()
            resp = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=timeout_ms)
            status = resp.status if resp else 0
            html = page.content()
            context.close()
            return DOMFetchResult(url=url, status=status, html=html)
        except Exception as e:  # noqa: BLE001
            context.close()
            raise e
    finally:
        stack.close()


def fetch_body_text(
    url: str,
    *,
    wait_until: str = "networkidle",
    wait_selector: str | None = None,
    timeout_ms: int = 15000,
    headless: bool = True,
) -> str:
    """
    Retorna apenas o texto do <body>. Evita dependência de bs4/lxml;
    faz extração ingênua que costuma bastar para indexação inicial.
    """
    res = fetch_html_dom(
        url,
        wait_until=wait_until,
        wait_selector=wait_selector,
        timeout_ms=timeout_ms,
        headless=headless,
    )
    html = res.html
    # Extração simples do conteúdo dentro de <body> .. </body>
    lower = html.lower()
    i = lower.find("<body")
    if i == -1:
        return html
    j = lower.find(">", i)
    if j == -1:
        return html
    k = lower.find("</body>", j)
    body_html = html[j + 1 : k if k != -1 else None]
    # Remover tags básicas
    import re

    text = re.sub(r"<script[\s\S]*?</script>", " ", body_html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
