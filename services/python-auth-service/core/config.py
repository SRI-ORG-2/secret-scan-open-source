import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ShopFlow Auth Service"
    debug: bool = False

    # Database
    database_url: str = "postgresql://shopflow_admin:Sup3rS3cr3t_PgPass!2024@localhost:5432/shopflow"

    # Redis
    redis_url: str = "redis://:r3d1s_P@ssw0rd_shopflow@localhost:6379/0"

    # JWT
    jwt_secret: str = "my-super-secret-jwt-key-that-should-be-very-long-and-random-2024!shopflow"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    jwt_refresh_secret: str = "refresh-secret-shopflow-2024-do-not-share-xK9pLmNqRtUvWxYzABCDEF"

    # SendGrid
    sendgrid_api_key: str = "SG.xK9pLmNqRtUvWxYz.0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO"
    sendgrid_from_email: str = "noreply@shopflow.com"

    # Twilio
    twilio_account_sid: str = "AC1234567890abcdef1234567890abcdef"
    twilio_auth_token: str = "1234567890abcdef1234567890abcdef"
    twilio_phone_number: str = "+15551234567"

    # Google OAuth
    google_client_id: str = "123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com"
    google_client_secret: str = "GOCSPX-xK9pLmNqRtUvWxYzAbCdEfGhIjKl"

    # GitHub OAuth
    github_client_id: str = "Iv1.abc123def456abc1"
    github_client_secret: str = "abc123def456abc123def456abc123def456abc1"

    class Config:
        env_file = ".env"


settings = Settings()
