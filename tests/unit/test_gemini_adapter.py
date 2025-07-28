import pytest
from aurora_platform.services.llm_adapters import GeminiAdapter
from pydantic import SecretStr as V2SecretStr


def test_gemini_adapter_key_types():
    # Teste com SecretStr v2
    adapter1 = GeminiAdapter(api_key=V2SecretStr("key1"))
    assert adapter1.api_key.get_secret_value() == "key1"

    # Teste com string simples
    adapter2 = GeminiAdapter(api_key="key2")
    assert adapter2.api_key.get_secret_value() == "key2"

    # Teste com None (deve falhar)
    with pytest.raises(ValueError):
        GeminiAdapter(api_key=None)

    print("✅ Todos os testes de tipo de chave passaram")
