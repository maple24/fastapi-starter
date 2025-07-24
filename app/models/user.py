"""
User database model using SQLModel
"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    """User database model"""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=100)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
