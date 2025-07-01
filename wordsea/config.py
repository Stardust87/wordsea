from enum import StrEnum
from pathlib import Path

from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ImageModel(StrEnum):
    FLUX_SCHNELL = "flux-schnell"
    FLUX_DEV = "flux-dev"
    PLAYGROUND = "playground"


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    mongodb_url: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URL",
    )

    openai_api_url: str = Field(
        default="http://localhost:8080/v1",
        description="OpenAI-compatible server base URL",
    )

    api_key: SecretStr = Field(description="API key for authentication")

    language_model_name: str = Field(
        default="mistral-small-3.2",
        description="Name of the language model to use",
    )

    logs_path: Path = Field(
        default=Path("logs"),
        description="Directory path for log files",
    )

    @computed_field
    @property
    def logs_path_created(self) -> Path:
        """Ensure logs directory exists and return the path."""
        self.logs_path.mkdir(parents=True, exist_ok=True)
        return self.logs_path


# Global settings instance
settings = Settings()
