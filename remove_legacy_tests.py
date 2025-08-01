import os

# Diretório base dos testes
TESTS_DIR = "tests"

# Lista branca dos testes CORE que devem permanecer
CORE_TESTS = {
    "test_qdrant_adapter.py",
    "test_knowledge_service_qdrant.py",
    "test_pipeline.py",
    "test_orchestrator.py",
}


def remove_non_core_tests(base_dir, core_tests):
    removed = []
    for root, dirs, files in os.walk(base_dir, topdown=False):
        # Remove arquivos de teste não-core
        for file in files:
            if (
                file.startswith("test_")
                and file.endswith(".py")
                and file not in core_tests
            ):
                full_path = os.path.join(root, file)
                os.remove(full_path)
                removed.append(full_path)
        # Remove diretórios vazios (ex: unit, integration)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                removed.append(dir_path)
    return removed


if __name__ == "__main__":
    removed = remove_non_core_tests(TESTS_DIR, CORE_TESTS)
    print("Arquivos e pastas removidos:")
    for path in removed:
        print(f" - {path}")
