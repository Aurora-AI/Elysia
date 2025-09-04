from fastapi import APIRouter, HTTPException

from aurora_platform.core.db_legacy import SessionLocal
from aurora_platform.models.pilar_antropologia import PilarAntropologia
from aurora_platform.models.pilar_estatistica import PilarEstatistica
from aurora_platform.models.pilar_psicologia import PilarPsicologia
from aurora_platform.models.pilar_vendas import PilarVendas

router = APIRouter(prefix="/pilares", tags=["pilares"])


def _serialize(rows):
    out = []
    for r in rows:
        d = dict(getattr(r, '__dict__', {}))
        d.pop("_sa_instance_state", None)
        out.append(d)
    return out


@router.get("/{nome}")
def get_pilar(nome: str):
    db = SessionLocal()
    try:
        mapping = {
            "antropologia": PilarAntropologia,
            "psicologia": PilarPsicologia,
            "vendas": PilarVendas,
            "estatistica": PilarEstatistica,
        }
        Model = mapping.get(nome.lower())
        if not Model:
            raise HTTPException(status_code=404, detail="Pilar não encontrado")
        rows = db.query(Model).all()
        return _serialize(rows)
    finally:
        db.close()
