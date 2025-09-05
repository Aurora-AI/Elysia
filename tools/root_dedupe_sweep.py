#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess as sp
import sys
from pathlib import Path

CANON = Path("src/aurora_platform")
MERGE = Path("src/aurora_platform__merge_candidates")
ROOTS = [
    ("aurora_platform", "aurora_platform_root"),
    ("aurora-core/src/aurora_platform", "aurora_core_src"),
    ("aurora-platform/src/aurora_platform", "aurora_platform_dash_src"),
]


def git(*args: str) -> int:
    return sp.call(["git", *args])


def list_files(root: Path):
    if not root.exists():
        return []
    # git-tracked
    try:
        out = sp.check_output(["git", "ls-files", "-z", str(root)], text=False)
        tracked = [p.decode("utf-8") for p in out.split(b"\x00") if p]
    except Exception:
        tracked = []
    # untracked (non-ignored)
    try:
        out = sp.check_output(
            ["git", "ls-files", "-z", "-o", "--exclude-standard", str(root)], text=False
        )
        untracked = [p.decode("utf-8") for p in out.split(b"\x00") if p]
    except Exception:
        untracked = []
    # keep only files
    files = []
    for p in tracked + untracked:
        if p and Path(p).is_file():
            files.append(p)
    return sorted(set(files))


def ensure_parent(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)


def mv_preserve(src: Path, dst: Path):
    ensure_parent(dst)
    # try git mv; fallback to mv + git add
    if git("mv", src.as_posix(), dst.as_posix()) != 0:
        shutil.move(src.as_posix(), dst.as_posix())
        git("add", "-A")


def sweep_one(root_str: str, label: str) -> int:
    root = Path(root_str)
    if not root.exists():
        print(f"[skip] {root} not found")
        return 0
    files = list_files(root)
    moved = 0
    for f in files:
        p = Path(f)
        if not p.exists():
            continue
        rel = p.relative_to(root)
        dst = MERGE / label / rel
        print(f"[mv] {p} -> {dst}")
        mv_preserve(p, dst)
        moved += 1
    # try remove empty dirs
    from contextlib import suppress

    with suppress(Exception):
        git("rm", "-r", "--ignore-unmatch", root.as_posix())
    return moved


def main():
    if not Path(".git").exists():
        print("Run from repo root", file=sys.stderr)
        sys.exit(2)
    MERGE.mkdir(parents=True, exist_ok=True)
    total = 0
    for root, label in ROOTS:
        total += sweep_one(root, label)
    print(f"[done] moved files: {total}")
    sys.exit(0)


if __name__ == "__main__":
    main()
