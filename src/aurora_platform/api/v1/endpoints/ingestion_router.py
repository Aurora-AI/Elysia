# src/aurora_platform/api/v1/endpoints/ingestion_router.py

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from aurora_platform.modules.rag.orchestrator import AuroraIngestionOrchestrator

router = APIRouter(prefix="/ingest", tags=["ingestion"])


class IngestRequest(BaseModel):
    """Schema for document ingestion requests."""

    content: str
    document_type: Optional[str] = "text"
    metadata: Optional[Dict[str, Any]] = None


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def ingest_document(request: IngestRequest):
    """
    Ingest a document into the RAG system.

    Args:
        request: Document ingestion request containing content and metadata

    Returns:
        Dictionary with ingestion result
    """
    try:
        orchestrator = AuroraIngestionOrchestrator()

        document_data = {
            "content": request.content,
            "document_type": request.document_type,
            "metadata": request.metadata or {},
        }

        result = await orchestrator.ingest_document(document_data)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting document: {str(e)}",
        )
