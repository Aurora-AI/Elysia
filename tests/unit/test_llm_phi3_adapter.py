import pytest
from src.aurora_platform.clients.adapters.llm_phi3_adapter import LLMPhi3Adapter

class MockResponse:
    def json(self):
        return {"choices": [{"text": "Resposta simulada do Phi-3"}]}

@pytest.fixture
def mock_post(monkeypatch):
    def fake_post(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr("httpx.post", fake_post)

def test_phi3_adapter_generate_method(mock_post):
    adapter = LLMPhi3Adapter(config={})
    prompt = "Qual a capital da França?"
    resposta = adapter.generate(prompt)
    assert resposta == "Resposta simulada do Phi-3"
