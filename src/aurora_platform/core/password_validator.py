import re
from typing import List

from .config import settings


def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    """Validate password strength according to security policy"""
    errors = []

    if len(password) < settings.MIN_PASSWORD_LENGTH:
        errors.append(
            f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long"
        )

    if settings.REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")

    if settings.REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")

    if settings.REQUIRE_NUMBERS and not re.search(r"\d", password):
        errors.append("Password must contain at least one number")

    if settings.REQUIRE_SPECIAL_CHARS and not re.search(
        r'[!@#$%^&*(),.?":{}|<>]', password
    ):
        errors.append("Password must contain at least one special character")

    # Check for common weak patterns
    if password.lower() in ["password", "123456", "qwerty", "admin", "letmein"]:
        errors.append("Password is too common and easily guessable")

    return len(errors) == 0, errors


def is_password_compromised(password: str) -> bool:
    """Check if password appears in common breach lists"""
    import hashlib

    # Common breached passwords (expanded list)
    breached_passwords = {
        "password",
        "123456",
        "123456789",
        "qwerty",
        "abc123",
        "password123",
        "admin",
        "letmein",
        "welcome",
        "12345678",
        "1234567890",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "password1",
        "password12",
        "iloveyou",
        "princess",
        "rockyou",
        "monkey",
        "dragon",
        "sunshine",
        "master",
        "trustno1",
        "football",
        "baseball",
        "superman",
        "hello",
        "freedom",
    }

    # Check against known breached passwords
    if password.lower() in breached_passwords:
        return True

    # Check SHA1 hash against HaveIBeenPwned patterns (simplified)
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    common_hashes = {
        "5E884898DA28047151D0E56F8DC6292773603D0D6AABBDD62A11EF721D1542D8",  # 'password'
        "7C4A8D09CA3762AF61E59520943DC26494F8941B",  # '123456'
    }

    return sha1_hash in common_hashes
