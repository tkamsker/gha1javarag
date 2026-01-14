"""
Unit tests for graph service (T040).

Tests relationship extraction, graph building, node/edge creation, and max node limits.
"""

import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from codeindex.web.services.graph_service import GraphService, GraphNode, GraphEdge


class TestGraphService:
    """Test suite for GraphService."""

    @pytest.fixture
    def graph_service(self):
        """Create graph service instance."""
        return GraphService(max_nodes=50)

    @pytest.fixture
    def sample_artifacts(self) -> List[Dict[str, Any]]:
        """Create sample artifacts for testing."""
        return [
            {
                "id": "artifact_001",
                "type": "GwtPresenter",
                "name": "UserPresenter",
                "relationships": [
                    {"target_id": "artifact_002", "type": "binds_to"}
                ]
            },
            {
                "id": "artifact_002",
                "type": "GwtView",
                "name": "UserView",
                "relationships": []
            },
            {
                "id": "artifact_003",
                "type": "BackendDoc",
                "name": "UserService",
                "relationships": [
                    {"target_id": "artifact_004", "type": "calls"}
                ]
            },
            {
                "id": "artifact_004",
                "type": "DaoCall",
                "name": "UserDao",
                "relationships": []
            }
        ]

    def test_initialization(self, graph_service):
        """Test that graph service initializes correctly."""
        assert graph_service is not None
        assert graph_service.max_nodes == 50

    def test_build_graph_from_artifacts(self, graph_service, sample_artifacts):
        """Test building graph from artifacts."""
        nodes, edges = graph_service.build_graph(sample_artifacts)

        # Should create nodes for all artifacts
        assert len(nodes) == 4
        assert all(isinstance(node, GraphNode) for node in nodes)

        # Should create edges from relationships
        assert len(edges) == 2
        assert all(isinstance(edge, GraphEdge) for edge in edges)

    def test_graph_node_creation(self, graph_service):
        """Test creating graph nodes from artifacts."""
        artifact = {
            "id": "test_001",
            "type": "GwtPresenter",
            "name": "TestPresenter",
            "file_path": "src/test/TestPresenter.java"
        }

        node = graph_service._create_node(artifact)

        assert node.id == "test_001"
        assert node.label == "TestPresenter"
        assert node.node_type == "GwtPresenter"
        assert node.metadata["file_path"] == "src/test/TestPresenter.java"

    def test_graph_edge_creation(self, graph_service):
        """Test creating graph edges from relationships."""
        relationship = {
            "target_id": "target_001",
            "type": "calls"
        }

        edge = graph_service._create_edge("source_001", relationship)

        assert edge.source == "source_001"
        assert edge.target == "target_001"
        assert edge.edge_type == "calls"

    def test_max_nodes_limit(self, graph_service):
        """Test that graph respects max node limit."""
        # Create 60 artifacts (over max of 50)
        many_artifacts = [
            {
                "id": f"artifact_{i:03d}",
                "type": "BackendDoc",
                "name": f"Service{i}",
                "relationships": []
            }
            for i in range(60)
        ]

        nodes, edges = graph_service.build_graph(many_artifacts)

        # Should limit to max_nodes
        assert len(nodes) == 50

    def test_extract_relationships(self, graph_service, sample_artifacts):
        """Test relationship extraction from artifacts."""
        nodes, edges = graph_service.build_graph(sample_artifacts)

        # Check that relationships are correctly extracted
        edge_types = [e.edge_type for e in edges]
        assert "binds_to" in edge_types
        assert "calls" in edge_types

    def test_get_relationships_for_artifact(self, graph_service):
        """Test getting relationships for specific artifact."""
        # Mock Weaviate query
        with patch.object(graph_service, '_query_weaviate_relationships') as mock_query:
            mock_query.return_value = [
                {"target_id": "rel_001", "type": "depends_on"},
                {"target_id": "rel_002", "type": "calls"}
            ]

            relationships = graph_service.get_relationships("artifact_001")

            assert len(relationships) == 2
            assert relationships[0]["type"] == "depends_on"

    def test_node_coloring_by_type(self, graph_service):
        """Test that nodes are colored by artifact type."""
        artifact_types = [
            "GwtPresenter",
            "GwtView",
            "BackendDoc",
            "DaoCall",
            "DbTable"
        ]

        for artifact_type in artifact_types:
            artifact = {
                "id": f"test_{artifact_type}",
                "type": artifact_type,
                "name": "Test"
            }

            node = graph_service._create_node(artifact)
            color = graph_service._get_node_color(node.node_type)

            assert color is not None
            assert isinstance(color, str)
            assert color.startswith("#")  # Hex color code

    def test_empty_artifacts_list(self, graph_service):
        """Test handling of empty artifacts list."""
        nodes, edges = graph_service.build_graph([])

        assert len(nodes) == 0
        assert len(edges) == 0

    def test_artifacts_with_no_relationships(self, graph_service):
        """Test artifacts with no relationships."""
        artifacts = [
            {
                "id": "isolated_001",
                "type": "BackendDoc",
                "name": "IsolatedService",
                "relationships": []
            }
        ]

        nodes, edges = graph_service.build_graph(artifacts)

        assert len(nodes) == 1
        assert len(edges) == 0

    def test_circular_relationships(self, graph_service):
        """Test handling of circular relationships."""
        artifacts = [
            {
                "id": "artifact_A",
                "type": "BackendDoc",
                "name": "ServiceA",
                "relationships": [{"target_id": "artifact_B", "type": "calls"}]
            },
            {
                "id": "artifact_B",
                "type": "BackendDoc",
                "name": "ServiceB",
                "relationships": [{"target_id": "artifact_A", "type": "calls"}]
            }
        ]

        nodes, edges = graph_service.build_graph(artifacts)

        # Should handle circular relationships without error
        assert len(nodes) == 2
        assert len(edges) == 2

    def test_filter_by_relationship_type(self, graph_service, sample_artifacts):
        """Test filtering edges by relationship type."""
        nodes, edges = graph_service.build_graph(sample_artifacts)

        # Filter only "calls" relationships
        calls_edges = [e for e in edges if e.edge_type == "calls"]

        assert len(calls_edges) == 1
        assert calls_edges[0].edge_type == "calls"

    def test_node_metadata_preservation(self, graph_service):
        """Test that artifact metadata is preserved in nodes."""
        artifact = {
            "id": "test_001",
            "type": "GwtPresenter",
            "name": "TestPresenter",
            "file_path": "src/test/TestPresenter.java",
            "confidence": 0.95,
            "line_count": 250
        }

        node = graph_service._create_node(artifact)

        assert "file_path" in node.metadata
        assert "confidence" in node.metadata
        assert "line_count" in node.metadata
        assert node.metadata["confidence"] == 0.95

    def test_duplicate_artifact_handling(self, graph_service):
        """Test handling of duplicate artifacts."""
        artifacts = [
            {"id": "dup_001", "type": "BackendDoc", "name": "ServiceA", "relationships": []},
            {"id": "dup_001", "type": "BackendDoc", "name": "ServiceA", "relationships": []}
        ]

        nodes, edges = graph_service.build_graph(artifacts)

        # Should deduplicate by ID
        assert len(nodes) == 1

    def test_invalid_relationship_handling(self, graph_service):
        """Test handling of invalid relationships (target not in graph)."""
        artifacts = [
            {
                "id": "valid_001",
                "type": "BackendDoc",
                "name": "Service",
                "relationships": [
                    {"target_id": "nonexistent_999", "type": "calls"}
                ]
            }
        ]

        nodes, edges = graph_service.build_graph(artifacts)

        # Should skip invalid edges
        assert len(nodes) == 1
        assert len(edges) == 0  # Edge to nonexistent target should be skipped


class TestGraphNode:
    """Test suite for GraphNode data class."""

    def test_graph_node_creation(self):
        """Test creating a graph node."""
        node = GraphNode(
            id="node_001",
            label="TestNode",
            node_type="GwtPresenter",
            metadata={"file_path": "test.java"}
        )

        assert node.id == "node_001"
        assert node.label == "TestNode"
        assert node.node_type == "GwtPresenter"
        assert node.metadata["file_path"] == "test.java"

    def test_graph_node_equality(self):
        """Test graph node equality comparison."""
        node1 = GraphNode(id="node_001", label="Test", node_type="Type")
        node2 = GraphNode(id="node_001", label="Test", node_type="Type")
        node3 = GraphNode(id="node_002", label="Test", node_type="Type")

        assert node1.id == node2.id
        assert node1.id != node3.id


class TestGraphEdge:
    """Test suite for GraphEdge data class."""

    def test_graph_edge_creation(self):
        """Test creating a graph edge."""
        edge = GraphEdge(
            source="node_001",
            target="node_002",
            edge_type="calls"
        )

        assert edge.source == "node_001"
        assert edge.target == "node_002"
        assert edge.edge_type == "calls"

    def test_graph_edge_with_metadata(self):
        """Test graph edge with metadata."""
        edge = GraphEdge(
            source="node_001",
            target="node_002",
            edge_type="depends_on",
            metadata={"weight": 5}
        )

        assert "weight" in edge.metadata
        assert edge.metadata["weight"] == 5
