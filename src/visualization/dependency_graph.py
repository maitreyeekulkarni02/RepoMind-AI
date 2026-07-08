"""Dependency graph builder for RepoMind AI Enterprise."""

from __future__ import annotations

from typing import Any

import networkx as nx

from src.core.logger import logger


class DependencyGraph:
    """
    Builds and manages repository dependency graphs.

    Uses NetworkX internally and prepares
    graph data for visualization layers.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

        logger.info("DependencyGraph initialized")

    def add_component(
        self,
        component_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Add repository component node.

        Args:
            component_name:
                Component identifier.

            metadata:
                Additional component information.
        """

        self.graph.add_node(
            component_name,
            **(metadata or {}),
        )

        logger.debug(
            "Added component: %s",
            component_name,
        )

    def add_dependency(
        self,
        source: str,
        target: str,
    ) -> None:
        """
        Add directed dependency relation.

        Example:
            service -> model
        """

        self.graph.add_edge(
            source,
            target,
        )

        logger.debug(
            "Added dependency %s -> %s",
            source,
            target,
        )

    def build_from_structure(
        self,
        structure: dict[str, list[str]],
    ) -> None:
        """
        Build graph from architecture mapping.
        """

        logger.info("Building dependency graph")

        for source, targets in structure.items():

            self.add_component(source)

            for target in targets:

                self.add_component(target)

                self.add_dependency(
                    source,
                    target,
                )

    def get_graph_data(
        self,
    ) -> dict[str, Any]:
        """
        Export graph representation.
        """

        return {
            "nodes": list(self.graph.nodes(data=True)),
            "edges": list(self.graph.edges()),
        }

    def get_statistics(
        self,
    ) -> dict[str, int]:
        """
        Return graph statistics.
        """

        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
        }

    def reset(self) -> None:
        """
        Clear dependency graph.
        """

        self.graph.clear()

        logger.info("Dependency graph reset")
