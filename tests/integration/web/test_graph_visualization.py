"""
Integration tests for graph visualization (T043).

Tests end-to-end graph visualization pipeline including:
- Graph service integration
- Relationship graph component
- Export functionality
"""

import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from codeindex.web.services.graph_service import GraphService, GraphNode, GraphEdge


class TestGraphVisualizationIntegration:
    """Integration test suite for graph visualization."""

    @pytest.fixture
    def mock_weaviate_artifacts(self) -> List[Dict[str, Any]]:
        """Mock Weaviate artifacts with relationships."""
        return [
            {
                "id": "presenter_001",
                "type": "GwtPresenter",
                "name": "UserPresenter",
                "file_path": "src/client/UserPresenter.java",
                "relationships": [
                    {"target_id": "view_001", "type": "binds_to"},
                    {"target_id": "service_001", "type": "calls"}
                ]
            },
            {
                "id": "view_001",
                "type": "GwtView",
                "name": "UserView",
                "file_path": "src/client/UserView.java",
                "relationships": [
                    {"target_id": "uibinder_001", "type": "uses_template"}
                ]
            },
            {
                "id": "uibinder_001",
                "type": "GwtUiBinder",
                "name": "UserView.ui.xml",
                "file_path": "src/client/UserView.ui.xml",
                "relationships": []
            },
            {
                "id": "service_001",
                "type": "BackendDoc",
                "name": "UserService",
                "file_path": "src/server/UserService.java",
                "relationships": [
                    {"target_id": "dao_001", "type": "calls"}
                ]
            },
            {
                "id": "dao_001",
                "type": "DaoCall",
                "name": "UserDao",
                "file_path": "src/server/UserDao.java",
                "relationships": [
                    {"target_id": "table_001", "type": "queries"}
                ]
            },
            {
                "id": "table_001",
                "type": "DbTable",
                "name": "users",
                "file_path": "schema/users.sql",
                "relationships": []
            }
        ]

    def test_full_graph_pipeline(self, mock_weaviate_artifacts):
        """Test complete graph visualization pipeline."""
        # Step 1: Build graph from artifacts
        graph_service = GraphService(max_nodes=50)
        nodes, edges = graph_service.build_graph(mock_weaviate_artifacts)

        # Verify graph structure
        assert len(nodes) == 6, "Should create 6 nodes"
        assert len(edges) == 5, "Should create 5 edges"

        # Verify node types
        node_types = {node.node_type for node in nodes}
        expected_types = {"GwtPresenter", "GwtView", "GwtUiBinder", "BackendDoc", "DaoCall", "DbTable"}
        assert node_types == expected_types

        # Verify edges follow relationships
        edge_map = {(edge.source, edge.target): edge.edge_type for edge in edges}
        assert edge_map[("presenter_001", "view_001")] == "binds_to"
        assert edge_map[("presenter_001", "service_001")] == "calls"
        assert edge_map[("view_001", "uibinder_001")] == "uses_template"
        assert edge_map[("service_001", "dao_001")] == "calls"
        assert edge_map[("dao_001", "table_001")] == "queries"

    def test_graph_export_to_cytoscape(self, mock_weaviate_artifacts):
        """Test Cytoscape export format."""
        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(mock_weaviate_artifacts)

        # Export to Cytoscape format
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Verify structure
        assert "elements" in cytoscape_data
        assert "style" in cytoscape_data

        elements = cytoscape_data["elements"]
        assert len(elements) == 11  # 6 nodes + 5 edges

        # Verify node elements have correct structure
        node_elements = [e for e in elements if "source" not in e["data"]]
        assert len(node_elements) == 6

        for node_elem in node_elements:
            assert "id" in node_elem["data"]
            assert "label" in node_elem["data"]
            assert "type" in node_elem["data"]
            assert "color" in node_elem["data"]
            assert "classes" in node_elem

        # Verify edge elements have correct structure
        edge_elements = [e for e in elements if "source" in e["data"]]
        assert len(edge_elements) == 5

        for edge_elem in edge_elements:
            assert "id" in edge_elem["data"]
            assert "source" in edge_elem["data"]
            assert "target" in edge_elem["data"]
            assert "label" in edge_elem["data"]

    def test_graph_export_to_mermaid(self, mock_weaviate_artifacts):
        """Test Mermaid export format."""
        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(mock_weaviate_artifacts)

        # Export to Mermaid format
        mermaid_content = graph_service.export_to_mermaid(nodes, edges)

        # Verify Mermaid syntax
        assert mermaid_content.startswith("graph LR")

        # Verify all nodes are defined
        for node in nodes:
            assert f'{node.id}[' in mermaid_content

        # Verify all edges are defined
        for edge in edges:
            assert f'{edge.source} -->|{edge.edge_type}| {edge.target}' in mermaid_content

    def test_graph_with_circular_dependencies(self):
        """Test handling of circular dependencies in graph."""
        circular_artifacts = [
            {
                "id": "a",
                "type": "BackendDoc",
                "name": "ServiceA",
                "relationships": [{"target_id": "b", "type": "calls"}]
            },
            {
                "id": "b",
                "type": "BackendDoc",
                "name": "ServiceB",
                "relationships": [{"target_id": "c", "type": "calls"}]
            },
            {
                "id": "c",
                "type": "BackendDoc",
                "name": "ServiceC",
                "relationships": [{"target_id": "a", "type": "calls"}]
            }
        ]

        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(circular_artifacts)

        # Should handle circular dependencies without errors
        assert len(nodes) == 3
        assert len(edges) == 3

        # Verify circular edges exist
        edge_map = {(e.source, e.target) for e in edges}
        assert ("a", "b") in edge_map
        assert ("b", "c") in edge_map
        assert ("c", "a") in edge_map

    def test_graph_performance_with_max_nodes_limit(self):
        """Test graph performance with node limit enforcement."""
        # Create 100 artifacts (exceeds max of 50)
        large_artifacts = [
            {
                "id": f"artifact_{i:03d}",
                "type": "BackendDoc",
                "name": f"Service{i}",
                "relationships": [{"target_id": f"artifact_{i+1:03d}", "type": "calls"}]
                if i < 99 else []
            }
            for i in range(100)
        ]

        graph_service = GraphService(max_nodes=50)
        nodes, edges = graph_service.build_graph(large_artifacts)

        # Should limit to max_nodes
        assert len(nodes) == 50
        assert len(edges) <= 49  # Max 49 edges for 50 nodes in chain

    @patch('streamlit.subheader')
    @patch('streamlit.spinner')
    @patch('streamlit.columns')
    @patch('streamlit.caption')
    @patch('streamlit.button')
    @patch('streamlit.checkbox')
    @patch('codeindex.web.components.relationship_graph._render_cytoscape_graph')
    def test_render_relationship_graph_integration(
        self,
        mock_render_cyto,
        mock_checkbox,
        mock_button,
        mock_caption,
        mock_columns,
        mock_spinner,
        mock_subheader,
        mock_weaviate_artifacts
    ):
        """Test full relationship graph rendering integration."""
        from codeindex.web.components.relationship_graph import render_relationship_graph

        # Mock Streamlit components
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()

        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_col4 = Mock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        for col in [mock_col1, mock_col2, mock_col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock()

        mock_button.return_value = False
        mock_checkbox.return_value = True

        # Render graph with pre-loaded artifacts
        render_relationship_graph(
            artifact_id="presenter_001",
            artifact_name="UserPresenter",
            artifacts=mock_weaviate_artifacts
        )

        # Verify rendering was called
        mock_render_cyto.assert_called_once()

        # Verify graph statistics were displayed
        mock_caption.assert_called()
        caption_text = str(mock_caption.call_args)
        assert "6 nodes" in caption_text
        assert "5 edges" in caption_text

    def test_graph_color_coding_by_artifact_type(self, mock_weaviate_artifacts):
        """Test that nodes are color-coded by artifact type."""
        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(mock_weaviate_artifacts)

        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Extract node colors
        node_colors = {}
        for elem in cytoscape_data["elements"]:
            if "source" not in elem["data"]:  # It's a node
                node_type = elem["data"]["type"]
                color = elem["data"]["color"]
                node_colors[node_type] = color

        # Verify different types have different colors
        assert len(set(node_colors.values())) == len(node_colors)

        # Verify expected artifact types are present
        assert "GwtPresenter" in node_colors
        assert "GwtView" in node_colors
        assert "BackendDoc" in node_colors
        assert "DaoCall" in node_colors
        assert "DbTable" in node_colors

    def test_graph_metadata_preservation(self, mock_weaviate_artifacts):
        """Test that artifact metadata is preserved in graph nodes."""
        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(mock_weaviate_artifacts)

        # Find presenter node
        presenter_node = next(n for n in nodes if n.id == "presenter_001")

        # Verify metadata is preserved
        assert "file_path" in presenter_node.metadata
        assert presenter_node.metadata["file_path"] == "src/client/UserPresenter.java"

    def test_graph_with_missing_targets(self):
        """Test graph handling when relationship targets are missing."""
        artifacts_with_missing_targets = [
            {
                "id": "service_001",
                "type": "BackendDoc",
                "name": "UserService",
                "relationships": [
                    {"target_id": "dao_001", "type": "calls"},
                    {"target_id": "nonexistent_999", "type": "calls"}  # Missing target
                ]
            },
            {
                "id": "dao_001",
                "type": "DaoCall",
                "name": "UserDao",
                "relationships": []
            }
        ]

        graph_service = GraphService()
        nodes, edges = graph_service.build_graph(artifacts_with_missing_targets)

        # Should create only 2 nodes (missing target not added)
        assert len(nodes) == 2

        # Should create only 1 edge (to dao_001, not to nonexistent_999)
        assert len(edges) == 1
        assert edges[0].target == "dao_001"

    def test_empty_graph_handling(self):
        """Test handling of empty artifact list."""
        graph_service = GraphService()
        nodes, edges = graph_service.build_graph([])

        assert len(nodes) == 0
        assert len(edges) == 0

        # Export should still work
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)
        assert cytoscape_data["elements"] == []

        mermaid_content = graph_service.export_to_mermaid(nodes, edges)
        assert mermaid_content == "graph LR"
