// Aurora Platform - Seed dos Pilares Fundamentais
// E2E Test Data

// Criar índices
CREATE INDEX pilar_name_idx IF NOT EXISTS FOR (p:Pilar) ON (p.name);
CREATE INDEX conceito_name_idx IF NOT EXISTS FOR (c:Conceito) ON (c.name);

// Pilares fundamentais
CREATE (p1:Pilar {
  id: "pilar_001", 
  name: "Governança Corporativa",
  description: "Estruturas e processos de tomada de decisão",
  created_at: datetime()
});

CREATE (p2:Pilar {
  id: "pilar_002",
  name: "Gestão de Riscos", 
  description: "Identificação e mitigação de riscos organizacionais",
  created_at: datetime()
});

CREATE (p3:Pilar {
  id: "pilar_003",
  name: "Compliance",
  description: "Conformidade com normas e regulamentações",
  created_at: datetime()
});

// Conceitos relacionados
CREATE (c1:Conceito {
  id: "conceito_001",
  name: "Auditoria Interna",
  description: "Processo de avaliação independente",
  pilar_id: "pilar_001"
});

CREATE (c2:Conceito {
  id: "conceito_002", 
  name: "Matriz de Riscos",
  description: "Ferramenta de mapeamento de riscos",
  pilar_id: "pilar_002"
});

// Relacionamentos
MATCH (p1:Pilar {id: "pilar_001"}), (c1:Conceito {id: "conceito_001"})
CREATE (p1)-[:CONTAINS]->(c1);

MATCH (p2:Pilar {id: "pilar_002"}), (c2:Conceito {id: "conceito_002"})
CREATE (p2)-[:CONTAINS]->(c2);

MATCH (p1:Pilar {id: "pilar_001"}), (p2:Pilar {id: "pilar_002"})
CREATE (p1)-[:RELATES_TO {strength: 0.8}]->(p2);

// Nó de teste E2E
CREATE (e2e:TestNode {
  id: "e2e_marker",
  name: "E2E Test Marker",
  created_at: datetime(),
  test_run: true
});

RETURN "Seed dos pilares executado com sucesso" AS status;