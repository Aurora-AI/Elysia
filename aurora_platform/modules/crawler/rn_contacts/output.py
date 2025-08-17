from __future__ import annotations
from typing import Dict, Any, Iterable, List
import csv, json, os, hashlib, datetime as dt

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()

def dedup(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for r in records:
        key = (r.get("email","" ).lower(), r.get("page_url",""))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out

def write_outputs(base_dir: str, records: List[Dict[str, Any]], meta: Dict[str, Any]) -> Dict[str, str]:
    ensure_dir(base_dir)
    ts = dt.datetime.utcnow().isoformat()
    meta = dict(meta, written_at=ts, total=len(records))

    jsonl_path = os.path.join(base_dir, "contacts.jsonl")
    csv_path = os.path.join(base_dir, "contacts.csv")
    meta_path = os.path.join(base_dir, "manifest.json")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if records:
        headers = sorted({k for r in records for k in r.keys()})
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(records)

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return {"jsonl": jsonl_path, "csv": csv_path, "manifest": meta_path}
