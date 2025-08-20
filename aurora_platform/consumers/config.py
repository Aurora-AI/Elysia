import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "aurora-pilares-consumer")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "PILAR_UPSERT")

# Postgres via SQLAlchemy (reutiliza o DATABASE_URL já usado no projeto)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/aurora")

# Neo4j
NEO4J_URI = os.getenv("NEO4J_URI",  "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test")

# Operação
POLL_TIMEOUT_S = float(os.getenv("POLL_TIMEOUT_S", "1.0"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "200"))
LOG_EVERY_N = int(os.getenv("LOG_EVERY_N", "100"))
