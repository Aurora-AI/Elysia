#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import sys

# Pastas que podem conter o pacote (ajuste se necessário)
CANDIDATES = [
    Path("src/aurora_platform"),
    Path("aurora_platform"),
    Path("aurora-core/src/aurora_platform"),
    Path("aurora-platform/src/aurora_platform"),
]


def list_python_files(base: Path):
    if not base.exists():
        return set()
    return {p.relative_to(base) for p in base.rglob("*.py")}


def main():
    seen = defaultdict(set)
    for base in CANDIDATES:
        files = list_python_files(base)
        for f in files:
            seen[f].add(str(base))

    duplicates = {f: bases for f, bases in seen.items() if len(bases) > 1}

    print("== Aurora duplicate package check ==")
    for base in CANDIDATES:
        print(f"[scan] {base} -> {'OK' if base.exists() else 'missing'}")

    if duplicates:
        print("\n[FAIL] Duplicates detected:")
        for f, bases in sorted(duplicates.items()):
            bases_s = ", ".join(sorted(bases))
            print(f" - {f}: {bases_s}")
        print("\nSugestão: consolidar tudo em src/aurora_platform e mover versões conflitantes para src/aurora_platform__merge_candidates/")
        sys.exit(2)
    else:
        print("\n[PASS] No duplicates found across candidate roots.")
        sys.exit(0)


if __name__ == "__main__":
    main()
