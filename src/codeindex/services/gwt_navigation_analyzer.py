"""
GWT Navigation Analyzer Service.

Implements Feature 007 US3 T059-T062.

Builds complete navigation graph from index.html/jsp through GWT modules
using BFS traversal with circular dependency detection.
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from collections import deque
from functools import lru_cache
from datetime import datetime

from codeindex.models.navigation import NavigationGraph, NavigationNode, NodeType
from codeindex.models.gwt_module import GWTModule
from codeindex.parsers.index_parser import IndexParser
from codeindex.parsers.gwt_module_parser import GWTModuleParser
from codeindex.utils.metrics import get_metrics_collector
from codeindex.models.metrics import NavigationMetric

logger = logging.getLogger(__name__)


class GWTNavigationAnalyzer:
    """
    Analyzes GWT navigation structure starting from index.html/jsp.

    Uses BFS traversal to discover all reachable GWT modules, presenters, and views.
    Implements circular dependency detection and module caching.
    """

    def __init__(self, source_dir: Path):
        """
        Initialize navigation analyzer.

        Args:
            source_dir: Root source directory containing GWT modules
        """
        self.source_dir = Path(source_dir)
        self.index_parser = IndexParser()
        self.module_parser = GWTModuleParser()
        self.logger = logging.getLogger(__name__)

        # Tracking for circular dependency detection
        self.visited_modules: Set[str] = set()
        self.module_stack: List[str] = []  # For cycle detection

    def build_navigation_graph(
        self,
        index_file: Path,
        source_dir: Optional[Path] = None
    ) -> NavigationGraph:
        """
        Build complete navigation graph from index.html/jsp.

        Implements T059, T060, T061.

        Starting from index file, discovers all GWT modules using BFS traversal,
        detects circular dependencies, and builds navigation graph.

        Args:
            index_file: Path to index.html or index.jsp
            source_dir: Optional source directory override

        Returns:
            NavigationGraph with all discovered modules and components

        Raises:
            FileNotFoundError: If index file doesn't exist
        """
        if source_dir:
            self.source_dir = Path(source_dir)

        start_time = datetime.now()
        self.logger.info(f"Building navigation graph from {index_file.name}")

        # Reset tracking state
        self.visited_modules.clear()
        self.module_stack.clear()

        # Step 1: Extract entry modules from index file
        entry_modules = self.index_parser.extract_gwt_modules(index_file)
        self.logger.info(f"Found {len(entry_modules)} entry modules in {index_file.name}")

        if not entry_modules:
            self.logger.warning(f"No GWT modules found in {index_file.name}")
            return NavigationGraph(
                project=self.source_dir.name,
                graph_id=f"nav_{index_file.stem}",
                entry_points=[str(index_file)],
                nodes={}
            )

        # Step 2: Build module graph using BFS traversal (T060)
        navigation_graph = NavigationGraph(
            project=self.source_dir.name,
            graph_id=f"nav_{index_file.stem}",
            entry_points=[str(index_file)],
            nodes={},
            metadata={'entry_modules': entry_modules}
        )

        # BFS traversal starting from entry modules
        self._bfs_traverse_modules(entry_modules, navigation_graph)

        # Step 3: Calculate statistics
        duration = (datetime.now() - start_time).total_seconds()
        navigation_graph.calculate_statistics()

        # Log navigation metrics
        self._log_navigation_metrics(navigation_graph, duration)

        self.logger.info(
            f"Navigation graph built: {len(navigation_graph.nodes)} modules, "
            f"{navigation_graph.max_depth} max depth, {duration:.2f}s"
        )

        return navigation_graph

    def _bfs_traverse_modules(
        self,
        entry_modules: List[str],
        navigation_graph: NavigationGraph
    ):
        """
        Traverse GWT modules using BFS (breadth-first search).

        Implements T060 (BFS traversal) and T061 (circular detection).

        Args:
            entry_modules: List of entry module names
            navigation_graph: NavigationGraph to populate
        """
        # BFS queue: (module_name, parent_module, depth)
        queue: deque = deque()

        # Initialize queue with entry modules
        for module_name in entry_modules:
            queue.append((module_name, None, 0))

        # BFS traversal
        while queue:
            module_name, parent_name, depth = queue.popleft()

            # Skip if already visited
            if module_name in self.visited_modules:
                # Check for circular dependency (T061)
                if parent_name and module_name in self.module_stack:
                    self._log_circular_dependency(parent_name, module_name)
                continue

            # Mark as visited
            self.visited_modules.add(module_name)
            self.module_stack.append(module_name)

            # Parse GWT module (with LRU cache - T062)
            gwt_module = self._parse_module_with_cache(module_name)

            if not gwt_module:
                self.logger.warning(f"Failed to parse module: {module_name}")
                self.module_stack.pop()
                continue

            # Create navigation node for module
            node = NavigationNode(
                node_id=module_name,
                node_type=NodeType.MODULE,
                label=module_name,
                source_file=gwt_module.module_file,
                module_name=module_name,
                depth=depth,
                parent_module=parent_name,
                entry_points=gwt_module.entry_point_classes,
                inherits=gwt_module.inherits,
                source_paths=gwt_module.source_paths
            )

            # Add to navigation graph
            navigation_graph.add_node(node)

            # Add inherited modules to queue (next level)
            for inherited_module in gwt_module.inherits:
                if inherited_module not in self.visited_modules:
                    queue.append((inherited_module, module_name, depth + 1))

            # Pop from module stack
            self.module_stack.pop()

        self.logger.info(f"BFS traversal complete: visited {len(self.visited_modules)} modules")

    @lru_cache(maxsize=256)
    def _parse_module_with_cache(self, module_name: str) -> Optional[GWTModule]:
        """
        Parse GWT module with LRU caching.

        Implements T062.

        Uses functools.lru_cache to cache parsed modules and avoid
        re-parsing the same module multiple times.

        Args:
            module_name: GWT module name (e.g., 'com.example.Application')

        Returns:
            GWTModule object or None if not found
        """
        # Find module XML file
        module_file = self._find_module_file(module_name)

        if not module_file:
            self.logger.debug(f"Module file not found: {module_name}")
            return None

        # Parse module
        return self.module_parser.parse_module(module_file)

    def _find_module_file(self, module_name: str) -> Optional[Path]:
        """
        Find *.gwt.xml file for module name.

        Searches source directory for module XML file using common patterns:
        - src/com/example/Application.gwt.xml
        - src/main/resources/com/example/Application.gwt.xml

        Args:
            module_name: Module name in dot notation

        Returns:
            Path to module XML file or None if not found
        """
        # Convert module name to path
        # com.example.Application → com/example/Application.gwt.xml
        module_path = module_name.replace('.', '/') + '.gwt.xml'

        # Search patterns
        search_patterns = [
            self.source_dir / module_path,
            self.source_dir / 'src' / module_path,
            self.source_dir / 'src' / 'main' / 'java' / module_path,
            self.source_dir / 'src' / 'main' / 'resources' / module_path,
        ]

        for pattern in search_patterns:
            if pattern.exists():
                self.logger.debug(f"Found module file: {pattern}")
                return pattern

        # Try glob search as fallback
        module_filename = module_name.split('.')[-1] + '.gwt.xml'
        matches = list(self.source_dir.glob(f"**/{module_filename}"))

        if matches:
            self.logger.debug(f"Found module file via glob: {matches[0]}")
            return matches[0]

        return None

    def _log_circular_dependency(self, parent_module: str, circular_module: str):
        """
        Log circular dependency warning.

        Implements T061.

        Args:
            parent_module: Module that inherits circular module
            circular_module: Module that creates circular dependency
        """
        # Build dependency path showing the cycle
        cycle_start_index = self.module_stack.index(circular_module)
        cycle_path = self.module_stack[cycle_start_index:] + [circular_module]

        warning_msg = (
            f"Circular dependency detected: {' -> '.join(cycle_path)}"
        )

        self.logger.warning(warning_msg)

        # Mark modules as having circular dependency
        # (Could update GWTModule.circular_inherits flag here)

    def _log_navigation_metrics(self, navigation_graph: NavigationGraph, duration: float):
        """
        Log navigation analysis metrics.

        Implements T066 - Navigation metrics logging.

        Args:
            navigation_graph: Completed navigation graph
            duration: Analysis duration in seconds
        """
        # Get entry point (first one from list)
        entry_point = navigation_graph.entry_points[0] if navigation_graph.entry_points else ""

        # Count entry points from all modules
        total_entry_points = sum(
            len(node.entry_points) for node in navigation_graph.nodes.values()
            if hasattr(node, 'entry_points') and node.entry_points
        )

        # Count navigation edges
        navigation_edges = len(navigation_graph.edges)

        # Calculate discovery rate (assuming ~10 presenters per module as baseline)
        expected_components = len(navigation_graph.nodes) * 10
        discovered_components = total_entry_points
        discovery_rate = (discovered_components / expected_components * 100.0) if expected_components > 0 else 0.0

        metric = NavigationMetric(
            entry_point=entry_point,
            modules_parsed=len(navigation_graph.nodes),
            presenters_discovered=total_entry_points,
            views_discovered=0,  # Will be populated by view analyzer
            activities_discovered=0,  # Will be populated by activity analyzer
            places_discovered=0,  # Will be populated by place analyzer
            navigation_edges=navigation_edges,
            circular_dependencies=0,  # Track separately in future
            discovery_rate=discovery_rate,
            timestamp=datetime.now()
        )

        metrics_collector = get_metrics_collector()
        metrics_collector.add_navigation_metric(metric)

        self.logger.info(
            f"Navigation metrics: {metric.modules_parsed} modules, "
            f"{metric.presenters_discovered} entry points, "
            f"max depth {navigation_graph.max_depth}, "
            f"{metric.navigation_edges} edges"
        )


    def map_presenter_view_bindings(
        self,
        navigation_graph: NavigationGraph
    ) -> Dict[str, Any]:
        """
        Map Presenter-View-UiBinder relationships from navigation graph.

        Implements T073-T076.

        For each entry point (Presenter) in the navigation graph, discovers:
        - Associated View implementation
        - UiBinder template (*.ui.xml)
        - Binding confidence score

        Args:
            navigation_graph: Navigation graph with entry points

        Returns:
            Dictionary mapping presenters to their views and templates
        """
        bindings = {}

        # Iterate through all modules and their entry points
        for node in navigation_graph.nodes.values():
            if not hasattr(node, 'entry_points') or not node.entry_points:
                continue

            for entry_point_class in node.entry_points:
                # Skip if not a Presenter
                if not entry_point_class.endswith('Presenter'):
                    continue

                # Find binding for this presenter
                binding = self._map_presenter_view_binding(entry_point_class)

                if binding:
                    bindings[entry_point_class] = binding

        self.logger.info(f"Mapped {len(bindings)} presenter-view bindings")
        return bindings

    def _map_presenter_view_binding(self, presenter_class: str) -> Optional[Dict[str, Any]]:
        """
        Map a single Presenter to its View and UiBinder template.

        Implements T073-T076.

        Args:
            presenter_class: Fully qualified presenter class name

        Returns:
            Binding dictionary with view_class, template_file, confidence, etc.
        """
        # Convert class name to file path
        # com.example.client.UserPresenter → com/example/client/UserPresenter.java
        presenter_path = presenter_class.replace('.', '/') + '.java'

        # Find presenter file
        presenter_file = self._find_source_file(presenter_path)

        if not presenter_file:
            self.logger.debug(f"Presenter file not found: {presenter_class}")
            return None

        try:
            content = presenter_file.read_text(encoding='utf-8')

            # T074: Detect Display interface (inner interface pattern)
            display_interface = self._detect_display_interface(content, presenter_class)

            # T075: Find View implementation
            view_class = self._find_view_implementation(presenter_class, display_interface, content)

            # T076: Find UiBinder template
            template_file = self._find_uibinder_template(view_class) if view_class else None

            # Calculate confidence based on detection method
            confidence = self._calculate_binding_confidence(
                display_interface=display_interface,
                view_class=view_class,
                template_file=template_file
            )

            return {
                'presenter_class': presenter_class,
                'presenter_file': str(presenter_file),
                'display_interface': display_interface,
                'view_class': view_class,
                'view_file': self._find_source_file(view_class.replace('.', '/') + '.java') if view_class else None,
                'template_file': template_file,
                'confidence': confidence,
                'binding_pattern': self._get_binding_pattern(display_interface, view_class)
            }

        except Exception as e:
            self.logger.error(f"Error mapping presenter binding for {presenter_class}: {e}", exc_info=True)
            return None

    def _detect_display_interface(self, content: str, presenter_class: str) -> Optional[str]:
        """
        Detect inner Display or View interface in Presenter.

        Implements T074.

        Args:
            content: Presenter Java source code
            presenter_class: Presenter class name

        Returns:
            Interface name or None
        """
        # Pattern: public interface Display { ... }
        interface_pattern = r'public\s+interface\s+(Display|View)\s*(?:extends\s+[\w<>,\s]+)?\s*\{'

        match = re.search(interface_pattern, content)

        if match:
            interface_name = match.group(1)
            # Return fully qualified name
            return f"{presenter_class}.{interface_name}"

        return None

    def _find_view_implementation(
        self,
        presenter_class: str,
        display_interface: Optional[str],
        presenter_content: str
    ) -> Optional[str]:
        """
        Find View implementation class for a Presenter.

        Implements T075.

        Strategy:
        1. If Display interface exists, look for "implements PresenterName.Display"
        2. Use naming convention: UserPresenter → UserView
        3. Check if view file exists

        Args:
            presenter_class: Presenter class name
            display_interface: Display interface name (if exists)
            presenter_content: Presenter source code

        Returns:
            Fully qualified view class name or None
        """
        # Extract presenter name without package
        presenter_name = presenter_class.split('.')[-1]

        # Strategy 1: Naming convention - replace Presenter with View
        if presenter_name.endswith('Presenter'):
            view_name = presenter_name.replace('Presenter', 'View')

            # Build view class name with same package
            package = '.'.join(presenter_class.split('.')[:-1])
            view_class = f"{package}.{view_name}"

            # Check if view file exists
            view_path = view_class.replace('.', '/') + '.java'
            view_file = self._find_source_file(view_path)

            if view_file:
                # Verify it implements the Display interface (if exists)
                if display_interface:
                    try:
                        view_content = view_file.read_text(encoding='utf-8')
                        if f"implements {presenter_name}.Display" in view_content:
                            return view_class
                        elif "implements Display" in view_content:
                            return view_class
                    except Exception:
                        pass

                # Return even without verification if file exists
                return view_class

        return None

    def _find_uibinder_template(self, view_class: Optional[str]) -> Optional[str]:
        """
        Find UiBinder template file for a View.

        Implements T076.

        Strategy:
        1. Check for @UiTemplate annotation in View file
        2. Use naming convention: UserView.java → UserView.ui.xml

        Args:
            view_class: Fully qualified view class name

        Returns:
            Path to .ui.xml template file or None
        """
        if not view_class:
            return None

        # Find view file
        view_path = view_class.replace('.', '/') + '.java'
        view_file = self._find_source_file(view_path)

        if not view_file:
            return None

        try:
            content = view_file.read_text(encoding='utf-8')

            # Look for @UiTemplate annotation
            template_pattern = r'@UiTemplate\s*\(\s*"([^"]+)"\s*\)'
            match = re.search(template_pattern, content)

            if match:
                template_name = match.group(1)
                # Resolve relative to view file
                template_file = view_file.parent / template_name
                if template_file.exists():
                    return str(template_file)

            # Default naming convention: ViewName.ui.xml
            template_file = view_file.parent / f"{view_file.stem}.ui.xml"
            if template_file.exists():
                return str(template_file)

        except Exception as e:
            self.logger.debug(f"Error finding UiBinder template for {view_class}: {e}")

        return None

    def _find_source_file(self, relative_path: str) -> Optional[Path]:
        """
        Find source file in source directory.

        Args:
            relative_path: Relative path from source root

        Returns:
            Absolute path to file or None
        """
        # Search patterns
        search_patterns = [
            self.source_dir / relative_path,
            self.source_dir / 'src' / relative_path,
            self.source_dir / 'src' / 'main' / 'java' / relative_path,
        ]

        for pattern in search_patterns:
            if pattern.exists():
                return pattern

        # Fallback: glob search
        filename = Path(relative_path).name
        matches = list(self.source_dir.glob(f"**/{filename}"))

        if matches:
            return matches[0]

        return None

    def _calculate_binding_confidence(
        self,
        display_interface: Optional[str],
        view_class: Optional[str],
        template_file: Optional[str]
    ) -> float:
        """
        Calculate confidence score for presenter-view binding.

        Args:
            display_interface: Display interface name
            view_class: View class name
            template_file: UiBinder template path

        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.0

        # Display interface found: +40%
        if display_interface:
            confidence += 0.40

        # View class found: +35%
        if view_class:
            confidence += 0.35

        # UiBinder template found: +25%
        if template_file:
            confidence += 0.25

        return confidence

    def _get_binding_pattern(
        self,
        display_interface: Optional[str],
        view_class: Optional[str]
    ) -> str:
        """
        Get binding pattern description.

        Args:
            display_interface: Display interface name
            view_class: View class name

        Returns:
            Pattern description
        """
        if display_interface and view_class:
            return "Display interface with View implementation"
        elif view_class:
            return "Naming convention (View without Display interface)"
        elif display_interface:
            return "Display interface only"
        else:
            return "No binding detected"


# ==============================================================================
# Standalone Functions
# ==============================================================================

def build_navigation_graph(index_file: Path, source_dir: Path) -> NavigationGraph:
    """
    Build navigation graph from index file (convenience function).

    Args:
        index_file: Path to index.html or index.jsp
        source_dir: Source directory containing GWT modules

    Returns:
        NavigationGraph with all discovered modules
    """
    analyzer = GWTNavigationAnalyzer(source_dir)
    return analyzer.build_navigation_graph(index_file)
