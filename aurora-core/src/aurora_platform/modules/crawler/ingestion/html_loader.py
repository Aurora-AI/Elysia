from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging
import re

try:
    from selectolax.parser import HTMLParser
    HAS_SELECTOLAX = True
except Exception:
    HAS_SELECTOLAX = False

try:
    import trafilatura
    HAS_TRAFILATURA = True
except Exception:
    HAS_TRAFILATURA = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except Exception:
    HAS_BS4 = False

logger = logging.getLogger(__name__)


@dataclass
class HTMLLoadResult:
    text: str
    html: Optional[str]
    meta: Dict[str, Any]


class HTMLLoader:
    """Extrai conteúdo e metadados de HTML:
       1) tenta 'artigo legível' via trafilatura (se disponível),
       2) senão parseia com selectolax (rápido) ou fallback bs4.
    """

    def __init__(self, prefer_readable: bool = True) -> None:
        self.prefer_readable = prefer_readable

    def load_from_string(self, html: str, base_url: Optional[str] = None) -> HTMLLoadResult:
        if self.prefer_readable and HAS_TRAFILATURA:
            try:
                extracted = trafilatura.extract(
                    html, include_comments=False, include_tables=False, url=base_url
                )
                if extracted and extracted.strip():
                    meta = self._extract_meta_trafilatura(html, base_url)
                    return HTMLLoadResult(text=extracted.strip(), html=html, meta=meta)
            except Exception as e:
                logger.warning("Trafilatura falhou: %s", e)
        if HAS_SELECTOLAX:
            return self._parse_with_selectolax(html, base_url)
        if HAS_BS4:
            return self._parse_with_bs4(html, base_url)
        return HTMLLoadResult(text=self._fallback_text(html), html=html, meta={"source_type": "html"})

    # -------- selectolax --------
    def _parse_with_selectolax(self, html: str, base_url: Optional[str]) -> HTMLLoadResult:
        tree = HTMLParser(html)
        title = self._first_text(tree, ["title", "h1"]) or ""
        text = self._heuristic_main_text_selectolax(tree)
        meta = {
            "title": title.strip() or None,
            "authors": self._guess_authors_selectolax(tree),
            "published_at": self._guess_date_selectolax(tree),
            "source_type": "html", "url": base_url, "parser": "selectolax",
        }
        return HTMLLoadResult(text=text, html=html, meta=meta)

    def _first_text(self, tree, selectors):
        for sel in selectors:
            n = tree.css_first(sel)
            if n and n.text():
                return n.text()
        return None

    def _heuristic_main_text_selectolax(self, tree) -> str:
        for sel in ["script", "style", "nav", "footer", "form", "aside"]:
            for n in tree.css(sel) or []:
                n.decompose()
        candidates = []
        for sel in ["article", "main", "[role=main]", ".article", ".post", ".content", ".entry-content"]:
            for n in tree.css(sel) or []:
                t = n.text(separator=" ").strip()
                if t:
                    candidates.append((len(t), t))
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]
        paragraphs = [n.text().strip()
                      for n in tree.css("p") or [] if n.text().strip()]
        if paragraphs:
            return "\n\n".join(paragraphs)
        return self._fallback_text(tree.html)

    def _guess_authors_selectolax(self, tree):
        authors = set()
        for sel in ["meta[name=author]", "[itemprop=author]", ".author", ".byline"]:
            for n in tree.css(sel) or []:
                content = n.attributes.get(
                    "content") if n.tag == "meta" else n.text()
                if content and content.strip():
                    authors.add(content.strip())
        return list(authors) or None

    def _guess_date_selectolax(self, tree):
        n = tree.css_first("meta[property='article:published_time']")
        if n and n.attributes.get("content"):
            return n.attributes["content"].strip()
        t = tree.css_first("time[datetime]")
        if t and t.attributes.get("datetime"):
            return t.attributes["datetime"].strip()
        return None

    # -------- bs4 --------
    def _parse_with_bs4(self, html: str, base_url: Optional[str]) -> HTMLLoadResult:
        soup = BeautifulSoup(html, "lxml")
        title = (soup.title.string if soup.title else None) or self._first_tag_text_bs4(
            soup, ["h1"])
        text = self._heuristic_main_text_bs4(soup)
        meta = {
            "title": (title.strip() if title else None),
            "authors": self._guess_authors_bs4(soup),
            "published_at": self._guess_date_bs4(soup),
            "source_type": "html", "url": base_url, "parser": "bs4",
        }
        return HTMLLoadResult(text=text, html=html, meta=meta)

    def _first_tag_text_bs4(self, soup, tags):
        for t in tags:
            el = soup.find(t)
            if el and el.get_text(strip=True):
                return el.get_text(strip=True)
        return None

    def _heuristic_main_text_bs4(self, soup):
        for tag in soup(["script", "style", "nav", "footer", "form", "aside"]):
            tag.decompose()
        candidates = []
        for sel in ["article", "main", {"role": "main"}, {"class": "article"}, {"class": "post"}, {"class": "content"}]:
            found = soup.find_all(sel) if isinstance(
                sel, str) else soup.find_all(attrs=sel)
            for n in found:
                t = n.get_text(" ", strip=True)
                if t:
                    candidates.append((len(t), t))
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        if paragraphs:
            return "\n\n".join(paragraphs)
        return self._fallback_text(str(soup))

    def _guess_authors_bs4(self, soup):
        authors = set()
        meta = soup.find("meta", attrs={"name": "author"})
        if meta and meta.get("content"):
            authors.add(meta["content"].strip())
        for cls in ["author", "byline"]:
            for tag in soup.select(f".{cls}"):
                txt = tag.get_text(" ", strip=True)
                if txt:
                    authors.add(txt)
        return list(authors) or None

    def _guess_date_bs4(self, soup):
        meta = soup.find("meta", attrs={"property": "article:published_time"})
        if meta and meta.get("content"):
            return meta["content"].strip()
        t = soup.find("time", attrs={"datetime": True})
        if t and t.get("datetime"):
            return t["datetime"].strip()
        return None

    # -------- util --------
    def _extract_meta_trafilatura(self, html: str, base_url: Optional[str]):
        # trafilatura já tenta extrair; mantemos meta mínima coerente
        return {"source_type": "html", "url": base_url, "parser": "trafilatura"}

    def _fallback_text(self, s: str) -> str:
        return re.sub(r"\s+", " ", s or "").strip()
