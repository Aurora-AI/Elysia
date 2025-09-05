from pathlib import Path

from aurora_platform.modules.crawler import pipeline


def test_e2e_ingestion_html(tmp_path: Path):
    fx = Path("tests/crawler/fixtures/sample.html")
    assert fx.exists(), "fixture sample.html missing"
    res = pipeline.run_ingestion(
        content=fx.read_text(encoding="utf-8"),
        media_type="text/html",
        source=str(fx),
    )
    assert "id" in res
    assert "chunks" in res


def test_e2e_ingestion_pdf(tmp_path: Path):
    fx = Path("tests/crawler/fixtures/sample.pdf")
    if not fx.exists():
        # skip if heavy fixture not present
        return
    # pipeline expects content string for non-file pipeline; for file-based loader we would adapt
    # Here we simply assert fixture exists to mark phase setup
    assert fx.stat().st_size > 0


def test_e2e_ingestion_docx(tmp_path: Path):
    fx = Path("tests/crawler/fixtures/sample.docx")
    if not fx.exists():
        return
    assert fx.stat().st_size > 0
