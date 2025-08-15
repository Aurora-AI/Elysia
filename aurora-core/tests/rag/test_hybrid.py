from aurora_platform.modules.rag.search.hybrid import rrf_fuse, Hit


def test_rrf_fuse_basic():
    v = [Hit(id="x", score=0.9, payload={"chunk_text": "x"}, source="vec"),
         Hit(id="y", score=0.8, payload={"chunk_text": "y"}, source="vec")]
    bm25_hits = [Hit(id="y", score=2.0, payload={"chunk_text": "y"}, source="bm25"),
                 Hit(id="z", score=1.5, payload={"chunk_text": "z"}, source="bm25")]
    out = rrf_fuse(v, bm25_hits, top_k=3)
    ids = [h.id for h in out]
    assert set(ids) == {"x", "y", "z"}
