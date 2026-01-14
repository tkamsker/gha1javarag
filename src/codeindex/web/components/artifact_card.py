"""
Artifact card component for displaying search results (T026 - US1.1).

This component renders individual artifact cards with:
- Artifact type with icon
- Confidence score visualization
- File path display
- Preview snippet
- Metadata (line numbers, etc.)
- Expandable details
"""

import streamlit as st
from typing import Dict, Any, Optional


# Artifact type to icon mapping
ARTIFACT_TYPE_ICONS = {
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


def get_artifact_icon(artifact_type: str) -> str:
    """
    Get icon for artifact type.

    Args:
        artifact_type: Artifact type name

    Returns:
        Icon emoji string
    """
    return ARTIFACT_TYPE_ICONS.get(artifact_type, "📄")


def get_confidence_color(confidence: float) -> str:
    """
    Get color for confidence score.

    Args:
        confidence: Confidence score (0.0 to 1.0)

    Returns:
        Color name (green, orange, red)
    """
    if confidence >= 0.8:
        return "green"
    elif confidence >= 0.5:
        return "orange"
    else:
        return "red"


def truncate_path(file_path: str, max_length: int = 80) -> str:
    """
    Truncate file path if too long.

    Args:
        file_path: Full file path
        max_length: Maximum display length

    Returns:
        Truncated path with ellipsis
    """
    if len(file_path) <= max_length:
        return file_path

    # Split path and show beginning and end
    parts = file_path.split("/")
    if len(parts) > 3:
        return f"/{parts[1]}/.../{parts[-1]}"

    return file_path[:max_length - 3] + "..."


def render_artifact_card(
    artifact: Dict[str, Any],
    show_details: bool = False,
    key: Optional[str] = None
):
    """
    Render artifact card component.

    Args:
        artifact: Artifact data dictionary with fields:
            - id: Artifact ID
            - artifact_type: Type of artifact
            - file_path: Source file path
            - confidence: Confidence score (0.0 to 1.0)
            - preview: Preview snippet text
            - metadata: Optional metadata dict
        show_details: Whether to show expanded details by default
        key: Optional Streamlit key for unique identification
    """
    artifact_id = artifact.get("id", "unknown")
    artifact_type = artifact.get("artifact_type", "Unknown")
    file_path = artifact.get("file_path", "")
    confidence = artifact.get("confidence", 0.0)
    preview = artifact.get("preview", "")
    metadata = artifact.get("metadata", {})

    # Generate unique key if not provided
    if key is None:
        key = f"artifact_{artifact_id}"

    # Get icon and color
    icon = get_artifact_icon(artifact_type)
    confidence_color = get_confidence_color(confidence)

    # Render card container
    with st.container():
        # Card header with artifact type
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        ">
            <h4 style="margin: 0;">{icon} {artifact_type}</h4>
        </div>
        """, unsafe_allow_html=True)

        # Card body with details
        col1, col2 = st.columns([4, 1])

        with col1:
            # File path
            truncated_path = truncate_path(file_path)
            st.caption(f"📁 **File**: `{truncated_path}`")

            # Show full path on hover (use expander)
            if len(file_path) > 80:
                with st.expander("Show full path"):
                    st.code(file_path)

            # Preview snippet
            if preview:
                with st.expander("📄 Preview", expanded=show_details):
                    st.markdown(preview)

            # Metadata
            if metadata:
                line_start = metadata.get("line_start")
                line_end = metadata.get("line_end")

                if line_start is not None and line_end is not None:
                    st.caption(f"📍 **Lines**: {line_start}-{line_end}")

                # Additional metadata
                complexity = metadata.get("complexity")
                if complexity:
                    st.caption(f"⚙️ **Complexity**: {complexity}")

                dependencies = metadata.get("dependencies")
                if dependencies:
                    st.caption(f"🔗 **Dependencies**: {dependencies}")

                test_coverage = metadata.get("test_coverage")
                if test_coverage is not None:
                    st.caption(f"🧪 **Test Coverage**: {test_coverage * 100:.1f}%")

        with col2:
            # Confidence score
            st.metric(
                label="Confidence",
                value=f"{confidence * 100:.1f}%"
            )

            # Visual progress bar
            st.progress(confidence)

            # Color indicator
            if confidence_color == "green":
                st.success("High", icon="✅")
            elif confidence_color == "orange":
                st.warning("Medium", icon="⚠️")
            else:
                st.error("Low", icon="❌")

        # Show Relationships button (T049)
        if st.button(
            "🔗 Relationships",
            key=f"{key}_relationships",
            use_container_width=True
        ):
            st.session_state["show_graph_for"] = artifact_id
            st.session_state["show_graph_name"] = artifact_type
            st.rerun()

        # Divider
        st.markdown("---")


def render_artifact_cards(
    artifacts: list[Dict[str, Any]],
    show_empty_message: bool = True
):
    """
    Render multiple artifact cards.

    Args:
        artifacts: List of artifact dictionaries
        show_empty_message: Whether to show message when no artifacts
    """
    if not artifacts:
        if show_empty_message:
            st.info("ℹ️ No artifacts to display")
        return

    for i, artifact in enumerate(artifacts):
        render_artifact_card(artifact, key=f"artifact_card_{i}")


def render_artifact_grid(
    artifacts: list[Dict[str, Any]],
    columns: int = 2
):
    """
    Render artifacts in a grid layout.

    Args:
        artifacts: List of artifact dictionaries
        columns: Number of columns in grid
    """
    if not artifacts:
        st.info("ℹ️ No artifacts to display")
        return

    # Create columns
    cols = st.columns(columns)

    # Distribute artifacts across columns
    for i, artifact in enumerate(artifacts):
        col_idx = i % columns

        with cols[col_idx]:
            render_artifact_card(artifact, key=f"grid_artifact_{i}")


def render_compact_artifact_card(artifact: Dict[str, Any]):
    """
    Render compact version of artifact card (for dense displays).

    Args:
        artifact: Artifact data dictionary
    """
    artifact_type = artifact.get("artifact_type", "Unknown")
    file_path = artifact.get("file_path", "")
    confidence = artifact.get("confidence", 0.0)

    icon = get_artifact_icon(artifact_type)
    truncated_path = truncate_path(file_path, max_length=60)

    # Single line compact display
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.markdown(f"### {icon}")

    with col2:
        st.markdown(f"**{artifact_type}**")
        st.caption(truncated_path)

    with col3:
        st.metric("", f"{confidence * 100:.0f}%")


def render_artifact_list(
    artifacts: list[Dict[str, Any]],
    compact: bool = False
):
    """
    Render artifacts as a list.

    Args:
        artifacts: List of artifact dictionaries
        compact: Whether to use compact card rendering
    """
    if not artifacts:
        st.info("ℹ️ No artifacts to display")
        return

    for i, artifact in enumerate(artifacts):
        if compact:
            render_compact_artifact_card(artifact)
        else:
            render_artifact_card(artifact, key=f"list_artifact_{i}")


# Export main function
__all__ = [
    "render_artifact_card",
    "render_artifact_cards",
    "render_artifact_grid",
    "render_artifact_list",
    "render_compact_artifact_card",
    "get_artifact_icon",
    "get_confidence_color",
    "truncate_path"
]
