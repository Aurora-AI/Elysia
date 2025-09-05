#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

CANON = Path("src/aurora_platform")
MERGE = Path("src/aurora_platform__merge_candidates")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_under_label(p: Path) -> Path:
    # p: MERGE/<label>/.../<path>
    # retorna a parte após <label>/ (isto é, o caminho relativo do pacote)
    parts = p.relative_to(MERGE).parts
    # parts[0] é o label de origem (ex.: aurora_platform_root)
    return Path(*parts[1:]) if len(parts) > 1 else Path()


def collect() -> list[dict]:
    items: list[dict] = []
    if not MERGE.exists():
        return items
    for file in MERGE.rglob("*"):
        if file.is_file():
            rel = rel_under_label(file)
            canon = CANON / rel
            entry = {
                "label": file.relative_to(MERGE).parts[0] if file.relative_to(MERGE).parts else "",
                "merge_path": str(file),
                "relpath": str(rel),
                "canon_path": str(canon),
                "exists_in_canon": canon.exists(),
                "merge_sha": sha256(file),
                "canon_sha": sha256(canon) if canon.exists() else None,
                "size_merge": file.stat().st_size,
                "size_canon": canon.stat().st_size if canon.exists() else None,
            }
            if not entry["exists_in_canon"]:
                # só existe no merge_candidates
                entry["status"] = "NEW_ONLY"
            else:
                entry["status"] = (
                    "DUP_IDENT" if entry["merge_sha"] == entry["canon_sha"] else "DUP_DIFF"
                )
            items.append(entry)
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-json", default="artifacts/merge_triage.json")
    ap.add_argument("--report-md", default="artifacts/merge_triage.md")
    ap.add_argument(
        "--apply-delete-identical",
        action="store_true",
        help=(
            "Remove do git os arquivos em MERGE que são idênticos "
            "aos da árvore canônica (DUP_IDENT)."
        ),
    )
    ap.add_argument(
        "--apply-adopt-new",
        action="store_true",
        help="Move (git mv) arquivos NEW_ONLY do MERGE para a árvore canônica.",
    )
    args = ap.parse_args()

    Path("artifacts").mkdir(exist_ok=True)
    items = collect()

    # Relatórios
    with open(args.report_json, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # MD resumido
    counts = {"NEW_ONLY": 0, "DUP_IDENT": 0, "DUP_DIFF": 0}
    for it in items:
        counts[it["status"]] = counts.get(it["status"], 0) + 1
    with open(args.report_md, "w", encoding="utf-8") as f:
        f.write("# Merge Candidates — Triagem\n\n")
        f.write(f"- NEW_ONLY: {counts.get('NEW_ONLY',0)}\n")
        f.write(f"- DUP_IDENT: {counts.get('DUP_IDENT',0)}\n")
        f.write(f"- DUP_DIFF: {counts.get('DUP_DIFF',0)}\n\n")
        f.write("## Amostras\n")
        for it in items[:50]:
            f.write(f"- {it['status']} — `{it['relpath']}` (label: {it['label']})\n")

    print(f"[info] Relatórios em: {args.report_json} e {args.report_md}")

    # Ações opcionais
    if args.apply_delete_identical:
        to_delete = [Path(it["merge_path"]) for it in items if it["status"] == "DUP_IDENT"]
        for p in to_delete:
            # usar git rm se possível
            os.system(f'git rm -f "{p.as_posix()}"')
        print(f"[apply] Removidos (DUP_IDENT): {len(to_delete)}")

    if args.apply_adopt_new:
        to_move = [it for it in items if it["status"] == "NEW_ONLY"]
        for it in to_move:
            src = Path(it["merge_path"])
            dst = Path(it["canon_path"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.system(f'git mv "{src.as_posix()}" "{dst.as_posix()}"')
        print(f"[apply] Adotados (NEW_ONLY -> canônico): {len(to_move)}")

        # Operational trace (non-blocking)
        try:
            from backend.app.core.cortex_logger import safe_log_execution

            safe_log_execution(
                os_id="TRIAGE_MERGE_CANDIDATES",
                agente_executor="tool",
                status="SUCESSO",
                resumo_execucao=(
                    f"items={len(items)} new_only={counts.get('NEW_ONLY', 0)} "
                    f"dup_ident={counts.get('DUP_IDENT', 0)} "
                    f"dup_diff={counts.get('DUP_DIFF', 0)}"
                ),
            )
        except Exception:
            # already non-fatal by design
            pass


if __name__ == "__main__":
    main()
