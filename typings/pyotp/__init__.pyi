from typing import Any

class TOTP:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def verify(self, *args: Any, **kwargs: Any) -> bool: ...

__all__ = ["TOTP"]
