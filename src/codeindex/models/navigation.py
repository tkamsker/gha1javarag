"""
Navigation models for GWT application structure analysis.

This module defines dataclasses for representing navigation graphs, nodes, and paths
discovered during GWT analysis.
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Any
from enum import Enum


class NodeType(Enum):
    """Type of navigation node in GWT application"""
    PRESENTER = "presenter"
    VIEW = "view"
    ACTIVITY = "activity"
    PLACE = "place"
    MODULE = "module"
    EXTERNAL = "external"


@dataclass
class NavigationNode:
    """
    Single node in the navigation graph.

    Represents a component (Presenter/View/Activity/Place/Module) or external URL
    in the GWT application navigation structure.
    """

    node_id: str
    """Unique identifier for this node (typically class name or URL)"""

    node_type: NodeType = NodeType.MODULE
    """Type of node (presenter, view, activity, place, module, external)"""

    label: str = ""
    """Human-readable label for display"""

    source_file: Optional[str] = None
    """Path to source file containing this component"""

    outgoing_targets: List[str] = field(default_factory=list)
    """List of node_ids this node navigates to"""

    confidence: float = 1.0
    """Confidence score for this node detection (0.0-1.0)"""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata (RPC calls, event handlers, etc.)"""

    # Additional fields for GWT module nodes
    module_name: Optional[str] = None
    """GWT module name (for MODULE type nodes)"""

    depth: int = 0
    """Depth in module hierarchy (0 for entry modules)"""

    parent_module: Optional[str] = None
    """Parent module name in dependency hierarchy"""

    entry_points: List[str] = field(default_factory=list)
    """Entry point classes for this module"""

    inherits: List[str] = field(default_factory=list)
    """Inherited module names"""

    source_paths: List[str] = field(default_factory=list)
    """Source paths defined in module"""

    def __post_init__(self):
        """Validate navigation node values"""
        if not self.node_id:
            raise ValueError("node_id cannot be empty")

        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")

        if not isinstance(self.node_type, NodeType):
            raise ValueError(f"node_type must be NodeType enum, got {type(self.node_type)}")

        # Set default label if not provided
        if not self.label:
            self.label = self.node_id

    def add_target(self, target_node_id: str):
        """Add a navigation target to this node"""
        if target_node_id not in self.outgoing_targets:
            self.outgoing_targets.append(target_node_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {
            'node_id': self.node_id,
            'node_type': self.node_type.value,
            'label': self.label,
            'source_file': self.source_file,
            'outgoing_targets': self.outgoing_targets,
            'confidence': self.confidence,
            'metadata': self.metadata
        }

        # Add module-specific fields if applicable
        if self.node_type == NodeType.MODULE:
            result.update({
                'module_name': self.module_name,
                'depth': self.depth,
                'parent_module': self.parent_module,
                'entry_points': self.entry_points,
                'inherits': self.inherits,
                'source_paths': self.source_paths
            })

        return result


@dataclass
class NavigationGraph:
    """
    Complete UI navigation structure from entry points through GWT modules.

    Represents the entire navigation graph discovered from analyzing index.html/jsp
    and following all GWT module references, entry points, and navigation paths.
    """

    project: str
    """Project identifier"""

    graph_id: str
    """Unique identifier for this graph"""

    entry_points: List[str]
    """List of entry point files (index.html, index.jsp)"""

    nodes: Dict[str, NavigationNode] = field(default_factory=dict)
    """Map of node_id to NavigationNode"""

    edges: List[tuple] = field(default_factory=list)
    """List of (source_node_id, target_node_id) tuples"""

    statistics: Dict[str, int] = field(default_factory=dict)
    """Summary statistics (presenter_count, view_count, etc.)"""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata for the graph"""

    def __post_init__(self):
        """Initialize statistics"""
        if not self.statistics:
            self.statistics = {
                'presenter_count': 0,
                'view_count': 0,
                'activity_count': 0,
                'place_count': 0,
                'module_count': 0,
                'external_count': 0,
                'edge_count': 0
            }

    def add_node(self, node: NavigationNode):
        """Add a node to the graph"""
        if node.node_id in self.nodes:
            # Merge with existing node if confidence is higher
            existing = self.nodes[node.node_id]
            if node.confidence > existing.confidence:
                self.nodes[node.node_id] = node
        else:
            self.nodes[node.node_id] = node
            # Update statistics
            node_type_key = f"{node.node_type.value}_count"
            if node_type_key in self.statistics:
                self.statistics[node_type_key] += 1

    def add_edge(self, source_id: str, target_id: str):
        """Add an edge (navigation path) to the graph"""
        edge = (source_id, target_id)
        if edge not in self.edges:
            self.edges.append(edge)
            self.statistics['edge_count'] += 1

    def get_node(self, node_id: str) -> Optional[NavigationNode]:
        """Get a node by ID"""
        return self.nodes.get(node_id)

    def get_presenters(self) -> List[NavigationNode]:
        """Get all Presenter nodes"""
        return [node for node in self.nodes.values() if node.node_type == NodeType.PRESENTER]

    def get_views(self) -> List[NavigationNode]:
        """Get all View nodes"""
        return [node for node in self.nodes.values() if node.node_type == NodeType.VIEW]

    def get_activities(self) -> List[NavigationNode]:
        """Get all Activity nodes"""
        return [node for node in self.nodes.values() if node.node_type == NodeType.ACTIVITY]

    def get_places(self) -> List[NavigationNode]:
        """Get all Place nodes"""
        return [node for node in self.nodes.values() if node.node_type == NodeType.PLACE]

    def get_outgoing_edges(self, node_id: str) -> List[str]:
        """Get all target nodes for a given source node"""
        return [target for source, target in self.edges if source == node_id]

    def get_incoming_edges(self, node_id: str) -> List[str]:
        """Get all source nodes that navigate to a given target node"""
        return [source for source, target in self.edges if target == node_id]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'project': self.project,
            'graph_id': self.graph_id,
            'entry_points': self.entry_points,
            'nodes': {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            'edges': self.edges,
            'statistics': self.statistics,
            'metadata': self.metadata
        }

    def calculate_discovery_rate(self, expected_components: int = 100) -> float:
        """
        Calculate component discovery rate as percentage.

        Args:
            expected_components: Expected number of major components (Presenters + Views)

        Returns:
            Discovery rate as percentage (0-100)
        """
        discovered = self.statistics['presenter_count'] + self.statistics['view_count']
        if expected_components <= 0:
            return 0.0

        rate = (discovered / expected_components) * 100.0
        return min(rate, 100.0)  # Cap at 100%

    def calculate_statistics(self):
        """
        Calculate and update graph statistics.

        Counts nodes by type and calculates max depth.
        """
        # Reset statistics
        self.statistics = {
            'presenter_count': 0,
            'view_count': 0,
            'activity_count': 0,
            'place_count': 0,
            'module_count': 0,
            'external_count': 0,
            'edge_count': len(self.edges)
        }

        # Count nodes by type
        for node in self.nodes.values():
            node_type_key = f"{node.node_type.value}_count"
            if node_type_key in self.statistics:
                self.statistics[node_type_key] += 1

    @property
    def max_depth(self) -> int:
        """
        Get maximum depth in the navigation graph.

        Returns:
            Maximum depth value from all nodes
        """
        if not self.nodes:
            return 0

        return max(
            (node.depth for node in self.nodes.values() if hasattr(node, 'depth')),
            default=0
        )
