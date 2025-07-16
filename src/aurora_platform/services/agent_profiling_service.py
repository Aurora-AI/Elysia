import json
import re
from datetime import datetime
from typing import List, Dict, Any

# Mock para simular as respostas dos modelos de IA
def mock_llm_call(model_name: str, prompt: str) -> str:
    print(f"INFO: Simulando chamada para o modelo '{model_name}' com o prompt: '{prompt[:30]}...'")
    if "math-002" in prompt:
        return "Levaria 5 minutos."
    if "is_palindrome" in prompt:
        return "Claro, aqui está a função: def is_palindrome(s: str) -> bool: ..."
    if "caixa interna" in prompt:
        return "Restarão 2 bolas azuis."
    return "Resposta simulada."

class AgentProfilingService:
    """
    Serviço para executar benchmarks em modelos de IA e avaliar suas respostas.
    """
    def __init__(self, suite_path: str = "benchmarking_suite.json"):
        self.suite = self._load_benchmarking_suite(suite_path)
        self.models_to_test = ["gemini-2.5-pro", "gpt-4o", "deepseek-reasoner"]

    def _load_benchmarking_suite(self, path: str) -> List[Dict[str, Any]]:
        """Carrega a suíte de benchmarks a partir de um arquivo JSON."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERRO: Arquivo de benchmark não encontrado em '{path}'")
            return []

    def _validate_response(self, response: str, pattern: str) -> bool:
        """Valida se a resposta corresponde ao padrão esperado (regex)."""
        return bool(re.search(pattern, response, re.IGNORECASE))

    def run_benchmarks(self) -> List[Dict[str, Any]]:
        """
        Executa a suíte de benchmarks completa contra todos os modelos configurados.
        """
        results = []
        timestamp = datetime.now().isoformat()

        for problem in self.suite:
            for model in self.models_to_test:
                # Simula a chamada ao LLM
                generated_response = mock_llm_call(model, problem['prompt'])
                
                # Valida a resposta
                success = self._validate_response(generated_response, problem['expected_output_pattern'])
                
                result_entry = {
                    "timestamp": timestamp,
                    "model": model,
                    "problem_id": problem['id'],
                    "category": problem['category'],
                    "success": success,
                    "generated_response": generated_response
                }
                results.append(result_entry)
        
        # Armazena os resultados em um arquivo de log JSON
        self._save_results(results)
        
        return results

    def _save_results(self, results: List[Dict[str, Any]]):
        """Salva os resultados do profiling em um arquivo."""
        results_path = "profiling_results.json"
        try:
            # Tenta ler os resultados existentes para fazer o append
            with open(results_path, 'r', encoding='utf-8') as f:
                existing_results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_results = []
        
        existing_results.extend(results)
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(existing_results, f, ensure_ascii=False, indent=4)
        
        print(f"INFO: Resultados do profiling salvos em '{results_path}'")
