"""Consumers package exports for tests and runtime.

Keep imports minimal so tests can import upsert_pilar without side-effects.
"""
from .kafka_consumer_pilares import upsert_pilar, run  # noqa: F401
# consumers package
