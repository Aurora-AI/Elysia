import os
from typing import AsyncGenerator

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncAzureOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class OpenAIService:
    def __init__(self):
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        if not api_key or not azure_endpoint or not deployment_name:
            raise ValueError("Variáveis de ambiente Azure OpenAI não configuradas")

        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version="2024-02-01",
            azure_endpoint=azure_endpoint,
            timeout=float(os.getenv("AZURE_OPENAI_HTTP_CLIENT_TIMEOUT", "90.0")),
        )
        self.deployment_name = deployment_name

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(
            (APITimeoutError, APIConnectionError, APIStatusError)
        ),
        reraise=True,
    )
    async def _call_llm_with_retry(
        self, user_question: str, system_prompt: str
    ) -> AsyncGenerator[str, None]:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ]
        llm_call_timeout = float(os.getenv("AZURE_OPENAI_CALL_TIMEOUT", "45.0"))

        response_iterator = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,  # type: ignore
            temperature=0.7,
            max_tokens=800,
            stream=True,
            timeout=llm_call_timeout,
        )

        async for chunk in response_iterator:
            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                yield chunk.choices[0].delta.content

    async def generate_answer_stream(
        self, user_question: str, context: str
    ) -> AsyncGenerator[str, None]:
        system_prompt = (
            "Você é Aurora, uma assistente de IA. Responda à pergunta do usuário baseando-se "
            "estritamente no contexto fornecido.\n\n"
            f"Contexto:\n---\n{context}\n---"
        )
        try:
            async for chunk in self._call_llm_with_retry(
                user_question=user_question, system_prompt=system_prompt
            ):
                yield chunk
        except Exception as e:
            print(f"Erro inesperado durante a chamada ao LLM: {e}")
            yield f"Desculpe, ocorreu um erro inesperado ao gerar a resposta: {str(e)}"
