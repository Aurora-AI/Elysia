import re
from typing import Optional

from fastapi import HTTPException, status


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def sanitize_input(text: str) -> str:
    # Remove potential XSS characters
    dangerous_chars = [
        "<",
        ">",
        '"',
        "'",
        "&",
        "javascript:",
        "script",
        "onload",
        "onerror",
    ]
    for char in dangerous_chars:
        text = text.replace(char, "")
    return text.strip()


def validate_user_input(email: Optional[str] = None, password: Optional[str] = None):
    if email and not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    if password and len(password) > 128:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password too long"
        )
