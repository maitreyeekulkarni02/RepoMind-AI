"""
Embedding service.

Generates vector embeddings for repository content
using Sentence Transformers.
"""

from typing import List

from sentence_transformers import SentenceTransformer

from src.core.config import settings
from src.core.logger import get_logger
from src.utils.chunking import DocumentChunk


logger = get_logger(__name__)


class EmbeddingService:
    """
    Handles text embedding generation.
    """

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        Initialize embedding model.

        Args:
            model_name:
                Sentence Transformer model name.
        """

        self.model_name = model_name or settings.embedding_model

        logger.info(
            "Loading embedding model: %s",
            self.model_name,
        )

        self.model = SentenceTransformer(self.model_name)

        logger.info("Embedding model loaded successfully")

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text:
                Input text.

        Returns:
            Vector embedding.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: List[DocumentChunk],
    ) -> List[List[float]]:
        """
        Generate embeddings for chunks.

        Args:
            chunks:
                Document chunks.

        Returns:
            List of embeddings.
        """

        if not chunks:
            return []

        texts = [chunk.content for chunk in chunks]

        logger.info(
            "Generating embeddings for %s chunks",
            len(texts),
        )

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return [vector.tolist() for vector in embeddings]
