#!/usr/bin/env python3
"""Utility to record an OS execution to the cortex DB from the command line."""
from pathlib import Path
from datetime import datetime
from backend.app.core.cortex_logger import log_execution


def main():
    now = datetime.utcnow().isoformat() + "Z"
    rowid = log_execution(
        os_id="MANUAL-001",
        timestamp_inicio=now,
        timestamp_fim=now,
        agente_executor="cli",
        status="SUCESSO",
        resumo_execucao="Registro manual via script",
    )
    print("Inserted row id:", rowid)


if __name__ == "__main__":
    main()
