import importlib.util
import sqlite3
from pathlib import Path

import pytest

# Compute repo root and load cortex_logger by file path so tests run in any runner
ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location(
    "cortex_logger", str(ROOT / "backend" / "app" /
                         "core" / "cortex_logger.py")
)
cortex_logger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cortex_logger)  # type: ignore


def test_safe_log_execution_success(tmp_path):
    db_file = tmp_path / "cortex.db"

    # monkeypatch the commit/git helpers to avoid calling git
    cortex_logger._get_commit_hash = lambda: "deadbeef"
    cortex_logger._get_commit_message = lambda: "test commit"
    cortex_logger._get_git_status = lambda: ""  # no changes

    rowid = cortex_logger.safe_log_execution(
        os_id="TEST_SUCCESS",
        agente_executor="pytest",
        status="SUCESSO",
        resumo_execucao="test success",
        db_path=str(db_file),
    )

    assert rowid is not None and isinstance(rowid, int)

    # verify row written
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM execution_logs WHERE os_id=?", ("TEST_SUCCESS",))
        count = cur.fetchone()[0]
        assert count == 1
    finally:
        conn.close()


def test_safe_log_execution_handles_exception_and_returns_none(monkeypatch, tmp_path):
    db_file = tmp_path / "cortex.db"

    # force log_execution to raise
    def raise_exc(*args, **kwargs):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr(cortex_logger, "log_execution", raise_exc)

    rowid = cortex_logger.safe_log_execution(
        os_id="TEST_FAIL",
        agente_executor="pytest",
        status="FALHA",
        resumo_execucao="test failure",
        db_path=str(db_file),
    )

    assert rowid is None


if __name__ == "__main__":
    pytest.main([__file__])
