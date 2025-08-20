CREATE TABLE IF NOT EXISTS pilar_antropologia (
    id SERIAL PRIMARY KEY,
    conceito TEXT NOT NULL,
    variavel TEXT,
    contexto TEXT,
    fonte TEXT,
    referencia TEXT
);

CREATE TABLE IF NOT EXISTS pilar_psicologia (
    id SERIAL PRIMARY KEY,
    vies TEXT NOT NULL,
    descricao TEXT,
    impacto TEXT,
    fonte TEXT,
    referencia TEXT
);

CREATE TABLE IF NOT EXISTS pilar_vendas (
    id SERIAL PRIMARY KEY,
    metodologia TEXT NOT NULL,
    descricao TEXT,
    aplicabilidade TEXT,
    fonte TEXT
);

CREATE TABLE IF NOT EXISTS pilar_estatistica (
    id SERIAL PRIMARY KEY,
    metodo TEXT NOT NULL,
    modelo TEXT,
    metricas TEXT,
    fonte TEXT,
    referencia TEXT
);

CREATE TABLE IF NOT EXISTS pilares_docs (
    id SERIAL PRIMARY KEY,
    pilar TEXT NOT NULL,
    documento TEXT,
    origem TEXT,
    versao TEXT,
    texto_full TEXT
);
