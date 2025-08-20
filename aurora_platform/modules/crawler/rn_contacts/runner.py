from __future__ import annotations
import asyncio
import re
import time
import os
import json
import random
from typing import Set, Dict, Any, List
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


async def _get_with_retry(client: httpx.AsyncClient, url: str, retries: int = 4):
    backoff = 0.5
    for attempt in range(1, retries + 1):
        try:
            r = await client.get(url, timeout=15.0, follow_redirects=True)
            if r.status_code >= 500 or r.status_code == 429:
                raise httpx.HTTPStatusError(
                    "retry", request=r.request, response=r)
            r.raise_for_status()
            return r
        except Exception:
            if attempt == retries:
                raise
            jitter = random.uniform(0, backoff)
            await asyncio.sleep(backoff + jitter)
            backoff *= 2


async def fetch_text(client: httpx.AsyncClient, url: str):
    r = await client.get(url, timeout=15.0, follow_redirects=True)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "").lower()
    if "pdf" in ctype or PDF_LINK_RE.search(url):
        return "pdf", r.content
    return "html", r.content


def extract_links(base_url: str, html: bytes):
    doc = HTMLParser(html.decode("utf-8", "ignore"))
    title = (doc.css_first("title").text(strip=True)
             if doc.css_first("title") else None)
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


async def crawl(*, seeds: List[str], out_dir: str, max_pages: int = 250, allow_non_official: bool = False, dry_run: bool = False, mission: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Crawl seeds and extract contacts.

    dry_run: when True, write deterministic empty outputs and skip network.
    """
    # dry-run: write deterministic empty outputs and return without network
    if dry_run:
        records = []
        stamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M")
        out_base = os.path.join(out_dir, f"rn_contacts_{stamp}")
        # Build meta and include mission_id when provided so manifest contains mission context
        meta = {
            "version": "rn-contacts-0.1",
            "seeds": seeds,
            "max_pages": max_pages,
            "allow_non_official": allow_non_official,
            "user_agent": USER_AGENT,
            "dry_run": True,
            # include a render capability hint so dry-run manifests signal render budget
            "render": {"cap": 1, "mode": "auto"},
        }
        if mission and isinstance(mission, dict) and mission.get("mission_id"):
            meta["mission_id"] = mission.get("mission_id")
            mission_name = mission.get("mission_id")
        else:
            mission_name = None
        paths = write_outputs(out_base, records, meta,
                              mission_name=mission_name)
        return {"count": 0, "paths": paths, "visited": 0}

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
            # per-host rate limit (min 0.7s)
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
                # use retry wrapper for GETs
                r = await _get_with_retry(client, url)
                ctype = r.headers.get("content-type", "").lower()
                if "pdf" in ctype or PDF_LINK_RE.search(url):
                    kind, body = "pdf", r.content
                else:
                    kind, body = "html", r.content
            except Exception:
                continue

            if kind == "html":
                title, links, text = extract_links(url, body)
                # extract emails from HTML
                found.extend(extract_from_text(url, title, text,
                             allow_non_official=allow_non_official))
                # extract mailto immediate
                for link in links:
                    if link.startswith("mailto:"):
                        email = link.split("mailto:", 1)[1]
                        found.extend(extract_from_text(
                            url, title, email, allow_non_official=allow_non_official))
                # enqueue new links
                for link in links:
                    if link.startswith("http"):
                        queue.append(link)
            else:  # pdf
                text = pdf_to_text(body or b"")
                if text:
                    found.extend(extract_from_text(
                        url, None, text, allow_non_official=allow_non_official))

            per_host_last[host] = time.monotonic()

    # dedup + write
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
    ap.add_argument("--out", default="data/outputs/rn_contacts",
                    help="output directory")
    ap.add_argument("--max-pages", type=int, default=250)
    ap.add_argument("--allow-non-official", action="store_true",
                    help="include non-gov emails")
    ap.add_argument("--dry-run", action="store_true",
                    dest="dry_run", help="run a deterministic offline dry-run")
    args = ap.parse_args()
    res = asyncio.run(
        crawl(
            seeds=SEEDS,
            out_dir=args.out,
            max_pages=args.max_pages,
            allow_non_official=args.allow_non_official,
            dry_run=args.dry_run,
        )
    )
    print(json.dumps(res, ensure_ascii=False))
