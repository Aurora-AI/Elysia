from typing import Any, Callable

class BaseHTTPMiddleware:
    def __init__(self, app: Any, dispatch: Callable[..., Any] | None = ...) -> None: ...

__all__ = ["BaseHTTPMiddleware"]
