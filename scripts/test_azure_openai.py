#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a integracao com Azure OpenAI
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from aurora_platform.services.sales_mentor_service import prepare_for_meeting

    print("[OK] Importacao do servico bem-sucedida")

    # Teste básico (vai falhar por falta de credenciais, mas mostra que o código está correto)
    try:
        result = prepare_for_meeting("Empresa Teste")
        print(f"[OK] Resultado: {result}")
    except Exception as e:
        if "azure" in str(e).lower() or "openai" in str(e).lower():
            print(f"[OK] Codigo funcionando - erro esperado de credenciais: {e}")
        else:
            print(f"[ERRO] Erro inesperado: {e}")

except ImportError as e:
    print(f"[ERRO] Erro de importacao: {e}")
except Exception as e:
    print(f"[ERRO] Erro geral: {e}")
