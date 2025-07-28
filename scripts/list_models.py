# list_models.py
import vertexai
from vertexai.generative_models import GenerativeModel

from src.aurora_platform.core.config import settings

print("--- Listando modelos disponíveis no Vertex AI ---")
try:
    # Inicializa usando as credenciais e projeto do arquivo de configuração
    vertexai.init(
        project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION
    )

    # Pylance reports a false positive here, so we ignore the type error.
    models = GenerativeModel.list_models()  # type: ignore

    # Usa uma parte do nome do modelo da configuração para filtrar
    filter_str = "gemini-1.5-pro"
    print(f"\nModelos encontrados que contêm '{filter_str}':")
    for model in models:
        # Filtramos para mostrar apenas os modelos relevantes para nós
        if filter_str in model.name:
            print(f"- {model.name}")

except Exception as e:
    print(f"\nOcorreu um erro ao listar os modelos: {e}")
