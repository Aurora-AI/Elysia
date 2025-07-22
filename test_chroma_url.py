#!/usr/bin/env python3
"""Teste específico com a URL do Chroma que estava falhando."""

import requests
import json


def test_chroma_ingest():
    """Testa ingestão da URL do Chroma que estava dando erro 401."""

    api_url = "http://127.0.0.1:8000/api/v1/knowledge/ingest-from-web"

    test_data = {"url": "https://docs.trychroma.com/docs/overview/introduction"}

    print(f"Testando URL problemática: {test_data['url']}")

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
            print("[OK] URL do Chroma processada com sucesso!")
            print("Problema do erro 401 resolvido!")
        else:
            print(f"[ERRO] Ainda há problema: {response.status_code}")

    except Exception as e:
        print(f"[ERRO] {e}")


if __name__ == "__main__":
    test_chroma_ingest()
