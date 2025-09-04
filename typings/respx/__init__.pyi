from collections.abc import Callable
from typing import Any

class Route:
    def mock(self, return_value: Any |
             Callable[..., Any] | None = ...) -> Route: ...

    @property
    def called(self) -> bool: ...


class MockRouter:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...


def mock(func: Any = ...) -> Any: ...


def get(url: str, *args: Any, **kwargs: Any) -> Route: ...


def post(url: str, *args: Any, **kwargs: Any) -> Route: ...


__all__ = ["MockRouter", "mock", "get", "post", "Route"]
