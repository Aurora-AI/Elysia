# src/aurora_platform/services/llm_adapters.py

from abc import ABC, abstractmethod
import os
from langchain_google_vertexai import VertexAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import SecretStr

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
        self.llm = VertexAI(model_name="gemini-2.5-pro")  # Nome do modelo atualizado para a geração 2.5
        print("INFO: Adaptador VertexAI inicializado com o modelo Gemini 2.5 Pro.")

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)

class AzureOpenAIAdapter(ILLMAdapter):
    """Adaptador para o Azure OpenAI Service."""
    def __init__(self):
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01",
            # --- CORREÇÃO DE PARÂMETRO AQUI ---
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=SecretStr(api_key) if api_key else None,
            temperature=0.7
        )
        print("INFO: Adaptador Azure OpenAI inicializado.")
    
    def generate(self, prompt: str) -> str:
        # --- CORREÇÃO DE TIPO DE RETORNO AQUI ---
        # A API retorna um objeto de mensagem, o texto está no atributo .content
        response_message = self.llm.invoke([HumanMessage(content=prompt)])
        content = response_message.content
        return str(content) if content else ""

class DeepSeekAdapter(ILLMAdapter):
    """Adaptador para o DeepSeek (usando um Mock para esta POC)."""
    def __init__(self):
        self.llm = DeepSeekMock()
        print("INFO: Adaptador DeepSeek (Mock) inicializado.")
        
    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)