"""
RAG service.

Combines retrieval and AI reasoning.
"""

from src.services.retrieval_service import RetrievalService
from src.services.ai_service import AIService
from src.core.logger import get_logger


logger = get_logger(__name__)


class RAGService:
    """
    Retrieval Augmented Generation pipeline.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        ai_service: AIService | None = None,
    ) -> None:

        self.retrieval_service = retrieval_service or RetrievalService()

        self.ai_service = ai_service or AIService()

        logger.info("RAGService initialized")

    def ask(
        self,
        question: str,
    ) -> str:

        logger.info(
            "Question: %s",
            question,
        )

        results = self.retrieval_service.retrieve(
            query=question,
            top_k=5,
        )

        logger.info(
            "Retrieved %s results",
            len(results),
        )

        context_parts = []

        for item in results:

            metadata = item.get("metadata", {})

            file = metadata.get("file", "unknown")

            content = metadata.get("content", "")

            context_parts.append(
                f"""
File: {file}

{content}
"""
            )

        context = "\n\n".join(context_parts)

        logger.info(
            "Context length: %s characters",
            len(context),
        )

        return self.ai_service.ask(
            question=question,
            context=context,
        )
