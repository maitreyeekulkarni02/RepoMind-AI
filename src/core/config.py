"""
Centralized application configuration.

Loads configuration from environment variables and .env.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import (
    ASSETS_DIR,
    DATA_DIR,
    GENERATED_DIAGRAMS_DIR,
    GENERATED_DOCS_DIR,
    LOGS_DIR,
    PROJECT_NAME,
    PROJECT_ROOT,
    REPOSITORIES_DIR,
    VECTORSTORE_DIR,
)


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = PROJECT_NAME
    app_version: str = "0.1.0"
    debug: bool = False

    google_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="GOOGLE_API_KEY",
    )

    gemini_model: str = "gemini-2.5-flash"
    use_gemini: bool = False
    embedding_model: str = "all-MiniLM-L6-v2"

    host: str = "0.0.0.0"
    port: int = 8501

    max_workers: int = 8
    chunk_size: int = 1200
    chunk_overlap: int = 200

    project_root: Path = PROJECT_ROOT
    repositories_dir: Path = REPOSITORIES_DIR
    data_dir: Path = DATA_DIR
    vectorstore_dir: Path = VECTORSTORE_DIR
    generated_docs_dir: Path = GENERATED_DOCS_DIR
    generated_diagrams_dir: Path = GENERATED_DIAGRAMS_DIR
    logs_dir: Path = LOGS_DIR
    assets_dir: Path = ASSETS_DIR

    def initialize_directories(self) -> None:
        directories = [
            self.repositories_dir,
            self.data_dir,
            self.vectorstore_dir,
            self.generated_docs_dir,
            self.generated_diagrams_dir,
            self.logs_dir,
            self.assets_dir,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.initialize_directories()
    return settings


settings = get_settings()
