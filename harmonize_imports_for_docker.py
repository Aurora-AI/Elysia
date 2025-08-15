import os
import sys

# O diretório que contém o código-fonte do aurora-core
# Ajuste se o nome da pasta do serviço for diferente
TARGET_DIR = "aurora-core"


def harmonize_imports():
    """
    Percorre todos os arquivos .py no diretório alvo e substitui
    'from src.aurora_platform' por 'from aurora_platform' e
    'import src.aurora_platform' por 'import aurora_platform'.
    """
    project_root = os.getcwd()
    target_path = os.path.join(project_root, TARGET_DIR)

    if not os.path.isdir(target_path):
        print(f"❌ ERRO: Diretório alvo '{target_path}' não encontrado.")
        sys.exit(1)

    print(f"🤖 Iniciando harmonização de imports no diretório: '{TARGET_DIR}'...")
    files_patched = 0

    for root, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if (
                        "from src.aurora_platform" in content
                        or "import src.aurora_platform" in content
                    ):
                        new_content = content.replace(
                            "from src.aurora_platform", "from aurora_platform"
                        )
                        new_content = new_content.replace(
                            "import src.aurora_platform", "import aurora_platform"
                        )

                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        print(f"  -> ✅ Patch aplicado em: {file_path}")
                        files_patched += 1

                except Exception as e:
                    print(f"  -> ❌ ERRO ao processar o arquivo {file_path}: {e}")

    if files_patched == 0:
        print("✅ Nenhum arquivo precisou de patch. Os imports já estão harmonizados.")
    else:
        print(
            f"\n🚀 Harmonização concluída. {files_patched} arquivo(s) foram atualizados."
        )


if __name__ == "__main__":
    harmonize_imports()
