from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # ── Application ───────────────────────────────────────────────────────────
    app_name: str = "HireMindAI API"
    environment: str = "local"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    # Comma-separated CORS origins, e.g. "http://localhost:3000,http://localhost:5173"
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins.",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = "postgresql+psycopg://hiremind:hiremind@localhost:5432/hiremind"

    # ── JWT / Auth ────────────────────────────────────────────────────────────
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # ── Google Gemini (AI) ────────────────────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # ── Qdrant Vector Database ────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "candidates"

    # ── File Storage ──────────────────────────────────────────────────────────
    local_storage_path: str = "./storage"
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10 MB

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> Any:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
            if normalized in {"debug", "dev", "development", "local"}:
                return True
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list (split from the comma-separated string)."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
