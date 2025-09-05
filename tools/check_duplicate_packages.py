#!/usr/bin/env python3
"""
Quick duplicate-root checker for aurora_platform.

Exit codes:
 - 0: OK (only src/aurora_platform exists)
 - 1: error (missing canonical root or alternative roots exist)
 - 2: duplicates detected (same files exist in multiple roots)
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VALID_ROOT = REPO / "src" / "aurora_platform"

CANDIDATES = [
    REPO / "src" / "aurora_platform",
    REPO / "aurora_platform",
    REPO / "aurora-core" / "src" / "aurora_platform",
    REPO / "aurora-platform" / "src" / "aurora_platform",
]


def list_python_files(base: Path) -> set[Path]:
    if not base.exists():
        return set()
    return {p.relative_to(base) for p in base.rglob("*.py")}


def main() -> int:
    print("== Aurora duplicate package check ==")
    for base in CANDIDATES:
        status = "OK" if base.exists() else "missing"
        print(f"[scan] {base.relative_to(REPO)} -> {status}")

    # Map file -> origins
    seen: dict[Path, set[str]] = defaultdict(set)
    for base in CANDIDATES:
        files = list_python_files(base)
        for f in files:
            seen[f].add(str(base))

    duplicates = {f: bases for f, bases in seen.items() if len(bases) > 1}
    if duplicates:
        print("\n[FAIL] Duplicates detected:")
        for f, bases in sorted(duplicates.items()):
            bases_s = ", ".join(sorted(bases))
            print(f" - {f}: {bases_s}")
        print(
            "\nSugestão: consolidar tudo em src/aurora_platform "
            "e mover versões conflitantes para src/aurora_platform__merge_candidates/"
        )
        return 2

    if not VALID_ROOT.exists():
        print(f"[ERR] Raiz canônica ausente: {VALID_ROOT}")
        return 1

    others = [p for p in CANDIDATES if p.exists() and p.resolve() != VALID_ROOT.resolve()]
    if others:
        print("\n[ERR] Encontradas raízes alternativas de aurora_platform:")
        for p in others:
            print(f"  - {p}")

        # operational trace (non-fatal)
        try:
            from backend.app.core.cortex_logger import safe_log_execution

            safe_log_execution(
                os_id="CHECK_DUP_PKGS",
                agente_executor="tool",
                status="ERRO",
                resumo_execucao=(f"others={len(others)}"),
            )
        except Exception:
            pass
        return 1

    print("\n[PASS] No duplicates found across candidate roots.")

    # operational trace (non-fatal)
    try:
        from backend.app.core.cortex_logger import safe_log_execution

        safe_log_execution(
            os_id="CHECK_DUP_PKGS",
            agente_executor="tool",
            status="SUCESSO",
            resumo_execucao="no_duplicates",
        )
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
