// Constraints (id e name únicos para Pilar)
CREATE CONSTRAINT pilar_id_unique IF NOT EXISTS
FOR (p:Pilar) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT pilar_name_unique IF NOT EXISTS
FOR (p:Pilar) REQUIRE p.name IS UNIQUE;

// Índices úteis
CREATE INDEX pilar_title IF NOT EXISTS FOR (p:Pilar) ON (p.titulo);

// Nós base (idempotente)
MERGE (a:Pilar {id: "PILAR-ANT"})
  ON CREATE SET a.name = "Antropologia", a.titulo = "Antropologia", a.created_at = datetime()
  ON MATCH  SET a.updated_at = datetime();

MERGE (p:Pilar {id: "PILAR-PSI"})
  ON CREATE SET p.name = "Psicologia", p.titulo = "Psicologia Comportamental", p.created_at = datetime()
  ON MATCH  SET p.updated_at = datetime();

MERGE (v:Pilar {id: "PILAR-VEN"})
  ON CREATE SET v.name = "Vendas", v.titulo = "Vendas & Gestão", v.created_at = datetime()
  ON MATCH  SET v.updated_at = datetime();

MERGE (e:Pilar {id: "PILAR-EST"})
  ON CREATE SET e.name = "Estatistica", e.titulo = "Estatística Aplicada & PLN", e.created_at = datetime()
  ON MATCH  SET e.updated_at = datetime();

// (Opcional) Relações conceituais
MERGE (a)-[:INFORMA]->(v);
MERGE (p)-[:INFLUENCIA]->(v);
MERGE (e)-[:MENSURA]->(v);
