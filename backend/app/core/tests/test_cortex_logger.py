import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

from backend.app.core.cortex_logger import ensure_table, log_execution


def test_log_execution_happy_path():
    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "cortex.db"
        # ensure table creation works
        ensure_table(db_path)
        rowid = log_execution(
            os_id="TEST-001",
            timestamp_inicio="2025-08-15T00:00:00Z",
            timestamp_fim="2025-08-15T00:00:01Z",
            agente_executor="test-agent",
            status="SUCESSO",
            resumo_execucao="teste",
            db_path=db_path,
        )
        assert isinstance(rowid, int) and rowid > 0
        # verify record exists
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT os_id, agente_executor, status FROM execution_logs WHERE id = ?", (rowid,))
        row = cur.fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "TEST-001"


def test_log_execution_invalid_path_raises():
    # Create a dir and remove write permission to simulate permission error
    td = tempfile.mkdtemp()
    try:
        os.chmod(td, 0o500)  # read+execute, no write
        db_path = Path(td) / "cortex.db"
        with pytest.raises(Exception):
            log_execution(
                os_id="TEST-002",
                timestamp_inicio="2025-08-15T00:00:00Z",
                timestamp_fim="2025-08-15T00:00:01Z",
                agente_executor="test-agent",
                status="FALHA",
                resumo_execucao="teste-fail",
                db_path=db_path,
            )
    finally:
        # restore permissions so cleanup can remove it
        try:
            os.chmod(td, 0o700)
        except Exception:
            pass
        try:
            Path(td).rmdir()
        except Exception:
            pass
