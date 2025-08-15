from __future__ import annotations
import json
import re
from datetime import datetime
from typing import Any, Dict, List
from collections import defaultdict


def mock_llm_call(model_name: str, prompt: str) -> str:
    if "math-002" in prompt:
        return "Levaria 5 minutos."
    return "Resposta simulada."


class AgentProfilingService:
    """Simplified profiling service used in tests and dev."""

    def __init__(self, suite_path: str = "benchmarking_suite.json"):
        self.suite = self._load_benchmarking_suite(suite_path)
        self.models_to_test = ["gemini-2.5-pro", "gpt-4o", "deepseek-reasoner"]

    def _load_benchmarking_suite(self, path: str) -> List[Dict[str, Any]]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _validate_response(self, response: str, pattern: str) -> bool:
        if not pattern:
            return True
        return bool(re.search(pattern, response, re.IGNORECASE))

    def run_benchmarks(self, temperatures: List[float] | None = None) -> List[Dict[str, Any]]:
        import time

        if temperatures is None:
            temperatures = [0.1, 0.5, 0.9]

        results: List[Dict[str, Any]] = []
        timestamp = datetime.now().isoformat()

        for problem in self.suite:
            for model in self.models_to_test:
                for temp in temperatures:
                    start = time.time()
                    resp = mock_llm_call(model, problem.get("prompt", ""))
                    latency = time.time() - start
                    token_cost = len(problem.get(
                        "prompt", "").split()) + len(resp.split())
                    success = self._validate_response(
                        resp, problem.get("expected_output_pattern", ""))
                    results.append({
                        "timestamp": timestamp,
                        "model": model,
                        "problem_id": problem.get("id"),
                        "category": problem.get("category"),
                        "success": success,
                        "generated_response": resp,
                        "temperature": temp,
                        "latency": latency,
                        "token_cost": token_cost,
                    })

        self._save_results(results)
        return results

    def generate_performance_report(self, results_path: str = "profiling_results.json") -> str:
        try:
            with open(results_path, "r", encoding="utf-8") as f:
                results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Nenhum resultado encontrado."

        report = "# Relatório de Faixa de Performance dos Modelos\n\n"
        modelos: dict[str, list] = defaultdict(list)
        for r in results:
            modelos[r.get("model")].append(r)

        for model, entradas in modelos.items():
            report += f"## Modelo: {model}\n"
            categorias: dict[str, list] = defaultdict(list)
            for e in entradas:
                categorias[e.get("category")].append(e)
            for cat, lista in categorias.items():
                report += f"### Categoria: {cat}\n"
                if not lista:
                    continue
                latencias = [entry.get("latency", 0) for entry in lista if entry.get(
                    "latency") is not None]
                custos = [entry.get("token_cost", 0) for entry in lista if entry.get(
                    "token_cost") is not None]
                success_count = sum(
                    1 for entry in lista if entry.get("success"))
                total = len(lista)
                temps = sorted({str(entry.get("temperature"))
                               for entry in lista if entry.get("temperature") is not None})
                report += f"- Total de testes: {total}\n"
                report += f"- Sucesso: {success_count}/{total}\n"
                if latencias:
                    report += f"- Latência média: {sum(latencias)/len(latencias):.2f}s\n"
                if custos:
                    report += f"- Custo médio em tokens: {sum(custos)/len(custos):.1f}\n"
                if temps:
                    report += f"- Temperaturas testadas: {', '.join(temps)}\n"
                report += "\n"

        return report

    def _save_results(self, results: List[Dict[str, Any]]):
        results_path = "profiling_results.json"
        try:
            with open(results_path, "r", encoding="utf-8") as f:
                existing_results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_results = []

        existing_results.extend(results)

        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(existing_results, f, ensure_ascii=False, indent=4)
