import secrets
from typing import Any

from passlib.context import CryptContext
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    prefix: str = Field(default="/api")
    cors_origins: list[str] = Field(default=["*"])
    show_docs: bool = Field(default=True)
    model_config = SettingsConfigDict(env_prefix="API_")


class SentrySettings(BaseSettings):
    dsn: str | None = Field(default=None)
    traces_sample_rate: float = Field(default=0.2)
    env_name: str = Field(default="dev")

    @field_validator("dsn", mode="before")
    @classmethod
    def sentry_dsn_can_be_blank(cls, v: str) -> str | None:
        if v is None or len(v) == 0:
            return None
        return v

    model_config = SettingsConfigDict(env_prefix="SENTRY_")


class DatabaseSettings(BaseSettings):
    dsn: str = Field(default=...)
    model_config = SettingsConfigDict(env_prefix="DB_")


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    sentry: SentrySettings = SentrySettings()
    db: DatabaseSettings = DatabaseSettings()

    class Config:
        extra = "allow"
