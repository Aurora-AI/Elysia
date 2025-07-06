# list_models.py
import vertexai
from vertexai.generative_models import GenerativeModel
from src.aurora_platform.core.config import settings

print("--- Testando conexão com Vertex AI ---")
try:
    # Inicializa usando as credenciais e projeto do arquivo de configuração
    vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location="us-central1")

    # GenerativeModel não tem método list_models
    # Vamos testar a conexão diretamente
    model = GenerativeModel("gemini-1.5-pro")
    print(f"Modelo configurado: gemini-1.5-pro")
    print(f"Projeto: {settings.GOOGLE_CLOUD_PROJECT}")
    
    # Teste básico de conexão
    response = model.generate_content("Hello, test connection")
    print(f"Teste de conexão bem-sucedido!")
    print(f"Resposta: {response.text[:100]}...")

except Exception as e:
    print(f"\nOcorreu um erro ao testar a conexão: {e}")