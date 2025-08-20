-- Constraints e índices para performance Neo4j
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

CREATE INDEX entity_type_idx IF NOT EXISTS
FOR (e:Entity) ON (e.entity_type);

CREATE CONSTRAINT rel_id_unique IF NOT EXISTS
FOR ()-[r:REL]-() REQUIRE r.id IS UNIQUE;

CREATE INDEX rel_type_idx IF NOT EXISTS
FOR ()-[r:REL]-() ON (r.type);
