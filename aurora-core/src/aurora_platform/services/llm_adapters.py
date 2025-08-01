# src/aurora_platform/services/llm_adapters.py

import os
from abc import ABC, abstractmethod

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import VertexAI
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr as V2SecretStr
from pydantic.v1.types import SecretStr as V1SecretStr


# Mock para o DeepSeek Adapter, já que não temos a biblioteca específica
class DeepSeekMock:
    def invoke(self, prompt: str) -> str:
        print("--- MOCK: Chamada para DeepSeek ---")
        return f"Resposta simulada pelo DeepSeek para: {prompt[:50]}..."


# --- PASSO 1: A Interface do Adaptador (O Contrato) ---
class ILLMAdapter(ABC):
    """
    Define a interface comum para todos os adaptadores de LLM, garantindo
    que o RAG Service possa interagir com qualquer um deles de forma uniforme.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Recebe um prompt final e retorna a resposta gerada pelo LLM.
        """
        pass


# --- PASSO 2: As Implementações Concretas ---


class VertexAIAdapter(ILLMAdapter):
    """Adaptador para o Google Vertex AI (Gemini)."""

    def __init__(self):
        self.llm = VertexAI(
            model_name="gemini-2.5-pro"
        )  # Nome do modelo atualizado para a geração 2.5
        print("INFO: Adaptador VertexAI inicializado com o modelo Gemini 2.5 Pro.")

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)


class AzureOpenAIAdapter(ILLMAdapter):
    """Adaptador para o Azure OpenAI Service."""

    def __init__(self):
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_key_v2 = V2SecretStr(api_key) if api_key else None
        api_key_v1 = V1SecretStr(api_key_v2.get_secret_value()) if api_key_v2 else None
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01",
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=api_key_v1,
            temperature=0.7,
        )
        print("INFO: Adaptador Azure OpenAI inicializado.")

    def generate(self, prompt: str) -> str:
        response_message = self.llm.invoke([HumanMessage(content=prompt)])
        content = getattr(response_message, "content", None)
        return str(content) if content is not None else ""


class DeepSeekAdapter(ILLMAdapter):
    """Adaptador para o DeepSeek (usando um Mock para esta POC)."""

    def __init__(self):
        self.llm = DeepSeekMock()
        print("INFO: Adaptador DeepSeek (Mock) inicializado.")

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)


class GeminiAdapter(ILLMAdapter):
    def __init__(
        self,
        api_key: V2SecretStr | str | None = None,
        model_name: str = "gemini-pro",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        api_key_str: str | None = None
        if isinstance(api_key, V2SecretStr):
            api_key_str = api_key.get_secret_value()
        elif isinstance(api_key, str):
            api_key_str = api_key
        if not api_key_str:
            raise ValueError("API key is required for GeminiAdapter")
        self.api_key = V1SecretStr(api_key_str)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        # Implementar o método de geração usando o adaptador Gemini
        return ""
