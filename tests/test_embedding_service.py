"""
Tests for RepoMind embedding service.
"""

import pytest

from src.services.embedding_service import EmbeddingService


@pytest.fixture(scope="module")
def embedding_service() -> EmbeddingService:
    """
    Create embedding service fixture.

    Returns:
        Initialized embedding service.
    """

    return EmbeddingService()


def test_embedding_service_initialization(
    embedding_service: EmbeddingService,
) -> None:
    """
    Verify embedding model loads correctly.
    """

    assert embedding_service is not None
    assert embedding_service.model is not None


def test_text_embedding_generation(
    embedding_service: EmbeddingService,
) -> None:
    """
    Verify text converts into vector embedding.
    """

    embedding = embedding_service.embed_text("RepoMind AI Enterprise")

    assert embedding is not None
    assert isinstance(
        embedding,
        list,
    )


def test_embedding_dimension(
    embedding_service: EmbeddingService,
) -> None:
    """
    Verify embedding dimension.

    all-MiniLM-L6-v2 produces
    384 dimensional embeddings.
    """

    embedding = embedding_service.embed_text("software repository analysis")

    assert len(embedding) == 384
