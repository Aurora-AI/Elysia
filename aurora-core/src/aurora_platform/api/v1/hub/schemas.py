from typing import Any, Dict

from pydantic import BaseModel


class HubRequest(BaseModel):
    task: str
    payload: Dict[str, Any] = {}


class HubResponse(BaseModel):
    result: Any
    agent: str
