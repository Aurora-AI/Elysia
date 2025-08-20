from .schemas import (
    IngestResponse,
    Metadata,
    Diagnostics,
    CostBreakdown,
    StepRecord,
    TableSchema,
    ImageSchema,
)
from .parsers.docling_parser import parse_with_docling
from .parsers.fallback_parser import parse_with_fallback
import time


async def process_document_pipeline(
    filename: str,
    content: bytes,
    *,
    sha256: str,
    sniffed_mime: str,
) -> IngestResponse:
    started = time.perf_counter_ns()
    steps: list[StepRecord] = []

    # Try primary parser
    try:
        t0 = time.perf_counter_ns()
        parsed = parse_with_docling(content)
        t1 = time.perf_counter_ns()
        steps.append(
            StepRecord(
                name="docling",
                started_ms=t0 // 1_000_000,
                ended_ms=t1 // 1_000_000,
                ok=True,
                notes=None,
            )
        )
        parser_usado = "docling"
        fallback_flag = False
        versao_parser = "0.0.1"
    except Exception as _:
        t0 = time.perf_counter_ns()
        parsed = parse_with_fallback(content)
        t1 = time.perf_counter_ns()
        steps.append(
            StepRecord(
                name="fallback",
                started_ms=t0 // 1_000_000,
                ended_ms=t1 // 1_000_000,
                ok=True,
                notes=None,
            )
        )
        parser_usado = "fallback"
        fallback_flag = True
        versao_parser = "0.0.1"

    texto_markdown: str = parsed.get("texto_markdown", "")
    tabelas = [TableSchema(**t) if not isinstance(t, TableSchema)
               else t for t in parsed.get("tabelas", [])]
    imagens = [ImageSchema(**i) if not isinstance(i, ImageSchema)
               else i for i in parsed.get("imagens", [])]

    ended = time.perf_counter_ns()
    diag = Diagnostics(
        parser_usado=parser_usado,
        versao_parser=versao_parser,
        fallback=fallback_flag,
        steps=steps,
        planned_chunks=None,
        embedding_model="bge-m3",
    )

    meta = Metadata(
        fonte=filename,
        mime_type=sniffed_mime,
        bytes=len(content),
        sha256=sha256,
        hash_conteudo=sha256,
        num_paginas=None,
    )

    cost = CostBreakdown(
        cpu_ms_parser=int((ended - started) / 1_000_000),
        usd_estimado=0.0001,
    )

    return IngestResponse(
        texto_markdown=texto_markdown,
        tabelas=tabelas,
        imagens=imagens,
        metadados=meta,
        proveniencia=diag,
        custo=cost,
    )
