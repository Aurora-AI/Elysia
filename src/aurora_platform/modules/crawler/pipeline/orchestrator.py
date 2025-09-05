from __future__ import annotations

import os

from aurora_platform.modules.crawler.loaders.url_loader import fetch_body_text, fetch_html_dom
from aurora_platform.modules.crawler.models.events import CrawlRequest, CrawlResult
from aurora_platform.modules.crawler.pipeline.normalize import extract_links, normalize_text
from aurora_platform.modules.crawler.pipeline.rate_limit import TokenBucket
from aurora_platform.modules.crawler.pipeline.robots import is_allowed

UA = os.getenv("CRAWLER_USER_AGENT", "AuroraCrawler/1.0")
TIMEOUT = int(os.getenv("CRAWLER_REQUEST_TIMEOUT_MS", "20000"))
RPS = float(os.getenv("CRAWLER_RATE_RPS", "0.5"))

bucket = TokenBucket(rps=RPS, burst=1)


def run_single_crawl(req: CrawlRequest) -> tuple[CrawlResult, str]:
    # robots
    if not is_allowed(str(req.url), user_agent=UA):
        return CrawlResult(
            url=req.url, status=999, body_text="", links=[], meta={"robots": "disallow"}
        ), ""

    # rate limit
    bucket.acquire()

    # fetch DOM + text
    dom = fetch_html_dom(str(req.url), timeout_ms=TIMEOUT, headless=True)
    text = fetch_body_text(str(req.url), timeout_ms=TIMEOUT, headless=True)
    links = extract_links(dom.html, str(req.url))
    res = CrawlResult(
        url=req.url, status=dom.status, body_text=normalize_text(text), links=links, meta={"ua": UA}
    )
    return res, dom.html
