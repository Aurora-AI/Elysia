#!/usr/bin/env python3
"""Teste da API real com ingestão de URL."""

import requests
import json


def test_ingest_api():
    """Testa o endpoint de ingestão via API."""

    # URL da API local
    api_url = "http://127.0.0.1:8000/api/v1/knowledge/ingest-from-web"

    # URL de teste
    test_data = {"url": "https://example.com"}

    print(f"Testando ingestão da URL: {test_data['url']}")

    try:
        response = requests.post(
            api_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 202]:
            print("[OK] Ingestão realizada com sucesso!")
        else:
            print(f"[ERRO] Falha na ingestão: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print(
            "[ERRO] Servidor não está rodando. Execute: uvicorn src.aurora_platform.main:app --reload"
        )
    except Exception as e:
        print(f"[ERRO] {e}")


if __name__ == "__main__":
    test_ingest_api()
