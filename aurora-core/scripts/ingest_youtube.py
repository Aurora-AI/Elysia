#!/usr/bin/env python3

from aurora_platform.modules.crawler.ingestion.loaders import YouTubeTranscriptLoader
from aurora_platform.modules.crawler.pipeline import run_ingestion, save_record
import os
import sys
import argparse

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(WORKSPACE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a YouTube transcript (pre-fetched text) into chunks."
    )
    parser.add_argument(
        "--text", required=True, help="Transcript text (already extracted)"
    )
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    bundle = YouTubeTranscriptLoader.load_transcript_text(args.text)
    record = run_ingestion(bundle.content, "youtube", args.source, {})
    out = save_record(record)
    print(out)


if __name__ == "__main__":
    main()
