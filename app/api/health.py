"""
Health check endpoints
Provides application health status and dependencies
"""

import platform
import time
from typing import Any

import psutil
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.config import Settings, get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    timestamp: float
    version: str
    environment: str
    uptime: float
    system_info: dict[str, Any]


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response model"""

    database: str
    redis: str
    memory_usage: dict[str, Any]
    disk_usage: dict[str, Any]


# Store application start time
app_start_time = time.time()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Basic health check endpoint
    Returns basic application status and system information
    """
    current_time = time.time()
    uptime = current_time - app_start_time

    return HealthResponse(
        status="healthy",
        timestamp=current_time,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        uptime=uptime,
        system_info={
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        },
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse, tags=["Health"])
async def detailed_health_check(settings: Settings = Depends(get_settings)):
    """
    Detailed health check endpoint
    Returns comprehensive application and system status
    """
    current_time = time.time()
    uptime = current_time - app_start_time

    # Get memory usage
    memory = psutil.virtual_memory()
    memory_usage = {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free,
    }

    # Get disk usage
    disk = psutil.disk_usage("/")
    disk_usage = {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": (disk.used / disk.total) * 100,
    }

    # Check database status (placeholder)
    database_status = "not_configured"
    if settings.DATABASE_URL:
        database_status = "connected"  # In real app, check actual connection

    # Check Redis status (placeholder)
    redis_status = "not_configured"
    if settings.REDIS_URL:
        redis_status = "connected"  # In real app, check actual connection

    return DetailedHealthResponse(
        status="healthy",
        timestamp=current_time,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        uptime=uptime,
        system_info={
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        },
        database=database_status,
        redis=redis_status,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
    )


@router.get("/ping", tags=["Health"])
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong"}


# Create the health router
health_router = APIRouter()
health_router.include_router(router)
