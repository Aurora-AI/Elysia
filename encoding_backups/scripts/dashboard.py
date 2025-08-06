#!/usr/bin/env python3
# dashboard.py
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

# Configuração da página
st.set_page_config(page_title="Aurora Project Dashboard", page_icon="🚀", layout="wide")


@st.cache_data
def load_project_data():
    """Carrega dados do project_plan.yaml."""
    plan_file = Path("project_plan_structured.yaml")
    if plan_file.exists():
        with open(plan_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"epics": []}


def get_status_color(status):
    """Retorna cor baseada no status."""
    colors = {"A FAZER": "#ff6b6b", "EM PROGRESSO": "#4ecdc4", "CONCLUÍDO": "#45b7d1"}
    return colors.get(status, "#gray")


def main():
    st.title("🚀 Aurora Project Dashboard")
    st.markdown("---")

    # Carregar dados
    data = load_project_data()

    if not data.get("epics"):
        st.error("Nenhum dado encontrado no project_plan.yaml")
        return

    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)

    total_tasks = sum(len(epic["tasks"]) for epic in data["epics"])
    completed_tasks = sum(
        1
        for epic in data["epics"]
        for task in epic["tasks"]
        if task["status"] == "CONCLUÍDO"
    )
    in_progress_tasks = sum(
        1
        for epic in data["epics"]
        for task in epic["tasks"]
        if task["status"] == "EM PROGRESSO"
    )
    todo_tasks = total_tasks - completed_tasks - in_progress_tasks

    with col1:
        st.metric("Total de Tarefas", total_tasks)
    with col2:
        st.metric("Concluídas", completed_tasks)
    with col3:
        st.metric("Em Progresso", in_progress_tasks)
    with col4:
        st.metric("A Fazer", todo_tasks)

    # Progress geral
    if total_tasks > 0:
        overall_progress = (completed_tasks / total_tasks) * 100
        st.progress(overall_progress / 100)
        st.write(f"**Progresso Geral: {overall_progress:.1f}%**")

    st.markdown("---")

    # Épicos e Tarefas
    for epic in data["epics"]:
        st.subheader(f"📋 {epic['name']}")

        # Métricas do épico
        epic_tasks = epic["tasks"]
        epic_completed = sum(1 for task in epic_tasks if task["status"] == "CONCLUÍDO")
        epic_total = len(epic_tasks)
        epic_progress = (epic_completed / epic_total * 100) if epic_total > 0 else 0

        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(epic_progress / 100)
        with col2:
            st.write(f"{epic_progress:.0f}% ({epic_completed}/{epic_total})")

        # Tabela de tarefas
        tasks_data = []
        for task in epic_tasks:
            tasks_data.append(
                {
                    "ID": task["id"],
                    "Nome": task["name"],
                    "Status": task["status"],
                    "Progresso": f"{task['progress_percent']}%",
                }
            )

        if tasks_data:
            df = pd.DataFrame(tasks_data)

            # Aplicar cores baseadas no status
            def color_status(val):
                color = get_status_color(val)
                return f"background-color: {color}; color: white"

            styled_df = df.style.map(color_status, subset=["Status"])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

        st.markdown("---")

    # Rodapé
    st.markdown("### 📊 Dashboard Aurora - Fábrica de IA")
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")


if __name__ == "__main__":
    main()
