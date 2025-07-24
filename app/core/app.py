"""
FastAPI Application Factory
Creates and configures the FastAPI application with all middleware, routers, and settings.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger

from app.api.health import health_router
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware, TimingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting FastAPI application...")
    yield
    # Shutdown
    logger.info("🛑 Shutting down FastAPI application...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=(
            f"{settings.API_V1_STR}/openapi.json"
            if settings.ENABLE_DOCS
            else None
        ),
        docs_url=(
            f"{settings.API_V1_STR}/docs"
            if settings.ENABLE_DOCS
            else None
        ),
        redoc_url=(
            f"{settings.API_V1_STR}/redoc"
            if settings.ENABLE_DOCS
            else None
        ),
        lifespan=lifespan,
    )

    # Security middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    if settings.ALLOWED_HOSTS and settings.ENVIRONMENT == "production":
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    # Custom middleware
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

    # Include routers
    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
