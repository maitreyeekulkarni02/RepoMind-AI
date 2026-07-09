import streamlit as st
from pathlib import Path
import os
import uuid
from typing import List, Optional, Dict, Any

from src.core.logger import get_logger
from src.core.dependencies import get_repository_service
from src.models.repository import RepositoryStatus, RepositoryType, Repository
from src.models.repository_file import RepositoryFile
from src.services.repository_service import RepositoryService


logger = get_logger(__name__)

# --- Mock Data and Utilities (for demonstration purposes) ---
# In a real application, repositories would be listed from a database or a discovery service.
_MOCK_REPOSITORIES_DATA = {
    "repo-1": {
        "id": "repo-1",
        "name": "RepoMind-AI-Example",
        "path": "data/repos/repomind_ai_example",
        "status": RepositoryStatus.INDEXED,
        "type": RepositoryType.GIT,
    },
    "repo-2": {
        "id": "repo-2",
        "name": "Another-Project",
        "path": "data/repos/another_project",
        "status": RepositoryStatus.INDEXED,
        "type": RepositoryType.GIT,
    },
}

# Convert mock data to Repository objects
MOCK_REPOSITORIES: Dict[str, Repository] = {
    repo_id: Repository(**data) for repo_id, data in _MOCK_REPOSITORIES_DATA.items()
}


def _create_mock_repo_files(repo_path: Path):
    """
    Creates dummy files in a mock repository path if they don't exist.
    This ensures RepositoryService has content to parse for demonstration.
    """
    if not repo_path.exists():
        repo_path.mkdir(parents=True, exist_ok=True)

    # Example files and directories
    files_to_create = {
        "README.md": "This is a sample README file for the mock repository.",
        "src/__init__.py": "# Source code init",
        "src/main.py": "def main():\n    print('Hello from main!')\n\nif __name__ == '__main__':\n    main()",
        "src/utils/helpers.py": "def helper_function():\n    return 'Helper data'",
        "docs/ARCHITECTURE.md": "# System Architecture\n\nThis is a dummy architecture document.",
        "tests/test_main.py": "import unittest\nfrom src.main import main\n\nclass TestMain(unittest.TestCase):\n    def test_main(self):\n        # Mock print or capture output if necessary\n        pass\n",
        "config.ini": "[settings]\nkey=value\nenabled=true",
        "requirements.txt": "streamlit\npydantic",
        "data/sample.json": '{"name": "test", "version": 1}',
    }

    for file_path_str, content in files_to_create.items():
        file_path = repo_path / file_path_str
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content)
            logger.info("Created mock file: %s", file_path)


# --- Page Rendering Functions ---
def _render_file_items(
    files_to_render: List[RepositoryFile], key_prefix: str, repository_root_path: Path
):
    """
    Helper to render a list of files with their details.
    """
    for repo_file in sorted(files_to_render, key=lambda f: Path(f.path).name.lower()):
        file_name = Path(repo_file.path).name
        relative_display_path = str(Path(repo_file.path).relative_to(repository_root_path))

        col1, col2, col3, col4 = st.columns([0.5, 0.2, 0.2, 0.1])
        with col1:
            # Display full relative path for clarity, especially in search results
            display_name = relative_display_path if "search" in key_prefix else file_name
            if st.button(display_name, key=f"file_select_{key_prefix}_{repo_file.id}"):
                st.session_state.selected_file_path = repo_file.path
        with col2:
            st.write(f"{repo_file.size} bytes")
        with col3:
            st.write(repo_file.extension)
        with col4:
            st.write("📄")


def _render_folder_tree(
    repository_path: Path, files: List[RepositoryFile], search_query: str = ""
):
    """
    Renders the folder tree and file list, with search filtering.
    """
    st.subheader("Repository Contents")

    # Filter files based on search query
    filtered_files = [
        f for f in files if search_query.lower() in f.path.lower()
    ]

    if not filtered_files and search_query:
        st.info(f"No files found matching '{search_query}'.")
        return
    elif not files:  # No files in repository at all
        st.info("No files found in the repository.")
        return

    if search_query:
        st.write(f"Found {len(filtered_files)} file(s) for '{search_query}':")
        _render_file_items(filtered_files, "search_results", repository_path)
    else:
        # Group files by their top-level directory or directly at root
        root_files = []
        directories = {}  # { "dir_name": [file1, file2, ...], "another_dir": [...] }

        for repo_file in filtered_files:
            relative_path = Path(repo_file.path).relative_to(repository_path)
            if len(relative_path.parts) == 1:  # File directly in root
                root_files.append(repo_file)
            else:  # File in a subdirectory, group by top-level directory
                top_level_dir = relative_path.parts[0]
                if top_level_dir not in directories:
                    directories[top_level_dir] = []
                directories[top_level_dir].append(repo_file)

        # Render root files first
        if root_files:
            with st.expander("Root Files", expanded=True, key="expander_root_files"):
                _render_file_items(root_files, "root", repository_path)

        # Render top-level directories as expanders
        for dir_name in sorted(directories.keys()):
            with st.expander(dir_name, expanded=False, key=f"expander_dir_{dir_name}"):
                # Inside each top-level directory expander, list all files
                # that fall under that directory or its subdirectories.
                _render_file_items(directories[dir_name], dir_name, repository_path)


def _render_file_viewer(selected_file_path: Optional[str]) -> None:
    """
    Renders the file content viewer with syntax highlighting.
    """
    st.subheader("File Content")

    if selected_file_path:
        try:
            with open(selected_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            file_extension = Path(selected_file_path).suffix.lstrip(".")
            # Map common extensions to languages for syntax highlighting
            language_map = {
                "py": "python",
                "js": "javascript",
                "html": "html",
                "css": "css",
                "md": "markdown",
                "json": "json",
                "xml": "xml",
                "sh": "bash",
                "yml": "yaml",
                "yaml": "yaml",
                "txt": "text",
                "c": "c",
                "cpp": "cpp",
                "java": "java",
                "go": "go",
                "rs": "rust",
                "ts": "typescript",
                "jsx": "jsx",
                "tsx": "tsx",
                "ini": "ini",
            }
            language = language_map.get(file_extension.lower(), "text")

            st.code(content, language=language, line_numbers=True)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            logger.error("Error reading file %s: %s", selected_file_path, e)
    else:
        st.info("Select a file from the list to view its contents.")


def render_page() -> None:
    """
    Renders the Repository Explorer page.
    """
    st.title("Repository Explorer")

    # Initialize session state for selected repository and file
    if "selected_repo_id" not in st.session_state:
        st.session_state.selected_repo_id = None
    if "selected_file_path" not in st.session_state:
        st.session_state.selected_file_path = None
    if "explorer_search_query" not in st.session_state:
        st.session_state.explorer_search_query = ""
    if "all_repo_files" not in st.session_state:
        st.session_state.all_repo_files = []
    if "current_repository_path" not in st.session_state:
        st.session_state.current_repository_path = None

    repository_service: RepositoryService = get_repository_service()

    # --- Repository Selector ---
    repo_ids = sorted(list(MOCK_REPOSITORIES.keys()))
    selected_repo_id = st.selectbox(
        "Select a repository:",
        options=[""] + repo_ids,
        format_func=lambda x: MOCK_REPOSITORIES[x].name if x else "--- Select a Repository ---",
        key="repo_selector",
    )

    if selected_repo_id and st.session_state.selected_repo_id != selected_repo_id:
        # Reset selected file if repository changes
        st.session_state.selected_file_path = None
        st.session_state.explorer_search_query = "" # Reset search too
        st.session_state.selected_repo_id = selected_repo_id

    if st.session_state.selected_repo_id:
        selected_repository = MOCK_REPOSITORIES[st.session_state.selected_repo_id]
        st.success(f"Repository '{selected_repository.name}' selected.")

        # Ensure mock repo files exist for parsing
        _create_mock_repo_files(Path(selected_repository.path))

        # Analyze repository only if it hasn't been analyzed or repo changed
        if (
            not st.session_state.all_repo_files
            or st.session_state.current_repository_path != Path(selected_repository.path)
        ):
            try:
                # Get all files for the selected repository
                all_repo_files: List[RepositoryFile] = (
                    repository_service.analyze_repository(selected_repository.path)
                )
                st.session_state.all_repo_files = all_repo_files
                st.session_state.current_repository_path = Path(selected_repository.path)
                logger.info(
                    "Repository analysis complete for %s. Found %d files.",
                    selected_repository.name,
                    len(all_repo_files),
                )
            except Exception as e:
                st.error(f"Error analyzing repository: {e}")
                logger.error(
                    "Error analyzing repository %s: %s", selected_repository.path, e
                )
                st.session_state.all_repo_files = []
                st.session_state.current_repository_path = None
                st.session_state.selected_file_path = None  # Reset selected file
    else:
        st.session_state.selected_repo_id = None
        st.session_state.all_repo_files = []
        st.session_state.current_repository_path = None
        st.session_state.selected_file_path = None  # Reset selected file if no repo


    # --- Layout for Folder Tree / File List and File Viewer ---
    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        if st.session_state.selected_repo_id and st.session_state.all_repo_files:
            # --- Search Files ---
            search_query = st.text_input(
                "Search files (e.g., 'main.py', '.md', 'config'):",
                value=st.session_state.explorer_search_query,
                key="file_search_input",
            )
            st.session_state.explorer_search_query = search_query

            _render_folder_tree(
                st.session_state.current_repository_path,
                st.session_state.all_repo_files,
                st.session_state.explorer_search_query,
            )
        else:
            st.info("Please select a repository to browse its contents.")

    with col2:
        _render_file_viewer(st.session_state.selected_file_path)
