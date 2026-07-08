"""Text chunking utilities for RepoMind AI Enterprise."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.logger import logger


@dataclass(frozen=True)
class DocumentChunk:
    """
    Represents a chunk of repository content.
    """

    content: str
    start_line: int = 0
    end_line: int = 0
    metadata: dict | None = None


# Backward compatibility
TextChunk = DocumentChunk


class TextChunker:
    """
    Splits repository files into manageable chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk size")

        self.chunk_size = chunk_size
        self.overlap = overlap

        logger.info("TextChunker initialized")

    def split_text(
        self,
        text: str,
    ) -> list[DocumentChunk]:

        if not text.strip():
            return []

        lines = text.splitlines()

        chunks = []

        start = 0

        while start < len(lines):

            end = min(
                start + self.chunk_size,
                len(lines),
            )

            content = "\n".join(lines[start:end])

            chunks.append(
                DocumentChunk(
                    content=content,
                    start_line=start + 1,
                    end_line=end,
                )
            )

            if end == len(lines):
                break

            start = end - self.overlap

        logger.info(
            "Generated %s chunks",
            len(chunks),
        )

        return chunks
