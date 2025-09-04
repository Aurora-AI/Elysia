from typing import Any, Callable


def fixture(*args: Any, **kwargs: Any) -> Callable[..., Any]: ...


class raises:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...


class _Mark:
    def __getattr__(self, name: str) -> Any: ...


mark: _Mark = _Mark()


__all__ = ["raises", "mark"]
