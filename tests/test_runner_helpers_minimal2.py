from aurora_platform.modules.crawler.rn_contacts import runner_helpers as rh


def test_derive_seed2():
    v = rh._derive_mission_id(None, {"seeds": ["https://example.com/path"]})
    assert isinstance(v, str) and "example" in v
