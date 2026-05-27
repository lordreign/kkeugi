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

    # Google Play Billing 서버 영수증 검증 (Step 6 실연동). dev는 FakeVerifier.
    google_play_package_name: str = Field(
        "kr.kkeugi.kkeugi", alias="GOOGLE_PLAY_PACKAGE_NAME",
    )
    google_play_service_account_json: str | None = Field(
        None, alias="GOOGLE_PLAY_SERVICE_ACCOUNT_JSON",
    )

    # Mailgun (이메일 채널). 미설정 시 발송 graceful skip.
    mailgun_api_key: str | None = Field(None, alias="MAILGUN_API_KEY")
    mailgun_domain: str | None = Field(None, alias="MAILGUN_DOMAIN")
    mailgun_from: str = Field("끊기 <noreply@kkeugi.kr>", alias="MAILGUN_FROM")

    # FCM (HTTP v1 API + Firebase 서비스계정). 미설정 시 graceful skip.
    fcm_project_id: str | None = Field(None, alias="FCM_PROJECT_ID")
    fcm_service_account_json: str | None = Field(None, alias="FCM_SERVICE_ACCOUNT_JSON")

    # Telegram Bot (wedge #3 multi-channel). BotFather 발급 — Play Console 무관.
    telegram_bot_token: str | None = Field(None, alias="TELEGRAM_BOT_TOKEN")
    telegram_bot_username: str = Field("kkeugi_bot", alias="TELEGRAM_BOT_USERNAME")
    # 웹훅 위변조 방지 (Telegram setWebhook secret_token). 미설정 시 dev에서 검증 skip.
    telegram_webhook_secret: str | None = Field(None, alias="TELEGRAM_WEBHOOK_SECRET")

    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
