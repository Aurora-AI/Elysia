from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Configuração do App
app = FastAPI(title="DeepSeek CPU Inference Server")

# Carrega o modelo e o tokenizador na inicialização
# O modelo será baixado do Hugging Face na primeira vez.
model_name = "deepseek-ai/deepseek-coder-v2-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16, # Use bfloat16 para melhor performance em CPUs compatíveis
    trust_remote_code=True
)

# Cria o pipeline de geração de texto
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1) # device=-1 força o uso da CPU

class GenerationRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 512

@app.post("/generate")
async def generate(request: GenerationRequest):
    """Gera texto a partir de um prompt usando o modelo DeepSeek na CPU."""
    try:
        outputs = pipe(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            return_full_text=False
        )
        generated_text = outputs[0]['generated_text']
        return {"response": generated_text}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    return {"status": "ok"}
