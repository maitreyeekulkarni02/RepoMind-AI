import streamlit as st
import logging

from src.core.logger import get_logger
from src.services.search_service import SearchService
from src.utils.chunking import DocumentChunk


logger = get_logger(__name__)


def render_page() -> None:
    """
    Renders the Semantic Search page.
    Allows users to search the repository using natural language.
    """
    st.title("🔎 Semantic Search")
    st.subheader("Search across your repository's knowledge base")

    search_query = st.text_input(
        "Enter your search query:",
        placeholder="e.g., 'how do I add a new service?' or 'where is the database configured?'",
        key="semantic_search_query",
    )

    search_button = st.button("Search", key="semantic_search_button")

    if search_button and search_query:
        search_service = SearchService()
        logger.info("Semantic search initiated for query: '%s'", search_query)

        try:
            with st.spinner("Searching for relevant code and documentation..."):
                # SearchService.search is expected to return a list of (DocumentChunk, score) tuples
                results = search_service.search(query=search_query)

            if not results:
                st.info("No results found for your query.")
                logger.info("No semantic search results found for query: '%s'", search_query)
            else:
                st.success(f"Found {len(results)} relevant results:")
                for i, (chunk, score) in enumerate(results):
                    if not isinstance(chunk, DocumentChunk) or not isinstance(score, float):
                        logger.warning(
                            "Unexpected search result format: chunk type %s, score type %s",
                            type(chunk),
                            type(score),
                        )
                        continue

                    with st.expander(f"**{chunk.file_path}** (Relevance: {score:.2f})"):
                        st.markdown(f"**File Path:** `{chunk.file_path}`")
                        st.markdown(f"**Relevance Score:** `{score:.4f}`")

                        content_lines = chunk.content.splitlines()
                        if content_lines:
                            st.subheader("Content Excerpt:")
                            st.code("\n".join(content_lines[:20]))
                            if len(content_lines) > 20:
                                st.markdown("... (truncated)")
                        else:
                            st.info("No content available for this chunk.")

                logger.info("Semantic search results displayed for query: '%s'", search_query)

        except Exception as e:
            st.error(f"An error occurred during search: {e}")
            logger.exception("Error during semantic search for query: '%s'", search_query)
    elif search_button and not search_query:
        st.warning("Please enter a search query to proceed.")
