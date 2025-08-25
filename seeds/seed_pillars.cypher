// Cria/garante nós dos Pilares Fundamentais (idempotente)
MERGE (p1:Pillar {key: "document_parsing"})
  ON CREATE SET p1.name = "DocParser", p1.updated_at = datetime()
  ON MATCH SET p1.updated_at = datetime();

MERGE (p2:Pillar {key: "memory_active"})
  ON CREATE SET p2.name = "Memória Ativa (RAG 2.0)", p2.updated_at = datetime()
  ON MATCH SET p2.updated_at = datetime();

MERGE (p3:Pillar {key: "router"})
  ON CREATE SET p3.name = "AuroraRouter", p3.updated_at = datetime()
  ON MATCH SET p3.updated_at = datetime();

MERGE (p4:Pillar {key: "hrm"})
  ON CREATE SET
    p4.name = "Motor de Raciocínio Híbrido (HRM)",
    p4.updated_at = datetime()
  ON MATCH SET p4.updated_at = datetime();

MERGE (p5:Pillar {key: "wasm_sandbox"})
  ON CREATE SET
    p5.name = "Execução Segura (WASM Sandbox)",
    p5.updated_at = datetime()
  ON MATCH SET p5.updated_at = datetime();

// Relações ilustrativas (não duplicam por conta do MERGE)
MERGE (p1)-[:SUPPORTS]->(p2);
MERGE (p2)-[:FEEDS]->(p3);
MERGE (p3)-[:CALLS]->(p4);
MERGE (p3)-[:ISOLATES_VIA]->(p5);
