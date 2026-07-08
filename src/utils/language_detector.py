"""
Programming language detection utilities.

Provides extension-based language identification.
Designed to be extended later with Tree-sitter parsing.
"""

from pathlib import Path
from typing import Dict, Optional

from src.core.logger import get_logger


logger = get_logger(__name__)


class LanguageDetector:
    """
    Detects programming languages from file paths.
    """

    LANGUAGE_MAP: Dict[str, str] = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript React",
        ".ts": "TypeScript",
        ".tsx": "TypeScript React",
        ".java": "Java",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".kts": "Kotlin Script",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".sql": "SQL",
        ".sh": "Shell",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".json": "JSON",
        ".xml": "XML",
        ".md": "Markdown",
    }

    def detect(
        self,
        file_path: Path,
    ) -> Optional[str]:
        """
        Detect language from file extension.

        Args:
            file_path:
                File path.

        Returns:
            Detected language or None.
        """

        extension = file_path.suffix.lower()

        language = self.LANGUAGE_MAP.get(extension)

        if language:
            return language

        logger.debug(
            "Unknown file extension: %s",
            extension,
        )

        return None

    def is_supported(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check whether file type is supported.

        Args:
            file_path:
                File path.

        Returns:
            True if supported.
        """

        return file_path.suffix.lower() in self.LANGUAGE_MAP
