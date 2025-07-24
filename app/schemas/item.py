"""
Item schemas for request/response validation
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base item schema with common fields"""

    title: str = Field(..., min_length=1, max_length=200, description="Item title")
    description: str | None = Field(
        None, max_length=1000, description="Item description"
    )


class ItemCreate(ItemBase):
    """Schema for creating a new item"""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating item information"""

    title: str | None = Field(
        None, min_length=1, max_length=200, description="Item title"
    )
    description: str | None = Field(
        None, max_length=1000, description="Item description"
    )


class ItemResponse(ItemBase):
    """Schema for item response"""

    id: int = Field(..., description="Item ID")
    owner_id: int = Field(..., description="Item owner ID")
    created_at: datetime = Field(..., description="Item creation timestamp")
    updated_at: datetime | None = Field(None, description="Item last update timestamp")

    class Config:
        from_attributes = True


class Item(ItemBase):
    """Complete item schema for internal use"""

    id: int = Field(..., description="Item ID")
    owner_id: int = Field(..., description="Item owner ID")
    created_at: datetime = Field(..., description="Item creation timestamp")
    updated_at: datetime | None = Field(None, description="Item last update timestamp")

    class Config:
        from_attributes = True
