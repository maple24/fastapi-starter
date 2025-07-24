"""
Item database model using SQLModel
"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class ItemModel(SQLModel, table=True):
    """Item database model"""

    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, index=True)
    description: str | None = Field(default=None, max_length=1000)
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    def __repr__(self):
        return f"<Item(id={self.id}, title={self.title}, owner_id={self.owner_id})>"
