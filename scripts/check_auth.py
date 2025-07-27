# check_auth.py
import vertexai
import os

print("--- Iniciando Teste de Autenticação Vertex AI ---")

try:
    # Verifica se variáveis conflitantes existem (apenas para debug)
    if os.getenv("GOOGLE_API_KEY"):
        print("AVISO: Variável GOOGLE_API_KEY encontrada no ambiente!")

    # Inicializa a biblioteca Vertex AI usando as credenciais padrão (ADC)
    # que configuramos com 'gcloud auth application-default login'
    vertexai.init(project="aurora-464614", location="us-central1")

    print(
        "\n✅ SUCESSO! A biblioteca Vertex AI foi inicializada e autenticada corretamente."
    )
    print(f"Projeto Padrão: {vertexai.preview.global_config.project}")
    print(f"Localização Padrão: {vertexai.preview.global_config.location}")

except Exception as e:
    print("\n❌ FALHA! Ocorreu um erro durante a inicialização do Vertex AI.")
    print(f"Erro: {e}")

print("\n--- Teste de Autenticação Concluído ---")
