import re
from typing import Any

WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\x00", " ")
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def extract_metadata_from_datajud(obj: dict[str, Any]) -> dict[str, Any]:
    # Ajuste leve para campos comuns; mantém resiliente a variações
    meta = {}
    meta["numero_processo"] = obj.get("numeroProcesso") or obj.get(
        "numero_processo") or obj.get("processo", {}).get("numero")
    meta["orgao"] = obj.get("orgaoJulgador") or obj.get("orgao")
    meta["tribunal"] = obj.get("tribunal") or obj.get(
        "grau") or obj.get("justica")
    meta["classe"] = obj.get("classeProcessual") or obj.get("classe")
    meta["assunto"] = obj.get("assunto")
    meta["data_distribuicao"] = obj.get(
        "dataDistribuicao") or obj.get("distribuicao")
    meta["fonte"] = "DataJud"
    return {k: v for k, v in meta.items() if v}
