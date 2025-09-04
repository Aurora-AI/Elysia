from datetime import datetime, timezone

import redis

from .config import settings

# Redis connection for token blacklist
redis_client = None
if settings.REDIS_URL:
    redis_client = redis.from_url(settings.REDIS_URL)

# In-memory fallback
blacklisted_tokens = set()


def blacklist_token(token: str, expires_at: datetime):
    """Add token to blacklist"""
    ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds())

    if redis_client:
        redis_client.setex(f"blacklist:{token}", ttl, "1")
    else:
        blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    if redis_client:
        return bool(redis_client.exists(f"blacklist:{token}"))
    return token in blacklisted_tokens


def revoke_all_user_tokens(user_id: int):
    """Revoke all tokens for a user"""
    if redis_client:
        redis_client.set(
            f"user_revoked:{user_id}", datetime.now(timezone.utc).isoformat()
        )
