import json
import re
from datetime import datetime
from typing import List, Dict, Any


# Mock para simular as respostas dos modelos de IA
def mock_llm_call(model_name: str, prompt: str) -> str:
    print(
        f"INFO: Simulando chamada para o modelo '{model_name}' com o prompt: '{prompt[:30]}...'"
    )
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
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERRO: Arquivo de benchmark não encontrado em '{path}'")
            return []

    def _validate_response(self, response: str, pattern: str) -> bool:
        """Valida se a resposta corresponde ao padrão esperado (regex)."""
        return bool(re.search(pattern, response, re.IGNORECASE))

    def run_benchmarks(self, temperatures=[0.1, 0.5, 0.9]) -> List[Dict[str, Any]]:
        """
        Executa a suíte de benchmarks completa contra todos os modelos configurados, variando parâmetros.
        """
        import time

        results = []
        timestamp = datetime.now().isoformat()

        for problem in self.suite:
            # Ignora problemas de decomposição aqui
            if problem.get("category") == "tarefa_decomponivel":
                continue
            for model in self.models_to_test:
                for temp in temperatures:
                    start = time.time()
                    generated_response = mock_llm_call(model, problem["prompt"])
                    latency = time.time() - start
                    # Simulação de custo em tokens
                    token_cost = len(problem["prompt"].split()) + len(
                        generated_response.split()
                    )
                    success = self._validate_response(
                        generated_response, problem["expected_output_pattern"]
                    )
                    result_entry = {
                        "timestamp": timestamp,
                        "model": model,
                        "problem_id": problem["id"],
                        "category": problem["category"],
                        "success": success,
                        "generated_response": generated_response,
                        "temperature": temp,
                        "latency": latency,
                        "token_cost": token_cost,
                    }
                    results.append(result_entry)
        self._save_results(results)
        return results

    def run_decomposition_benchmark(self) -> List[Dict[str, Any]]:
        """
        Executa benchmarks para problemas de decomposição de tarefas.
        """
        import time

        results = []
        timestamp = datetime.now().isoformat()
        for problem in self.suite:
            if problem.get("category") != "tarefa_decomponivel":
                continue
            for model in self.models_to_test:
                # Executa o prompt pai
                start = time.time()
                resp_pai = mock_llm_call(model, problem["prompt_pai"])
                latency_pai = time.time() - start
                token_cost_pai = len(problem["prompt_pai"].split()) + len(
                    resp_pai.split()
                )
                result_entry_pai = {
                    "timestamp": timestamp,
                    "model": model,
                    "problem_id": problem["id"],
                    "category": problem["category"],
                    "subtask": "pai",
                    "generated_response": resp_pai,
                    "latency": latency_pai,
                    "token_cost": token_cost_pai,
                }
                results.append(result_entry_pai)
                # Executa prompts filhos
                for filho in problem.get("prompts_filhos", []):
                    start = time.time()
                    resp_filho = mock_llm_call(model, filho["prompt"])
                    latency_filho = time.time() - start
                    token_cost_filho = len(filho["prompt"].split()) + len(
                        resp_filho.split()
                    )
                    result_entry_filho = {
                        "timestamp": timestamp,
                        "model": model,
                        "problem_id": problem["id"],
                        "category": filho["category"],
                        "subtask": filho["subtask_id"],
                        "generated_response": resp_filho,
                        "latency": latency_filho,
                        "token_cost": token_cost_filho,
                    }
                    results.append(result_entry_filho)
        self._save_results(results)
        return results

    def generate_performance_report(self, results_path="profiling_results.json") -> str:
        """
        Gera um relatório em Markdown sobre a faixa de performance ótima dos modelos.
        """
        try:
            with open(results_path, "r", encoding="utf-8") as f:
                results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Nenhum resultado encontrado."
        # Agrupa por modelo e categoria
        from collections import defaultdict

        report = "# Relatório de Faixa de Performance dos Modelos\n\n"
        modelos = defaultdict(list)
        for r in results:
            modelos[r["model"]].append(r)
        for model, entradas in modelos.items():
            report += f"## Modelo: {model}\n"
            categorias = defaultdict(list)
            for e in entradas:
                categorias[e["category"]].append(e)
                for cat, lista in categorias.items():
                    report += f"### Categoria: {cat}\n"
                    # Faixa ótima: menor latência e maior sucesso
                    if lista:
                        latencias = [log_entry["latency"] for log_entry in lista if "latency" in log_entry]
                        custos = [log_entry["token_cost"] for log_entry in lista if "token_cost" in log_entry]
                        success_count = sum(1 for log_entry in lista if log_entry.get("success"))
                        total = len(lista)
                        temp_usados = set(
                            str(log_entry.get("temperature")) for log_entry in lista if "temperature" in log_entry
                        )
                        report += f"- Total de testes: {total}\n"
                        report += f"- Sucesso: {success_count}/{total}\n"
                        if latencias:
                            report += (
                                f"- Latência média: {sum(latencias)/len(latencias):.2f}s\n"
                            )
                        if custos:
                            report += (
                                f"- Custo médio em tokens: {sum(custos)/len(custos):.1f}\n"
                            )
                        if temp_usados:
                            report += f"- Temperaturas testadas: {', '.join(temp_usados)}\n"
                        report += "\n"
        return report

    def _save_results(self, results: List[Dict[str, Any]]):
        """Salva os resultados do profiling em um arquivo."""
        results_path = "profiling_results.json"
        try:
            # Tenta ler os resultados existentes para fazer o append
            with open(results_path, "r", encoding="utf-8") as f:
                existing_results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_results = []

        existing_results.extend(results)

        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(existing_results, f, ensure_ascii=False, indent=4)

        print(f"INFO: Resultados do profiling salvos em '{results_path}'")
