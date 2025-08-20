from typing import Dict
from sqlalchemy import text
from sqlalchemy.orm import Session

# Upsert simples para tabelas dos pilares.
# Neste MVP, garantimos a presença mínima em uma tabela canônica `pilares_docs`
# (ou escolha uma tabela específica e ajuste aqui).


def upsert_pilar_basico(db: Session, payload: Dict):
    """
    Armazena registro mínimo do Pilar em 'pilares_docs' para rastreabilidade.
    Se você quiser usar tabelas específicas por pilar, crie funções irmãs.
    """
    pilar = payload.get("name") or payload["slug"]
    fonte = payload.get("fonte", "unknown")
    orig = "kafka:PILAR_UPSERT"

    # Cria a tabela se não existir (só por robustez; ideal é Alembic)
    db.execute(text("""
    CREATE TABLE IF NOT EXISTS pilares_docs (
        id SERIAL PRIMARY KEY,
        pilar TEXT NOT NULL,
        documento TEXT,
        origem TEXT,
        versao TEXT,
        texto_full TEXT
    )
    """))

    # Upsert simplificado: insert "log" resumido (idempotência lógica no Neo4j)
    db.execute(text("""
        INSERT INTO pilares_docs (pilar, documento, origem, versao, texto_full)
        VALUES (:pilar, :documento, :origem, :versao, :texto_full)
    """), {
        "pilar": pilar,
        "documento": f"upsert:{payload['slug']}",
        "origem": orig,
        "versao": payload.get("ts"),
        "texto_full": ""
    })
