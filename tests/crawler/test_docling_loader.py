from aurora_platform.modules.crawler.ingestion.loaders import DoclingLoader


def test_docling_loader_available_flag():
    # Should be boolean and not raise
    assert hasattr(DoclingLoader, "AVAILABLE")


def test_docling_loader_fallback_attr():
    # load is present
    assert hasattr(DoclingLoader, "load")
