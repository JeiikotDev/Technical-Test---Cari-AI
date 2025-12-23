"""Application-wide configuration constants."""

from functools import lru_cache
import json
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_PATH = ROOT_DIR / "resources" / "knowledge_base.json"
DEFAULT_FALLBACK_SUGGESTION = (
    "No encontré una coincidencia exacta, ¿podrías darme más detalles?"
)


def _safe_json_loads(value: str) -> object:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_json_loads=_safe_json_loads,
    )

    env: str = "dev"
    knowledge_base_path: Path = KNOWLEDGE_BASE_PATH
    fallback_message: str = DEFAULT_FALLBACK_SUGGESTION
    cors_origins: list[str] = Field(default_factory=list)
    api_v1_prefix: str = "/api/v1"
    docs_enabled: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            if not value.strip():
                return []
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return value
        return []


@lru_cache
def get_settings() -> Settings:
    return Settings()
