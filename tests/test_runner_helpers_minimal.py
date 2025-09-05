from aurora_platform.modules.crawler.rn_contacts import runner_helpers as rh


def test_derive_seed():
    """Minimal test to ensure runner_helpers is importable and derives a mission id."""
    v = rh._derive_mission_id(None, {"seeds": ["https://example.com/path"]})
    assert isinstance(v, str) and "example" in v
