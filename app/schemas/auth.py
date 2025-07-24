"""
Authentication schemas for request/response validation
"""

from pydantic import BaseModel, Field

from app.schemas.user import UserBase


class Token(BaseModel):
    """Token response schema"""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Token data schema for JWT payload"""

    email: str | None = Field(None, description="User email from token")


class UserCreate(UserBase):
    """Schema for user registration"""

    password: str = Field(
        ..., min_length=8, max_length=100, description="User password"
    )


class UserResponse(BaseModel):
    """User response schema for registration"""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(..., description="Whether the user is active")
    created_at: str = Field(..., description="User creation timestamp")

    class Config:
        from_attributes = True
