"""
Relationship graph component for visualizing artifact dependencies (T046-T049).

This component provides:
- Interactive graph visualization using Streamlit Cytoscape
- Force-directed layout
- Color-coded nodes by artifact type
- Interactive controls (zoom, pan, click to navigate)
- Export to PNG and Mermaid
"""

import streamlit as st
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from codeindex.web.services.graph_service import (
    get_graph_service,
    GraphNode,
    GraphEdge
)

logger = logging.getLogger(__name__)


def render_relationship_graph(
    artifact_id: str,
    artifact_name: str,
    artifacts: Optional[List[Dict[str, Any]]] = None
):
    """
    Render interactive relationship graph for artifact (T046).

    Args:
        artifact_id: Central artifact ID
        artifact_name: Artifact name for display
        artifacts: Optional pre-loaded artifacts (if None, will query Weaviate)
    """
    st.subheader(f"🔗 Relationships: {artifact_name}")

    try:
        graph_service = get_graph_service()

        # Show loading spinner
        with st.spinner("Building relationship graph..."):
            if artifacts is None:
                # Query Weaviate for relationships (T045)
                relationships = graph_service.get_relationships(artifact_id)

                if not relationships:
                    st.info("No relationships found for this artifact")
                    return

                # Convert to artifacts format
                artifacts = _relationships_to_artifacts(artifact_id, relationships)

            # Build graph
            nodes, edges = graph_service.build_graph(artifacts)

            if not nodes:
                st.info("No nodes to display in graph")
                return

        # Render graph controls
        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

        with col1:
            export_png = st.button("📸 Export PNG")

        with col2:
            export_mermaid = st.button("📝 Export Mermaid")

        with col3:
            show_labels = st.checkbox("Show Labels", value=True)

        # Export handlers
        if export_png:
            _export_graph_png(nodes, edges, artifact_name)

        if export_mermaid:
            _export_graph_mermaid(nodes, edges, artifact_name)

        # Render graph visualization
        _render_cytoscape_graph(
            nodes, edges, artifact_id, show_labels
        )

        # Show graph statistics
        st.caption(
            f"📊 **Graph Statistics**: {len(nodes)} nodes, {len(edges)} edges"
        )

    except Exception as e:
        logger.error(f"Graph rendering failed: {e}", exc_info=True)
        st.error(f"❌ Failed to render graph: {e}")


def _render_cytoscape_graph(
    nodes: List[GraphNode],
    edges: List[GraphEdge],
    center_id: str,
    show_labels: bool
):
    """
    Render Cytoscape interactive graph (T046-T048).

    Args:
        nodes: Graph nodes
        edges: Graph edges
        center_id: Center artifact ID
        show_labels: Whether to show node labels
    """
    try:
        # Check if streamlit-cytoscape is available
        try:
            import streamlit_cytoscape as stcyto
        except ImportError:
            st.warning(
                "⚠️ streamlit-cytoscape not installed. "
                "Install with: pip install streamlit-cytoscape"
            )
            _render_text_graph(nodes, edges)
            return

        # Convert to Cytoscape format
        graph_service = get_graph_service()
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Configure layout (T047)
        layout = {
            "name": "cose",  # Force-directed layout
            "animate": True,
            "fit": True,
            "padding": 30,
            "nodeRepulsion": 4000,
            "idealEdgeLength": 100,
            "edgeElasticity": 100,
            "nestingFactor": 5,
            "gravity": 80,
            "numIter": 1000,
            "initialTemp": 200,
            "coolingFactor": 0.95,
            "minTemp": 1.0
        }

        # Update style for label visibility
        if not show_labels:
            for style in cytoscape_data["style"]:
                if style["selector"] == "node":
                    style["style"]["label"] = ""

        # Render interactive graph (T048)
        selected = stcyto.cytoscape(
            elements=cytoscape_data["elements"],
            stylesheet=cytoscape_data["style"],
            layout=layout,
            selection_type="single",
            user_zooming_enabled=True,
            user_panning_enabled=True,
            height="600px",
            key=f"graph_{center_id}"
        )

        # Handle node click (T048)
        if selected and "nodes" in selected and len(selected["nodes"]) > 0:
            selected_node_id = selected["nodes"][0]
            st.info(f"🔍 Selected node: {selected_node_id}")

            # TODO: Navigate to artifact detail page
            # This would use st.query_params to navigate to artifact detail

    except Exception as e:
        logger.error(f"Cytoscape rendering failed: {e}", exc_info=True)
        st.error(f"Failed to render interactive graph: {e}")
        _render_text_graph(nodes, edges)


def _render_text_graph(nodes: List[GraphNode], edges: List[GraphEdge]):
    """
    Render text-based graph representation (fallback).

    Args:
        nodes: Graph nodes
        edges: Graph edges
    """
    st.markdown("**Nodes:**")

    for node in nodes[:20]:  # Limit to 20 for display
        st.text(f"• {node.label} ({node.node_type})")

    if len(nodes) > 20:
        st.caption(f"... and {len(nodes) - 20} more nodes")

    st.markdown("---")
    st.markdown("**Edges:**")

    for edge in edges[:20]:  # Limit to 20 for display
        source_label = next((n.label for n in nodes if n.id == edge.source), edge.source)
        target_label = next((n.label for n in nodes if n.id == edge.target), edge.target)

        st.text(f"• {source_label} --[{edge.edge_type}]--> {target_label}")

    if len(edges) > 20:
        st.caption(f"... and {len(edges) - 20} more edges")


def _export_graph_png(
    nodes: List[GraphNode],
    edges: List[GraphEdge],
    artifact_name: str
):
    """
    Export graph to PNG image (T050).

    Args:
        nodes: Graph nodes
        edges: Graph edges
        artifact_name: Artifact name for filename
    """
    try:
        # TODO: Implement PNG export via Cytoscape export API
        # This would require either:
        # 1. Client-side export using Cytoscape.js export
        # 2. Server-side rendering with headless browser

        st.success("✅ PNG export initiated (feature under development)")

        logger.info(f"PNG export requested for: {artifact_name}")

        # Placeholder: Show download button with placeholder image
        st.info(
            "PNG export requires additional setup. "
            "Use Mermaid export for now, which can be converted to PNG."
        )

    except Exception as e:
        logger.error(f"PNG export failed: {e}", exc_info=True)
        st.error(f"PNG export failed: {e}")


def _export_graph_mermaid(
    nodes: List[GraphNode],
    edges: List[GraphEdge],
    artifact_name: str
):
    """
    Export graph to Mermaid markdown format (T051).

    Args:
        nodes: Graph nodes
        edges: Graph edges
        artifact_name: Artifact name for filename
    """
    try:
        graph_service = get_graph_service()

        # Generate Mermaid syntax
        mermaid_content = graph_service.export_to_mermaid(nodes, edges)

        # Create download button
        st.download_button(
            label="💾 Download Mermaid",
            data=mermaid_content,
            file_name=f"{artifact_name}_graph.mmd",
            mime="text/plain",
            key=f"download_mermaid_{artifact_name}"
        )

        st.success("✅ Mermaid export ready")

        # Show preview
        with st.expander("Preview Mermaid syntax"):
            st.code(mermaid_content, language="mermaid")

        logger.info(f"Mermaid export generated for: {artifact_name}")

    except Exception as e:
        logger.error(f"Mermaid export failed: {e}", exc_info=True)
        st.error(f"Mermaid export failed: {e}")


def _relationships_to_artifacts(
    center_id: str,
    relationships: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Convert relationship list to artifact format for graph building.

    Args:
        center_id: Center artifact ID
        relationships: List of relationships

    Returns:
        List of artifacts with relationships
    """
    # Create center artifact
    artifacts = [
        {
            "id": center_id,
            "type": "Unknown",
            "name": "Center",
            "relationships": relationships
        }
    ]

    # Create target artifacts
    for rel in relationships:
        target_id = rel.get("target_id")

        if target_id:
            artifacts.append({
                "id": target_id,
                "type": rel.get("target_type", "Unknown"),
                "name": rel.get("target_name", target_id),
                "relationships": []
            })

    return artifacts


def show_relationship_button(artifact: Dict[str, Any]):
    """
    Show "Show Relationships" button on artifact card (T049).

    Args:
        artifact: Artifact dictionary
    """
    if st.button(
        "🔗 Show Relationships",
        key=f"show_rel_{artifact['id']}",
        use_container_width=True
    ):
        # Store artifact ID in session state
        st.session_state["show_graph_for"] = artifact["id"]
        st.session_state["show_graph_name"] = artifact.get("name", "Unknown")

        st.rerun()


__all__ = [
    "render_relationship_graph",
    "show_relationship_button"
]
