"""Mermaid diagram generator for RepoMind AI Enterprise."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.logger import logger


class MermaidGenerator:
    """
    Generates Mermaid architecture diagrams.

    Used by:
    - Architecture viewer
    - Documentation generator
    - Repository analysis reports
    """

    def __init__(
        self,
        output_directory: str = "generated_diagrams",
    ) -> None:
        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info("MermaidGenerator initialized")

    def generate_architecture_diagram(
        self,
        graph_data: dict[str, list[str]],
        filename: str = "architecture.md",
    ) -> str:
        """
        Generate Mermaid flowchart markdown.

        Args:
            graph_data:
                Component relationship mapping.

            filename:
                Output markdown filename.

        Returns:
            Generated file path.
        """

        logger.info("Generating Mermaid architecture diagram")

        lines = [
            "```mermaid",
            "flowchart TD",
        ]

        for source, targets in graph_data.items():

            if not targets:
                lines.append(f"    {source}")

            for target in targets:
                lines.append(f"    {source} --> {target}")

        lines.append("```")

        content = "\n".join(lines)

        output_path = self.output_directory / filename

        output_path.write_text(
            content,
            encoding="utf-8",
        )

        logger.info(
            "Mermaid diagram saved: %s",
            output_path,
        )

        return str(output_path)

    def generate_component_diagram(
        self,
        components: list[dict[str, Any]],
        filename: str = "components.md",
    ) -> str:
        """
        Generate component-only Mermaid diagram.
        """

        graph = {
            "Repository": [
                component.get(
                    "name",
                    "Unknown",
                )
                for component in components
            ]
        }

        return self.generate_architecture_diagram(
            graph,
            filename,
        )
