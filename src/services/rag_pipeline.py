"""RAG pipeline for RepoMind AI Enterprise."""

from __future__ import annotations

from typing import Any

from src.core.logger import logger
from src.services.ai_service import AIService
from src.services.retrieval_service import RetrievalService


class RAGPipeline:
    """
    Retrieval Augmented Generation pipeline.

    Combines:
    - Semantic search
    - Repository context
    - Gemini reasoning
    """

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        ai_service: AIService | None = None,
    ) -> None:

        self.retrieval_service = retrieval_service or RetrievalService()

        self.ai_service = ai_service or AIService()

        logger.info("RAGPipeline initialized")

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Answer repository questions.
        """

        logger.info("Processing RAG query")

        results = self.retrieval_service.retrieve(
            question,
            top_k,
        )

        context = self.retrieval_service.build_context(results)

        prompt = f"""
You are RepoMind AI, an expert software engineer.

Answer the user's question using the repository context.

Repository Context:
{context}


User Question:
{question}


Provide:
- Clear explanation
- Relevant files/classes
- Technical reasoning
"""

        response = self.ai_service.generate_text(prompt)

        return response

    def analyze_repository(
        self,
        repository_summary: dict[str, Any],
    ) -> str:
        """
        Generate high-level repository analysis.
        """

        prompt = f"""
Analyze this software repository.

Repository information:

{repository_summary}

Explain:
- Architecture
- Main components
- Potential improvements
"""

        return self.ai_service.generate_text(prompt)
