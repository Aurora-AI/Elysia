from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from ..services.kafka_producer import send_entity_upsert, send_relation_upsert
import uuid

app = FastAPI(
    title="Aurora Platform KG API",
    description="Kafka + Knowledge Graph RAG 2.0",
    version="2.0.0"
)

router = APIRouter(prefix="/kg", tags=["Knowledge Graph"])

class EntityUpsert(BaseModel):
    entity_id: Optional[str] = None
    entity_type: str
    labels: List[str]
    properties: Dict
    provenance: Optional[Dict] = None

class RelationUpsert(BaseModel):
    relation_id: Optional[str] = None
    from_id: str
    to_id: str
    rel_type: str
    properties: Dict
    provenance: Optional[Dict] = None

@router.post("/upsert-entity")
async def upsert_entity(entity: EntityUpsert):
    """Publica evento de upsert de entidade no Kafka"""
    try:
        if not entity.entity_id:
            entity.entity_id = str(uuid.uuid4())

        payload = entity.dict()
        send_entity_upsert(payload)

        return {"status": "published", "entity_id": entity.entity_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upsert-relation")
async def upsert_relation(relation: RelationUpsert):
    """Publica evento de upsert de relação no Kafka"""
    try:
        if not relation.relation_id:
            relation.relation_id = str(uuid.uuid4())

        payload = relation.dict()
        send_relation_upsert(payload)

        return {"status": "published", "relation_id": relation.relation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def kg_health():
    """Health check do sistema KG"""
    return {"status": "ok", "service": "knowledge-graph"}

@app.get("/")
async def root():
    return {"message": "Aurora Platform KG API", "version": "2.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "aurora-kg-api"}

app.include_router(router)
