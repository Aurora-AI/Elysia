from collections.abc import Callable
from typing import Any

class BaseHTTPMiddleware:
    def __init__(self, app: Any, dispatch: Callable[..., Any] | None = ...) -> None: ...

__all__ = ["BaseHTTPMiddleware"]
