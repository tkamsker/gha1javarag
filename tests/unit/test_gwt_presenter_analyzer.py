"""
Unit tests for GWT Presenter Analyzer.

Tests:
- T044: Display interface detection (90% confidence)
- T045: Separate interface detection (85% confidence)
- T046: Naming convention detection (70% confidence)
- T047: Event handler extraction
- T048: Navigation logic extraction
"""

import pytest
from pathlib import Path

# These imports will fail initially until GwtPresenterAnalyzer is implemented
try:
    from codeindex.services.gwt_presenter_analyzer import GwtPresenterAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def flash_admin_presenter_content(gwt_fixtures_dir):
    """Load FlashAdministrationPresenter.java content."""
    file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"
    return file_path.read_text(encoding='utf-8')


@pytest.fixture
def user_list_presenter_content(gwt_fixtures_dir):
    """Load UserListPresenter.java content."""
    file_path = gwt_fixtures_dir / "UserListPresenter.java"
    return file_path.read_text(encoding='utf-8')


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestDisplayInterfaceDetection:
    """T044: Test Display interface detection (90% confidence)."""

    def test_detect_nested_display_interface(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test detection of nested Display interface pattern."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        assert result is not None
        assert 'view_binding' in result
        assert result['view_binding'] is not None

        binding = result['view_binding']
        assert binding['strategy'] == 'nested_display_interface'
        assert binding['confidence'] >= 0.90
        assert binding['view_interface'] == 'Display'

    def test_display_interface_in_constructor(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test that Display parameter is detected in constructor."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        binding = result['view_binding']
        assert 'constructor_param' in binding
        assert binding['constructor_param'] == 'view'

    def test_display_interface_stored_in_field(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test that Display is stored in field."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        binding = result['view_binding']
        assert 'view_field' in binding
        assert binding['view_field'] == 'view'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestSeparateInterfaceDetection:
    """T045: Test separate interface detection (85% confidence)."""

    def test_detect_separate_view_interface(self, gwt_fixtures_dir, user_list_presenter_content):
        """Test detection of separate view interface pattern."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "UserListPresenter.java"

        result = analyzer.analyze(file_path, user_list_presenter_content)

        assert result is not None
        assert 'view_binding' in result
        binding = result['view_binding']

        assert binding['strategy'] == 'separate_interface'
        assert binding['confidence'] >= 0.85
        assert binding['view_interface'] == 'IUserListView'

    def test_separate_interface_constructor_injection(self, gwt_fixtures_dir, user_list_presenter_content):
        """Test that separate interface is injected via constructor."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "UserListPresenter.java"

        result = analyzer.analyze(file_path, user_list_presenter_content)

        binding = result['view_binding']
        assert binding['constructor_param'] == 'view'
        assert binding['view_field'] == 'view'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestNamingConventionDetection:
    """T046: Test naming convention detection (70% confidence)."""

    def test_detect_by_naming_convention(self, tmp_path):
        """Test detection by naming convention (Presenter/View pattern)."""
        analyzer = GwtPresenterAnalyzer()

        # Create presenter with naming convention pattern
        content = """
        package com.example.client;

        import com.example.client.FlashInfoView;

        public class FlashInfoPresenter {
            private final FlashInfoView view;

            public FlashInfoPresenter(FlashInfoView view) {
                this.view = view;
            }
        }
        """

        file_path = tmp_path / "FlashInfoPresenter.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        assert result is not None
        assert 'view_binding' in result
        binding = result['view_binding']

        assert binding['strategy'] == 'naming_convention'
        assert binding['confidence'] >= 0.70
        assert 'FlashInfoView' in binding['view_interface']

    def test_naming_convention_lower_confidence(self, tmp_path):
        """Test that naming convention has lower confidence than explicit patterns."""
        analyzer = GwtPresenterAnalyzer()

        content = """
        public class UserPresenter {
            private final UserView view;
            public UserPresenter(UserView view) { this.view = view; }
        }
        """

        file_path = tmp_path / "UserPresenter.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)
        binding = result['view_binding']

        # Naming convention should have lower confidence (70%)
        assert binding['confidence'] < 0.85


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestEventHandlerExtraction:
    """T047: Test event handler extraction."""

    def test_extract_click_handlers(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test extraction of ClickHandler event handlers."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        assert 'event_handlers' in result
        handlers = result['event_handlers']

        assert len(handlers) >= 3  # create, refresh, delete buttons

        # Check handler structure
        for handler in handlers:
            assert 'handler_type' in handler
            assert 'widget_getter' in handler
            assert 'action_method' in handler

    def test_identify_handler_actions(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test that handler actions are correctly identified."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)
        handlers = result['event_handlers']

        # Find create button handler
        create_handler = next((h for h in handlers if 'Create' in h['widget_getter']), None)
        assert create_handler is not None
        assert create_handler['action_method'] == 'handleCreate'

    def test_multiple_handler_types(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test extraction of different handler types."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)
        handlers = result['event_handlers']

        # Should all be ClickHandler for this fixture
        handler_types = [h['handler_type'] for h in handlers]
        assert 'ClickHandler' in handler_types


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestNavigationLogicExtraction:
    """T048: Test navigation logic extraction."""

    def test_extract_navigation_calls(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test extraction of navigation method calls."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        assert 'navigation_logic' in result
        navigation = result['navigation_logic']

        assert len(navigation) >= 2  # handleCreate and navigateToDashboard

    def test_identify_place_navigation(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test identification of Place-based navigation."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)
        navigation = result['navigation_logic']

        # Check for Place navigation pattern
        place_nav = [n for n in navigation if 'Place' in n.get('target', '')]
        assert len(place_nav) >= 1

        # Should have DashboardPlace
        dashboard_nav = next((n for n in navigation if 'Dashboard' in n.get('target', '')), None)
        assert dashboard_nav is not None

    def test_identify_url_navigation(self, gwt_fixtures_dir, user_list_presenter_content):
        """Test identification of URL-based navigation."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "UserListPresenter.java"

        result = analyzer.analyze(file_path, user_list_presenter_content)
        navigation = result['navigation_logic']

        # UserListPresenter uses navigateTo("/user/...")
        url_nav = [n for n in navigation if n.get('navigation_type') == 'url']
        assert len(url_nav) >= 2  # /user/create and /user/edit

    def test_navigation_from_method(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test that navigation calls are linked to their source methods."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)
        navigation = result['navigation_logic']

        # Check navigation structure
        for nav in navigation:
            assert 'source_method' in nav
            assert 'target' in nav


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtPresenterAnalyzer not yet implemented")
class TestPresenterAnalyzerIntegration:
    """Integration tests for complete presenter analysis."""

    def test_analyze_complete_presenter(self, gwt_fixtures_dir, flash_admin_presenter_content):
        """Test complete analysis of presenter."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        result = analyzer.analyze(file_path, flash_admin_presenter_content)

        # Check structure
        assert result['gwt_role'] == 'presenter'
        assert 'presenter_name' in result
        assert result['presenter_name'] == 'FlashAdministrationPresenter'
        assert 'view_binding' in result
        assert 'event_handlers' in result
        assert 'navigation_logic' in result
        assert 'rpc_calls' in result

    def test_can_analyze_presenter_files(self, gwt_fixtures_dir):
        """Test that analyzer can identify presenter files."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationPresenter.java"

        assert analyzer.can_analyze(file_path) is True

    def test_cannot_analyze_non_presenter_files(self, gwt_fixtures_dir):
        """Test that analyzer rejects non-presenter files."""
        analyzer = GwtPresenterAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        assert analyzer.can_analyze(file_path) is False

    def test_confidence_scoring_comparison(self, gwt_fixtures_dir, flash_admin_presenter_content, user_list_presenter_content):
        """Test that different patterns have different confidence scores."""
        analyzer = GwtPresenterAnalyzer()

        # Analyze Display interface pattern (should be 90%)
        result1 = analyzer.analyze(
            gwt_fixtures_dir / "FlashAdministrationPresenter.java",
            flash_admin_presenter_content
        )

        # Analyze separate interface pattern (should be 85%)
        result2 = analyzer.analyze(
            gwt_fixtures_dir / "UserListPresenter.java",
            user_list_presenter_content
        )

        confidence1 = result1['view_binding']['confidence']
        confidence2 = result2['view_binding']['confidence']

        # Display interface should have higher confidence
        assert confidence1 > confidence2
        assert confidence1 >= 0.90
        assert confidence2 >= 0.85
