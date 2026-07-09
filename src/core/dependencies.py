from functools import lru_cache

from src.core.config import get_settings
from src.core.logger import get_logger
from src.services.embedding_service import EmbeddingService
from src.services.retrieval_service import RetrievalService
from src.services.ai_service import AIService
from src.services.rag_service import RAGService
from src.services.repository_service import RepositoryService
from src.parsers.repository_parser import RepositoryParser
from src.vectorstore.faiss_store import FAISSVectorStore


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """
    Returns a cached instance of EmbeddingService.
    """
    settings = get_settings()
    model_name = settings.embedding_model
    logger.info("Initializing EmbeddingService with model: %s", model_name)
    return EmbeddingService(model_name=model_name)


@lru_cache(maxsize=1)
def get_ai_service() -> AIService:
    """
    Returns a cached instance of AIService.
    """
    settings = get_settings()
    model_name = settings.gemini_model # Assuming AIService uses gemini_model from config
    logger.info("Initializing AIService with model: %s", model_name)
    return AIService(model_name=model_name)


@lru_cache(maxsize=1)
def get_retrieval_service() -> RetrievalService:
    """
    Returns a cached instance of RetrievalService.
    """
    embedding_service = get_embedding_service()
    vector_store = FAISSVectorStore() # Assuming default initialization is sufficient
    logger.info("Initializing RetrievalService.")
    return RetrievalService(embedding_service=embedding_service, vector_store=vector_store)


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    """
    Returns a cached instance of RAGService.
    """
    retrieval_service = get_retrieval_service()
    ai_service = get_ai_service()
    logger.info("Initializing RAGService.")
    return RAGService(retrieval_service=retrieval_service, ai_service=ai_service)


@lru_cache(maxsize=1)
def get_repository_service() -> RepositoryService:
    """
    Returns a cached instance of RepositoryService.
    """
    repository_parser = RepositoryParser()
    return RepositoryService(parser=repository_parser)
