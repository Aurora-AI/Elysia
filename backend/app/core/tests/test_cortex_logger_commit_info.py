import sqlite3
import tempfile
from pathlib import Path

from backend.app.core.cortex_logger import ensure_table, log_execution


def test_commit_fields_present():
    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "cortex.db"
        ensure_table(db_path)
        rowid = log_execution(
            os_id="TEST-CHK",
            timestamp_inicio="2025-08-15T00:00:00Z",
            timestamp_fim="2025-08-15T00:00:01Z",
            agente_executor="test-agent",
            status="SUCESSO",
            resumo_execucao="check commit fields",
            db_path=db_path,
        )
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT commit_hash, commit_message, git_status FROM execution_logs WHERE id = ?",
            (rowid,),
        )
        row = cur.fetchone()
        conn.close()
        assert row is not None
        # Fields may be None or empty in CI, but columns should exist
        assert len(row) == 3
