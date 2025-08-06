# scripts/project_manager.py - v2.0 Corrigido para Sprints

import argparse
from pathlib import Path

import yaml

PLAN_FILE = Path(__file__).parent.parent / "project_plan.yaml"


def read_plan():
    """L√™ o arquivo de plano do projeto."""
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_plan(data):
    """Salva os dados de volta no arquivo de plano."""
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def show_status():
    """Exibe o status completo do projeto, organizado por sprints."""
    plan = read_plan()
    print("=== STATUS DO PROJETO AURORA ===")
    # CORRE√á√ÉO: Itera sobre 'sprints', n√£o 'epics'
    for sprint in plan.get("sprints", []):
        sprint_id = sprint.get("id", "N/A")
        sprint_name = sprint.get("name", "N/A")
        sprint_status = sprint.get("status", "N/A")
        print(f"\n--- SPRINT: {sprint_id} - {sprint_name} [{sprint_status}] ---")

        tasks = sprint.get("tasks", [])
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.get("status") == "CONCLU√çDO")

        if total_tasks > 0:
            sprint_progress = (completed_tasks / total_tasks) * 100
            print(
                f"Progresso do Sprint: {sprint_progress:.2f}% ({completed_tasks}/{total_tasks} tarefas conclu√≠das)"
            )

        for task in tasks:
            task_id = task.get("id", "N/A")
            task_name = task.get("name", "N/A")
            task_status = task.get("status", "N/A")
            task_progress = task.get("progress_percent", 0)
            task_epic = task.get("epic", "N/A")
            print(
                f"  - [{task_status}] {task_id}: {task_name} (√âpico: {task_epic}) ({task_progress}%)"
            )


def update_task(task_id_to_update, progress, status):
    """Atualiza o progresso e o status de uma tarefa espec√≠fica."""
    plan = read_plan()
    task_found = False
    # CORRE√á√ÉO: Itera sobre 'sprints' para encontrar a tarefa
    for sprint in plan.get("sprints", []):
        for task in sprint.get("tasks", []):
            if task.get("id") == task_id_to_update:
                if progress is not None:
                    task["progress_percent"] = int(progress)
                if status is not None:
                    task["status"] = status
                task_found = True
                break
        if task_found:
            break

    if task_found:
        save_plan(plan)
        print(f"‚úÖ Tarefa {task_id_to_update} atualizada com sucesso.")
    else:
        print(f"‚ùå Erro: Tarefa com ID '{task_id_to_update}' n√£o encontrada.")


def find_next_task():
    """Encontra a primeira tarefa 'A FAZER' no sprint 'EM ANDAMENTO'."""
    plan = read_plan()
    # CORRE√á√ÉO: Itera sobre 'sprints'
    for sprint in plan.get("sprints", []):
        if sprint.get("status") == "EM ANDAMENTO":
            for task in sprint.get("tasks", []):
                if task.get("status") == "A FAZER":
                    print("\n--- PR√ìXIMA TAREFA NO BACKLOG ---")
                    print(f"  ID: {task.get('id')}")
                    print(f"  SPRINT: {sprint.get('id')} - {sprint.get('name')}")
                    print(f"  NOME: {task.get('name')}")
                    print(f"  STATUS: {task.get('status')}")
                    return
    print(
        "üéâ Todas as tarefas do sprint atual foram conclu√≠das ou n√£o h√° sprints em andamento!"
    )


def main():
    """Fun√ß√£o principal para analisar os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(description="Gerenciador de Projeto Aurora")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comandos
    subparsers.add_parser("status", help="Exibe o status completo do projeto.")

    parser_update = subparsers.add_parser(
        "update", help="Atualiza o status de uma tarefa."
    )
    parser_update.add_argument(
        "--task-id", required=True, help="O ID da tarefa a ser atualizada."
    )
    parser_update.add_argument(
        "--progress", type=int, help="O novo percentual de progresso (0-100)."
    )
    parser_update.add_argument(
        "--status", help="O novo status (ex: EM ANDAMENTO, CONCLU√çDO)."
    )

    subparsers.add_parser("next", help="Mostra a pr√≥xima tarefa a ser feita.")

    args = parser.parse_args()

    if args.command == "status":
        show_status()
    elif args.command == "update":
        update_task(args.task_id, args.progress, args.status)
    elif args.command == "next":
        find_next_task()


if __name__ == "__main__":
    main()
