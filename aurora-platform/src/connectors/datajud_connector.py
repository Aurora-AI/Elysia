"""
Conector DataJud (stub amigável a testes).
Em produção, chame o cliente/SDK real aqui.
"""

from typing import Any, Dict


def search_by_process_number(numero_processo: str) -> Dict[str, Any]:
    # Stub default: útil para smoke/local quando não há rede
    # Em produção, substituir por chamada real (HTTP/SDK) ou injetar via DI.
    return {
        "status": "ok",
        "source": "DataJud",
        "numero_processo": numero_processo,
        "mock": True,
    }
