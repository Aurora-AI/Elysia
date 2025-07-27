# alembic/env.py - Versão Definitiva com Correção de Caminho e Tipagem

import sys
from logging.config import fileConfig
from pathlib import Path
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool

from alembic import context

# --- CORREÇÃO DE CAMINHO ---
# Adiciona o diretório raiz do projeto (que contém a pasta 'src')
# ao caminho de busca do Python. Isso deve ser feito ANTES de qualquer
# importação de módulos do nosso projeto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
# --- FIM DA CORREÇÃO ---

# Agora que o caminho está correto, podemos importar nossos módulos
from src.aurora_platform.core.config import settings  # noqa: E402

# Importe aqui todos os seus modelos para que o Alembic os reconheça.
# Isso garante que eles sejam registrados no metadata do SQLModel.

# Esta é a configuração do Alembic que lê o alembic.ini
config = context.config

# Interpreta o arquivo de configuração para logging do Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- CORREÇÃO PARA SecretStr ---
# Extrai o valor da string de SecretStr de forma segura.
# Usar .get_secret_value() é crucial para obter a URL real.
db_url_str = settings.DATABASE_URL.get_secret_value()

# Garante que a URL do banco de dados use a codificação correta
if "client_encoding" not in db_url_str:
    separator = "?" if "?" not in db_url_str else "&"
    db_url_str += f"{separator}client_encoding=utf8"

# Define a URL no contexto do Alembic, sobrescrevendo a do alembic.ini
config.set_main_option("sqlalchemy.url", db_url_str)
# --- FIM DA CORREÇÃO ---

# Define o target_metadata para que o 'autogenerate' funcione
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # --- CORREÇÃO PARA ACESSO DE ATRIBUTO ---
    # Pylance pode ter dificuldade em analisar estaticamente o objeto `config`.
    # Usamos getattr para acessar com segurança o nome da seção principal.
    main_section_name = getattr(config, "config_main_section", "alembic")
    connectable = engine_from_config(
        config.get_section(main_section_name, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # --- FIM DA CORREÇÃO ---
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
