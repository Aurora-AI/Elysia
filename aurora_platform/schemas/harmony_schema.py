from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
import uuid


class HarmonyMetadata(BaseModel):
    context_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    compression: Literal["high", "medium", "low"] = "medium"
    delegation_target: Optional[str] = None
    rag_slot: Optional[str] = None


class HarmonyMessage(BaseModel):
    role: Literal["sistema", "agente", "usuário", "ferramenta"]
    content: str | Dict[str, Any]
    metadata: HarmonyMetadata = Field(default_factory=HarmonyMetadata)
