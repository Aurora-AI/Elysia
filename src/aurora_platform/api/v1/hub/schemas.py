from pydantic import BaseModel
from typing import Any, Dict

class HubRequest(BaseModel):
    task: str
    payload: Dict[str, Any] = {}

class HubResponse(BaseModel):
    result: Any
    agent: str
