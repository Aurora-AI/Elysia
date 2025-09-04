from typing import Any
from typing import Any, Callable


class Session:
    def run(self, cypher: str, **params: Any) -> Any: ...
    def execute_write(
        self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any: ...


class Driver:
    def session(self) -> Session: ...
    def close(self) -> None: ...


class GraphDatabase:
    @staticmethod
    def driver(uri: str, auth: tuple[str, str] | None = ...) -> Driver: ...


__all__ = ["GraphDatabase", "Driver", "Session"]


class GraphDatabase:
    @staticmethod
    def driver(*args: Any, **kwargs: Any) -> Any: ...


__all__ = ["GraphDatabase"]
