from aurora_platform.modules.crawler.chunking.splitter import split_markdown


def test_splitter_naive():
    text = "A" * 1200
    chunks = split_markdown(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2
    assert all("text" in c for c in chunks)
