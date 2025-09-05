import os

import pytest

pytestmark = pytest.mark.skipif(os.getenv("TESTING") != "1", reason="Set TESTING=1")

from aurora_platform.modules.crawler.rn_contacts.runner import crawl


def test_crawl_writes_missionized_manifest(tmp_path):
    mission = {
        "mission_id": "rn_smoke_auto",
        "constraints": {
            "max_pages": 20,
            "render_js": {"mode": "auto", "budget": 0.2, "timeout_sec": 10},
        },
        "seeds": ["https://natal.rn.gov.br/"],
    }
    out_base = tmp_path / "out"
    import asyncio

    res = asyncio.run(
        crawl(seeds=mission["seeds"], out_dir=str(out_base), mission=mission, dry_run=True)
    )
    assert res.get("ok", True) is True
    import json as _json
    import pathlib

    mpath = next(pathlib.Path(str(out_base)).rglob("manifest.json"))
    meta = _json.load(open(mpath, encoding="utf-8"))
    assert meta["mission_id"] == "rn_smoke_auto"
    assert "render" in meta and meta["render"]["cap"] >= 1
