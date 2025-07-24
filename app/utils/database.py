"""
Database utilities and connection management
"""

from collections.abc import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings


def get_database_url(async_mode: bool = False) -> str:
    """Get database URL with proper driver for sync/async mode"""
    settings = get_settings()

    if not settings.DATABASE_URL:
        # Default to SQLite for development
        if async_mode:
            return "sqlite+aiosqlite:///./app.db"
        else:
            return "sqlite:///./app.db"

    # Convert sync URLs to async if needed
    if async_mode and not settings.DATABASE_URL.startswith(
        ("postgresql+asyncpg", "sqlite+aiosqlite")
    ):
        if "postgresql" in settings.DATABASE_URL:
            return settings.DATABASE_URL.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
        elif "sqlite" in settings.DATABASE_URL:
            return settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

    return settings.DATABASE_URL


# Sync engine for migrations and initial setup
sync_engine = create_engine(
    get_database_url(async_mode=False),
    echo=get_settings().DB_ECHO,
    connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {},
)

# Async engine for application runtime
async_engine = create_async_engine(
    get_database_url(async_mode=True), echo=get_settings().DB_ECHO
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(sync_engine)


def get_session() -> Generator[Session]:
    """Get sync database session"""
    with Session(sync_engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Get async database session"""
    async with AsyncSession(async_engine) as session:
        yield session
