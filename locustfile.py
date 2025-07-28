# locustfile.py

import random

from locust import HttpUser, between, task

URLS_PARA_INGERIR = [
    "https://docs.trychroma.com/getting-started",
    "https://fastapi.tiangolo.com/tutorial/",
    "https://pge.rj.gov.br/checklists-lei-1413321",
]

PERGUNTAS_PARA_RAG = [
    "What is Chroma?",
    "How do I create a FastAPI application?",
    "Summarize the main points of Lei 14.133",
]


class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(1)
    def ingestao_de_conhecimento(self):
        url_aleatoria = random.choice(URLS_PARA_INGERIR)
        payload = {"url": url_aleatoria}
        headers = {"Content-Type": "application/json"}
        self.client.post(
            "/api/v1/knowledge/ingest-from-web",
            json=payload,
            headers=headers,
            name="/api/v1/knowledge/ingest-from-web",
        )

    @task(3)
    def consulta_com_rag(self):
        pergunta_aleatoria = random.choice(PERGUNTAS_PARA_RAG)
        payload = {"query": pergunta_aleatoria, "n_results": 2}
        headers = {"Content-Type": "application/json"}

        # --- CORREÇÃO: Alvo alterado de /ask para /search ---
        self.client.post(
            "/api/v1/knowledge/search",
            json=payload,
            headers=headers,
            name="/api/v1/knowledge/search",
        )
