"""
Graph service for building relationship graphs from artifacts (T044-T045).

This service provides:
- Relationship graph building from Weaviate
- Node and edge creation
- Max node limiting for performance
- Relationship querying
"""

import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class GraphNode:
    """
    Represents a node in the relationship graph.

    Attributes:
        id: Unique identifier
        label: Display label
        node_type: Artifact type (GwtPresenter, BackendDoc, etc.)
        metadata: Additional node data
    """
    id: str
    label: str
    node_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    """
    Represents an edge in the relationship graph.

    Attributes:
        source: Source node ID
        target: Target node ID
        edge_type: Relationship type (calls, binds_to, depends_on, etc.)
        metadata: Additional edge data
    """
    source: str
    target: str
    edge_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class GraphService:
    """
    Service for building and managing relationship graphs.

    Features:
    - Build graphs from artifact data
    - Query Weaviate for relationships
    - Create nodes and edges
    - Enforce max node limits for performance
    """

    # Color mapping for different artifact types
    TYPE_COLORS = {
        "GwtPresenter": "#FF6B6B",      # Red
        "GwtView": "#4ECDC4",           # Teal
        "GwtUiBinder": "#45B7D1",       # Blue
        "BackendDoc": "#96CEB4",        # Green
        "DaoCall": "#FFEAA7",           # Yellow
        "DbTable": "#DFE6E9",           # Gray
        "IbatisStatement": "#FD79A8",   # Pink
        "GwtEndpoint": "#A29BFE",       # Purple
        "JspForm": "#FF7675",           # Light Red
        "DtoArtifact": "#74B9FF",       # Light Blue
        "JsArtifact": "#FAB1A0"         # Peach
    }

    def __init__(self, max_nodes: int = 50):
        """
        Initialize graph service.

        Args:
            max_nodes: Maximum number of nodes in graph (performance limit)
        """
        self.max_nodes = max_nodes

    def build_graph(
        self,
        artifacts: List[Dict[str, Any]]
    ) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Build relationship graph from artifacts.

        Args:
            artifacts: List of artifact dictionaries with relationships

        Returns:
            Tuple of (nodes, edges) for graph visualization
        """
        logger.info(f"Building graph from {len(artifacts)} artifacts")

        # Limit to max_nodes
        if len(artifacts) > self.max_nodes:
            logger.warning(f"Limiting graph to {self.max_nodes} nodes (from {len(artifacts)})")
            artifacts = artifacts[:self.max_nodes]

        # Create nodes
        nodes = []
        node_ids = set()

        for artifact in artifacts:
            node = self._create_node(artifact)

            # Deduplicate by ID
            if node.id not in node_ids:
                nodes.append(node)
                node_ids.add(node.id)

        # Create edges
        edges = []

        for artifact in artifacts:
            artifact_id = artifact.get("id")
            relationships = artifact.get("relationships", [])

            for relationship in relationships:
                edge = self._create_edge(artifact_id, relationship)

                # Only add edge if both nodes exist in graph
                if edge.source in node_ids and edge.target in node_ids:
                    edges.append(edge)

        logger.info(f"Built graph: {len(nodes)} nodes, {len(edges)} edges")

        return nodes, edges

    def _create_node(self, artifact: Dict[str, Any]) -> GraphNode:
        """
        Create graph node from artifact.

        Args:
            artifact: Artifact dictionary

        Returns:
            GraphNode instance
        """
        return GraphNode(
            id=artifact.get("id", "unknown"),
            label=artifact.get("name", "Unknown"),
            node_type=artifact.get("type", "Unknown"),
            metadata={
                k: v for k, v in artifact.items()
                if k not in ("id", "name", "type", "relationships")
            }
        )

    def _create_edge(
        self,
        source_id: str,
        relationship: Dict[str, Any]
    ) -> GraphEdge:
        """
        Create graph edge from relationship.

        Args:
            source_id: Source artifact ID
            relationship: Relationship dictionary

        Returns:
            GraphEdge instance
        """
        return GraphEdge(
            source=source_id,
            target=relationship.get("target_id", "unknown"),
            edge_type=relationship.get("type", "related"),
            metadata={
                k: v for k, v in relationship.items()
                if k not in ("target_id", "type")
            }
        )

    def _get_node_color(self, node_type: str) -> str:
        """
        Get color for node based on artifact type.

        Args:
            node_type: Artifact type

        Returns:
            Hex color code
        """
        return self.TYPE_COLORS.get(node_type, "#95A5A6")  # Default gray

    def get_relationships(self, artifact_id: str) -> List[Dict[str, Any]]:
        """
        Get relationships for specific artifact from Weaviate.

        TODO: Integrate with Weaviate to query actual relationships

        Args:
            artifact_id: Artifact ID to query

        Returns:
            List of relationship dictionaries
        """
        # TODO: Replace with actual Weaviate query
        # This is a placeholder that would query:
        # - FK relationships from DbTable
        # - Presenter-View bindings from GwtPresenter
        # - Service-DAO calls from BackendDoc

        logger.debug(f"Querying relationships for: {artifact_id}")

        return self._query_weaviate_relationships(artifact_id)

    def _query_weaviate_relationships(self, artifact_id: str) -> List[Dict[str, Any]]:
        """
        Query Weaviate for artifact relationships.

        TODO: Implement actual Weaviate GraphQL query

        Args:
            artifact_id: Artifact ID

        Returns:
            List of relationships
        """
        # TODO: Replace with actual Weaviate query
        # Query would extract:
        # 1. Foreign key relationships (DbTable → DbTable)
        # 2. Presenter-View bindings (GwtPresenter → GwtView)
        # 3. Service-DAO calls (BackendDoc → DaoCall)
        # 4. DTO usage (BackendDoc → DtoArtifact)

        logger.debug(f"Weaviate query for relationships: {artifact_id}")

        return []

    def build_artifact_subgraph(
        self,
        center_artifact_id: str,
        depth: int = 1
    ) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Build subgraph centered on specific artifact.

        Args:
            center_artifact_id: Central artifact ID
            depth: Relationship depth to traverse (1 = direct connections only)

        Returns:
            Tuple of (nodes, edges) for subgraph
        """
        # TODO: Implement BFS traversal from center artifact
        # 1. Start with center artifact
        # 2. Query relationships up to depth levels
        # 3. Build subgraph with max_nodes limit

        logger.info(f"Building subgraph: center={center_artifact_id}, depth={depth}")

        # Placeholder implementation
        return [], []

    def export_to_cytoscape(
        self,
        nodes: List[GraphNode],
        edges: List[GraphEdge]
    ) -> Dict[str, Any]:
        """
        Export graph to Cytoscape format.

        Args:
            nodes: List of graph nodes
            edges: List of graph edges

        Returns:
            Cytoscape JSON format
        """
        cytoscape_elements = []

        # Add nodes
        for node in nodes:
            cytoscape_elements.append({
                "data": {
                    "id": node.id,
                    "label": node.label,
                    "type": node.node_type,
                    "color": self._get_node_color(node.node_type),
                    **node.metadata
                },
                "classes": node.node_type.lower()
            })

        # Add edges
        for edge in edges:
            cytoscape_elements.append({
                "data": {
                    "id": f"{edge.source}_{edge.target}",
                    "source": edge.source,
                    "target": edge.target,
                    "label": edge.edge_type,
                    **edge.metadata
                },
                "classes": edge.edge_type.lower()
            })

        return {
            "elements": cytoscape_elements,
            "style": self._get_cytoscape_style()
        }

    def _get_cytoscape_style(self) -> List[Dict[str, Any]]:
        """
        Get Cytoscape stylesheet.

        Returns:
            Cytoscape style configuration
        """
        return [
            {
                "selector": "node",
                "style": {
                    "label": "data(label)",
                    "background-color": "data(color)",
                    "width": "60px",
                    "height": "60px",
                    "font-size": "12px",
                    "text-valign": "center",
                    "text-halign": "center"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "label": "data(label)",
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    "line-color": "#9CA3AF",
                    "target-arrow-color": "#9CA3AF",
                    "font-size": "10px"
                }
            }
        ]

    def export_to_mermaid(
        self,
        nodes: List[GraphNode],
        edges: List[GraphEdge]
    ) -> str:
        """
        Export graph to Mermaid markdown format.

        Args:
            nodes: List of graph nodes
            edges: List of graph edges

        Returns:
            Mermaid markdown syntax
        """
        lines = ["graph LR"]

        # Add node definitions
        for node in nodes:
            # Sanitize label for Mermaid
            label = node.label.replace('"', "'")
            lines.append(f'    {node.id}["{label}"]')

        # Add edges
        for edge in edges:
            label = edge.edge_type.replace('"', "'")
            lines.append(f'    {edge.source} -->|{label}| {edge.target}')

        return "\n".join(lines)


# Global service instance
_graph_service: Optional[GraphService] = None


def get_graph_service() -> GraphService:
    """
    Get global graph service instance.

    Returns:
        GraphService singleton
    """
    global _graph_service

    if _graph_service is None:
        _graph_service = GraphService()
        logger.info("Initialized graph service")

    return _graph_service


__all__ = [
    "GraphService",
    "GraphNode",
    "GraphEdge",
    "get_graph_service"
]
