# test_gcp_access.py
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "aurora-core-prod"
LOCATION = "us-central1"

print(f"--- Tentando inicializar o Vertex AI para o projeto {PROJECT_ID} em {LOCATION} ---")

try:
    # Passo 1: Inicializar o SDK
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("✅ SDK do Vertex AI inicializado com sucesso.")

    # Passo 2: Tentar instanciar um modelo
    print("\n--- Tentando instanciar o modelo 'gemini-pro' ---")
    # Usamos 'gemini-pro' por ser o mais estável e com maior probabilidade de estar disponível
    model = GenerativeModel("gemini-pro")
    print("✅ SUCESSO! Acesso ao modelo 'gemini-pro' confirmado.")
    print("\nO ambiente Google Cloud está configurado corretamente. Podemos prosseguir.")

except Exception as e:
    print(f"\n❌ FALHA! Ocorreu um erro.")
    print(f"\nDIAGNÓSTICO DO ERRO: {e}")
    print("\nINSTRUÇÃO: O problema persiste na configuração do projeto/conta no Google Cloud. Contate o suporte do Google.")