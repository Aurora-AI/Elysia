import pytest
from aurora.memory import adk_client

import os


@pytest.mark.skipif("VERTEX_MEMORY_BANK_ID" not in os.environ, reason="Memory Bank não configurado")
def test_search_and_save_memory():
    scope = {"user_id": "test-user"}
    adk_client.autosave_to_memory(
        [{"role": "user", "content": "Teste Aurora"}], scope)
    results = adk_client.search_memory("Aurora", scope)
    assert isinstance(results, list)
