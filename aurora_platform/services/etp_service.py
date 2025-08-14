import os
from pathlib import Path

class ETPGeneratorService:
    TEMPLATE_PATH = Path("Template ERP/Modelo CGP - Estudo Técnico Preliminar - ETP.pdf")

    def generate_etp(self, data: dict) -> str:
        # 1. Carregar o template PDF (simulação para MVP)
        if not self.TEMPLATE_PATH.exists():
            raise FileNotFoundError(f"Template não encontrado: {self.TEMPLATE_PATH}")
        # 2. Construir prompt para IA (simulação)
        prompt = self._build_prompt(data)
        # 3. Chamar modelo de IA (simulação)
        ia_response = self._call_ia_model(prompt)
        # 4. Processar resposta e formatar documento (simulação)
        return self._format_etp(ia_response)

    def _build_prompt(self, data: dict) -> str:
        return f"Preencha o ETP para o cliente {data['nome_cliente']} com a necessidade: {data['descricao_necessidade']}."

    def _call_ia_model(self, prompt: str) -> str:
        # Aqui você integraria com o modelo real
        return f"[ETP preenchido com base no prompt: {prompt}]"

    def _format_etp(self, ia_response: str) -> str:
        # Para o MVP, retornamos texto simples
        return ia_response
