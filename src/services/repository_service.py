"""Repository management service for RepoMind AI Enterprise."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.core.logger import logger
from src.models.repository import Repository
from src.parsers.repository_parser import RepositoryParser


class RepositoryService:
    """
    Service layer responsible for repository operations.

    Handles repository validation,
    parsing and metadata generation.
    """

    def __init__(
        self,
        parser: Optional[RepositoryParser] = None,
    ) -> None:
        self.parser = parser or RepositoryParser()

        logger.info("RepositoryService initialized")

    def validate_repository(
        self,
        repository_path: str,
    ) -> bool:
        """
        Validate repository directory.

        Args:
            repository_path:
                Path to repository.

        Returns:
            True if repository is valid.
        """

        path = Path(repository_path)

        valid = path.exists() and path.is_dir()

        logger.info(
            "Repository validation result: %s",
            valid,
        )

        return valid

    def analyze_repository(
        self,
        repository_path: str,
    ) -> Repository:
        """
        Analyze repository and generate metadata.

        Args:
            repository_path:
                Repository location.

        Returns:
            Repository model.
        """

        if not self.validate_repository(repository_path):
            raise ValueError(f"Invalid repository path: {repository_path}")

        logger.info(
            "Analyzing repository: %s",
            repository_path,
        )

        repository = self.parser.parse(Path(repository_path))

        logger.info("Repository analysis completed")

        return repository
