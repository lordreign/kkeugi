from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = Field("development", alias="ENVIRONMENT")
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 15
    jwt_refresh_days: int = 30

    google_client_id: str = Field(
        "dev-google-client-id-not-set", alias="GOOGLE_CLIENT_ID",
    )

    anthropic_api_key: str | None = Field(None, alias="ANTHROPIC_API_KEY")
    sentry_dsn: str | None = Field(None, alias="SENTRY_DSN_BACKEND")

    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
