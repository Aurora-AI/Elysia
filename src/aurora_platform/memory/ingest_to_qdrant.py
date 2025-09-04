import argparse
import json
import os
import uuid
from pathlib import Path
from typing import Any

from docx import Document
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from src.memory.chunker import split_into_chunks
from src.memory.embeddings import encode_texts
from src.memory.normalizer import extract_metadata_from_datajud, normalize_text

DEFAULT_SOURCE = os.getenv("DEFAULT_SOURCE", "DataJud")
DEFAULT_JUR = os.getenv("DEFAULT_JURISDICAO", "")


def qdr():
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY") or None
    return QdrantClient(url=url, api_key=api_key)


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text


def read_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def read_json(path: Path) -> tuple[str, dict[str, Any]]:
    obj = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    # Tenta campos de texto evidentes
    text = obj.get("conteudo") or obj.get("texto") or obj.get(
        "ementa") or json.dumps(obj, ensure_ascii=False)
    meta = extract_metadata_from_datajud(obj)
    return text, meta


def upsert_one(client: QdrantClient, collection: str, vectors: list[list[float]] | Any, payloads: list[dict[str, Any]]):
    points = [qm.PointStruct(id=str(uuid.uuid4()), vector=v, payload=p)
              for v, p in zip(vectors, payloads, strict=False)]
    client.upsert(collection_name=collection, points=points)


def ingest_file(client: QdrantClient, path: Path):
    ext = path.suffix.lower()
    raw_text = ""
    meta: dict[str, Any] = {}

    if ext == ".pdf":
        raw_text = read_pdf(path)
        meta = {}
    elif ext == ".docx":
        raw_text = read_docx(path)
        meta = {}
    elif ext == ".json":
        raw_text, meta = read_json(path)
    else:
        raw_text = path.read_text(encoding="utf-8", errors="ignore")

    raw_text = normalize_text(raw_text)
    if not raw_text:
        return

    base_payload = {
        "title": path.stem,
        "text": raw_text,
        "source": DEFAULT_SOURCE,
        "file_path": str(path),
        "jurisdicao": meta.get("tribunal") or DEFAULT_JUR,
        **meta,
    }

    # 1) RAW (documento integral)
    v_raw = encode_texts([raw_text])
    upsert_one(client, "cases_raw", v_raw, [base_payload])

    # 2) NORM (por ora, igual ao raw: já normalizado)
    v_norm = v_raw
    upsert_one(client, "cases_norm", v_norm, [base_payload])

    # 3) CHUNKS
    chunks = split_into_chunks(raw_text, max_chars=1200, overlap=150)
    if chunks:
        vecs = encode_texts(chunks).tolist()
        payloads = []
        for idx, ch in enumerate(chunks):
            p = dict(base_payload)
            p["text"] = ch
            p["chunk_index"] = idx
            payloads.append(p)
        upsert_one(client, "cases_chunks", vecs, payloads)


def main():
    parser = argparse.ArgumentParser(
        description="Ingestão de documentos no Qdrant")
    parser.add_argument("--input", required=True,
                        help="Diretório com arquivos .json/.pdf/.docx")
    args = parser.parse_args()

    root = Path(args.input)
    if not root.exists():
        raise SystemExit(f"Diretório não encontrado: {root}")

    client = qdr()

    files = [p for p in root.rglob(
        "*") if p.is_file() and p.suffix.lower() in {".json", ".pdf", ".docx", ".txt", ".md"}]
    if not files:
        print(f"Nenhum arquivo suportado encontrado em {root}")
        return

    for f in files:
        print(f"Ingerindo: {f}")
        try:
            ingest_file(client, f)
        except Exception as e:
            print(f"[WARN] Falha ao ingerir {f}: {e}")

    print("OK: Ingestão concluída.")


if __name__ == "__main__":
    main()
