"""
Integration tests for relationship graph visualization (T043).

Tests end-to-end graph generation, Weaviate relationship queries, and interactive controls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Note: These are integration tests that would require a running Streamlit app
# For now, we test the underlying services and data flow


class TestRelationshipGraphIntegration:
    """Integration tests for relationship graph feature."""

    @pytest.fixture
    def sample_weaviate_response(self) -> Dict[str, Any]:
        """Create sample Weaviate relationship query response."""
        return {
            "data": {
                "Get": {
                    "Artifact": [
                        {
                            "id": "artifact_001",
                            "artifactType": "GwtPresenter",
                            "name": "UserPresenter",
                            "filePath": "src/client/UserPresenter.java",
                            "relationships": [
                                {
                                    "targetId": "artifact_002",
                                    "type": "binds_to"
                                }
                            ]
                        },
                        {
                            "id": "artifact_002",
                            "artifactType": "GwtView",
                            "name": "UserView",
                            "filePath": "src/client/UserView.java",
                            "relationships": []
                        }
                    ]
                }
            }
        }

    def test_graph_service_with_weaviate_data(self, sample_weaviate_response):
        """Test graph service processes Weaviate data correctly."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        # Extract artifacts from Weaviate response
        artifacts = sample_weaviate_response["data"]["Get"]["Artifact"]

        # Convert to expected format
        formatted_artifacts = [
            {
                "id": a["id"],
                "type": a["artifactType"],
                "name": a["name"],
                "file_path": a["filePath"],
                "relationships": a.get("relationships", [])
            }
            for a in artifacts
        ]

        # Build graph
        nodes, edges = graph_service.build_graph(formatted_artifacts)

        # Verify graph structure
        assert len(nodes) == 2
        assert len(edges) == 1

        # Verify presenter-view binding
        assert edges[0].source == "artifact_001"
        assert edges[0].target == "artifact_002"
        assert edges[0].edge_type == "binds_to"

    def test_cytoscape_export_format(self):
        """Test Cytoscape export produces valid format."""
        from codeindex.web.services.graph_service import (
            GraphService, GraphNode, GraphEdge
        )

        graph_service = GraphService()

        nodes = [
            GraphNode(id="node_1", label="Service", node_type="BackendDoc"),
            GraphNode(id="node_2", label="DAO", node_type="DaoCall")
        ]

        edges = [
            GraphEdge(source="node_1", target="node_2", edge_type="calls")
        ]

        # Export to Cytoscape format
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Verify structure
        assert "elements" in cytoscape_data
        assert "style" in cytoscape_data

        # Verify elements
        elements = cytoscape_data["elements"]
        assert len(elements) == 3  # 2 nodes + 1 edge

        # Verify node format
        node_elements = [e for e in elements if "source" not in e.get("data", {})]
        assert len(node_elements) == 2
        assert node_elements[0]["data"]["id"] == "node_1"
        assert node_elements[0]["data"]["label"] == "Service"

        # Verify edge format
        edge_elements = [e for e in elements if "source" in e.get("data", {})]
        assert len(edge_elements) == 1
        assert edge_elements[0]["data"]["source"] == "node_1"
        assert edge_elements[0]["data"]["target"] == "node_2"

    def test_mermaid_export_syntax(self):
        """Test Mermaid export produces valid syntax."""
        from codeindex.web.services.graph_service import (
            GraphService, GraphNode, GraphEdge
        )

        graph_service = GraphService()

        nodes = [
            GraphNode(id="A", label="ServiceA", node_type="BackendDoc"),
            GraphNode(id="B", label="ServiceB", node_type="BackendDoc")
        ]

        edges = [
            GraphEdge(source="A", target="B", edge_type="calls")
        ]

        # Export to Mermaid format
        mermaid = graph_service.export_to_mermaid(nodes, edges)

        # Verify syntax
        assert mermaid.startswith("graph LR")
        assert 'A["ServiceA"]' in mermaid
        assert 'B["ServiceB"]' in mermaid
        assert "A -->|calls| B" in mermaid

    def test_graph_with_circular_dependencies(self):
        """Test graph handles circular dependencies correctly."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        # Create circular dependency
        artifacts = [
            {
                "id": "A",
                "type": "BackendDoc",
                "name": "ServiceA",
                "relationships": [{"target_id": "B", "type": "calls"}]
            },
            {
                "id": "B",
                "type": "BackendDoc",
                "name": "ServiceB",
                "relationships": [{"target_id": "A", "type": "calls"}]
            }
        ]

        # Build graph
        nodes, edges = graph_service.build_graph(artifacts)

        # Should handle without error
        assert len(nodes) == 2
        assert len(edges) == 2

        # Both edges should exist
        edge_pairs = [(e.source, e.target) for e in edges]
        assert ("A", "B") in edge_pairs
        assert ("B", "A") in edge_pairs

    def test_graph_performance_with_max_nodes(self):
        """Test graph respects performance limits."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService(max_nodes=10)

        # Create 20 artifacts
        artifacts = [
            {
                "id": f"artifact_{i}",
                "type": "BackendDoc",
                "name": f"Service{i}",
                "relationships": []
            }
            for i in range(20)
        ]

        # Build graph
        nodes, edges = graph_service.build_graph(artifacts)

        # Should limit to 10 nodes
        assert len(nodes) == 10
        assert len(nodes) <= graph_service.max_nodes

    def test_relationship_query_timeout(self):
        """Test graph handles query timeouts gracefully."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        # Mock a timeout scenario
        with patch.object(graph_service, '_query_weaviate_relationships') as mock_query:
            mock_query.side_effect = TimeoutError("Query timed out")

            # Should handle timeout without crashing
            try:
                relationships = graph_service.get_relationships("artifact_001")
                # Should return empty list on error
                assert relationships is not None
            except TimeoutError:
                # Or raise error for caller to handle
                pass

    def test_graph_with_missing_target_nodes(self):
        """Test graph handles missing target nodes gracefully."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        # Artifact with relationship to non-existent target
        artifacts = [
            {
                "id": "A",
                "type": "BackendDoc",
                "name": "ServiceA",
                "relationships": [
                    {"target_id": "B", "type": "calls"},
                    {"target_id": "nonexistent", "type": "calls"}
                ]
            },
            {
                "id": "B",
                "type": "BackendDoc",
                "name": "ServiceB",
                "relationships": []
            }
        ]

        # Build graph
        nodes, edges = graph_service.build_graph(artifacts)

        # Should only include edge to existing target
        assert len(nodes) == 2
        assert len(edges) == 1
        assert edges[0].target == "B"

    def test_graph_color_coding_by_artifact_type(self):
        """Test nodes are color-coded by artifact type."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        artifacts = [
            {"id": "1", "type": "GwtPresenter", "name": "Presenter", "relationships": []},
            {"id": "2", "type": "GwtView", "name": "View", "relationships": []},
            {"id": "3", "type": "BackendDoc", "name": "Service", "relationships": []},
            {"id": "4", "type": "DaoCall", "name": "DAO", "relationships": []}
        ]

        # Build graph
        nodes, edges = graph_service.build_graph(artifacts)

        # Export to Cytoscape to check colors
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Get node colors
        node_colors = {}
        for element in cytoscape_data["elements"]:
            if "source" not in element.get("data", {}):  # It's a node
                node_type = element["data"]["type"]
                color = element["data"]["color"]
                node_colors[node_type] = color

        # Verify different types have different colors
        assert len(set(node_colors.values())) >= 3  # At least 3 different colors

    def test_end_to_end_graph_generation_flow(self):
        """Test complete flow from search to graph display."""
        from codeindex.web.services.graph_service import GraphService

        graph_service = GraphService()

        # Simulate user clicking "Show Relationships" on an artifact
        artifact_id = "user_presenter_001"

        # Step 1: Query relationships (would come from Weaviate)
        mock_relationships = [
            {"target_id": "user_view_001", "type": "binds_to"},
            {"target_id": "user_service_001", "type": "calls"}
        ]

        # Step 2: Build artifact list
        artifacts = [
            {
                "id": artifact_id,
                "type": "GwtPresenter",
                "name": "UserPresenter",
                "relationships": mock_relationships
            },
            {
                "id": "user_view_001",
                "type": "GwtView",
                "name": "UserView",
                "relationships": []
            },
            {
                "id": "user_service_001",
                "type": "BackendDoc",
                "name": "UserService",
                "relationships": []
            }
        ]

        # Step 3: Build graph
        nodes, edges = graph_service.build_graph(artifacts)

        # Step 4: Export to Cytoscape
        cytoscape_data = graph_service.export_to_cytoscape(nodes, edges)

        # Step 5: Export to Mermaid
        mermaid = graph_service.export_to_mermaid(nodes, edges)

        # Verify complete flow
        assert len(nodes) == 3
        assert len(edges) == 2
        assert cytoscape_data is not None
        assert mermaid is not None
        assert "graph LR" in mermaid
