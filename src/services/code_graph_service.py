"""
Code dependency graph generation service.
"""

from pathlib import Path
import ast

from src.core.logger import logger


class CodeGraphService:

    def __init__(self):

        logger.info("CodeGraphService initialized")

    def generate_graph(
        self,
        repository_path: str,
    ):

        root = Path(repository_path).resolve()

        graph = {}

        python_files = list(root.rglob("*.py"))

        available_modules = set()

        # Build module index
        for file in python_files:

            if any(x in file.parts for x in [".venv", ".git", "__pycache__"]):
                continue

            relative = file.relative_to(root)

            module = (
                str(relative).replace("\\", ".").replace("/", ".").replace(".py", "")
            )

            if module.endswith(".__init__"):

                module = module.replace(".__init__", "")

            available_modules.add(module)

        # Analyze imports
        for file in python_files:

            if any(x in file.parts for x in [".venv", ".git", "__pycache__"]):
                continue

            relative = file.relative_to(root)

            module_name = (
                str(relative).replace("\\", ".").replace("/", ".").replace(".py", "")
            )

            if module_name.endswith(".__init__"):

                module_name = module_name.replace(".__init__", "")

            dependencies = set()

            try:

                tree = ast.parse(file.read_text(encoding="utf-8-sig"))

                for node in ast.walk(tree):

                    if isinstance(node, ast.Import):

                        for item in node.names:

                            imported = item.name

                            for existing in available_modules:

                                if existing.startswith(imported):

                                    dependencies.add(existing)

                    elif isinstance(node, ast.ImportFrom):

                        if node.module:

                            imported = node.module

                            for existing in available_modules:

                                if existing.startswith(imported):

                                    dependencies.add(existing)

            except Exception as e:

                logger.warning("Failed parsing %s : %s", file, e)

            graph[module_name] = sorted(dependencies)

        return graph

    def generate_mermaid(self, graph):

        lines = ["graph TD"]

        for source, targets in graph.items():

            for target in targets:

                lines.append(f"{source} --> {target}")

        return "\n".join(lines)
