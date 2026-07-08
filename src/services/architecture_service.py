"""
Architecture Intelligence Service for RepoMind AI.
"""

from pathlib import Path
import ast

from src.core.logger import logger


class ArchitectureService:

    IGNORE_DIRS = {
        ".venv",
        ".venv-1",
        ".git",
        "__pycache__",
        "legacy",
        "tests",
    }

    def __init__(self):

        logger.info("ArchitectureService initialized")

    def should_ignore(self, path: Path):

        return any(part in self.IGNORE_DIRS for part in path.parts)

    def analyze_structure(
        self,
        repository_path: str,
    ):

        root = Path(repository_path)

        if not root.exists():

            raise FileNotFoundError(repository_path)

        architecture = {
            "repository": root.name,
            "files": 0,
            "python_files": 0,
            "layers": {},
            "classes": [],
            "functions": [],
        }

        for file in root.rglob("*.py"):

            if self.should_ignore(file):
                continue

            architecture["files"] += 1

            architecture["python_files"] += 1

            relative = file.relative_to(root)

            parts = relative.parts

            layer = parts[0] if len(parts) > 1 else "root"

            if layer not in architecture["layers"]:

                architecture["layers"][layer] = []

            architecture["layers"][layer].append(str(relative))

            try:

                tree = ast.parse(file.read_text(encoding="utf-8"))

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        architecture["classes"].append(
                            {"name": node.name, "file": str(relative)}
                        )

                    if isinstance(node, ast.FunctionDef):

                        architecture["functions"].append(
                            {"name": node.name, "file": str(relative)}
                        )

            except Exception as error:

                logger.warning("Unable to parse %s : %s", file, error)

        return architecture

    def generate_architecture_summary(self, architecture_data):

        repository = architecture_data.get("repository", "Repository")

        layers = architecture_data.get("layers", {})

        classes = architecture_data.get("classes", [])

        functions = architecture_data.get("functions", [])

        summary = []

        summary.append(f"Repository: {repository}")

        summary.append(f"Python Files: {architecture_data.get('python_files',0)}")

        summary.append(f"Layers: {', '.join(layers.keys())}")

        summary.append(f"Classes Detected: {len(classes)}")

        summary.append(f"Functions Detected: {len(functions)}")

        return "\n".join(summary)

    def create_component_graph_data(self, architecture_data):

        graph = {}

        for layer, files in architecture_data.get("layers", {}).items():

            graph[layer] = files

        return graph
