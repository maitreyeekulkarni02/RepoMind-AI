"""
AI service.

Provides reasoning capabilities
for repository intelligence.
"""

from typing import Optional

from src.core.config import settings
from src.core.logger import logger


class AIService:
    """
    Repository reasoning service.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
    ):

        self.model_name = model_name or settings.gemini_model

        self.gemini_active = False

        if settings.google_api_key:

            try:
                from langchain_google_genai import ChatGoogleGenerativeAI

                self.client = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    google_api_key=(settings.google_api_key.get_secret_value()),
                    temperature=0.2,
                )

                self.gemini_active = True

            except Exception:

                self.client = None

        else:

            self.client = None

        logger.info("Gemini active: %s", self.gemini_active)

    def ask(
        self,
        question: str,
        context: str | None = None,
    ) -> str:

        if self.gemini_active:

            from langchain_core.messages import (
                HumanMessage,
                SystemMessage,
            )

            messages = [
                SystemMessage(
                    content="""
                    You are RepoMind AI.

                    You are an expert
                    software architect.

                    Analyze repositories,
                    explain architecture,
                    dependencies,
                    and code flow.
                    """
                ),
                HumanMessage(
                    content=f"""
Question:
{question}


Repository Context:

{context}
"""
                ),
            ]

            response = self.client.invoke(messages)

            return response.content

        return self.local_reasoning(question, context)

    def local_reasoning(
        self,
        question: str,
        context: str | None,
    ) -> str:

        if not context:

            return "No repository context found."

        files = []

        for line in context.splitlines():

            if line.startswith("File:"):
                files.append(line.replace("File:", "").strip())

        answer = []

        answer.append("## RepoMind AI Architecture Analysis\n")

        answer.append("### Repository Components\n")

        for file in files:

            answer.append(f"- {file}")

        answer.append(
            """

### Architecture Flow

1. RepositoryService
   - Validates repository
   - Parses repository metadata


2. Repository Model
   - Maintains repository information
   - Tracks lifecycle states


3. RepositoryIntelligence
   - Discovers files
   - Reads source code
   - Creates chunks
   - Generates embeddings


4. Vector Store
   - Stores embeddings
   - Enables semantic search


5. Retrieval Layer
   - Finds relevant code context


6. AI Layer
   - Generates repository explanations


### Overall Architecture

RepoMind AI follows a modular RAG architecture:

Repository
      |
      v
Repository Intelligence
      |
      v
Chunking + Embeddings
      |
      v
FAISS Vector Database
      |
      v
Semantic Retrieval
      |
      v
AI Reasoning Layer

"""
        )

        return "\n".join(answer)
