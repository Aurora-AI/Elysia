"""Minimal CLI for the crawler module (Fase 9 skeleton)."""
from pathlib import Path
import argparse
from .pipeline import run_ingestion


def main():
    p = argparse.ArgumentParser(prog="aurora-crawler")
    p.add_argument("--path", dest="source", required=True,
                   help="File path or URL to ingest")
    p.add_argument(
        "--media", dest="media", choices=["auto", "html", "pdf", "docx"], default="auto"
    )
    p.add_argument("--out", dest="out", required=False)
    args = p.parse_args()
    source = args.source
    media = args.media
    out = args.out
    # If source is a file, read content and use pipeline.run_ingestion(content, media, source)
    try:
        pth = Path(source)
        if pth.exists():
            content = pth.read_text(encoding="utf-8")
        else:
            content = source
    except Exception:
        content = source
    record = run_ingestion(content=content, media_type=media, source=source)
    if out:
        from .pipeline import save_record

        save_record(record, out_dir=out)
    print(record)


if __name__ == "__main__":
    main()
