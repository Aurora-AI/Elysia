import asyncio

from aurora_platform.services.langgraph_adapter import LangGraphAdapter


def test_langgraph_adapter_shim_sync():
    adapter = LangGraphAdapter()
    res = adapter.generate("hello world")
    assert isinstance(res, dict)
    assert "text" in res


def test_langgraph_adapter_shim_async():
    adapter = LangGraphAdapter()
    loop = asyncio.new_event_loop()
    try:
        res = loop.run_until_complete(adapter.generate_async("async hello"))
        assert isinstance(res, dict)
        assert "text" in res
    finally:
        loop.close()
