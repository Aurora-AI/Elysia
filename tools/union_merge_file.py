#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

CANON_BASE = Path("src/aurora_platform")
MERGE_BASE = Path("src/aurora_platform__merge_candidates")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def uniq_lines(lines):
    seen = set()
    out = []
    for ln in lines:
        k = ln.rstrip()
        if k not in seen:
            seen.add(k)
            out.append(ln)
    return out


def merge_init(canon: str, cand: str) -> str:
    # 1) manter docstring do canônico (se houver)
    doc_re = r'^(?P<doc>(?:[ \t]*[ru]?"""(?:.|\n)*?"""[ \t]*\n)?)'
    m = re.match(doc_re, canon, flags=re.M)
    doc = m.group("doc") if m else ""
    # 2) unir imports (começo do arquivo)
    imp_re = r'^(?:from\s+\S+\s+import\s+[^\n]+|import\s+[^\n]+)\s*$'
    canon_imps = [ln for ln in canon.splitlines(True) if re.match(imp_re, ln)]
    cand_imps = [ln for ln in cand.splitlines(True) if re.match(imp_re, ln)]
    imports = uniq_lines(canon_imps + cand_imps)
    # 3) unir __all__

    def all_items(s: str):
        m = re.search(r'__all__\s*=\s*\[([^\]]*)\]', s, flags=re.S)
        if not m:
            return []
        inner = m.group(1)
        items = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        return [i for i in items if i]
    canon_all = all_items(canon)
    cand_all = all_items(cand)
    all_union = []
    for i in canon_all + cand_all:
        if i not in all_union:
            all_union.append(i)
    all_block = ""
    if all_union:
        all_block = "__all__ = [" + \
            ", ".join(f"'{x}'" for x in all_union) + "]\n"
    # 4) restante do canônico (sem imports/__all__ duplicados)

    def strip_imps_all(s: str) -> str:
        out = []
        skip = False
        for ln in s.splitlines(True):
            if re.match(imp_re, ln):
                continue
            if re.match(r'\s*__all__\s*=', ln):
                skip = True
                continue
            if skip:
                if "]" in ln:
                    skip = False
                continue
            out.append(ln)
        return "".join(out)
    body = strip_imps_all(canon)
    # 5) Montagem
    parts = []
    if doc:
        parts.append(doc if doc.endswith("\n") else doc + "\n")
    if imports:
        parts.append("".join(imports))
    if all_block:
        parts.append(all_block if all_block.endswith(
            "\n") else all_block + "\n")
    parts.append(body if body.endswith("\n") else body + "\n")
    # 6) Comentário de procedência
    parts.append(
        "\n# NOTE: merged imports/__all__ with merge_candidates version\n")
    return "".join(parts)


def merge_api_router(canon: str, cand: str) -> str:
    # Unir linhas com include_router(...) que existam no candidato e não no canônico.
    inc_re = r'^\s*(?:\w+\.)?include_router\s*\('
    canon_incs = [ln for ln in canon.splitlines(True) if re.search(inc_re, ln)]
    cand_incs = [ln for ln in cand.splitlines(True) if re.search(inc_re, ln)]
    extra = [ln for ln in cand_incs if ln not in canon_incs]
    if not extra:
        return canon
    # Append bloco ao final do arquivo
    joined = canon
    if not joined.endswith("\n"):
        joined += "\n"
    joined += "\n# === merged from merge_candidates (extra include_router) ===\n"
    for ln in extra:
        joined += ln if ln.endswith("\n") else ln+"\n"
    return joined


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="ex: aurora_platform_root")
    ap.add_argument("--relpath", required=True, help="ex: api/v1/api.py")
    ap.add_argument("--mode", choices=["init", "api", "raw"], required=True)
    args = ap.parse_args()

    canon_p = CANON_BASE / args.relpath
    cand_p = MERGE_BASE / args.label / args.relpath

    canon = read(canon_p)
    cand = read(cand_p)
    if not cand:
        print(f"[skip] candidate not found: {cand_p}")
        return

    if args.mode == "init":
        merged = merge_init(canon, cand)
    elif args.mode == "api":
        merged = merge_api_router(canon, cand)
    else:
        # fallback conservador: mantém canônico e anexa comentário com caminho do candidato
        merged = canon
        if not merged.endswith("\n"):
            merged += "\n"
        merged += f"\n# NOTE: candidate exists at {cand_p}\n"

    write(canon_p, merged)
    print(f"[merged] {canon_p}  <- {cand_p}")


if __name__ == "__main__":
    main()
