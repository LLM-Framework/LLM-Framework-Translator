import time
from collections import defaultdict
from fastapi import HTTPException, Request
from src.config import settings


class RateLimiter:
    def __init__(self, requests: int, period_seconds: int):
        self.requests = requests
        self.period = period_seconds
        self.clients: defaultdict = defaultdict(list)

    async def __call__(self, request: Request):
        if not settings.rate_limit_enabled:
            return

        client_ip = request.client.host
        now = time.time()

        # Clean old entries
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < self.period
        ]

        # Check limit
        if len(self.clients[client_ip]) >= self.requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.requests} requests per {self.period} seconds"
            )

        self.clients[client_ip].append(now)


# Global rate limiter
rate_limiter = RateLimiter(
    requests=settings.rate_limit_requests,
    period_seconds=settings.rate_limit_period_seconds
)