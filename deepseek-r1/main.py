#!/usr/bin/env python3
"""
Servidor DeepSeek R1 simples usando FastAPI e transformers
Compatível com OpenAI API para integração com Aurora
"""

import logging
import os
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DeepSeek R1 API", version="1.0.0")

# Configurações
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))


# Modelos de dados para compatibilidade OpenAI
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    max_tokens: int | None = 100
    temperature: float | None = 0.7
    stream: bool | None = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[dict[str, Any]]
    usage: dict[str, int]


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "deepseek"


# Simulação simples do modelo (para demonstração)
# Em produção, aqui carregaria o modelo real
model_loaded = False


def load_model():
    """Simula carregamento do modelo"""
    global model_loaded
    try:
        logger.info(f"Simulando carregamento do modelo {MODEL_NAME}")
        # Aqui seria: model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        model_loaded = True
        logger.info("Modelo carregado com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        return False


def generate_response(messages: list[ChatMessage], max_tokens: int = 100) -> str:
    """Gera resposta simples (mock para demonstração)"""
    if not model_loaded:
        return "Modelo não carregado. Resposta simulada: Olá! Sou o DeepSeek R1."

    # Pega a última mensagem do usuário
    user_message = messages[-1].content if messages else "Olá"

    # Resposta simulada baseada na mensagem
    if "hello" in user_message.lower() or "olá" in user_message.lower():
        return "Olá! Como posso ajudá-lo hoje?"
    elif "como" in user_message.lower() and "você" in user_message.lower():
        return "Sou o DeepSeek R1, um modelo de linguagem desenvolvido pela DeepSeek."
    else:
        return f"Entendi sua mensagem: '{user_message}'. Como posso ajudar?"


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "model_loaded": model_loaded, "model_name": MODEL_NAME}


@app.get("/v1/models")
async def list_models():
    """Lista modelos disponíveis (compatibilidade OpenAI)"""
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "created": 1640995200,
                "owned_by": "deepseek",
            }
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Endpoint de chat completions (compatibilidade OpenAI)"""
    try:
        if not model_loaded:
            # Tenta carregar o modelo se não estiver carregado
            if not load_model():
                raise HTTPException(status_code=503, detail="Modelo não disponível")

        # Gera resposta
        response_text = generate_response(request.messages, request.max_tokens or 100)

        # Formato de resposta compatível com OpenAI
        return {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1640995200,
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response_text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "completion_tokens": len(response_text.split()),
                "total_tokens": sum(len(msg.content.split()) for msg in request.messages)
                + len(response_text.split()),
            },
        }

    except Exception as e:
        logger.error(f"Erro no chat completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Carrega modelo na inicialização"""
    logger.info("Iniciando servidor DeepSeek R1...")
    load_model()


if __name__ == "__main__":
    logger.info(f"Iniciando servidor em {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
