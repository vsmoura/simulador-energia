from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="CLARKE_", env_file=".env", case_sensitive=False)

    environment: str = Field(default="development")
    database_url: str = Field(default="sqlite:///./clark.db")
    app_name: str = Field(default="Clarke Energia API")
    api_version: str = Field(default="v1")
    log_level: str = Field(default="INFO")
    cors_origins: List[str] = Field(default_factory=list)


@lru_cache
def get_settings() -> Settings:
    return Settings()
