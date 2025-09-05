def test_upsert_pilar_happy_path():
    # Imports done inside the test to let tests/conftest.py set PYTHONPATH and env first
    from aurora_platform.consumers.kafka_consumer_pilares import upsert_pilar
    from aurora_platform.core.db_legacy import Base, SessionLocal, get_engine
    from aurora_platform.models import PilarAntropologia

    payload = {
        "pilar_id": "ANT-0002",
        "pilar": "antropologia",
        "titulo": "Hierarquia baixa",
        "descricao": "Estruturas planas tendem a ...",
        "fonte": "DeepSeek-V3",
        "referencia_url": None,
        "versao": 1,
        "extra": {"escala": 0.2},
    }
    # ensure tables exist in the test DB (conftest already created them, but keep as safety)
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        upsert_pilar(db, payload)
        # Verifica se persistiu
        obj = db.query(PilarAntropologia).filter_by(pilar_id="ANT-0002").one()
        assert obj.titulo == "Hierarquia baixa"
        assert obj.versao == 1
