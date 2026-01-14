"""
Files page for GEMINI Code Analysis Pipeline Web UI (Phase 11).

This page provides code browsing with:
- File tree navigation
- File content viewer with syntax highlighting
- Search within files
- Jump to line number
- Copy code snippets
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Optional, List

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.utils.config import get_config
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value
)


def initialize_files_state():
    """Initialize session state for files page."""
    defaults = {
        "current_file": None,
        "file_tree": [],
        "file_content": "",
        "file_error": None,
        "search_in_file": "",
        "jump_to_line": None
    }

    initialize_session_state(defaults)


def load_file_tree():
    """Load file tree from source directory."""
    try:
        config = get_config()
        source_dir = config.get("JAVA_SOURCE_DIR")

        if not source_dir:
            set_value("file_error", "JAVA_SOURCE_DIR not configured")
            return

        source_path = Path(source_dir)

        if not source_path.exists():
            set_value("file_error", f"Source directory not found: {source_dir}")
            return

        # Get all source files
        files = []
        for pattern in ["**/*.java", "**/*.jsp", "**/*.xml", "**/*.js"]:
            files.extend(source_path.glob(pattern))

        # Sort and format
        file_list = sorted([str(f.relative_to(source_path)) for f in files])

        set_value("file_tree", file_list)

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to load file tree: {e}")
        set_value("file_error", str(e))


def load_file_content(file_path: str):
    """Load file content."""
    try:
        config = get_config()
        source_dir = Path(config.get("JAVA_SOURCE_DIR"))
        full_path = source_dir / file_path

        if not full_path.exists():
            set_value("file_error", f"File not found: {file_path}")
            return

        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        set_value("current_file", file_path)
        set_value("file_content", content)
        set_value("file_error", None)

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to load file: {e}")
        set_value("file_error", str(e))


def render_file_tree():
    """Render file tree in sidebar."""
    st.sidebar.subheader("🗂️ File Browser")

    # Search files
    search_query = st.sidebar.text_input(
        "Search files",
        placeholder="Filter by filename..."
    )

    file_tree = get("file_tree", [])

    if not file_tree:
        st.sidebar.info("Loading file tree...")
        load_file_tree()
        return

    # Filter files
    if search_query:
        filtered_files = [f for f in file_tree if search_query.lower() in f.lower()]
    else:
        filtered_files = file_tree

    st.sidebar.caption(f"📁 {len(filtered_files)} files")

    # Show files (limit to 100 for performance)
    display_files = filtered_files[:100]

    for file in display_files:
        if st.sidebar.button(f"📄 {Path(file).name}", key=f"file_{file}"):
            load_file_content(file)
            st.rerun()

        st.sidebar.caption(f"   {file}")

    if len(filtered_files) > 100:
        st.sidebar.warning(f"⚠️ Showing first 100 of {len(filtered_files)} files. Use search to narrow down.")


def get_language_from_extension(file_path: str) -> str:
    """Get language for syntax highlighting."""
    ext = Path(file_path).suffix.lower()

    language_map = {
        ".java": "java",
        ".jsp": "jsp",
        ".xml": "xml",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".py": "python",
        ".sql": "sql"
    }

    return language_map.get(ext, "text")


def render_file_viewer():
    """Render file content viewer."""
    current_file = get("current_file")

    if not current_file:
        st.info("👈 Select a file from the sidebar to view its contents")
        return

    # File header
    st.subheader(f"📄 {current_file}")

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        config = get_config()
        source_dir = config.get("JAVA_SOURCE_DIR")
        full_path = Path(source_dir) / current_file
        st.caption(f"**Path**: `{full_path}`")

    with col2:
        # File stats
        if full_path.exists():
            size = full_path.stat().st_size
            st.caption(f"**Size**: {size:,} bytes")

    with col3:
        # Line count
        content = get("file_content", "")
        line_count = content.count('\n') + 1
        st.caption(f"**Lines**: {line_count:,}")

    st.markdown("---")

    # File actions
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🔍 Search in File"):
            set_value("search_in_file", "")  # Toggle search

    with col2:
        if st.button("📋 Copy All"):
            st.code(content, language=get_language_from_extension(current_file))
            st.caption("💡 Use your browser's copy function")

    # Search in file
    if get("search_in_file", "") is not None:
        search_term = st.text_input("Search in file", placeholder="Enter text to search...")

        if search_term:
            lines = content.split('\n')
            matches = []

            for line_no, line in enumerate(lines, 1):
                if search_term.lower() in line.lower():
                    matches.append((line_no, line))

            if matches:
                st.success(f"✅ Found {len(matches)} matches")

                for line_no, line in matches[:20]:  # Limit to 20 matches
                    st.code(f"Line {line_no}: {line.strip()}")

                if len(matches) > 20:
                    st.info(f"Showing first 20 of {len(matches)} matches")
            else:
                st.warning("No matches found")

    # Jump to line
    jump_line = st.number_input(
        "Jump to line",
        min_value=1,
        max_value=line_count,
        value=1,
        step=1
    )

    st.markdown("---")

    # Display file content with syntax highlighting
    language = get_language_from_extension(current_file)

    if jump_line > 1:
        # Show context around target line
        lines = content.split('\n')
        start_line = max(0, jump_line - 10)
        end_line = min(len(lines), jump_line + 10)

        context = '\n'.join(
            f"{i+1:4d} | {lines[i]}"
            for i in range(start_line, end_line)
        )

        st.code(context, language=language)
        st.info(f"📍 Showing lines {start_line+1}-{end_line} (centered on line {jump_line})")

    else:
        # Show entire file
        st.code(content, language=language)


def main():
    """Main files page function."""
    # Page configuration
    st.title("🗂️ Code Browser")

    st.markdown("""
    Browse and search through your indexed source code files.
    """)

    # Initialize session state
    initialize_files_state()

    # Render file tree in sidebar
    render_file_tree()

    # Show error if present
    error = get("file_error")
    if error:
        st.error(f"❌ {error}")

    # Render file viewer
    render_file_viewer()


if __name__ == "__main__":
    main()
