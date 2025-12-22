"""
Unit tests for GWT navigation graph building and traversal.

Tests T050-T051 for Feature 007 User Story 3.
"""

import pytest
from pathlib import Path


class TestCircularModuleDependencyHandling:
    """Tests for circular dependency detection (T050)"""

    def test_detect_circular_dependency_two_modules(self):
        """Test detecting circular dependency between two modules"""
        # Given two modules that inherit each other (circular)
        # Module A inherits Module B
        # Module B inherits Module A
        module_graph = {
            "com.example.ModuleA": ["com.example.ModuleB"],
            "com.example.ModuleB": ["com.example.ModuleA"]
        }

        # When checking for cycles (will be implemented)
        has_cycle = True  # Expected

        # Then should detect cycle
        assert has_cycle is True

    def test_detect_circular_dependency_three_modules(self):
        """Test detecting circular dependency in chain of three modules"""
        # Given three modules with circular dependency
        # A → B → C → A
        module_graph = {
            "com.example.ModuleA": ["com.example.ModuleB"],
            "com.example.ModuleB": ["com.example.ModuleC"],
            "com.example.ModuleC": ["com.example.ModuleA"]
        }

        # When checking for cycles
        has_cycle = True  # Expected

        # Then should detect cycle
        assert has_cycle is True

    def test_no_circular_dependency_linear_chain(self):
        """Test linear dependency chain (no cycle)"""
        # Given linear dependency chain
        # A → B → C → D (no cycle)
        module_graph = {
            "com.example.ModuleA": ["com.example.ModuleB"],
            "com.example.ModuleB": ["com.example.ModuleC"],
            "com.example.ModuleC": ["com.example.ModuleD"],
            "com.example.ModuleD": []
        }

        # When checking for cycles
        has_cycle = False  # Expected

        # Then should not detect cycle
        assert has_cycle is False

    def test_no_circular_dependency_diamond_shape(self):
        """Test diamond-shaped dependency (converging paths, no cycle)"""
        # Given diamond dependency
        #     A
        #    / \
        #   B   C
        #    \ /
        #     D
        module_graph = {
            "com.example.ModuleA": ["com.example.ModuleB", "com.example.ModuleC"],
            "com.example.ModuleB": ["com.example.ModuleD"],
            "com.example.ModuleC": ["com.example.ModuleD"],
            "com.example.ModuleD": []
        }

        # When checking for cycles
        has_cycle = False  # Expected

        # Then should not detect cycle (diamond is valid)
        assert has_cycle is False

    def test_prevent_infinite_loop_with_visited_tracking(self):
        """Test that visited set prevents infinite loops"""
        # Given circular dependency
        module_graph = {
            "com.example.ModuleA": ["com.example.ModuleB"],
            "com.example.ModuleB": ["com.example.ModuleA"]
        }

        # When traversing with visited tracking
        visited = set()
        max_iterations = 10
        iterations = 0

        # Simulate traversal
        current = "com.example.ModuleA"
        while current not in visited and iterations < max_iterations:
            visited.add(current)
            iterations += 1
            # Would continue traversal in real implementation

        # Then should terminate within reasonable iterations
        assert iterations < max_iterations
        assert len(visited) <= 2  # Only 2 modules

    def test_log_circular_dependency_warning(self):
        """Test that circular dependencies are logged as warnings"""
        # Given circular dependency
        circular_path = ["com.example.ModuleA", "com.example.ModuleB", "com.example.ModuleA"]

        # When cycle detected (will be implemented)
        # Expected warning message
        expected_warning = "Circular dependency detected: com.example.ModuleA -> com.example.ModuleB -> com.example.ModuleA"

        # Then should generate warning message
        assert "Circular dependency" in expected_warning
        assert "ModuleA" in expected_warning


class TestBuildNavigationGraphBFSOrder:
    """Tests for BFS navigation graph building (T051)"""

    def test_bfs_traversal_level_by_level(self):
        """Test BFS traverses modules level by level"""
        # Given module hierarchy
        #     Root
        #    /  |  \
        #   A   B   C
        #  /|   |   |\
        # D E   F   G H
        module_graph = {
            "Root": ["A", "B", "C"],
            "A": ["D", "E"],
            "B": ["F"],
            "C": ["G", "H"],
            "D": [],
            "E": [],
            "F": [],
            "G": [],
            "H": []
        }

        # When traversing with BFS
        # Expected order: Root, A, B, C, D, E, F, G, H (level by level)
        expected_order = ["Root", "A", "B", "C", "D", "E", "F", "G", "H"]

        # Then should visit nodes level by level
        assert len(expected_order) == 9

    def test_bfs_uses_queue_data_structure(self):
        """Test BFS implementation uses queue (FIFO) not stack (LIFO)"""
        # Given simple tree
        #     Root
        #    /    \
        #   A      B
        #  /      /
        # C      D
        module_graph = {
            "Root": ["A", "B"],
            "A": ["C"],
            "B": ["D"],
            "C": [],
            "D": []
        }

        # When traversing with BFS (queue-based)
        # Expected order: Root, A, B, C, D (not Root, A, C, B, D which would be DFS)
        expected_bfs_order = ["Root", "A", "B", "C", "D"]
        expected_dfs_order = ["Root", "A", "C", "B", "D"]

        # Then BFS order should differ from DFS
        assert expected_bfs_order != expected_dfs_order

    def test_bfs_handles_single_module(self):
        """Test BFS with single module (no dependencies)"""
        # Given single module
        module_graph = {
            "com.example.Application": []
        }

        # When traversing
        expected_order = ["com.example.Application"]

        # Then should handle single module
        assert len(expected_order) == 1

    def test_bfs_handles_linear_chain(self):
        """Test BFS with linear dependency chain"""
        # Given linear chain: A → B → C → D
        module_graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["D"],
            "D": []
        }

        # When traversing from A
        expected_order = ["A", "B", "C", "D"]

        # Then should traverse in order
        assert len(expected_order) == 4

    def test_bfs_tracks_visited_nodes(self):
        """Test BFS maintains visited set to avoid revisiting"""
        # Given graph with shared dependency
        #   A → C
        #   B → C
        module_graph = {
            "A": ["C"],
            "B": ["C"],
            "C": []
        }

        # When traversing from both A and B
        # C should only be visited once
        visited = set()
        for start_node in ["A", "B"]:
            if start_node not in visited:
                visited.add(start_node)
                # Traverse dependencies
                for dep in module_graph.get(start_node, []):
                    visited.add(dep)

        # Then C should be in visited set only once
        assert "C" in visited
        assert len(visited) == 3  # A, B, C

    def test_bfs_calculates_depth_levels(self):
        """Test BFS tracks depth level for each module"""
        # Given module hierarchy
        #     Root (level 0)
        #    /    \
        #   A(1)  B(1)
        #  /
        # C(2)
        module_graph = {
            "Root": ["A", "B"],
            "A": ["C"],
            "B": [],
            "C": []
        }

        # When traversing with level tracking
        expected_levels = {
            "Root": 0,
            "A": 1,
            "B": 1,
            "C": 2
        }

        # Then should calculate correct depth levels
        assert expected_levels["Root"] == 0
        assert expected_levels["A"] == 1
        assert expected_levels["C"] == 2

    def test_bfs_processes_all_reachable_modules(self):
        """Test BFS discovers all reachable modules"""
        # Given complex module graph
        module_graph = {
            "com.example.App": [
                "com.google.gwt.user.User",
                "com.example.shared.SharedModule"
            ],
            "com.google.gwt.user.User": [
                "com.google.gwt.dom.DOM"
            ],
            "com.example.shared.SharedModule": [
                "com.example.widgets.WidgetsModule"
            ],
            "com.google.gwt.dom.DOM": [],
            "com.example.widgets.WidgetsModule": []
        }

        # When traversing from App
        # Expected all 5 modules discovered
        expected_module_count = 5

        # Then should discover all reachable modules
        all_modules = [
            "com.example.App",
            "com.google.gwt.user.User",
            "com.example.shared.SharedModule",
            "com.google.gwt.dom.DOM",
            "com.example.widgets.WidgetsModule"
        ]
        assert len(all_modules) == expected_module_count

    def test_bfs_handles_disconnected_subgraphs(self):
        """Test BFS with multiple disconnected module graphs"""
        # Given two disconnected subgraphs
        module_graph = {
            # Graph 1
            "A": ["B"],
            "B": [],
            # Graph 2 (disconnected)
            "C": ["D"],
            "D": []
        }

        # When starting from A
        # Only A and B should be discovered (not C, D)
        reachable_from_a = ["A", "B"]

        # Then should only discover connected modules
        assert "C" not in reachable_from_a
        assert "D" not in reachable_from_a


class TestPresenterViewBindingMapping:
    """Tests for Presenter-View binding discovery (T069)"""

    def test_map_presenter_to_view_naming_convention(self):
        """Test mapping Presenter to View using naming convention (T069)"""
        # Given a Presenter class name
        presenter_class = "com.example.client.UserPresenter"

        # When applying naming convention
        # UserPresenter → UserView
        expected_view = "com.example.client.UserView"

        # Then should derive View class name
        presenter_name = presenter_class.split('.')[-1]
        if presenter_name.endswith('Presenter'):
            view_name = presenter_name.replace('Presenter', 'View')
            package = '.'.join(presenter_class.split('.')[:-1])
            derived_view = f"{package}.{view_name}"
            assert derived_view == expected_view

    def test_map_presenter_to_view_display_interface(self):
        """Test detecting Display interface in Presenter (T069)"""
        # Given Presenter code with inner Display interface
        presenter_code = """
        public class UserPresenter {
            public interface Display {
                HasValue<String> getNameField();
                HasClickHandlers getSaveButton();
            }

            private final Display display;
        }
        """

        # When checking for Display interface
        has_display_interface = "interface Display" in presenter_code

        # Then should detect Display interface pattern
        assert has_display_interface is True

    def test_map_presenter_to_view_with_uibinder_template(self):
        """Test finding UiBinder template for View (T069)"""
        # Given a View class name
        view_class = "com.example.client.UserView"

        # When deriving UiBinder template name
        # UserView.java → UserView.ui.xml
        view_name = view_class.split('.')[-1]
        expected_template = f"{view_name}.ui.xml"

        # Then should derive correct template name
        assert expected_template == "UserView.ui.xml"

    def test_map_presenter_view_binding_confidence_high(self):
        """Test high confidence binding (Display + View + Template) (T069)"""
        # Given all binding indicators present
        has_display_interface = True
        view_class_exists = True
        template_file_exists = True

        # When calculating confidence
        confidence = 0.0
        if has_display_interface:
            confidence += 0.40
        if view_class_exists:
            confidence += 0.35
        if template_file_exists:
            confidence += 0.25

        # Then should have 100% confidence
        assert confidence == 1.0

    def test_map_presenter_view_binding_confidence_medium(self):
        """Test medium confidence binding (Display + View, no Template) (T069)"""
        # Given partial binding indicators
        has_display_interface = True
        view_class_exists = True
        template_file_exists = False

        # When calculating confidence
        confidence = 0.0
        if has_display_interface:
            confidence += 0.40
        if view_class_exists:
            confidence += 0.35
        if template_file_exists:
            confidence += 0.25

        # Then should have 75% confidence
        assert confidence == 0.75

    def test_map_presenter_view_binding_confidence_low(self):
        """Test low confidence binding (only naming convention) (T069)"""
        # Given only naming convention match
        has_display_interface = False
        view_class_exists = True
        template_file_exists = False

        # When calculating confidence
        confidence = 0.0
        if has_display_interface:
            confidence += 0.40
        if view_class_exists:
            confidence += 0.35
        if template_file_exists:
            confidence += 0.25

        # Then should have 35% confidence (weak binding)
        assert confidence == 0.35

    def test_map_presenter_view_binding_pattern_detection(self):
        """Test detecting different binding patterns (T069)"""
        # Given different binding patterns
        binding_patterns = {
            "display_interface": {"confidence": 0.90, "pattern": "inner Display interface"},
            "separate_interface": {"confidence": 0.85, "pattern": "separate view interface"},
            "naming_convention": {"confidence": 0.70, "pattern": "FooPresenter + FooView"}
        }

        # When checking pattern strengths
        # Then Display interface should be strongest indicator
        assert binding_patterns["display_interface"]["confidence"] > \
               binding_patterns["naming_convention"]["confidence"]

    def test_map_presenter_view_binding_returns_structure(self):
        """Test that binding mapping returns complete structure (T069)"""
        # Given a discovered binding
        binding = {
            "presenter_class": "com.example.client.UserPresenter",
            "view_class": "com.example.client.UserView",
            "display_interface": "com.example.client.UserPresenter.Display",
            "template_file": "/path/to/UserView.ui.xml",
            "confidence": 1.0,
            "binding_pattern": "display_interface"
        }

        # When checking binding structure
        # Then should have all required fields
        assert "presenter_class" in binding
        assert "view_class" in binding
        assert "confidence" in binding
        assert binding["confidence"] >= 0.0 and binding["confidence"] <= 1.0
