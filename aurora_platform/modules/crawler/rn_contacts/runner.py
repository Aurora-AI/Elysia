from __future__ import annotations
import asyncio, re, time, os, json
from typing import Set, Dict, Any, List, Tuple
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib import robotparser
from .config import USER_AGENT, SEEDS, ALLOWED_SUFFIXES
from .extract import extract_from_text
from .pdf import pdf_to_text
from .output import write_outputs, dedup
import datetime as dt

PDF_LINK_RE = re.compile(r"\.pdf($|\?)", re.IGNORECASE)

def allow_url(u: str) -> bool:
    host = urlparse(u).netloc.lower()
    return host.endswith(tuple(s.lstrip(".") for s in ALLOWED_SUFFIXES))

async def fetch_text(client: httpx.AsyncClient, url: str):
    r = await client.get(url, timeout=15.0, follow_redirects=True)
    r.raise_for_status()
    ctype = r.headers.get("content-type","" ).lower()
    if "pdf" in ctype or PDF_LINK_RE.search(url):
        return "pdf", r.content
    return "html", r.content

def extract_links(base_url: str, html: bytes):
    doc = HTMLParser(html.decode("utf-8", "ignore"))
    title = (doc.css_first("title").text(strip=True) if doc.css_first("title") else None)
    links = []
    for a in doc.css("a[href]"):
        href = a.attributes.get("href")
        if not href:
            continue
        url = urljoin(base_url, href)
        if url.startswith("mailto:"):
            links.append(url)
        elif allow_url(url):
            links.append(url)
    text = doc.text(separator=" ", strip=True)[:200000]
    return title, links, text

def can_fetch(robots: robotparser.RobotFileParser, url: str) -> bool:
    try:
        return robots.can_fetch(USER_AGENT, url)
    except Exception:
        return True

async def crawl(*, seeds: List[str], out_dir: str, max_pages: int = 250, allow_non_official: bool=False) -> Dict[str, Any]:
    visited: Set[str] = set()
    queue: List[str] = [u for u in seeds if allow_url(u)]
    found: List[Dict[str, Any]] = []

    robots_cache: Dict[str, robotparser.RobotFileParser] = {}
    per_host_last = {}

    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}, http2=True) as client:
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            host = urlparse(url).netloc.lower()
            # rate limit por host (mín. 0.7s)
            last = per_host_last.get(host, 0.0)
            delta = time.monotonic() - last
            if delta < 0.7:
                await asyncio.sleep(0.7 - delta)

            # robots.txt
            if host not in robots_cache:
                rp = robotparser.RobotFileParser()
                rp.set_url(f"https://{host}/robots.txt")
                try:
                    rp.read()
                except Exception:
                    pass
                robots_cache[host] = rp
            if not can_fetch(robots_cache[host], url):
                continue

            try:
                kind, body = await fetch_text(client, url)
            except Exception:
                continue

            if kind == "html":
                title, links, text = extract_links(url, body)
                # extrair emails do HTML
                found.extend(extract_from_text(url, title, text, allow_non_official=allow_non_official))
                # extrair mailto imediatos
                for l in links:
                    if l.startswith("mailto:"):
                        email = l.split("mailto:",1)[1]
                        found.extend(extract_from_text(url, title, email, allow_non_official=allow_non_official))
                # enfileirar novos links
                for l in links:
                    if l.startswith("http"):
                        queue.append(l)
            else:  # pdf
                text = pdf_to_text(body or b"")
                if text:
                    found.extend(extract_from_text(url, None, text, allow_non_official=allow_non_official))

            per_host_last[host] = time.monotonic()

    # dedup + gravação
    records = dedup(found)
    stamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M")
    out_base = os.path.join(out_dir, f"rn_contacts_{stamp}")
    paths = write_outputs(out_base, records, {
        "version": "rn-contacts-0.1",
        "seeds": seeds,
        "max_pages": max_pages,
        "allow_non_official": allow_non_official,
        "user_agent": USER_AGENT,
    })
    return {"count": len(records), "paths": paths, "visited": len(visited)}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="RN contacts crawler (POC)")
    ap.add_argument("--out", default="data/outputs/rn_contacts", help="output directory")
    ap.add_argument("--max-pages", type=int, default=250)
    ap.add_argument("--allow-non-official", action="store_true", help="include non-gov emails")
    args = ap.parse_args()
    res = asyncio.run(crawl(seeds=SEEDS, out_dir=args.out, max_pages=args.max_pages, allow_non_official=args.allow_non_official))
    print(json.dumps(res, ensure_ascii=False))
