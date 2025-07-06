# src/aurora_platform/services/sales_mentor_service.py - Versão Final e Funcional

import vertexai
from vertexai.generative_models import GenerativeModel
from src.aurora_platform.core.config import settings

# Inicializa o Vertex AI de forma segura, lendo do nosso config.py
try:
    vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)
except Exception:
    # Ignora o erro se a biblioteca já foi inicializada
    pass

def prepare_for_meeting(client_name: str) -> str:
    """
    Usa o Gemini para gerar um plano de preparação para uma reunião.
    """
    # Usa o ID do modelo que acabamos de validar com sucesso
    model = GenerativeModel("gemini-2.5-pro")

    prompt = f"""
    **Persona:**
    Você é um "Mentor de Vendas de IA" da Aurora. Você foi treinado com base nas metodologias SPIN Selling e MEDDIC. Seu tom é empático, experiente e proativo.

    **Tarefa:**
    Escreva o diálogo de resposta para a seguinte solicitação de um vendedor: "Como posso me preparar para a reunião com o cliente '{client_name}' amanhã?"

    **Diretrizes para a Resposta:**
    1. **Demonstre Memória:** Faça referência a uma interação passada fictícia.
    2. **Seja Proativo:** Busque informações novas e relevantes.
    3. **Dê Orientação Estratégica:** Forneça um plano de ação claro.
    4. **Finalize com uma Pergunta Aberta:** Incentive a colaboração.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao contatar a API do Vertex AI: {e}"