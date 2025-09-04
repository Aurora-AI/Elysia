from typing import Any


class Response:
    def __init__(self, content: Any = ..., status_code: int = 200,
                 media_type: str | None = ...) -> None: ...


class JSONResponse(Response):
    ...


class PlainTextResponse(Response):
    ...


class StreamingResponse(Response):
    ...


__all__ = ["Response", "JSONResponse",
           "PlainTextResponse", "StreamingResponse"]
