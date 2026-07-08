"""
Repository data models.

Defines the structure of a software repository handled by RepoMind AI.
"""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class RepositoryStatus(str, Enum):
    """
    Processing lifecycle states of a repository.
    """

    CREATED = "created"
    CLONING = "cloning"
    LOADING = "loading"
    PARSING = "parsing"
    EMBEDDING = "embedding"
    READY = "ready"
    FAILED = "failed"


class RepositoryType(str, Enum):
    """
    Supported repository sources.
    """

    GIT = "git"
    ZIP = "zip"


class Repository(BaseModel):
    """
    Represents a software repository analyzed by RepoMind AI.

    This model is shared between loaders, services,
    vector store, and UI layers.
    """

    id: str = Field(description="Unique repository identifier")

    name: str = Field(description="Repository name")

    source: str = Field(description="Original repository source")

    repository_type: RepositoryType

    local_path: Path

    status: RepositoryStatus = RepositoryStatus.CREATED

    description: Optional[str] = None

    detected_languages: List[str] = Field(default_factory=list)

    total_files: int = 0

    total_lines: int = 0

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """
        Pydantic model configuration.
        """

        arbitrary_types_allowed = True

    def update_status(
        self,
        status: RepositoryStatus,
    ) -> None:
        """
        Update repository processing status.
        """

        self.status = status
        self.updated_at = datetime.now(timezone.utc)
