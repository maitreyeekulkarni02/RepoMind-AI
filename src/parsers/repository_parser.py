"""
Repository parser engine.

Scans repositories and extracts structured metadata
from source files.
"""

import hashlib
from pathlib import Path
from typing import List

from src.core.logger import get_logger
from src.models.repository import (
    Repository,
    RepositoryStatus,
)
from src.models.repository_file import RepositoryFile


logger = get_logger(__name__)


class RepositoryParser:
    """
    Parses software repositories into analyzable files.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        ".github",
        ".venv",
        ".venv-1",
        "venv",
        "env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "logs",
        "vectorstore",
        "docs",
    }

    IGNORED_FILES = {
        ".aider.chat.history.md",
        ".aider.input.history",
        "metadata.pkl",
        "index.faiss",
    }

    TEXT_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".cs",
        ".go",
        ".rs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
        ".html",
        ".css",
        ".scss",
        ".sql",
        ".md",
        ".yaml",
        ".yml",
        ".json",
        ".xml",
        ".txt",
    }

    def parse(
        self,
        repository: Repository,
    ) -> List[RepositoryFile]:
        """
        Parse repository files.

        Args:
            repository:
                Repository metadata.

        Returns:
            List of repository files.
        """

        logger.info(
            "Starting repository parsing: %s",
            repository.name,
        )

        repository.status = RepositoryStatus.PARSING

        files = []

        for file_path in self._discover_files(repository.local_path):

            try:
                repository_file = self._create_repository_file(file_path)

                files.append(repository_file)

            except Exception:
                logger.exception(
                    "Failed processing file: %s",
                    file_path,
                )

        repository.total_files = len(files)

        repository.total_lines = sum(file.line_count for file in files)

        repository.status = RepositoryStatus.READY

        logger.info(
            "Repository parsing completed. Files: %s",
            len(files),
        )

        return files

    def _discover_files(
        self,
        root: Path,
    ):
        """
        Discover valid source files.
        """

        for path in root.rglob("*"):

            if any(directory in self.IGNORED_DIRECTORIES for directory in path.parts):
                continue

            if not path.is_file():
                continue

            if path.name in self.IGNORED_FILES:
                continue

            if path.suffix.lower() in self.TEXT_EXTENSIONS:
                yield path

    def _create_repository_file(
        self,
        path: Path,
    ) -> RepositoryFile:
        """
        Create RepositoryFile model.
        """

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return RepositoryFile(
            path=path,
            name=path.name,
            extension=path.suffix,
            size_bytes=path.stat().st_size,
            line_count=len(content.splitlines()),
            content_hash=self._hash_content(content),
        )

    def _hash_content(
        self,
        content: str,
    ) -> str:
        """
        Generate SHA256 hash.
        """

        return hashlib.sha256(content.encode("utf-8")).hexdigest()
