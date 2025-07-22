from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ConverseRequest(BaseModel):
    text: str


@router.post("/converse")
def converse(request: ConverseRequest):
    return {"response": f"Recebido: {request.text}"}
