# Stub de respostas (ex.: typings/starlette/responses.pyi ou typings/fastapi/responses.pyi)
from collections.abc import Mapping
from typing import Any

class Response:
    status_code: int
    headers: Mapping[str, str]
    media_type: str | None
    background: Any | None

    def __init__(
        self,
        content: Any = ...,
        status_code: int | None = ...,
        headers: Mapping[str, str] | None = ...,
        media_type: str | None = ...,
        **kwargs: Any,
    ) -> None: ...

class JSONResponse(Response):
    def __init__(
        self,
        content: Any = ...,
        status_code: int | None = ...,
        headers: Mapping[str, str] | None = ...,
        media_type: str | None = ...,
        **kwargs: Any,
    ) -> None: ...

class PlainTextResponse(Response):
    def __init__(
        self,
        content: Any = ...,
        status_code: int | None = ...,
        headers: Mapping[str, str] | None = ...,
        media_type: str | None = ...,
        **kwargs: Any,
    ) -> None: ...

class StreamingResponse(Response):
    def __init__(
        self,
        content: Any = ...,
        status_code: int | None = ...,
        headers: Mapping[str, str] | None = ...,
        media_type: str | None = ...,
        **kwargs: Any,
    ) -> None: ...

__all__ = ["Response", "JSONResponse", "PlainTextResponse", "StreamingResponse"]
