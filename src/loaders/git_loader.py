"""
Git repository loader.

Handles cloning and loading repositories from Git sources.
"""

from pathlib import Path
from uuid import uuid4

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from src.core.config import settings
from src.core.logger import get_logger
from src.models.repository import (
    Repository,
    RepositoryStatus,
    RepositoryType,
)

logger = get_logger(__name__)


class GitRepositoryLoader:
    """
    Loads repositories from Git providers such as GitHub.
    """

    def __init__(
        self,
        destination: Path | None = None,
    ) -> None:
        """
        Initialize Git loader.

        Args:
            destination:
                Directory where repositories are stored.
        """

        self.destination = destination or settings.repositories_dir

        self.destination.mkdir(
            parents=True,
            exist_ok=True,
        )

    def clone(
        self,
        repository_url: str,
    ) -> Repository:
        """
        Clone a Git repository.

        Args:
            repository_url:
                Git clone URL.

        Returns:
            Repository model.

        Raises:
            ValueError:
                If URL is invalid.
            RuntimeError:
                If cloning fails.
        """

        if not repository_url.startswith(
            (
                "http://",
                "https://",
                "git@",
            )
        ):
            raise ValueError("Invalid Git repository URL")

        repository_id = str(uuid4())

        repository_name = repository_url.rstrip("/").split("/")[-1].replace(".git", "")

        local_path = self.destination / f"{repository_name}_{repository_id[:8]}"

        logger.info(
            "Cloning repository: %s",
            repository_url,
        )

        try:
            Repo.clone_from(
                repository_url,
                local_path,
            )

        except GitCommandError as exc:
            logger.exception("Git clone failed")

            raise RuntimeError(f"Unable to clone repository: {exc}") from exc

        except Exception as exc:
            logger.exception("Unexpected cloning error")

            raise RuntimeError("Unexpected repository loading error") from exc

        repository = Repository(
            id=repository_id,
            name=repository_name,
            source=repository_url,
            repository_type=RepositoryType.GIT,
            local_path=local_path,
            status=RepositoryStatus.LOADING,
        )

        logger.info(
            "Repository cloned successfully: %s",
            local_path,
        )

        return repository

    def validate_repository(
        self,
        path: Path,
    ) -> bool:
        """
        Check whether a path contains a valid Git repository.

        Args:
            path:
                Repository path.

        Returns:
            True if valid Git repository.
        """

        try:
            Repo(path)

            return True

        except InvalidGitRepositoryError:
            return False
