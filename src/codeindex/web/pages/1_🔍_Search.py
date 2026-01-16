"""
Search page for GEMINI Code Analysis Pipeline Web UI (T023 - US1.1).

This page provides natural language semantic search over indexed artifacts with:
- Multi-line search input
- Real-time search execution
- Filter by artifact type and project
- Paginated results display with artifact cards
- Loading states and error handling
- Performance logging
"""

import streamlit as st
import sys
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.web.services.search_service import get_search_service
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    update_nested,
    clear_list,
    append_to_list
)
from codeindex.web.utils.url_params import (
    encode_url_params,
    decode_url_params,
    clean_url_params
)
from codeindex.web.components.artifact_card import render_artifact_cards
from codeindex.web.components.relationship_graph import render_relationship_graph
from codeindex.web.components.code_viewer import CodeViewer
from codeindex.web.services.code_service import get_code_service


def restore_state_from_url():
    """Restore search state from URL parameters (T039)."""
    # Get URL query parameters
    query_params = st.query_params

    if not query_params:
        return {}

    # Decode parameters
    try:
        decoded = decode_url_params(dict(query_params))
        return decoded
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to restore state from URL: {e}")
        return {}


def update_url_params():
    """Update URL parameters with current search state (T038)."""
    # Build current state
    params = {
        "query": get("search_query", ""),
        "page": get("search_page", 1),
    }

    # Add filters if present
    filters = get("search_filters", {})
    if filters.get("artifact_types") or filters.get("project"):
        params["filters"] = filters

    # Clean and encode
    params = clean_url_params(params)
    encoded = encode_url_params(params)

    # Update URL without reloading page
    try:
        st.query_params.clear()
        st.query_params.update(encoded)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Failed to update URL params: {e}")


def initialize_search_state():
    """Initialize session state for search page."""
    # First, try to restore from URL (T039)
    url_state = restore_state_from_url()

    # Set defaults
    defaults = {
        "search_query": url_state.get("query", ""),
        "search_results": [],
        "search_total": 0,
        "search_filters": url_state.get("filters", {
            "artifact_types": [],
            "project": None
        }),
        "search_page": url_state.get("page", 1),
        "search_page_size": 50,
        "search_loading": False,
        "search_error": None,
        "search_execution_time": 0,
        "url_restored": False  # Track if we've restored from URL
    }

    initialize_session_state(defaults)

    # If we restored from URL and haven't executed search yet, do it now
    if url_state.get("query") and not get("url_restored", False):
        set_value("url_restored", True)
        # Execute search with restored state
        execute_search()


def render_search_input():
    """Render search input field (T024)."""
    st.subheader("🔍 Natural Language Search")

    st.markdown("""
    Search for artifacts using natural language queries. Examples:
    - "authentication flow"
    - "database access layer"
    - "user management forms"
    - "REST API endpoints"
    """)

    # Search input
    query = st.text_area(
        "Enter your search query",
        value=get("search_query", ""),
        height=100,
        max_chars=2000,
        help="Enter a natural language query to search across all indexed artifacts",
        placeholder="e.g., How is user authentication implemented?"
    )

    # Search button
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

    with col2:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        set_value("search_query", "")
        clear_list("search_results")
        set_value("search_total", 0)
        set_value("search_error", None)
        update_url_params()  # T038: Update URL
        st.rerun()

    if search_clicked and query.strip():
        set_value("search_query", query)
        set_value("search_page", 1)  # Reset to first page
        execute_search()
        st.rerun()

    # Auto-search on Enter (query changed)
    if query != get("search_query", ""):
        set_value("search_query", query)


def render_filters():
    """Render search filters sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Filters")

    search_service = get_search_service()

    # Artifact type filter (T034 - will be implemented in Phase 4)
    artifact_types = search_service.get_artifact_types()

    selected_types = st.sidebar.multiselect(
        "Artifact Types",
        options=artifact_types,
        default=get("search_filters", {}).get("artifact_types", []),
        help="Filter by specific artifact types"
    )

    # Project filter (T035 - will be implemented in Phase 4)
    projects = search_service.get_all_projects()

    selected_project = None
    if projects:
        selected_project = st.sidebar.selectbox(
            "Project",
            options=["All Projects"] + projects,
            index=0,
            help="Filter by specific project"
        )

        if selected_project == "All Projects":
            selected_project = None

    # Update filters in session state
    update_nested("search_filters", "artifact_types", selected_types)
    update_nested("search_filters", "project", selected_project)

    # Apply filters button
    if st.sidebar.button("Apply Filters", use_container_width=True):
        set_value("search_page", 1)  # Reset to first page
        execute_search()
        update_url_params()  # T038: Update URL
        st.rerun()

    # Clear filters button (T037)
    if st.sidebar.button("Clear Filters", use_container_width=True):
        update_nested("search_filters", "artifact_types", [])
        update_nested("search_filters", "project", None)
        set_value("search_page", 1)
        execute_search()
        update_url_params()  # T038: Update URL
        st.rerun()


def execute_search():
    """Execute search with current query and filters (T025)."""
    query = get("search_query", "")
    filters = get("search_filters", {})
    page = get("search_page", 1)
    page_size = get("search_page_size", 50)

    if not query.strip():
        return

    # Set loading state (T028)
    set_value("search_loading", True)
    set_value("search_error", None)

    try:
        # Calculate offset for pagination
        offset = (page - 1) * page_size

        # Get search service
        search_service = get_search_service()

        # Execute search (T025)
        start_time = time.time()

        # Build filters dict (remove empty values)
        search_filters = {}
        if filters.get("artifact_types"):
            search_filters["artifact_types"] = filters["artifact_types"]
        if filters.get("project"):
            search_filters["project"] = filters["project"]

        result = search_service.search(
            query=query,
            filters=search_filters if search_filters else None,
            limit=page_size,
            offset=offset
        )

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Performance logging (T030)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Search executed: query='{query[:50]}...', "
            f"filters={search_filters}, "
            f"results={result['total_results']}, "
            f"time={execution_time:.2f}ms"
        )

        # Update session state with results
        clear_list("search_results")
        for raw_result in result.get("results", []):
            formatted = search_service.format_search_result(raw_result)
            append_to_list("search_results", formatted)

        set_value("search_total", result.get("total_results", 0))
        set_value("search_execution_time", execution_time)

        # Error handling (T029)
        if result.get("error"):
            set_value("search_error", result["error"])

    except Exception as e:
        # Error handling (T029)
        set_value("search_error", str(e))

        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Search failed: {e}", exc_info=True)

    finally:
        # Clear loading state (T028)
        set_value("search_loading", False)

        # Update URL with current state (T038)
        update_url_params()


def render_results():
    """Render search results with pagination (T027)."""
    results = get("search_results", [])
    total = get("search_total", 0)
    loading = get("search_loading", False)
    error = get("search_error")
    execution_time = get("search_execution_time", 0)
    page = get("search_page", 1)
    page_size = get("search_page_size", 50)

    # Show loading spinner (T028)
    if loading:
        with st.spinner("🔍 Searching..."):
            time.sleep(0.1)  # Ensure spinner is visible

    # Show error message (T029)
    if error:
        st.error(f"❌ Search failed: {error}")

        st.markdown("""
        **Troubleshooting**:
        - Check that Weaviate is running at http://localhost:8080
        - Check that Ollama is running at http://localhost:11434
        - Verify your codebase has been indexed using the CLI
        - Check the sidebar for service status
        """)

        if st.button("Retry Search"):
            execute_search()
            st.rerun()

        return

    # Show results summary
    if total > 0:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.metric("Total Results", f"{total:,}")

        with col2:
            st.metric("Execution Time", f"{execution_time:.0f}ms")

        with col3:
            total_pages = (total + page_size - 1) // page_size
            st.metric("Page", f"{page} of {total_pages}")

        st.markdown("---")

    # Show results
    if results:
        for result in results:
            render_artifact_card(result)

        # Pagination controls (T027)
        total_pages = (total + page_size - 1) // page_size

        if total_pages > 1:
            st.markdown("---")

            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

            with col1:
                if page > 1:
                    if st.button("⏮️ First"):
                        set_value("search_page", 1)
                        execute_search()
                        st.rerun()

            with col2:
                if page > 1:
                    if st.button("◀️ Previous"):
                        set_value("search_page", page - 1)
                        execute_search()
                        st.rerun()

            with col3:
                st.markdown(f"<center>Page {page} of {total_pages}</center>", unsafe_allow_html=True)

            with col4:
                if page < total_pages:
                    if st.button("Next ▶️"):
                        set_value("search_page", page + 1)
                        execute_search()
                        st.rerun()

            with col5:
                if page < total_pages:
                    if st.button("Last ⏭️"):
                        set_value("search_page", total_pages)
                        execute_search()
                        st.rerun()

    elif get("search_query", "").strip():
        # No results found
        st.info("ℹ️ No results found for your query.")

        st.markdown("""
        **Tips**:
        - Try different search terms
        - Remove filters to broaden your search
        - Check that your codebase has been indexed
        - Verify service status in the sidebar
        """)


def render_artifact_card(artifact: Dict[str, Any]):
    """Render artifact card component (T026)."""
    # Import will be from actual component when implemented
    # For now, inline implementation

    artifact_type = artifact.get("artifact_type", "Unknown")
    file_path = artifact.get("file_path", "")
    confidence = artifact.get("confidence", 0.0)
    preview = artifact.get("preview", "")
    metadata = artifact.get("metadata", {})

    # Artifact type icon mapping
    icon_map = {
        "DaoCall": "🗄️",
        "GwtPresenter": "🎯",
        "GwtView": "👁️",
        "GwtUiBinder": "📄",
        "DtoArtifact": "📦",
        "IbatisStatement": "📝",
        "DbTable": "🗃️",
        "GwtEndpoint": "🔌",
        "JspForm": "📋",
        "BackendDoc": "📚",
        "JsArtifact": "⚡"
    }

    icon = icon_map.get(artifact_type, "📄")

    # Confidence color
    if confidence >= 0.8:
        confidence_color = "green"
    elif confidence >= 0.5:
        confidence_color = "orange"
    else:
        confidence_color = "red"

    # Render card
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
            <h4>{icon} {artifact_type}</h4>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])

        with col1:
            st.caption(f"📁 **File**: `{file_path}`")

            if preview:
                with st.expander("Preview"):
                    st.markdown(preview)

            if metadata:
                line_start = metadata.get("line_start")
                line_end = metadata.get("line_end")

                if line_start and line_end:
                    st.caption(f"📍 Lines {line_start}-{line_end}")

        with col2:
            st.metric("Confidence", f"{confidence * 100:.1f}%")

            # Visual progress bar
            st.progress(confidence)

        st.markdown("---")


def main():
    """Main search page function."""
    # Page configuration
    st.title("🔍 Semantic Search")

    st.markdown("""
    Search across all indexed artifacts using natural language queries.
    Results are ranked by semantic similarity using AI-powered embeddings.
    """)

    # Initialize session state
    initialize_search_state()

    # Render filters in sidebar
    render_filters()

    # Render search input
    render_search_input()

    # Show code viewer if triggered (T191 - US4.1)
    if "view_source_file" in st.session_state and st.session_state.get("view_source_file"):
        st.markdown("---")

        file_path = st.session_state["view_source_file"]
        artifact_type = st.session_state.get("view_source_artifact_type", "Unknown")
        highlight_lines = st.session_state.get("view_source_highlight_lines", [])

        # Header with close button
        col_h1, col_h2 = st.columns([5, 1])
        with col_h1:
            st.subheader(f"📄 Source Code: {Path(file_path).name}")
            st.caption(f"Type: {artifact_type} | Path: {file_path}")
        with col_h2:
            if st.button("✖️ Close", key="close_code_viewer"):
                st.session_state["view_source_file"] = None
                st.session_state["view_source_artifact_id"] = None
                st.session_state["view_source_highlight_lines"] = []
                st.rerun()

        # Render code viewer
        try:
            code_service = get_code_service()

            # Try to read file content
            try:
                content = code_service.read_file(file_path)
            except Exception as e:
                st.error(f"❌ Could not read file: {e}")
                content = None

            if content:
                # Create code viewer
                viewer = CodeViewer(
                    content=content,
                    file_path=file_path,
                    show_line_numbers=True,
                    highlighted_lines=highlight_lines
                )

                # Render with Streamlit
                viewer.render_streamlit()

                # Download button
                col_d1, col_d2, col_d3 = st.columns([1, 1, 4])
                with col_d1:
                    st.download_button(
                        label="⬇️ Download",
                        data=viewer.get_copy_content(),
                        file_name=Path(file_path).name,
                        mime="text/plain",
                        help="Download source file"
                    )
                with col_d2:
                    # Search in file
                    if st.button("🔍 Search in File", key="search_in_file"):
                        st.session_state["show_file_search"] = True
                        st.rerun()

                # Search functionality
                if st.session_state.get("show_file_search"):
                    search_query = st.text_input("Search in file:", key="file_search_query")
                    if search_query:
                        matches = viewer.search(search_query)
                        if matches:
                            st.success(f"✅ Found {len(matches)} matches")
                            for match in matches[:10]:  # Show first 10
                                st.caption(f"Line {match.line_number}: {match.line_content}")
                        else:
                            st.info("No matches found")

        except Exception as e:
            st.error(f"❌ Error displaying source code: {e}")
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Code viewer error: {e}", exc_info=True)

    # Show relationship graph if triggered (T052)
    if "show_graph_for" in st.session_state and st.session_state["show_graph_for"]:
        st.markdown("---")

        artifact_id = st.session_state["show_graph_for"]
        artifact_name = st.session_state.get("show_graph_name", "Unknown")

        # Close button
        if st.button("✖️ Close Graph"):
            st.session_state["show_graph_for"] = None
            st.rerun()

        # Render graph
        render_relationship_graph(artifact_id, artifact_name)

        # Clear graph state after rendering
        # (keep it so user can refresh)

    # Show results
    st.markdown("---")

    if get("search_query", "").strip():
        st.subheader("📊 Search Results")
        render_results()
    else:
        st.info("👆 Enter a search query above to get started")


if __name__ == "__main__":
    main()
