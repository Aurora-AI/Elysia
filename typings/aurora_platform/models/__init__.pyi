from typing import Any, Dict, Optional


class PilarBase:
    pilar_id: str
    titulo: Optional[str]
    descricao: Optional[str]
    fonte: Optional[str]
    referencia_url: Optional[str]
    versao: int
    extra: Optional[Dict[str, Any]]


class PilarAntropologia(PilarBase):
    ...


class PilarPsicologia(PilarBase):
    ...


class PilarVendas(PilarBase):
    ...


class PilarEstatistica(PilarBase):
    ...


__all__ = [
    "PilarAntropologia",
    "PilarPsicologia",
    "PilarVendas",
    "PilarEstatistica",
]
