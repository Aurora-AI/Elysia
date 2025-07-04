# src/aurora_platform/services/sales_mentor_service.py
import vertexai
from vertexai.generative_models import GenerativeModel

from src.aurora_platform.core.config import settings

# Inicializa o Vertex AI (ele usará as credenciais ADC que já configuramos)
vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)

def prepare_for_meeting(client_name: str) -> str:
    """
    Usa o Gemini para gerar um plano de preparação para uma reunião.
    """
    # Carrega o modelo generativo
    model = GenerativeModel("gemini-1.5-pro-preview-0409") # Ou o modelo que preferir

    # O prompt que projetamos e validamos
    prompt = f"""
    **Persona:**
    Você é um "Mentor de Vendas de IA" da Aurora. Você foi treinado com base nas metodologias SPIN Selling e MEDDIC e tem acesso ao histórico de interações do seu usuário. Seu tom é empático, experiente e proativo.

    **Tarefa:**
    Escreva o diálogo de resposta para a seguinte solicitação de um vendedor: "Como posso me preparar para a reunião com o cliente '{client_name}' amanhã?"

    **Diretrizes para a Resposta:**
    1. **Demonstre Memória:** Comece a resposta fazendo referência a uma interação passada fictícia (ex: "Claro. Da última vez que falamos sobre a {client_name}, a principal objeção deles era o preço...").
    2. **Seja Proativo:** Não espere por mais perguntas. Busque informações novas (ex: "Fiz uma busca rápida e vi que o principal concorrente deles acabou de anunciar um novo produto...").
    3. **Dê Orientação Estratégica:** Em vez de uma lista de fatos, forneça um plano de ação claro e conciso baseado na sua base de conhecimento (ex: "Sugiro focarmos em reforçar nosso diferencial de 'integração fácil'...").
    4. **Finalize com uma Pergunta Aberta:** Termine a interação incentivando a colaboração (ex: "Isso faz sentido para você? Gostaria que eu preparasse alguns pontos para a sua apresentação com base nesta estratégia?").
    """

    try:
        # Envia o prompt para o modelo
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Em caso de erro na API, retorna uma mensagem clara
        return f"Erro ao contatar a API do Vertex AI: {e}"