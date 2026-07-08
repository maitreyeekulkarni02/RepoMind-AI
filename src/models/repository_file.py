"""
Repository file data models.

Represents individual files discovered during repository analysis.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field


class RepositoryFile(BaseModel):
    """
    Represents a single file inside a software repository.
    """

    path: Path = Field(description="Absolute or relative file path")

    name: str = Field(description="File name")

    extension: str = Field(description="File extension")

    language: Optional[str] = Field(
        default=None, description="Detected programming language"
    )

    size_bytes: int = Field(default=0, ge=0, description="File size in bytes")

    line_count: int = Field(default=0, ge=0, description="Number of lines in file")

    content_hash: Optional[str] = Field(
        default=None, description="SHA256 hash of file content"
    )

    is_binary: bool = Field(default=False)

    metadata: Dict[str, str] = Field(default_factory=dict)

    indexed: bool = Field(
        default=False, description="Whether embeddings were generated"
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_indexed(self) -> None:
        """
        Mark file as successfully indexed.
        """

        self.indexed = True

    def update_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Add or update file metadata.

        Args:
            key:
                Metadata key.

            value:
                Metadata value.
        """

        self.metadata[key] = value
