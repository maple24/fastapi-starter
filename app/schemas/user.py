"""
User schemas for request/response validation
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields"""

    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(
        ..., min_length=1, max_length=100, description="User full name"
    )
    is_active: bool = Field(default=True, description="Whether the user is active")


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: str = Field(
        ..., min_length=8, max_length=100, description="User password"
    )


class UserUpdate(BaseModel):
    """Schema for updating user information"""

    email: EmailStr | None = Field(None, description="User email address")
    full_name: str | None = Field(
        None, min_length=1, max_length=100, description="User full name"
    )
    is_active: bool | None = Field(None, description="Whether the user is active")
    password: str | None = Field(
        None, min_length=8, max_length=100, description="User password"
    )


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive data)"""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="User creation timestamp")

    class Config:
        from_attributes = True


class User(UserBase):
    """Complete user schema for internal use"""

    id: int = Field(..., description="User ID")
    is_superuser: bool = Field(
        default=False, description="Whether the user is a superuser"
    )
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime | None = Field(None, description="User last update timestamp")

    class Config:
        from_attributes = True
