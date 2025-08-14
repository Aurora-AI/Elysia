import asyncio
import json
import sys
from pathlib import Path

from backend.app.services.docparser.pipeline import process_document_pipeline

# Ensure repo root is on sys.path so 'backend' package is importable when running directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    content = b"conteudo-de-teste"
    result = asyncio.run(process_document_pipeline("teste.pdf", content))
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
