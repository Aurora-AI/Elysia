from __future__ import annotations
import re
from typing import List
from urllib.parse import urljoin, urlparse

TAG_LINK = re.compile(r'href=["\'](.*?)["\']', flags=re.I)

def extract_links(html: str, base_url: str) -> List[str]:
    links = []
    for m in TAG_LINK.finditer(html or ""):
        href = m.group(1).strip()
        if href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        abs_url = urljoin(base_url, href)
        links.append(abs_url)
    # dedupe por host+path simples
    seen = set()
    out = []
    for u in links:
        p = urlparse(u)
        key = (p.scheme, p.netloc, p.path, p.query)
        if key in seen:
            continue
        seen.add(key)
        out.append(u)
    return out

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()