"""
Main API v1 Router
Combines all API v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, items, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
