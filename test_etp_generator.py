#!/usr/bin/env python3
"""Teste do Gerador de ETP."""

import requests
import json

def test_etp_generation():
    """Testa geração de ETP via API."""
    
    api_url = "http://127.0.0.1:8000/api/v1/etp/generate"
    
    # Dados de teste para ETP
    etp_data = {
        "objeto_licitacao": "Contratação de serviços de consultoria em logística para otimização de processos administrativos",
        "valor_estimado": 150000.00,
        "justificativa": "Necessidade de modernização dos processos logísticos do órgão, visando maior eficiência e redução de custos operacionais, conforme diretrizes da Rede Logística do Estado.",
        "modalidade_sugerida": "Concorrência Pública"
    }
    
    print("[TESTE] Gerando ETP com dados da Rede Log RJ...")
    print(f"Objeto: {etp_data['objeto_licitacao']}")
    print(f"Valor: R$ {etp_data['valor_estimado']:,.2f}")
    
    try:
        response = requests.post(
            api_url,
            json=etp_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            etp_document = response.text
            print("\n" + "="*80)
            print("ESTUDO TÉCNICO PRELIMINAR GERADO:")
            print("="*80)
            print(etp_document)
            print("="*80)
            
            # Salvar ETP gerado
            with open("etp_gerado.txt", "w", encoding="utf-8") as f:
                f.write(etp_document)
            print("\n[OK] ETP salvo em 'etp_gerado.txt'")
            
        else:
            print(f"[ERRO] Falha na geração: {response.text}")
            
    except Exception as e:
        print(f"[ERRO] {e}")

if __name__ == "__main__":
    test_etp_generation()