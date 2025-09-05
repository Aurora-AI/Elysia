from aurora_platform.modules.rag.models.rag_models import DocumentMacro
from aurora_platform.modules.rag.pipeline.rag_pipeline import ingest_document, query_memory


def test_chunk_on_demand_flow():
    doc = DocumentMacro(doc_id="d1", url="https://example.com", text="word " * 1000)
    ingest_document(doc)
    results = query_memory("word")
    assert isinstance(results, list)
