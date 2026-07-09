import streamlit as st

from src.core.logger import get_logger
from src.core.dependencies import get_rag_service


logger = get_logger(__name__)


def render_page() -> None:
    """
    Renders the AI Repository Chat page.
    """

    st.title("AI Repository Chat")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Text input for user's question
    user_query = st.text_area(
        "Ask anything about your repository...",
        key="user_query_input",
        height=100,
    )

    col1, col2 = st.columns([1, 9])

    with col1:
        send_button = st.button("Send")
    with col2:
        clear_button = st.button("Clear Chat")

    if clear_button:
        st.session_state.chat_history = []
        logger.info("Chat history cleared.")
        st.rerun()

    if send_button and user_query:
        # Add user query to history and display immediately
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        logger.info("User query: %s", user_query)

        try:
            with st.spinner("Generating response..."):
                rag_service = get_rag_service()
                ai_response = rag_service.ask(question=user_query)

            # Add AI response to history and display
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            logger.info("AI response generated successfully.")
            st.rerun() # Rerun to clear the input text area and update display properly
        except Exception as e:
            logger.exception("Error during AI chat interaction:")
            st.error(f"An error occurred while processing your request: {e}")
            # Optionally remove the last user message if AI failed to respond
            if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
                st.session_state.chat_history.pop()
