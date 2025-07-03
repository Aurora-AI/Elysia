import time
import os
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from ..core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting in test mode
        if os.getenv("TESTING") == "1":
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "127.0.0.1"
        current_time = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        limit = settings.LOGIN_RATE_LIMIT_PER_MINUTE if "/auth/" in str(request.url) else settings.RATE_LIMIT_PER_MINUTE
        
        if len(self.requests[client_ip]) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        self.requests[client_ip].append(current_time)
        return await call_next(request)