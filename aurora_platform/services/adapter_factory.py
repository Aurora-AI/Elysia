# src/aurora_platform/services/adapter_factory.py

from .llm_adapters import (
    AzureOpenAIAdapter,
    DeepSeekAdapter,
    ILLMAdapter,
    VertexAIAdapter,
)
from .langgraph_adapter import LangGraphAdapter


class AdapterFactory:
    """
    Fábrica responsável por criar a instância correta do adaptador de LLM
    com base no nome do provedor.
    """

    @staticmethod
    def create_adapter(provider_name: str) -> ILLMAdapter:
        provider_name = provider_name.lower()
        if provider_name == "google":
            return VertexAIAdapter()
        elif provider_name == "azure":
            return AzureOpenAIAdapter()
        elif provider_name == "deepseek":
            return DeepSeekAdapter()
        elif provider_name == "langgraph":
            # Provide a LangGraph shim adapter for compatibility.
            return LangGraphAdapter()
        else:
            raise ValueError(
                f"Provedor de LLM desconhecido: '{provider_name}'. Os provedores suportados são: google, azure, deepseek."
            )
