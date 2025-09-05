from __future__ import annotations

import urllib.robotparser as rp

_cache: dict[str, rp.RobotFileParser] = {}


def is_allowed(url: str, user_agent: str = "AuroraCrawler/1.0") -> bool:
    from urllib.parse import urlparse, urlunparse

    p = urlparse(url)
    robots_url = urlunparse((p.scheme, p.netloc, "/robots.txt", "", "", ""))
    if robots_url not in _cache:
        r = rp.RobotFileParser()
        try:
            r.set_url(robots_url)
            r.read()
        except Exception:
            r = None
        _cache[robots_url] = r
    parser = _cache[robots_url]
    if parser is None:
        return True
    return parser.can_fetch(user_agent, url)
