from dataclasses import dataclass, field  # noqa: F401 (reservado p/ fut.)
from typing import List, Pattern
import re

USER_AGENT = "AuroraCrawler/1.0 (+https://aurora.example)"

# prioriza RN; permite gov.br (estadual/municipal)
ALLOWED_SUFFIXES = [".rn.gov.br", ".gov.br"]

# por padrão, não exportar emails pessoais (pode ser liberado por flag)
DISALLOW_PERSONAL = True

SEEDS: List[str] = [
    "https://www.rn.gov.br/",
    "https://www.natal.rn.gov.br/",
    "https://www.mossoro.rn.gov.br/",
    "https://www.parnamirim.rn.gov.br/",
    "https://www.caico.rn.gov.br/",
    "https://www.curraisnovos.rn.gov.br/",
]

KEYWORDS_BY_CATEGORY = {
    "licitacoes": ["licit", "pregao", "compras", "suprimentos", "contrat", "edital"],
    "administracao": ["administra", "planej", "finan", "meio ambiente", "semurb", "gestao"],
    "rh": ["recursos humanos", "rh", "pessoal"],
    "secretariado": ["secretaria", "secretário", "secretaria adjunta", "gabinete", "diretoria", "diretor"],
    "consorcios": ["consórcio", "consorcio", "intermunicipal"],
}

EMAIL_RE: Pattern = re.compile(
    r"(?P<email>[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})",
    re.IGNORECASE,
)

NAME_HINT_RE: Pattern = re.compile(
    r"(?:(?:Secretári[oa]|Diretor[ae]?|Gerent[ea]|Chefe|Coordenador[ae]?|Pregoeir[oa]))[:\s-]+"
    r"(?P<nome>[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÀ-ÖØ-öø-ÿ'`´^~ ]{5,80})"
)
