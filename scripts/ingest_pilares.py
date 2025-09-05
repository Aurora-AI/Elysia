import json
import os
import sys

from aurora_platform.core.db_legacy import Base, SessionLocal, get_engine
from aurora_platform.models.pilar_antropologia import PilarAntropologia
from aurora_platform.models.pilar_estatistica import PilarEstatistica
from aurora_platform.models.pilar_psicologia import PilarPsicologia
from aurora_platform.models.pilar_vendas import PilarVendas

# Ensure repository root is on sys.path when running script directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilares_normalized")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def ensure_tables():
    # Create tables if not exists
    Base.metadata.create_all(bind=get_engine())


def ingest():
    ensure_tables()
    db = SessionLocal()
    try:
        antropologia = load_json("antropologia.json")
        for item in antropologia:
            db.add(PilarAntropologia(**item))

        psicologia = load_json("psicologia.json")
        for item in psicologia:
            db.add(PilarPsicologia(**item))

        vendas = load_json("vendas.json")
        for item in vendas:
            db.add(PilarVendas(**item))

        estatistica = load_json("estatistica.json")
        for item in estatistica:
            db.add(PilarEstatistica(**item))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    ingest()
    print("✅ Pilares ingeridos com sucesso")
