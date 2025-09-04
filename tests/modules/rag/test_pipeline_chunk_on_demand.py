# /tests/modules/rag/test_pipeline_chunk_on_demand.py
import os

import pytest

from aurora_platform.modules.rag.pipeline import DocRecord, QdrantRAGPipeline

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")


@pytest.mark.skipif(
    os.getenv("ENABLE_QDRANT_TESTS") != "1",
    reason="Defina ENABLE_QDRANT_TESTS=1 para rodar este teste de integração.",
)
def test_chunk_on_demand_flow(tmp_path):
    rag = QdrantRAGPipeline(
        qdrant_url=qdrant_url,
        collection_docs="test_docs",
        collection_chunks="test_chunks_on_demand",
    )

    doc_id = "doc-xyz"
    text = "Aurora é uma plataforma. " * 100  # cria várias janelas para chunking
    rag.index_document(DocRecord(doc_id=doc_id, text=text, metadata={"uri": "mem://doc-xyz"}))

    res = rag.search(
        "plataforma",
        get_full_text_fn=lambda did: text if did == doc_id else "",
        get_doc_meta_fn=lambda did: {"uri": "mem://doc-xyz"},
        top_k_docs=1,
        top_k_chunks=3,
    )

    assert res.doc_hits, "Esperava ao menos 1 hit no nível de documento"
    assert res.chunk_hits, "Esperava chaves de chunks após o on-demand"
