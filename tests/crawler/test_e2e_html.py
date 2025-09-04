from __future__ import annotations

from pathlib import Path

from aurora_platform.modules.crawler.pipeline import run_ingestion


def test_e2e_html():
    src = "tests/crawler/fixtures/sample.html"
    p = Path(src)
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    rec = run_ingestion(content=content, media_type="html", source=src)
    assert rec["id"]
    assert rec["chunks"]
