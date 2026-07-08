"""Repository intelligence engine for RepoMind AI Enterprise."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.logger import logger
from src.utils.file_utils import discover_files, get_file_extension
from src.utils.chunking import TextChunker
from src.services.embedding_service import EmbeddingService
from src.vectorstore.faiss_store import FAISSVectorStore


class RepositoryIntelligence:
    """
    Main repository analysis engine.

    Responsibilities:
    - Scan repository
    - Extract files
    - Generate chunks
    - Create embeddings
    - Build searchable knowledge base
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: FAISSVectorStore | None = None,
    ) -> None:

        self.embedding_service = embedding_service or EmbeddingService()

        self.vector_store = vector_store or FAISSVectorStore()

        self.chunker = TextChunker()

        logger.info("RepositoryIntelligence initialized")

    def analyze(
        self,
        repository_path: str,
    ) -> dict[str, Any]:
        """
        Analyze repository and create knowledge base.
        """

        root = Path(repository_path)

        logger.info(
            "Analyzing repository: %s",
            root,
        )

        files = discover_files(root)

        chunks = []
        metadata = []

        for file in files:

            try:

                content = file.read_text(encoding="utf-8")

            except Exception:

                logger.warning(
                    "Skipping unreadable file: %s",
                    file,
                )

                continue

            file_chunks = self.chunker.split_text(content)

            for chunk in file_chunks:

                # Keep DocumentChunk object
                # because embedding_service expects chunk.content
                chunks.append(chunk)

                metadata.append(
                    {
                        "file": str(file),
                        "extension": get_file_extension(file),
                        "start_line": chunk.start_line,
                        "end_line": chunk.end_line,
                        "content": chunk.content,
                    }
                )

        if chunks:

            embeddings = self.embedding_service.embed_chunks(chunks)

            self.vector_store.add_embeddings(
                embeddings,
                metadata,
            )

        result = {
            "repository": str(root),
            "files_analyzed": len(files),
            "chunks_created": len(chunks),
        }

        logger.info(
            "Repository analysis completed: %s",
            result,
        )

        return result
