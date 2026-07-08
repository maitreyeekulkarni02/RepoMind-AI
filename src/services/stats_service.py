"""
Statistics service for analyzing repositories.

This module provides functionality to generate repository statistics,
including file counts, language distribution, Python code metrics,
and general repository information.
"""

from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path
from typing import Any
from src.utils.file_utils import discover_files
from src.core.logger import get_logger

logger = get_logger(__name__)


class StatsService:
    """
    Service responsible for generating repository statistics.
    """

    _IGNORE_DIRS: set[str] = {
        ".git",
        ".venv",
        ".venv-1",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".idea",
        ".vscode",
        "node_modules",
        "build",
        "dist",
        "vectorstore",
        "docs",
    }

    _LANGUAGE_MAP: dict[str, str] = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript React",
        ".jsx": "JavaScript React",
        ".java": "Java",
        ".kt": "Kotlin",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".c": "C",
        ".h": "C Header",
        ".hpp": "C++ Header",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".scala": "Scala",
        ".r": "R",
        ".sh": "Shell",
        ".ps1": "PowerShell",
        ".html": "HTML",
        ".htm": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".sass": "SASS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".xml": "XML",
        ".md": "Markdown",
        ".txt": "Text",
        ".toml": "TOML",
        ".ini": "INI",
        ".cfg": "Config",
        ".sql": "SQL",
        ".dockerfile": "Dockerfile",
    }

    def __init__(self) -> None:
        """
        Initialize the statistics service.
        """
        logger.info("StatsService initialized")

    def generate_statistics(self, repository_path: str) -> dict[str, Any]:
        """
        Generate repository statistics.

        Args:
            repository_path: Path to the repository.

        Returns:
            Dictionary containing repository statistics.
        """
        try:
            repo_path = Path(repository_path).resolve()

            if not repo_path.exists() or not repo_path.is_dir():
                raise FileNotFoundError(f"Repository not found: {repo_path}")

            total_files = 0
            python_files = 0
            total_lines = 0
            total_classes = 0
            total_functions = 0
            total_imports = 0

            largest_file = ""
            largest_file_lines = 0

            language_counter: Counter[str] = Counter()

            for file_path in discover_files(repo_path):
                total_files += 1

                language = self._detect_language(file_path)
                language_counter[language] += 1

                try:
                    line_count = self._count_lines(file_path)
                except Exception as exc:
                    logger.warning(
                        "Failed to read file %s: %s",
                        file_path,
                        exc,
                    )
                    continue

                total_lines += line_count

                if line_count > largest_file_lines:
                    largest_file_lines = line_count
                    try:
                        largest_file = str(file_path.relative_to(repo_path))
                    except ValueError:
                        largest_file = str(file_path)

                if file_path.suffix.lower() == ".py":
                    python_files += 1

                    try:
                        metrics = self._analyze_python_file(file_path)
                        total_classes += metrics["classes"]
                        total_functions += metrics["functions"]
                        total_imports += metrics["imports"]
                    except Exception as exc:
                        logger.warning(
                            "Failed to analyze Python file %s: %s",
                            file_path,
                            exc,
                        )

            average_lines = round(total_lines / total_files, 2) if total_files else 0.0

            return {
                "repository": repo_path.name,
                "python_files": python_files,
                "total_files": total_files,
                "total_lines": total_lines,
                "classes": total_classes,
                "functions": total_functions,
                "imports": total_imports,
                "average_lines_per_file": average_lines,
                "largest_file": largest_file,
                "largest_file_lines": largest_file_lines,
                "languages": dict(sorted(language_counter.items())),
            }

        except Exception as exc:
            logger.exception("Failed to generate repository statistics: %s", exc)

            return {
                "repository": Path(repository_path).name,
                "python_files": 0,
                "total_files": 0,
                "total_lines": 0,
                "classes": 0,
                "functions": 0,
                "imports": 0,
                "average_lines_per_file": 0.0,
                "largest_file": "",
                "largest_file_lines": 0,
                "languages": {},
                "error": str(exc),
            }

    @staticmethod
    def _count_lines(file_path: Path) -> int:
        """
        Count lines in a file.

        Args:
            file_path: File path.

        Returns:
            Number of lines.
        """
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)

    @staticmethod
    def _analyze_python_file(file_path: Path) -> dict[str, int]:
        """
        Analyze a Python file using AST.

        Args:
            file_path: Python file path.

        Returns:
            Dictionary containing class, function, and import counts.
        """
        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = ast.parse(source)

        classes = 0
        functions = 0
        imports = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports += 1

        return {
            "classes": classes,
            "functions": functions,
            "imports": imports,
        }

    def _detect_language(self, file_path: Path) -> str:
        """
        Detect programming language from file extension.

        Args:
            file_path: File path.

        Returns:
            Language name.
        """
        name = file_path.name.lower()

        if name == "dockerfile":
            return "Dockerfile"

        return self._LANGUAGE_MAP.get(
            file_path.suffix.lower(),
            "Other",
        )
