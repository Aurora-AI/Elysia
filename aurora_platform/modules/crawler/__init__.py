"""Aurora Platform - Crawler module (canonical path)

This package contains loaders, pipeline and utilities for ingestion.
"""

from . import loaders  # expose loaders package
from . import pipeline

__all__ = ["loaders", "pipeline"]
