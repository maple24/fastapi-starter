"""
Custom middleware for FastAPI application
Includes logging, timing, rate limiting, and security middleware
"""

import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url} - "
            f"User-Agent: {request.headers.get('user-agent', 'N/A')}"
        )

        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} - Processing time: {process_time:.4f}s"
        )

        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """Add timing information to response headers"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware"""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/api/v1/health"]:
            return await call_next(request)

        current_time = time.time()

        # Clean old requests
        self.clients[client_ip] = [
            timestamp
            for timestamp in self.clients[client_ip]
            if current_time - timestamp < self.period
        ]

        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Rate limit exceeded. Maximum {self.calls} requests per {self.period} seconds."
                },
            )

        # Add current request
        self.clients[client_ip].append(current_time)

        response = await call_next(request)

        # Add rate limit headers
        remaining = max(0, self.calls - len(self.clients[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.period))

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        return response
