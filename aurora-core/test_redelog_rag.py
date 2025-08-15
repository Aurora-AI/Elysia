#!/usr/bin/env python3
"""Teste do RAG com conteúdo da Rede Log RJ."""

import requests


def test_redelog_search():
    """Testa busca no conteúdo da Rede Log RJ."""

    api_url = "http://127.0.0.1:8000/api/v1/knowledge/search"

    queries = [
        "O que é a Rede Log RJ?",
        "PCA sistema treinamento",
        "almoxarifado virtual",
        "informes 2025",
        "quem somos rede log",
    ]

    for query in queries:
        print(f"\n--- PERGUNTA: {query} ---")

        try:
            response = requests.post(
                api_url,
                json={"query": query, "n_results": 2},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 200:
                results = response.json()["results"]
                for i, result in enumerate(results):
                    print(f"[{i + 1}] {result[:200]}...")
            else:
                print(f"[ERRO] Status {response.status_code}")

        except Exception as e:
            print(f"[ERRO] {e}")


if __name__ == "__main__":
    print("[TESTE] RAG com conteúdo da Rede Log RJ")
    test_redelog_search()
