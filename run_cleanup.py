import os
import shutil
from pathlib import Path

# --- CONFIGURAÇÃO DA ARQUITETURA CANÔNICA ---
PROJECT_ROOT = Path(__file__).parent.resolve()
LEGACY_DIRS_TO_REMOVE = ["apps"]
DUPLICATE_FILES_TO_REMOVE_IN_SERVICES = [
    "pyproject.toml",
    "poetry.lock",
    "docker-compose.yml",
]
NESTED_GIT_DIRS_TO_REMOVE = [
    "aurora-knowledge-base",
    "gpt-oss",
    "aurora-core",
]  # Adicionado aurora-core por segurança
# -------------------------------------------


def run_cleanup():
    """
    Executa um protocolo de limpeza completo para alinhar a estrutura do projeto
    com a arquitetura canônica da Aurora.
    """
    print("Iniciando Protocolo de Saneamento Arquitetural...")

    # AÇÃO 1: Remover diretórios legados
    for legacy_dir in LEGACY_DIRS_TO_REMOVE:
        path_to_remove = PROJECT_ROOT / legacy_dir
        if path_to_remove.is_dir():
            print(f"   -> Removendo diretório legado: '{legacy_dir}'...")
            shutil.rmtree(path_to_remove)
            print(f"   Diretório '{legacy_dir}' removido.")

    # AÇÃO 2: Remover arquivos de configuração duplicados
    for service_dir in os.listdir(PROJECT_ROOT):
        service_path = PROJECT_ROOT / service_dir
        if service_path.is_dir():
            for file_to_remove in DUPLICATE_FILES_TO_REMOVE_IN_SERVICES:
                file_path = service_path / file_to_remove
                if file_path.is_file():
                    print(
                        f"   -> Removendo configuração duplicada: '{file_path.relative_to(PROJECT_ROOT)}'..."
                    )
                    os.remove(file_path)
                    print(f"   Arquivo '{file_path.name}' removido de '{service_dir}'.")

    # AÇÃO 3: Remover repositórios Git aninhados
    for nested_dir in NESTED_GIT_DIRS_TO_REMOVE:
        git_path = PROJECT_ROOT / nested_dir / ".git"
        if git_path.exists() and git_path.is_dir():
            print(f"   -> Removendo repositório Git aninhado em: '{nested_dir}'...")
            shutil.rmtree(git_path)
            print(f"   Repositório '.git' removido de '{nested_dir}'.")

    print("\nProtocolo de Saneamento concluído.")
    print("Por favor, execute o auditor novamente para validar o resultado.")


if __name__ == "__main__":
    run_cleanup()
