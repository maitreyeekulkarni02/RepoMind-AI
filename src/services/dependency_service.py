"""
Dependency analysis service.
"""

from pathlib import Path
import ast

from src.core.logger import get_logger

logger = get_logger(__name__)


class DependencyService:

    def __init__(self):

        logger.info("DependencyService initialized")

    def analyze(self, repository_path: str):

        repository = Path(repository_path)

        dependencies = {}

        for file in repository.rglob("*.py"):

            if ".venv" in str(file):
                continue

            try:

                tree = ast.parse(file.read_text(encoding="utf-8"))

            except Exception:

                continue

            imports = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imports.append(node.module)

            dependencies[str(file.relative_to(repository))] = sorted(set(imports))

        return dependencies
