import ast
import os
from pathlib import Path

import toml

# --- Configuração ---
SRC_DIRECTORY = "src"
PYPROJECT_FILE = "pyproject.toml"
PROJECT_ROOT_PACKAGE = "aurora_platform"  # Nome do pacote principal em 'src'
# --------------------

# Lista de bibliotecas padrão do Python para ignorar
STANDARD_LIBS = {
    "abc",
    "argparse",
    "ast",
    "asyncio",
    "base64",
    "collections",
    "contextlib",
    "datetime",
    "enum",
    "functools",
    "hashlib",
    "io",
    "json",
    "logging",
    "math",
    "multiprocessing",
    "os",
    "pathlib",
    "re",
    "shutil",
    "subprocess",
    "sys",
    "tempfile",
    "time",
    "typing",
    "uuid",
    "warnings",
}

# Mapeamento de nomes de import para nomes de pacotes PyPI
IMPORT_TO_PACKAGE_MAP = {
    "fitz": "PyMuPDF",
    "jose": "python-jose",
    "dotenv": "python-dotenv",
    "google.auth": "google-auth",
    "google.api_core": "google-api-core",
}


def get_declared_dependencies(pyproject_path):
    """Lê o pyproject.toml e extrai todas as dependências declaradas."""
    try:
        data = toml.load(pyproject_path)
        # Unifica dependências principais e de desenvolvimento
        deps = set(
            data.get("tool", {}).get("poetry", {}).get("dependencies", {}).keys()
        )
        dev_deps = set(
            data.get("tool", {})
            .get("poetry", {})
            .get("group", {})
            .get("dev", {})
            .get("dependencies", {})
            .keys()
        )

        # Normaliza nomes (ex: sentry-sdk[fastapi] -> sentry-sdk)
        normalized_deps = {dep.split("[")[0] for dep in deps.union(dev_deps)}
        return normalized_deps
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo '{PYPROJECT_FILE}': {e}")
        return None


def find_imports(start_path):
    """Encontra todos os pacotes de alto nível importados nos arquivos .py."""
    imported_modules = set()
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=str(file_path))
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported_modules.add(alias.name.split(".")[0])
                            elif isinstance(node, ast.ImportFrom):
                                if (
                                    node.module and node.level == 0
                                ):  # Apenas imports absolutos
                                    imported_modules.add(node.module.split(".")[0])
                    except Exception:
                        pass  # Ignora erros de parsing em arquivos incompletos
    return imported_modules


def main():
    print("--- 🔍 Iniciando Verificador de Dependências da Aurora (v2) ---")
    declared_deps = get_declared_dependencies(Path(PYPROJECT_FILE))

    if declared_deps is None:
        return

    imported_modules = find_imports(SRC_DIRECTORY)

    # Filtra bibliotecas padrão, o próprio projeto e as já declaradas
    missing_deps_imports = (
        imported_modules - declared_deps - STANDARD_LIBS - {PROJECT_ROOT_PACKAGE}
    )

    # Converte nomes de import para nomes de pacotes PyPI
    missing_packages = {
        IMPORT_TO_PACKAGE_MAP.get(imp, imp) for imp in missing_deps_imports
    }

    if not missing_packages:
        print("\n✅ SUCESSO! Todas as dependências externas parecem estar declaradas.")
    else:
        print("\n🚨 ALERTA! Dependências ausentes encontradas:")
        print(
            "As seguintes bibliotecas são importadas no código, mas não estão no 'pyproject.toml':"
        )
        for pkg in sorted(list(missing_packages)):
            print(f"  - {pkg}")

        print("\n👉 Ação Recomendada:")
        print("Execute o seguinte comando para adicioná-las:")
        print(f'\npoetry add {" ".join(sorted(list(missing_packages)))}')

    print("\n--- Verificação Concluída ---")


if __name__ == "__main__":
    main()
