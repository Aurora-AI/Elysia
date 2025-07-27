# tests/integration/test_ingestion_api.py

import pytest
import sys
import os

# Add src to path for direct imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from aurora_platform.modules.rag.orchestrator import AuroraIngestionOrchestrator


@pytest.mark.asyncio
async def test_ingest_document_success():
    """Test successful document ingestion via orchestrator directly."""
    # Test the orchestrator directly since the router isn't registered yet
    orchestrator = AuroraIngestionOrchestrator()

    test_data = {
        "content": "This is a test document content for ingestion.",
        "document_type": "text",
        "metadata": {"source": "test", "author": "test_user"},
    }

    result = await orchestrator.ingest_document(test_data)

    assert "status" in result
    assert result["status"] == "success"
    assert "message" in result
    assert result["message"] == "Document ingested successfully"


def test_ingest_router_imports():
    """Test that the ingestion router can be imported."""
    from aurora_platform.api.v1.endpoints.ingestion_router import router, IngestRequest

    # Verify router is configured correctly
    assert router.prefix == "/ingest"
    assert "ingestion" in router.tags

    # Verify schema is available
    assert IngestRequest is not None

    # Test schema validation
    test_request = IngestRequest(content="test content")
    assert test_request.content == "test content"
    assert test_request.document_type == "text"  # default value
    assert test_request.metadata is None  # default value
