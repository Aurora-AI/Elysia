import os
import sys

from aurora_platform.core.db_legacy import SessionLocal
from aurora_platform.models.pilar_antropologia import PilarAntropologia
from aurora_platform.models.pilar_estatistica import PilarEstatistica
from aurora_platform.models.pilar_psicologia import PilarPsicologia
from aurora_platform.models.pilar_vendas import PilarVendas

# Ensure repository root is on sys.path when running script directly
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def main():
    db = SessionLocal()
    print('📊 Validação de ingestão dos pilares:')
    try:
        print('Antropologia:', db.query(PilarAntropologia).count())
        print('Psicologia:', db.query(PilarPsicologia).count())
        print('Vendas:', db.query(PilarVendas).count())
        print('Estatística:', db.query(PilarEstatistica).count())
    finally:
        db.close()


if __name__ == '__main__':
    main()
