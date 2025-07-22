import logging
from datetime import datetime
from typing import Optional

# Configure security logger
security_logger = logging.getLogger("aurora.security")
security_logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - SECURITY - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
security_logger.addHandler(handler)


def log_login_attempt(email: str, success: bool, ip: str):
    status = "SUCCESS" if success else "FAILED"
    security_logger.info(f"Login {status} - Email: {email} - IP: {ip}")


def log_security_event(event: str, details: str, ip: Optional[str] = None):
    message = f"{event} - {details}"
    if ip:
        message += f" - IP: {ip}"
    security_logger.warning(message)


def log_rate_limit_exceeded(ip: str, endpoint: str):
    security_logger.warning(f"Rate limit exceeded - IP: {ip} - Endpoint: {endpoint}")
