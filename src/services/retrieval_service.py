"""
Retrieval service.

Handles semantic search over repository knowledge.
"""

from typing import Any

from src.core.logger import logger
from src.services.embedding_service import EmbeddingService
from src.vectorstore.faiss_store import FAISSVectorStore


class RetrievalService:
    """
    Hybrid repository retrieval service.

    Uses:
    - Vector similarity
    - Keyword relevance
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: FAISSVectorStore | None = None,
    ) -> None:

        self.embedding_service = embedding_service or EmbeddingService()

        self.vector_store = vector_store or FAISSVectorStore()

        logger.info("RetrievalService initialized")

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        logger.info("Retrieving context for query")

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_embedding,
            k=top_k * 5,
        )

        query_words = {word.lower() for word in query.split()}

        ranked = []

        for item in results:

            metadata = item.get("metadata", {})

            file = metadata.get("file", "")

            content = metadata.get("content", "").lower()

            if ".venv" in file:
                continue

            score = item.get("score", 999)

            keyword_bonus = 0

            for word in query_words:

                if word in file.lower():
                    keyword_bonus += 5

                if word in content:
                    keyword_bonus += 2

            item["final_score"] = score - keyword_bonus

            ranked.append(item)

        ranked.sort(key=lambda x: x["final_score"])

        logger.info("Retrieved %s results", len(ranked[:top_k]))

        return ranked[:top_k]
