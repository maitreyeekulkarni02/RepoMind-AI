"""
Application-wide constants for RepoMind AI Enterprise.

This module contains immutable values shared across the application.
Avoid hardcoding these values in business logic.
"""

from pathlib import Path

# ==========================================================
# Project Information
# ==========================================================

PROJECT_NAME = "RepoMind AI Enterprise"
PROJECT_VERSION = "0.1.0"

# ==========================================================
# Root Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
REPOSITORIES_DIR = PROJECT_ROOT / "repositories"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"
GENERATED_DOCS_DIR = PROJECT_ROOT / "generated_docs"
GENERATED_DIAGRAMS_DIR = PROJECT_ROOT / "generated_diagrams"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# ==========================================================
# Repository Settings
# ==========================================================

SUPPORTED_REPOSITORY_EXTENSIONS = {
    ".zip",
}

SUPPORTED_SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".kt",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".scala",
    ".sql",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".xml",
    ".sh",
    ".bat",
    ".ps1",
    ".dockerfile",
}

# ==========================================================
# Ignored Directories
# ==========================================================

IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    "bin",
    "obj",
    ".next",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

# ==========================================================
# Ignored Files
# ==========================================================

IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

# ==========================================================
# Chunking
# ==========================================================

DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200

# ==========================================================
# Embedding
# ==========================================================

DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================================================
# Gemini
# ==========================================================

DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"

# ==========================================================
# Limits
# ==========================================================

MAX_FILE_SIZE_MB = 5
MAX_FILES_TO_PROCESS = 10000

# ==========================================================
# Logging
# ==========================================================

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

LOG_FILE_NAME = "repomind.log"
