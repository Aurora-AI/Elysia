import os
from pathlib import Path

# --- CONFIGURAÇÃO DA ARQUITETURA CANÔNICA ---
# Esta seção define a "fonte da verdade" da nossa arquitetura.
PROJECT_ROOT = Path(__file__).parent.resolve()
EXPECTED_SERVICES = ["aurora-core", "aurora-crawler", "deepseek-r1"]
LEGACY_DIRS = ["apps"]
CONFIG_FILES_IN_ROOT_ONLY = ["pyproject.toml", "poetry.lock", "docker-compose.yml"]
# -------------------------------------------

class ArchitectureAuditor:
    """
    Analisa a estrutura do monorepo Aurora-Plataform em busca de inconsistências.
    """
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.errors = []
        self.warnings = []

    def run_audit(self):
        """Executa todas as verificações de auditoria."""
        print("Iniciando Auditoria de Conformidade Arquitetural...")
        self._check_for_legacy_dirs()
        self._check_for_duplicate_configs()
        self._check_service_structure()
        self._check_for_nested_git_repos()
        self._print_report()

    def _check_for_legacy_dirs(self):
        """Verifica a existência de diretórios legados que deveriam ser removidos."""
        for legacy_dir in LEGACY_DIRS:
            if (self.root / legacy_dir).exists():
                self.errors.append(
                    f"Diretório Legado Encontrado: A pasta '{legacy_dir}' existe na raiz. "
                    f"Seu conteúdo deve ser migrado para um serviço canônico (ex: 'aurora-crawler') e ela deve ser removida."
                )

    def _check_for_duplicate_configs(self):
        """Garante que arquivos de configuração mestres existam apenas na raiz."""
        for config_file in CONFIG_FILES_IN_ROOT_ONLY:
            found_files = list(self.root.glob(f"**/{config_file}"))
            if not (self.root / config_file).exists():
                 self.errors.append(f"Configuração Ausente na Raiz: O arquivo mestre '{config_file}' não foi encontrado na raiz do projeto.")
            elif len(found_files) > 1:
                offending_paths = [str(p.relative_to(self.root)) for p in found_files if p.parent != self.root]
                self.errors.append(
                    f"Configuração Duplicada: O arquivo '{config_file}' foi encontrado fora da raiz. "
                    f"Deve haver apenas uma versão na raiz do projeto. Encontrado em: {', '.join(offending_paths)}"
                )

    def _check_service_structure(self):
        """Verifica se cada serviço esperado tem a estrutura correta."""
        for service in EXPECTED_SERVICES:
            service_path = self.root / service
            if not service_path.is_dir():
                self.warnings.append(f"Serviço Ausente: O diretório para o serviço '{service}' não foi encontrado na raiz.")
                continue

            dockerfile_path = service_path / "Dockerfile"
            if not dockerfile_path.is_file():
                self.errors.append(f"Dockerfile Ausente: O serviço '{service}' não possui um arquivo 'Dockerfile'.")

    def _check_for_nested_git_repos(self):
        """Verifica a existência de repositórios .git aninhados."""
        nested_gits = list(self.root.glob("**/.git"))
        # Filtra para incluir apenas diretórios e ignorar o .git da raiz
        offending_paths = [str(p.parent.relative_to(self.root)) for p in nested_gits if p.is_dir() and p.parent != self.root]
        if offending_paths:
            self.errors.append(
                f"Repositório Git Aninhado: Um diretório '.git' foi encontrado dentro de um subdiretório. "
                f"Isso indica um silo de projeto. Remova os repositórios aninhados em: {', '.join(offending_paths)}"
            )

    def _print_report(self):
        """Imprime o relatório final da auditoria."""
        print("\n--- Relatório de Auditoria da Arquitetura ---")
        if not self.errors and not self.warnings:
            print("\nStatus: 100% CONFORME!")
            print("A estrutura do projeto está perfeitamente alinhada com a Doutrina Aurora.")
            return

        if self.errors:
            print(f"\nERROS CRÍTICOS ENCONTRADOS ({len(self.errors)}):")
            print("   (Estes problemas violam a nossa arquitetura e devem ser corrigidos)")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")

        if self.warnings:
            print(f"\nAVISOS ({len(self.warnings)}):")
            print("   (Estes pontos podem indicar uma configuração incompleta)")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")

        print("\n--- Fim do Relatório ---")


if __name__ == "__main__":
    auditor = ArchitectureAuditor(PROJECT_ROOT)
    auditor.run_audit()
