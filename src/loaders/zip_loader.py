"""
ZIP repository loader.

Handles uploaded repository archives securely.
"""

from pathlib import Path
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from src.core.config import settings
from src.core.constants import SUPPORTED_REPOSITORY_EXTENSIONS
from src.core.logger import get_logger
from src.models.repository import (
    Repository,
    RepositoryStatus,
    RepositoryType,
)

logger = get_logger(__name__)


class ZipRepositoryLoader:
    """
    Loads repositories from ZIP archives.
    """

    def __init__(
        self,
        destination: Path | None = None,
    ) -> None:
        """
        Initialize ZIP loader.

        Args:
            destination:
                Directory for extracted repositories.
        """

        self.destination = destination or settings.repositories_dir

        self.destination.mkdir(
            parents=True,
            exist_ok=True,
        )

    def extract(
        self,
        zip_path: Path,
    ) -> Repository:
        """
        Extract ZIP repository safely.

        Args:
            zip_path:
                Path to ZIP archive.

        Returns:
            Repository model.

        Raises:
            ValueError:
                Invalid archive format.
            RuntimeError:
                Extraction failure.
        """

        if zip_path.suffix.lower() not in (SUPPORTED_REPOSITORY_EXTENSIONS):
            raise ValueError("Only ZIP repositories are supported")

        repository_id = str(uuid4())

        repository_name = zip_path.stem

        extract_path = self.destination / f"{repository_name}_{repository_id[:8]}"

        extract_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Extracting repository archive: %s",
            zip_path,
        )

        try:
            with ZipFile(zip_path, "r") as archive:
                self._safe_extract(
                    archive,
                    extract_path,
                )

        except BadZipFile as exc:
            logger.exception("Invalid ZIP archive")

            raise RuntimeError("Uploaded file is not a valid ZIP archive") from exc

        except Exception as exc:
            logger.exception("ZIP extraction failed")

            raise RuntimeError("Unable to extract repository archive") from exc

        repository = Repository(
            id=repository_id,
            name=repository_name,
            source=str(zip_path),
            repository_type=RepositoryType.ZIP,
            local_path=extract_path,
            status=RepositoryStatus.LOADING,
        )

        logger.info(
            "Repository extracted successfully: %s",
            extract_path,
        )

        return repository

    def _safe_extract(
        self,
        archive: ZipFile,
        destination: Path,
    ) -> None:
        """
        Secure ZIP extraction.

        Prevents path traversal attacks such as:
        ../../malicious_file

        Args:
            archive:
                Open ZIP archive.

            destination:
                Extraction directory.
        """

        destination = destination.resolve()

        for member in archive.infolist():

            target_path = (destination / member.filename).resolve()

            if not str(target_path).startswith(str(destination)):
                raise RuntimeError("Unsafe ZIP archive detected")

        archive.extractall(destination)
