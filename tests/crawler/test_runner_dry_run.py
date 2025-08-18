import pytest
from aurora_platform.modules.crawler.rn_contacts import runner


@pytest.mark.asyncio
async def test_crawl_dry_run(tmp_path, event_loop):
    outdir = tmp_path / "out"
    await runner.crawl(seeds=["https://example.com"], out_dir=str(outdir), dry_run=True)
    assert outdir.exists()
    children = [p for p in outdir.iterdir() if p.is_dir()]
    assert children, "no output subdir created"
    assert any((c / "manifest.json").exists() for c in children)
