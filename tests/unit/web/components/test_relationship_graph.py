"""
Unit tests for relationship graph component (T041).

Tests graph rendering, exports, and interactive controls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List

from codeindex.web.services.graph_service import GraphNode, GraphEdge


class TestRelationshipGraphRendering:
    """Test suite for relationship graph rendering."""

    @pytest.fixture
    def sample_nodes(self) -> List[GraphNode]:
        """Create sample graph nodes."""
        return [
            GraphNode(id="node1", label="UserPresenter", node_type="GwtPresenter"),
            GraphNode(id="node2", label="UserView", node_type="GwtView"),
            GraphNode(id="node3", label="UserService", node_type="BackendDoc")
        ]

    @pytest.fixture
    def sample_edges(self) -> List[GraphEdge]:
        """Create sample graph edges."""
        return [
            GraphEdge(source="node1", target="node2", edge_type="binds_to"),
            GraphEdge(source="node1", target="node3", edge_type="calls")
        ]

    @patch('streamlit.subheader')
    @patch('streamlit.spinner')
    @patch('streamlit.info')
    @patch('codeindex.web.components.relationship_graph.get_graph_service')
    def test_render_with_no_relationships(
        self,
        mock_get_service,
        mock_info,
        mock_spinner,
        mock_subheader
    ):
        """Test rendering when artifact has no relationships."""
        from codeindex.web.components.relationship_graph import render_relationship_graph

        # Mock service to return empty relationships
        mock_service = Mock()
        mock_service.get_relationships.return_value = []
        mock_get_service.return_value = mock_service

        # Mock spinner context manager
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()

        render_relationship_graph("artifact_001", "TestArtifact")

        # Should show info message about no relationships
        mock_info.assert_called_once()
        assert "No relationships found" in str(mock_info.call_args)

    @patch('streamlit.subheader')
    @patch('streamlit.spinner')
    @patch('streamlit.columns')
    @patch('streamlit.caption')
    @patch('codeindex.web.components.relationship_graph.get_graph_service')
    @patch('codeindex.web.components.relationship_graph._render_cytoscape_graph')
    def test_render_with_artifacts(
        self,
        mock_render_cyto,
        mock_get_service,
        mock_caption,
        mock_columns,
        mock_spinner,
        mock_subheader,
        sample_nodes,
        sample_edges
    ):
        """Test rendering with provided artifacts."""
        from codeindex.web.components.relationship_graph import render_relationship_graph

        # Mock service
        mock_service = Mock()
        mock_service.build_graph.return_value = (sample_nodes, sample_edges)
        mock_get_service.return_value = mock_service

        # Mock spinner context manager
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock()

        # Mock columns
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_col4 = Mock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        # Mock column context managers
        for col in [mock_col1, mock_col2, mock_col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock()

        artifacts = [
            {"id": "art1", "type": "GwtPresenter", "name": "Test", "relationships": []}
        ]

        render_relationship_graph("art1", "TestArtifact", artifacts=artifacts)

        # Should render cytoscape graph
        mock_render_cyto.assert_called_once()

        # Should show graph statistics
        mock_caption.assert_called()
        caption_text = str(mock_caption.call_args)
        assert "3 nodes" in caption_text
        assert "2 edges" in caption_text

    @patch('streamlit.error')
    @patch('streamlit.subheader')
    @patch('streamlit.spinner')
    @patch('codeindex.web.components.relationship_graph.get_graph_service')
    def test_render_handles_errors(
        self,
        mock_get_service,
        mock_spinner,
        mock_subheader,
        mock_error
    ):
        """Test error handling during graph rendering."""
        from codeindex.web.components.relationship_graph import render_relationship_graph

        # Mock service to raise exception
        mock_service = Mock()
        mock_service.get_relationships.side_effect = Exception("Weaviate error")
        mock_get_service.return_value = mock_service

        # Mock spinner context manager
        mock_spinner.return_value.__enter__ = Mock()
        mock_spinner.return_value.__exit__ = Mock(return_value=False)

        render_relationship_graph("artifact_001", "TestArtifact")

        # Should display error
        mock_error.assert_called_once()
        assert "Failed to render graph" in str(mock_error.call_args)


class TestTextGraphFallback:
    """Test suite for text-based graph fallback."""

    @patch('streamlit.markdown')
    @patch('streamlit.text')
    @patch('streamlit.caption')
    def test_render_text_graph(
        self,
        mock_caption,
        mock_text,
        mock_markdown
    ):
        """Test text-based graph rendering."""
        from codeindex.web.components.relationship_graph import _render_text_graph

        nodes = [
            GraphNode(id="n1", label="Service1", node_type="BackendDoc"),
            GraphNode(id="n2", label="DAO1", node_type="DaoCall")
        ]

        edges = [
            GraphEdge(source="n1", target="n2", edge_type="calls")
        ]

        _render_text_graph(nodes, edges)

        # Should show nodes
        assert mock_text.call_count >= 2

        # Should show edges
        calls = [str(call) for call in mock_text.call_args_list]
        assert any("Service1" in call for call in calls)
        assert any("calls" in call for call in calls)

    @patch('streamlit.markdown')
    @patch('streamlit.text')
    @patch('streamlit.caption')
    def test_render_text_graph_truncates_long_lists(
        self,
        mock_caption,
        mock_text,
        mock_markdown
    ):
        """Test that text graph truncates long node/edge lists."""
        from codeindex.web.components.relationship_graph import _render_text_graph

        # Create 30 nodes (more than 20 limit)
        nodes = [
            GraphNode(id=f"n{i}", label=f"Node{i}", node_type="BackendDoc")
            for i in range(30)
        ]

        edges = [
            GraphEdge(source=f"n{i}", target=f"n{i+1}", edge_type="calls")
            for i in range(29)
        ]

        _render_text_graph(nodes, edges)

        # Should show truncation message
        caption_calls = [str(call) for call in mock_caption.call_args_list]
        assert any("10 more nodes" in call for call in caption_calls)
        assert any("9 more edges" in call for call in caption_calls)


class TestGraphExports:
    """Test suite for graph export functionality."""

    @patch('streamlit.success')
    @patch('streamlit.info')
    def test_export_graph_png(
        self,
        mock_info,
        mock_success
    ):
        """Test PNG export functionality."""
        from codeindex.web.components.relationship_graph import _export_graph_png

        nodes = [GraphNode(id="n1", label="Test", node_type="BackendDoc")]
        edges = []

        _export_graph_png(nodes, edges, "TestArtifact")

        # Should show success message (feature under development)
        mock_success.assert_called_once()

    @patch('streamlit.download_button')
    @patch('streamlit.success')
    @patch('streamlit.expander')
    @patch('codeindex.web.components.relationship_graph.get_graph_service')
    def test_export_graph_mermaid(
        self,
        mock_get_service,
        mock_expander,
        mock_success,
        mock_download_button
    ):
        """Test Mermaid export functionality."""
        from codeindex.web.components.relationship_graph import _export_graph_mermaid

        nodes = [
            GraphNode(id="n1", label="Service1", node_type="BackendDoc"),
            GraphNode(id="n2", label="DAO1", node_type="DaoCall")
        ]

        edges = [
            GraphEdge(source="n1", target="n2", edge_type="calls")
        ]

        # Mock service
        mock_service = Mock()
        mock_service.export_to_mermaid.return_value = "graph LR\n    n1[Service1]"
        mock_get_service.return_value = mock_service

        # Mock expander context manager
        mock_expander_instance = Mock()
        mock_expander_instance.__enter__ = Mock(return_value=mock_expander_instance)
        mock_expander_instance.__exit__ = Mock()
        mock_expander.return_value = mock_expander_instance

        _export_graph_mermaid(nodes, edges, "TestArtifact")

        # Should create download button
        mock_download_button.assert_called_once()
        download_call = mock_download_button.call_args

        assert "TestArtifact_graph.mmd" in str(download_call)
        assert "graph LR" in str(download_call)

        # Should show success
        mock_success.assert_called_once()

    @patch('streamlit.error')
    @patch('codeindex.web.components.relationship_graph.get_graph_service')
    def test_export_mermaid_handles_errors(
        self,
        mock_get_service,
        mock_error
    ):
        """Test error handling in Mermaid export."""
        from codeindex.web.components.relationship_graph import _export_graph_mermaid

        # Mock service to raise exception
        mock_service = Mock()
        mock_service.export_to_mermaid.side_effect = Exception("Export failed")
        mock_get_service.return_value = mock_service

        nodes = [GraphNode(id="n1", label="Test", node_type="BackendDoc")]
        edges = []

        _export_graph_mermaid(nodes, edges, "TestArtifact")

        # Should show error
        mock_error.assert_called_once()
        assert "failed" in str(mock_error.call_args).lower()


class TestRelationshipsToArtifacts:
    """Test suite for relationship conversion."""

    def test_convert_relationships_to_artifacts(self):
        """Test converting relationships to artifact format."""
        from codeindex.web.components.relationship_graph import _relationships_to_artifacts

        relationships = [
            {
                "target_id": "target1",
                "target_type": "DaoCall",
                "target_name": "UserDAO",
                "type": "calls"
            },
            {
                "target_id": "target2",
                "target_type": "DbTable",
                "target_name": "users",
                "type": "queries"
            }
        ]

        artifacts = _relationships_to_artifacts("center_id", relationships)

        # Should create center artifact + target artifacts
        assert len(artifacts) == 3

        # Center artifact should have relationships
        center = artifacts[0]
        assert center["id"] == "center_id"
        assert len(center["relationships"]) == 2

        # Target artifacts should have no relationships
        target1 = artifacts[1]
        assert target1["id"] == "target1"
        assert target1["type"] == "DaoCall"
        assert target1["name"] == "UserDAO"
        assert len(target1["relationships"]) == 0

    def test_convert_empty_relationships(self):
        """Test converting empty relationships list."""
        from codeindex.web.components.relationship_graph import _relationships_to_artifacts

        artifacts = _relationships_to_artifacts("center_id", [])

        # Should create only center artifact
        assert len(artifacts) == 1
        assert artifacts[0]["id"] == "center_id"


class TestShowRelationshipButton:
    """Test suite for show relationship button."""

    @patch('streamlit.button')
    @patch('streamlit.session_state', new_callable=dict)
    @patch('streamlit.rerun')
    def test_show_relationship_button_clicked(
        self,
        mock_rerun,
        mock_session_state,
        mock_button
    ):
        """Test clicking show relationships button."""
        from codeindex.web.components.relationship_graph import show_relationship_button

        # Mock button to return True (clicked)
        mock_button.return_value = True

        artifact = {
            "id": "artifact_123",
            "name": "UserService"
        }

        show_relationship_button(artifact)

        # Should store artifact in session state
        assert mock_session_state["show_graph_for"] == "artifact_123"
        assert mock_session_state["show_graph_name"] == "UserService"

        # Should trigger rerun
        mock_rerun.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.session_state', new_callable=dict)
    @patch('streamlit.rerun')
    def test_show_relationship_button_not_clicked(
        self,
        mock_rerun,
        mock_session_state,
        mock_button
    ):
        """Test when show relationships button not clicked."""
        from codeindex.web.components.relationship_graph import show_relationship_button

        # Mock button to return False (not clicked)
        mock_button.return_value = False

        artifact = {
            "id": "artifact_123",
            "name": "UserService"
        }

        show_relationship_button(artifact)

        # Should not modify session state
        assert "show_graph_for" not in mock_session_state

        # Should not trigger rerun
        mock_rerun.assert_not_called()
