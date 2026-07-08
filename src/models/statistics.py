"""
Repository statistics data models.

Contains structured metrics generated during repository analysis.
"""

from typing import Dict, List

from pydantic import BaseModel, Field


class LanguageStatistics(BaseModel):
    """
    Statistics for a programming language detected
    inside a repository.
    """

    language: str = Field(description="Programming language name")

    file_count: int = Field(default=0, ge=0)

    line_count: int = Field(default=0, ge=0)

    percentage: float = Field(default=0.0, ge=0.0, le=100.0)


class RepositoryStatistics(BaseModel):
    """
    Complete repository analytics information.
    """

    total_files: int = Field(default=0, ge=0)

    total_lines: int = Field(default=0, ge=0)

    total_size_bytes: int = Field(default=0, ge=0)

    languages: List[LanguageStatistics] = Field(default_factory=list)

    file_extensions: Dict[str, int] = Field(default_factory=dict)

    largest_files: List[str] = Field(default_factory=list)

    important_files: List[str] = Field(default_factory=list)

    dependency_count: int = Field(default=0, ge=0)

    health_score: float = Field(default=0.0, ge=0.0, le=100.0)

    security_score: float = Field(default=0.0, ge=0.0, le=100.0)

    maintainability_score: float = Field(default=0.0, ge=0.0, le=100.0)

    def add_language(
        self,
        language_stat: LanguageStatistics,
    ) -> None:
        """
        Add language statistics.
        """

        self.languages.append(language_stat)

    def update_health_score(
        self,
        score: float,
    ) -> None:
        """
        Update repository health score.

        Args:
            score:
                Score between 0 and 100.
        """

        self.health_score = max(
            0.0,
            min(score, 100.0),
        )
