import time
import os
import redis
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..core.config import settings


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))  # requisições por minuto
WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))  # segundos

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting in test mode
        if os.getenv("TESTING") == "1":
            return await call_next(request)

        identifier = request.headers.get("Authorization")
        if not identifier:
            identifier = getattr(request.client, "host", None)
        if not identifier:
            identifier = "anonymous"
        now = int(time.time())
        window_key = f"rate:{identifier}:{now // WINDOW}"
        try:
            current = await redis_client.incr(window_key)
            current = int(current)
            if current == 1:
                await redis_client.expire(window_key, WINDOW)
            if current > RATE_LIMIT:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded"},
                )
        except Exception as e:
            # Em caso de erro no Redis, não bloqueia a requisição
            pass
        response = await call_next(request)
        return response
