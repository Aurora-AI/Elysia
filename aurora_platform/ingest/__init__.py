"""Ingest package for Docling -> Qdrant MVP1.

This package contains a minimal, dependency-light skeleton to ingest documents,
chunk them and index them. It uses a file-backed fallback for local testing
when Qdrant isn't available.
"""

__all__ = ["models", "docling_pipeline", "router"]
