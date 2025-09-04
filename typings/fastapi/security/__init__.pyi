class OAuth2PasswordRequestForm:
    def __init__(self, username: str = ..., password: str = ...,
                 scope: str | None = ...) -> None: ...
    username: str
    password: str
    scope: str | None


__all__ = ["OAuth2PasswordRequestForm"]
