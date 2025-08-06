# src/aurora_platform/services/adapter_factory.py

from .llm_adapters import (
    AzureOpenAIAdapter,
    DeepSeekAdapter,
    ILLMAdapter,
    VertexAIAdapter,
)


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
        else:
            raise ValueError(
<<<<<<< HEAD
                f"Provedor de LLM desconhecido: '{provider_name}'. Os provedores suportados são: google, azure, deepseek."
=======
                f"Provedor de LLM desconhecido: '{provider_name}'. "
                "Os provedores suportados são: google, azure, deepseek."
>>>>>>> origin/main
            )
