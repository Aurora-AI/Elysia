#!/usr/bin/env python3
# scripts/project_manager.py
import yaml
import argparse
import sys
from pathlib import Path

def load_project_plan():
    """Carrega o arquivo project_plan.yaml."""
    plan_file = Path(__file__).parent.parent / "project_plan.yaml"
    with open(plan_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_project_plan(data):
    """Salva o arquivo project_plan.yaml."""
    plan_file = Path(__file__).parent.parent / "project_plan.yaml"
    with open(plan_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)

def show_status():
    """Exibe o status atual de todos os Sprints e Tarefas."""
    data = load_project_plan()
    
    print("=== STATUS DO PROJETO AURORA ===\n")
    
    for sprint in data.get('sprints', []):
        print(f"[SPRINT] {sprint['id']}: {sprint['name']} [{sprint['status']}]")
        
        for task in sprint.get('tasks', []):
            status_icon = {
                'A FAZER': '[PENDENTE]',
                'EM ANDAMENTO': '[ATIVO]',
                'CONCLUÍDO': '[OK]'
            }.get(task['status'], '[?]')
            
            print(f"  {status_icon} {task['id']}: {task['name']}")
            print(f"     Status: {task['status']} | Progresso: {task['progress_percent']}%")
        print()

def update_task(task_id, progress, status):
    """Atualiza o progresso e status de uma tarefa específica."""
    data = load_project_plan()
    
    task_found = False
    for sprint in data.get('sprints', []):
        for task in sprint.get('tasks', []):
            if task['id'] == task_id:
                task['progress_percent'] = progress
                task['status'] = status
                task_found = True
                break
        if task_found:
            break
    
    if task_found:
        save_project_plan(data)
        print(f"[OK] Tarefa {task_id} atualizada: {status} ({progress}%)")
    else:
        print(f"[ERRO] Tarefa {task_id} não encontrada")
        sys.exit(1)

def show_next_task():
    """Identifica e exibe a próxima tarefa com status 'A FAZER'."""
    data = load_project_plan()
    
    for sprint in data.get('sprints', []):
        if sprint.get('status') == 'EM ANDAMENTO':
            for task in sprint.get('tasks', []):
                if task['status'] == 'A FAZER':
                    print("=== PRÓXIMA TAREFA ===")
                    print(f"Sprint: {sprint['name']}")
                    print(f"Tarefa: {task['id']} - {task['name']}")
                    print(f"Status: {task['status']}")
                    print(f"Progresso: {task['progress_percent']}%")
                    return
    
    print("[SUCESSO] Todas as tarefas foram concluídas!")

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Projeto Aurora")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando status
    subparsers.add_parser('status', help='Exibe o status atual do projeto')
    
    # Comando update
    update_parser = subparsers.add_parser('update', help='Atualiza uma tarefa')
    update_parser.add_argument('--task-id', required=True, help='ID da tarefa')
    update_parser.add_argument('--progress', type=int, required=True, help='Progresso (0-100)')
    update_parser.add_argument('--status', required=True, help='Status da tarefa')
    
    # Comando next
    subparsers.add_parser('next', help='Mostra a próxima tarefa a fazer')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        show_status()
    elif args.command == 'update':
        update_task(args.task_id, args.progress, args.status)
    elif args.command == 'next':
        show_next_task()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()