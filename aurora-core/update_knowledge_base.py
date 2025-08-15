import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS_DIR = os.path.join(BASE_DIR, "knowledge-base", "errors")
TECH_DIR = os.path.join(BASE_DIR, "knowledge-base", "technologies")
README_PATH = os.path.join(BASE_DIR, "README.md")

ERROR_TEMPLATE = os.path.join(BASE_DIR, "knowledge-base", "template-error.md")
TECH_TEMPLATE = os.path.join(BASE_DIR, "knowledge-base", "template-technology.md")

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "knowledge-base", "update_knowledge_base.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def register_error(description, stacktrace, solution, refs=None):
    try:
        now = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"error-{now}.md"
        path = os.path.join(ERRORS_DIR, filename)
        with open(ERROR_TEMPLATE) as f:
            template = f.read()
        content = template.replace(
            "YYYY-MM-DD HH:MM", datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        content = content.replace("- **Descrição:**", f"- **Descrição:** {description}")
        content = content.replace(
            "- **Stacktrace:**", f"- **Stacktrace:** {stacktrace}"
        )
        content = content.replace(
            "- **Solução Aplicada:**", f"- **Solução Aplicada:** {solution}"
        )
        content = content.replace(
            "- **Referências:**", f"- **Referências:** {refs or '-'}"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Registro de erro criado: {filename}")
        update_readme()
    except Exception as e:
        logging.error(f"Erro ao registrar erro: {e}")


def document_technology(name, version, description, commands, links):
    try:
        filename = f"{name.lower()}.md"
        path = os.path.join(TECH_DIR, filename)
        with open(TECH_TEMPLATE) as f:
            template = f.read()
        content = template.replace("- **Nome:**", f"- **Nome:** {name}")
        content = content.replace("- **Versão:**", f"- **Versão:** {version}")
        content = content.replace("- **Descrição:**", f"- **Descrição:** {description}")
        content = content.replace(
            "- **Principais comandos:**",
            "- **Principais comandos:**\n  - " + "\n  - ".join(commands),
        )
        content = content.replace(
            "- **Links úteis:**", "- **Links úteis:**\n  - " + "\n  - ".join(links)
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Documentação de tecnologia criada: {filename}")
        update_readme()
    except Exception as e:
        logging.error(f"Erro ao documentar tecnologia: {e}")


def update_readme():
    try:
        error_files = sorted(os.listdir(ERRORS_DIR))
        tech_files = sorted(os.listdir(TECH_DIR))
        lines = ["# Índice da Base de Conhecimento\n", "## Erros\n"]
        for ef in error_files:
            lines.append(f"- [Erro: {ef}](/knowledge-base/errors/{ef})\n")
        lines.append("\n## Tecnologias\n")
        for tf in tech_files:
            lines.append(f"- [Tecnologia: {tf}](/knowledge-base/technologies/{tf})\n")
        with open(README_PATH, "a", encoding="utf-8") as f:
            f.writelines(lines)
        logging.info("README.md atualizado com índice da base de conhecimento")
    except Exception as e:
        logging.error(f"Erro ao atualizar README.md: {e}")


# Estrutura para integração futura
# def integrate_with_external_system(data):
#     # Exemplo: enviar para API, webhook, etc.
#     pass
