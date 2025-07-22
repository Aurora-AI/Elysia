import redis
from aurora_platform.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    socket_connect_timeout=1,
)


def ping():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        return False
