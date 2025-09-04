from aurora_platform.ingest.docling_pipeline import chunk_text, run_pipeline, to_markdown


def test_run_pipeline_from_url():
    doc_id, count = run_pipeline(source_url="http://example.com/doc1")
    assert isinstance(doc_id, str) and len(doc_id) > 0
    assert count >= 1


def test_chunk_text_basic():
    md = to_markdown("This is a small document with some text." * 20)
    chunks = chunk_text(md, doc_id="doc1", max_chars=100)
    assert len(chunks) >= 1
