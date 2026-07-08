from pathlib import Path


IGNORED_DIRS = {
    ".git",
    ".venv",
    ".venv-1",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
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

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}


def discover_files(root: Path):

    files = []

    for path in root.rglob("*"):

        if any(ignored in path.parts for ignored in IGNORED_DIRS):
            continue

        if path.name.startswith(".aider"):
            continue

        if path.name == ".env":
            continue

        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            files.append(path)

    return files


def get_file_extension(file: Path) -> str:
    return file.suffix.lower()
