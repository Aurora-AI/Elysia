from backend.app.connectors.tce_rn import pipeline, schemas


def make_raw(**kwargs):
    return schemas.RawApiExpense(**kwargs)


def test_normalize_cnpj_and_fields():
    raw = make_raw(
        fornecedor_cnpj="12.345.678/0001-90",
        orgao="Org",
        unidade="Un1",
        fornecedor_nome="Supplier",
        valor_pago=123.45,
        empenho_numero="E123",
        competencia="2024-01",
    )
    rec = pipeline.normalize(raw)
    assert rec.fornecedor_cnpj == "12345678000190"
    assert rec.orgao == "Org"
    assert rec.valor_pago == 123.45
    assert rec.record_id.startswith("tce-rn-")


def test_deterministic_id_with_id_registro():
    raw = make_raw(id_registro="ABC-123")
    rec = pipeline.normalize(raw)
    assert rec.record_id == "ABC-123"


def test_run_batches_posts(monkeypatch):
    # prepare 7 items, batch_size=3 => posts of sizes [3,3,1]
    items = [make_raw(id_registro=f"id{i}") for i in range(7)]

    class FakeClient:
        def __init__(self):
            pass

        def iter_expenses(self, *args, **kwargs):
            for it in items:
                yield it

        def close(self):
            pass

    # Replace the real client reference used by the pipeline with our fake
    monkeypatch.setattr(pipeline, "TCERNClient", lambda *a, **k: FakeClient())

    called = []

    def fake_post(payload):
        called.append(len(payload.items))
        return {"ok": True}

    monkeypatch.setattr(pipeline, "_post_ingest",
                        lambda payload: fake_post(payload))

    res = pipeline.run(batch_size=3)
    assert res["ok"]
    assert res["ingested"] == 7
    assert called == [3, 3, 1]
