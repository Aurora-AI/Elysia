from pydantic import BaseModel


class SummarizeURLRequest(BaseModel):
    url: str
