"""Logger para gravar execuções de Ordens de Serviço no cortex.db"""
from __future__ import annotations

import logging
import sqlite3
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

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

SQL_INSERT = """
INSERT INTO execution_logs (
    os_id, timestamp_inicio, timestamp_fim, agente_executor, status,
    resumo_execucao, erros_encontrados, resolucao_aplicada, commit_hash,
    commit_message, git_status
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def _default_db_path() -> Path:
    # Resolve repo root by looking for a marker file (pyproject.toml) or by walking
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent / "db" / "cortex.db"
    # Fallback to workspace relative path
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "db" / "cortex.db"


def _get_commit_hash() -> str | None:
    """Try to obtain the current git commit hash for the repository root.

    Returns: commit hash string or None on failure.
    """
    try:
        repo_root = None
        p = Path(__file__).resolve()
        for parent in p.parents:
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                repo_root = parent
                break
        if repo_root is None:
            repo_root = Path(__file__).resolve().parents[3]
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, capture_output=True, text=True
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        logger.debug("Could not obtain commit hash via git", exc_info=True)
    return None


def _get_commit_message() -> str | None:
    try:
        repo_root = None
        p = Path(__file__).resolve()
        for parent in p.parents:
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                repo_root = parent
                break
        if repo_root is None:
            repo_root = Path(__file__).resolve().parents[3]
        res = subprocess.run(["git", "log", "-1", "--pretty=%B"],
                             cwd=repo_root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        logger.debug("Could not obtain commit message via git", exc_info=True)
    return None


def _get_git_status() -> str | None:
    try:
        repo_root = None
        p = Path(__file__).resolve()
        for parent in p.parents:
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                repo_root = parent
                break
        if repo_root is None:
            repo_root = Path(__file__).resolve().parents[3]
        res = subprocess.run(["git", "status", "--porcelain"],
                             cwd=repo_root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        logger.debug("Could not obtain git status via git", exc_info=True)
    return None


def ensure_table(db_path: Path | str | None = None) -> None:
    db = Path(db_path) if db_path else _default_db_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        cur.execute(SQL_CREATE)
        conn.commit()
    finally:
        conn.close()


def _verify_table_schema(conn: sqlite3.Connection) -> None:
    """Ensure the execution_logs table has the expected columns.

    Raises a RuntimeError with a helpful message if required columns are missing.
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info('execution_logs')")
    rows = cur.fetchall()
    # PRAGMA table_info returns rows like (cid, name, type, notnull, dflt_value, pk)
    existing_cols = [r[1] for r in rows]
    expected = [
        "os_id",
        "timestamp_inicio",
        "timestamp_fim",
        "agente_executor",
        "status",
        "resumo_execucao",
        "erros_encontrados",
        "resolucao_aplicada",
        "commit_hash",
        "commit_message",
        "git_status",
    ]
    missing = [c for c in expected if c not in existing_cols]
    if missing:
        raise RuntimeError(
            "cortex DB 'execution_logs' table schema mismatch: missing columns: "
            f"{missing}. Expected at least: {expected}.\n"
            "Please run 'scripts/init_cortex_db.py' or migrate the DB to add the missing columns."
        )


def log_execution(
    os_id: str,
    timestamp_inicio: str,
    timestamp_fim: str,
    agente_executor: str,
    status: str,
    resumo_execucao: str | None = None,
    erros_encontrados: str | None = None,
    resolucao_aplicada: str | None = None,
    commit_hash: str | None = None,
    db_path: str | Path | None = None,
) -> int:
    """Insere um registo na tabela execution_logs.

    Retorna o id da linha inserida.
    """
    db = Path(db_path) if db_path else _default_db_path()
    ensure_table(db)
    # If no commit_hash provided, try to obtain it automatically
    if not commit_hash:
        commit_hash = _get_commit_hash()
    commit_message = _get_commit_message()
    git_status = _get_git_status()
    conn = sqlite3.connect(db)
    try:
        # verify schema before attempting the INSERT to provide a clearer error
        _verify_table_schema(conn)
        cur = conn.cursor()
        cur.execute(
            SQL_INSERT,
            (
                os_id,
                timestamp_inicio,
                timestamp_fim,
                agente_executor,
                status,
                resumo_execucao,
                erros_encontrados,
                resolucao_aplicada,
                commit_hash,
                commit_message,
                git_status,
            ),
        )
        conn.commit()
        rowid = int(cur.lastrowid or 0)
        logger.info("Logged execution %s as id=%s", os_id, rowid)
        return rowid
    except Exception:
        logger.exception("Failed to log execution to cortex DB: %s", db)
        raise
    finally:
        conn.close()


def safe_log_execution(
    os_id: str,
    agente_executor: str = "script",
    status: str = "SUCESSO",
    resumo_execucao: str | None = None,
    erros_encontrados: str | None = None,
    resolucao_aplicada: str | None = None,
    commit_hash: str | None = None,
    db_path: str | Path | None = None,
) -> int | None:
    """A thin, non-raising wrapper around log_execution.

    This helper will attempt to record a simple execution row using current
    UTC timestamps. On failure it logs the error but does not propagate it,
    ensuring scripts can call it in finalizers without changing program flow.
    Returns the inserted row id on success, or None on failure.
    """
    try:
        from datetime import datetime

        now = datetime.utcnow().isoformat() + "Z"
        try:
            return log_execution(
                os_id=os_id,
                timestamp_inicio=now,
                timestamp_fim=now,
                agente_executor=agente_executor,
                status=status,
                resumo_execucao=resumo_execucao,
                erros_encontrados=erros_encontrados,
                resolucao_aplicada=resolucao_aplicada,
                commit_hash=commit_hash,
                db_path=db_path,
            )
        except Exception:
            logger.exception(
                "safe_log_execution: failed to write execution row for %s", os_id)
            return None
    except Exception:
        # protect against any import-time or other unexpected failure
        logger.exception(
            "safe_log_execution: unexpected error preparing log for %s", os_id)
        return None
