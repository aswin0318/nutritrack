"""
Application configuration using Pydantic Settings.
Supports environment-based configuration for local, staging, and production.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "NutriTrack360"
    app_env: str = "development"
    app_debug: bool = False
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # Database
    database_url: str = "postgresql+asyncpg://nutritrack:nutritrack_secret@localhost:5432/nutritrack360"
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    cors_allow_credentials: bool = True

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # AWS
    aws_region: str = "us-east-1"
    aws_rds_endpoint: Optional[str] = None
    aws_elasticache_endpoint: Optional[str] = None

    # URLs
    frontend_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
