from aurora_platform.modules.rag.search.lexical_bm25 import LexicalBM25
import pathlib
import json


def _write_lex(coll: str, rows):
    p = pathlib.Path("artifacts/lexical")
    p.mkdir(parents=True, exist_ok=True)
    f = p / f"{coll}.jsonl"
    with f.open("w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_bm25_basic(monkeypatch, tmp_path):
    coll = "test_coll@v1"
    monkeypatch.setenv("QDRANT_COLLECTION", coll)
    rows = [
        {
            "id": "a:0",
            "text": "gatos são animais domésticos",
            "meta": {"chunk_text": "gatos são animais domésticos"},
        },
        {
            "id": "b:0",
            "text": "cães e gatos podem conviver",
            "meta": {"chunk_text": "cães e gatos podem conviver"},
        },
        {
            "id": "c:0",
            "text": "aviões voam no céu",
            "meta": {"chunk_text": "aviões voam no céu"},
        },
    ]
    _write_lex(coll, rows)
    bm = LexicalBM25(coll)
    hits = bm.search("gatos", top_k=2)
    assert hits and hits[0].id in ("a:0", "b:0")
