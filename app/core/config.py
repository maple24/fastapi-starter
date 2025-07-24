"""
Application configuration management using Pydantic Settings
Supports environment variables, .env files, and multiple environments
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-based configuration"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        env_ignore_empty=True,
    )

    # Basic app info
    PROJECT_NAME: str = "FastAPI Starter"
    DESCRIPTION: str = "A comprehensive FastAPI scaffolder with best practices"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, production",
    )

    # API Configuration
    API_V1_STR: str = "/api/v1"

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-this-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"]
    )
    ALLOWED_HOSTS: list[str] = Field(default=["localhost", "127.0.0.1"])

    # Database
    DATABASE_URL: str | None = Field(
        default=None, description="Database connection URL"
    )
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")

    # Redis (for caching and rate limiting)
    REDIS_URL: str | None = Field(default=None, description="Redis connection URL")

    # Email configuration
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    # Feature flags
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_METRICS: bool = True
    ENABLE_DOCS: bool = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
