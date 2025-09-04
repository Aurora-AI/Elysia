from typing import Any

from pydantic import BaseModel


class HubRequest(BaseModel):
    task: str
    payload: dict[str, Any] = {}


class HubResponse(BaseModel):
    result: Any
    agent: str
