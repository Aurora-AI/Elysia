# src/aurora_platform/services/sales_mentor_service.py - Versão Final com Azure OpenAI

import logging
from openai import AzureOpenAI
from src.aurora_platform.core.config import settings

# Configuração do logger para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Template do prompt para o "Mentor de Vendas"
# Definido como uma constante para clareza e reutilização
SYSTEM_PROMPT_TEMPLATE = """
Você é um "Mentor de Vendas de IA" da Aurora. Você foi treinado com base nas metodologias SPIN Selling e MEDDIC. Seu tom é empático, experiente e proativo.
Sua tarefa é analisar o pedido do usuário e fornecer um plano de ação claro e conciso para a reunião solicitada.

Diretrizes para a Resposta:
1.  **Demonstre Memória:** Comece a resposta fazendo referência a uma interação passada fictícia com o cliente ou com o usuário.
2.  **Seja Proativo:** Simule a busca por informações novas e relevantes sobre o cliente ou seus concorrentes.
3.  **Dê Orientação Estratégica:** Forneça um plano de ação claro e numerado, sugerindo perguntas e abordagens baseadas nas metodologias SPIN e MEDDIC.
4.  **Finalize com uma Pergunta Aberta:** Termine a interação incentivando a colaboração e oferecendo ajuda adicional.
"""


def prepare_for_meeting(client_name: str) -> str:
    """
    Usa o Azure OpenAI (GPT-4) para gerar um plano estratégico para uma reunião de vendas.
    """
    logger.info(f"Iniciando preparação para a reunião com o cliente: {client_name}")

    try:
        # 1. Inicializa o Cliente Azure OpenAI com as credenciais do nosso config
        client = AzureOpenAI(
            api_version=settings.openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint.get_secret_value(),
            api_key=settings.azure_openai_api_key.get_secret_value(),
        )

        # 2. Formata a mensagem para o padrão da API OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE},
            {
                "role": "user",
                "content": f"Como posso me preparar para a reunião com o cliente '{client_name}' amanhã?",
            },
        ]

        logger.info(
            f"Enviando prompt para o deployment '{settings.azure_openai_deployment_name}' no Azure..."
        )

        # 3. Chama a API usando streaming para melhor responsividade
        response_stream = client.chat.completions.create(
            model=settings.azure_openai_deployment_name,  # ex: "aurora-flagship-reasoning"
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE},
                {
                    "role": "user",
                    "content": f"Como posso me preparar para a reunião com o cliente '{client_name}' amanhã?",
                },
            ],
            stream=True,
        )

        # 4. Concatena os pedaços da resposta recebida via streaming
        full_response = ""
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        logger.info("Resposta recebida com sucesso do Azure OpenAI.")
        return full_response

    except Exception as e:
        logger.error(f"Erro ao contatar a API do Azure OpenAI.", exc_info=True)
        # Retorna uma mensagem de erro clara para a API
        return f"Erro ao contatar a API de IA: {e}"
