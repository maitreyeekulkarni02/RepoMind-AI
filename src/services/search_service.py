"""
Smart semantic search service for RepoMind AI.
"""

from typing import Any

from src.core.logger import logger
from src.services.retrieval_service import RetrievalService


class SearchService:
    """
    Provides intelligent repository search.
    """

    IGNORE_KEYWORDS = {
        ".aider",
        "legacy",
        "log",
        "cache",
        "metadata",
        "vectorstore",
    }

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
    ) -> None:

        self.retrieval_service = retrieval_service or RetrievalService()

        logger.info("SearchService initialized")

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search repository with semantic ranking.
        """

        logger.info(
            "Searching repository: %s",
            query,
        )

        results = self.retrieval_service.retrieve(
            query=query,
            top_k=top_k * 3,
        )

        query_words = {word.lower() for word in query.split() if len(word) > 2}

        ranked = []

        for item in results:

            metadata = item.get("metadata", {})

            file_name = metadata.get(
                "file",
                "",
            ).lower()

            content = metadata.get(
                "content",
                "",
            ).lower()

            score = item.get(
                "score",
                0,
            )

            boost = 0

            # filename relevance boost
            for word in query_words:

                if word in file_name:
                    boost += 5

                if word in content:
                    boost += 2

            # remove noisy files
            if any(bad in file_name for bad in self.IGNORE_KEYWORDS):
                boost -= 10

            final_score = score - boost

            ranked.append(
                {
                    **item,
                    "ranking_score": final_score,
                }
            )

        ranked.sort(key=lambda x: x["ranking_score"])

        return ranked[:top_k]
