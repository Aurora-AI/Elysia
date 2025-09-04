
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="GPT-OSS Embedding Service")


class EmbeddingRequest(BaseModel):
    texts: list[str]


class EmbeddingResponse(BaseModel):
    embeddings: list[list[float]]


@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "cpu"}


@app.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    # Mock embeddings para CPU-only
    embeddings = [[0.1, 0.2, 0.3] for _ in request.texts]
    return EmbeddingResponse(embeddings=embeddings)
