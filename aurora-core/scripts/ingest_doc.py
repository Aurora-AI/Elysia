#!/usr/bin/env python3
import os
import sys
import argparse
from aurora_platform.modules.crawler.pipeline import run_ingestion, save_record
from aurora_platform.modules.crawler.ingestion.loaders import DoclingLoader, HTMLLoader


WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(WORKSPACE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a document (PDF/HTML) into normalized markdown + chunks.")
    parser.add_argument("--path", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--tags", default="")
    args = parser.parse_args()

    ext = os.path.splitext(args.path)[1].lower()
    if ext == ".pdf":
        bundle = DoclingLoader.load(args.path)
        media = "pdf"
    elif ext in {".html", ".htm"}:
        bundle = HTMLLoader.load_from_file(args.path)
        media = "html"
    else:
        raise SystemExit(f"Unsupported file type: {ext}")

    tags = {}
    if args.tags:
        for kv in args.tags.split(","):
            if not kv.strip():
                continue
            if "=" in kv:
                k, v = kv.split("=", 1)
                tags[k.strip()] = v.strip()
            else:
                tags[kv.strip()] = True

    record = run_ingestion(bundle.content, media, args.source, tags)
    out = save_record(record)
    print(out)


if __name__ == "__main__":
    main()
