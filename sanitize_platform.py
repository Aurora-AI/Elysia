#!/usr/bin/env python3
"""
Script de Saneamento da Plataforma Aurora CRM
ID: AUR-PLAT-SAN-002
Descrição: Remove arquivos/diretórios redundantes com base no Relatório de Saneamento v5.0
Requisitos: Python 3.8+, apenas biblioteca padrão
"""

import logging
import os
import shutil
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Lista de artefatos redundantes (baseado no Relatório de Saneamento)
REDUNDANT_PATHS = [
    # Diretórios obsoletos
    "aurora-core/legacy",
    "aurora-crawler",
    "docs/old",
    "experimental",
    "deprecated_scripts",

    # Arquivos duplicados/desatualizados
    "aurora-core/.env.backup",
    "docker-compose.override.yml",
    "config_old.yaml",
    "aurora-dashboard/.env.local",

    # Artefatos temporários
    "temp_logs",
    "*.tmp",
    "*.bak",
    "*.log"
]

def sanitize_platform():
    """Executa o processo de saneamento da plataforma"""
    root_dir = Path.cwd()
    logging.info(f"Iniciando saneamento em: {root_dir}")

    removed_count = 0
    errors = []

    for pattern in REDUNDANT_PATHS:
        try:
            # Processa padrões glob
            if "*" in pattern:
                for path in root_dir.glob(pattern):
                    _remove_path(path)
                    removed_count += 1
            # Processa caminhos específicos
            else:
                path = root_dir / pattern
                if path.exists():
                    _remove_path(path)
                    removed_count += 1
                else:
                    logging.debug(f"Path não encontrado: {pattern}")
        except Exception as e:
            errors.append(f"Falha em {pattern}: {str(e)}")

    # Resultado final
    logging.info(f"\n✅ Saneamento completo! {removed_count} itens removidos.")
    if errors:
        logging.warning("\n⚠️ Erros encontrados:")
        for error in errors:
            logging.error(f"  - {error}")

def _remove_path(path: Path):
    """Remove arquivo/diretório com logging"""
    try:
        if path.is_file():
            os.remove(path)
            logging.info(f"Removido arquivo: {path}")
        elif path.is_dir():
            shutil.rmtree(path)
            logging.info(f"Removido diretório: {path}")
    except PermissionError:
        logging.warning(f"Permissão negada: {path}. Tentando forçar remoção...")
        os.chmod(path, 0o777)
        _remove_path(path)

if __name__ == "__main__":
    # Modo seguro para execuções repetidas
    try:
        sanitize_platform()
    except KeyboardInterrupt:
        logging.warning("\nOperação cancelada pelo usuário")
