import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field


class HarmonyMetadata(BaseModel):
    context_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    compression: Literal["high", "medium", "low"] = "medium"
    delegation_target: str | None = None
    rag_slot: str | None = None


class HarmonyMessage(BaseModel):
    role: Literal["sistema", "agente", "usuário", "ferramenta"]
    content: str | dict[str, Any]
    metadata: HarmonyMetadata = Field(default_factory=HarmonyMetadata)
