"""
Code explanation service.
"""

import ast
from pathlib import Path

from src.core.logger import get_logger


logger = get_logger(__name__)


class ExplainService:
    """
    Explains Python source files using AST.
    """

    def explain(
        self,
        file_path: str,
    ) -> str:

        path = Path(file_path)

        if not path.exists():

            return f"File not found: {file_path}"

        source = path.read_text(encoding="utf-8-sig")

        tree = ast.parse(source)

        imports = []
        classes = []
        functions = []

        module_docstring = ast.get_docstring(tree) or "No module docstring."

        for node in tree.body:

            if isinstance(
                node,
                ast.Import,
            ):

                for item in node.names:

                    imports.append(item.name)

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                module = node.module or ""

                imports.append(module)

            elif isinstance(
                node,
                ast.ClassDef,
            ):

                methods = []

                for child in node.body:

                    if isinstance(
                        child,
                        ast.FunctionDef,
                    ):

                        methods.append(child.name)

                classes.append(
                    (
                        node.name,
                        methods,
                    )
                )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                functions.append(node.name)

        lines = []

        lines.append("=" * 40)

        lines.append("RepoMind AI Code Explanation")

        lines.append("=" * 40)

        lines.append("")

        lines.append(f"File: {file_path}")

        lines.append("")

        lines.append("Purpose:")

        lines.append(module_docstring)

        lines.append("")

        lines.append("Imports:")

        if imports:

            for item in imports:

                lines.append(f"  • {item}")

        else:

            lines.append("  None")

        lines.append("")

        lines.append("Classes:")

        if classes:

            for cls, methods in classes:

                lines.append(f"  • {cls}")

                for method in methods:

                    lines.append(f"      - {method}()")

        else:

            lines.append("  None")

        lines.append("")

        lines.append("Functions:")

        if functions:

            for func in functions:

                lines.append(f"  • {func}()")

        else:

            lines.append("  None")

        lines.append("")

        lines.append("Summary:")

        lines.append(f"Imports: {len(imports)}")

        lines.append(f"Classes: {len(classes)}")

        lines.append(f"Functions: {len(functions)}")

        logger.info(
            "Explained %s",
            file_path,
        )

        return "\n".join(lines)
