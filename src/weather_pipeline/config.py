from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    weather_api_key: str = Field(..., alias="WEATHER_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
