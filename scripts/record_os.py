#!/usr/bin/env python3
"""Utility to record an OS execution to the cortex DB from the command line."""

from backend.app.core.cortex_logger import safe_log_execution


def main():
    rowid = safe_log_execution(
        os_id="MANUAL-001",
        agente_executor="cli",
        status="SUCESSO",
        resumo_execucao="Registro manual via script",
    )
    print("Inserted row id:", rowid)


if __name__ == "__main__":
    main()
