from typing import Any

class PilarBase:
    pilar_id: str
    titulo: str | None
    descricao: str | None
    fonte: str | None
    referencia_url: str | None
    versao: int
    extra: dict[str, Any] | None

class PilarAntropologia(PilarBase): ...
class PilarPsicologia(PilarBase): ...
class PilarVendas(PilarBase): ...
class PilarEstatistica(PilarBase): ...

__all__ = [
    "PilarAntropologia",
    "PilarPsicologia",
    "PilarVendas",
    "PilarEstatistica",
]
