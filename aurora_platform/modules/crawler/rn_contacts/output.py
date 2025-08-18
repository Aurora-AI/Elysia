from __future__ import annotations

from typing import Dict, Any, Iterable, List, Optional
import csv, json, os, hashlib, datetime as dt


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()


def dedup(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for r in records:
        key = (r.get("email", "").lower(), r.get("page_url", ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def _to_google_contact_row(r: Dict[str, Any]) -> Dict[str, str]:
    """Map internal contact record to Google Contacts CSV fields."""
    name = r.get("name") or ""
    email = r.get("email") or ""
    phone = r.get("phone") or ""
    position = r.get("position") or r.get("role") or ""
    source = r.get("page_url") or r.get("source_url") or ""

    # naive split for given/family name
    given = ""
    family = ""
    if name:
        parts = name.strip().split()
        if len(parts) == 1:
            given = parts[0]
        else:
            given = parts[0]
            family = " ".join(parts[1:])

    return {
        "Name": name,
        "Given Name": given,
        "Family Name": family,
        "E-mail 1 - Value": email,
        "Phone 1 - Value": phone,
        "Organization 1 - Name": "",
        "Organization 1 - Title": position,
        "Notes": f"Contato extraído da fonte: {source}",
    }


def write_google_csv(out_dir: str, records: List[Dict[str, Any]]) -> str:
    """Write Google Contacts compatible CSV to out_dir/processed/google_contacts.csv"""
    proc_dir = os.path.join(out_dir, "processed")
    ensure_dir(proc_dir)
    csv_path = os.path.join(proc_dir, "google_contacts.csv")

    headers = [
        "Name",
        "Given Name",
        "Family Name",
        "E-mail 1 - Value",
        "Phone 1 - Value",
        "Organization 1 - Name",
        "Organization 1 - Title",
        "Notes",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in records:
            row = _to_google_contact_row(r)
            w.writerow(row)

    return csv_path


def write_outputs(base_dir: str, records: List[Dict[str, Any]], meta: Dict[str, Any], mission_name: Optional[str] = None) -> Dict[str, str]:
    """Write outputs in missionized structure.

    If mission_name is provided, outputs will be saved under data/outputs/[mission_name]/rn_contacts_<stamp>/...
    Otherwise base_dir is used as-is.
    """
    ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M")

    if mission_name:
        base_container = os.path.join(base_dir, mission_name)
        ensure_dir(base_container)
        out_base = os.path.join(base_container, f"rn_contacts_{ts}")
    else:
        out_base = base_dir

    ensure_dir(out_base)
    iso_ts = dt.datetime.utcnow().isoformat()
    meta = dict(meta, written_at=iso_ts, total=len(records))

    raw_dir = os.path.join(out_base, "raw")
    ensure_dir(raw_dir)

    jsonl_path = os.path.join(raw_dir, "contacts.jsonl")
    csv_raw_path = os.path.join(raw_dir, "contacts.csv")
    meta_path = os.path.join(out_base, "manifest.json")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if records:
        headers = sorted({k for r in records for k in r.keys()})
        with open(csv_raw_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(records)

    # write google-compatible processed CSV
    google_csv_path = write_google_csv(out_base, records) if records else ""

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return {"jsonl": jsonl_path, "csv": csv_raw_path, "manifest": meta_path, "google_csv": google_csv_path}
