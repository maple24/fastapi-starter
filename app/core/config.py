"""
Application configuration management using Pydantic Settings
Supports environment variables, .env files, and multiple environments
"""

from functools import lru_cache

from pydantic import Field
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

    # CORS - stored as strings, converted to lists via computed properties
    BACKEND_CORS_ORIGINS_STR: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        alias="BACKEND_CORS_ORIGINS",
        description="Comma-separated list of CORS origins"
    )
    ALLOWED_HOSTS_STR: str = Field(
        default="localhost,127.0.0.1",
        alias="ALLOWED_HOSTS",
        description="Comma-separated list of allowed hosts"
    )

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

    # LDAP Configuration
    LDAP_ENABLED: bool = Field(default=False, description="Enable LDAP authentication")
    LDAP_SERVER: str | None = Field(default=None, description="LDAP server address (e.g., ldap://ldap.example.com)")
    LDAP_PORT: int = Field(default=389, description="LDAP server port (389 for LDAP, 636 for LDAPS)")
    LDAP_USE_SSL: bool = Field(default=False, description="Use SSL/TLS for LDAP connection")
    LDAP_BIND_DN: str | None = Field(default=None, description="LDAP bind DN for authentication (e.g., cn=admin,dc=example,dc=com)")
    LDAP_BIND_PASSWORD: str | None = Field(default=None, description="LDAP bind password")
    LDAP_BASE_DN: str | None = Field(default=None, description="LDAP base DN for user search (e.g., ou=users,dc=example,dc=com)")
    LDAP_USER_FILTER: str = Field(default="(uid={username})", description="LDAP search filter for users. Use {username} as placeholder")
    LDAP_ATTR_EMAIL: str = Field(default="mail", description="LDAP attribute for email")
    LDAP_ATTR_FULLNAME: str = Field(default="cn", description="LDAP attribute for full name")
    LDAP_TIMEOUT: int = Field(default=10, description="LDAP connection timeout in seconds")

    @property
    def BACKEND_CORS_ORIGINS(self) -> list[str]:
        """Get CORS origins as a list"""
        if self.BACKEND_CORS_ORIGINS_STR:
            return [i.strip() for i in self.BACKEND_CORS_ORIGINS_STR.split(",") if i.strip()]
        return []

    @property
    def ALLOWED_HOSTS(self) -> list[str]:
        """Get allowed hosts as a list"""
        if self.ALLOWED_HOSTS_STR:
            return [i.strip() for i in self.ALLOWED_HOSTS_STR.split(",") if i.strip()]
        return []


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
