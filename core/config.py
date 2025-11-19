"""Configuration management for the AI Agent Collective."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Environment
    environment: str = Field(default="development")

    # Database
    database_url: str = Field(default="postgresql://personas:personas_dev_password@localhost:5432/personas")
    redis_url: str = Field(default="redis://localhost:6379/0")

    # AI Services
    anthropic_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)

    # Image Generation
    midjourney_api_key: Optional[str] = Field(default=None)
    sd_api_url: Optional[str] = Field(default=None)

    # Social Media - Twitter
    twitter_api_key: Optional[str] = Field(default=None)
    twitter_api_secret: Optional[str] = Field(default=None)
    twitter_access_token: Optional[str] = Field(default=None)
    twitter_access_secret: Optional[str] = Field(default=None)
    twitter_bearer_token: Optional[str] = Field(default=None)

    # Social Media - Instagram
    instagram_username: Optional[str] = Field(default=None)
    instagram_password: Optional[str] = Field(default=None)

    # Social Media - Discord
    discord_bot_token: Optional[str] = Field(default=None)

    # Content Generation
    runway_api_key: Optional[str] = Field(default=None)
    eleven_labs_api_key: Optional[str] = Field(default=None)
    suno_api_key: Optional[str] = Field(default=None)

    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None)

    # Agent Configuration (Updated November 2025)
    default_model: str = Field(default="claude-sonnet-4-5-20250929")  # Latest Sonnet 4.5 model
    max_tokens_per_request: int = Field(default=4096)
    agent_timezone: str = Field(default="America/New_York")

    # Safety & Limits
    max_daily_cost_usd: float = Field(default=50.0)
    enable_content_moderation: bool = Field(default=True)
    require_human_approval: bool = Field(default=True)

    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/app.log")

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
