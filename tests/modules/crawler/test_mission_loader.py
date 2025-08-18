from aurora_platform.modules.crawler.mission.spec import load_mission
import os, textwrap

def test_load_mission_ok(tmp_path):
    p = tmp_path / "m.yml"
    p.write_text(textwrap.dedent("""
      mission_id: test_m1
      objective: licitacoes
      topics: [software, TI]
      entities: [{tipo: secretaria, nome: "SEAD"}]
    """).strip())
    m = load_mission(str(p))
    assert m["mission_id"] == "test_m1"
    assert m["objective"] == "licitacoes"
    assert m["constraints"]["max_pages"] > 0
    assert "_mission_hash" in m
