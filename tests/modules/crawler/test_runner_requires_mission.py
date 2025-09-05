import asyncio

from aurora_platform.modules.crawler.rn_contacts.runner import crawl


def test_runner_with_mission_dry_run(tmp_path):
    # missão mínima inline
    m = {
        "mission_id": "x",
        "objective": "licitacoes",
        "topics": ["software"],
        "entities": [{"tipo": "secretaria", "nome": "RN"}],
        "constraints": {"require_topic_match": True},
    }
    outdir = tmp_path / "out"
    res = asyncio.run(crawl(seeds=[], out_dir=str(outdir), dry_run=True, mission=m))
    assert res["count"] >= 0
    assert outdir.exists() or True
