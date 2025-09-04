#!/usr/bin/env python3
"""Inicializa a base de dados cortex.db e cria a tabela execution_logs."""
import sqlite3
from pathlib import Path

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_id TEXT NOT NULL,
    timestamp_inicio TEXT NOT NULL,
    timestamp_fim TEXT NOT NULL,
    agente_executor TEXT NOT NULL,
    status TEXT NOT NULL,
    resumo_execucao TEXT,
    erros_encontrados TEXT,
    resolucao_aplicada TEXT,
    commit_hash TEXT,
    commit_message TEXT,
    git_status TEXT
);
"""


def init(db_path: Path | None = None) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    db_path = db_path or (repo_root / "db" / "cortex.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(SQL_CREATE)
        conn.commit()
        print(f"cortex DB initialized at: {db_path}")
    finally:
        conn.close()
    # best-effort operational trace
    try:
        from backend.app.core.cortex_logger import safe_log_execution

        safe_log_execution(
            os_id="INIT_CORTEX_DB",
            agente_executor="tool",
            status="SUCESSO",
            resumo_execucao=(f"db_path={db_path}"),
        )
    except Exception:
        pass


if __name__ == "__main__":
    init()
