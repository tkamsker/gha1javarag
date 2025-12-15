"""
Unit tests for GWT View Analyzer.

Tests:
- T049: View component type detection
- T050: UiBinder template linking
"""

import pytest
from pathlib import Path

# These imports will fail initially until GwtViewAnalyzer is implemented
try:
    from codeindex.services.gwt_view_analyzer import GwtViewAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def flash_admin_view_content(gwt_fixtures_dir):
    """Load FlashAdministrationView.java content."""
    file_path = gwt_fixtures_dir / "FlashAdministrationView.java"
    return file_path.read_text(encoding='utf-8')


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtViewAnalyzer not yet implemented")
class TestComponentTypeDetection:
    """T049: Test view component type detection."""

    def test_detect_composite_view(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test detection of Composite-based views."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        assert result is not None
        assert 'component_type' in result
        assert result['component_type'] == 'Composite'

    def test_detect_popup_dialog(self, tmp_path):
        """Test detection of PopupPanel/DialogBox views."""
        analyzer = GwtViewAnalyzer()

        content = """
        package com.example.client;

        import com.google.gwt.user.client.ui.PopupPanel;

        public class ConfirmDialog extends PopupPanel {
            public ConfirmDialog() {
                super(true);  // auto-hide
            }
        }
        """

        file_path = tmp_path / "ConfirmDialog.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        assert result['component_type'] == 'PopupPanel'

    def test_detect_portlet(self, tmp_path):
        """Test detection of Portlet views."""
        analyzer = GwtViewAnalyzer()

        content = """
        package com.example.client;

        import com.google.gwt.user.client.ui.Panel;

        public class DashboardPortlet extends Panel {
            public DashboardPortlet() {
                // Portlet initialization
            }
        }
        """

        file_path = tmp_path / "DashboardPortlet.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        # Should detect as Panel-based component
        assert result['component_type'] in ['Panel', 'Portlet']

    def test_detect_widget_type(self, tmp_path):
        """Test detection of custom Widget views."""
        analyzer = GwtViewAnalyzer()

        content = """
        package com.example.client;

        import com.google.gwt.user.client.ui.Widget;

        public class CustomButton extends Widget {
            public CustomButton(String label) {
                // Custom widget
            }
        }
        """

        file_path = tmp_path / "CustomButton.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        assert result['component_type'] == 'Widget'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtViewAnalyzer not yet implemented")
class TestUiBinderTemplateLink:
    """T050: Test UiBinder template linking."""

    def test_detect_uibinder_interface(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test detection of UiBinder interface."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        assert 'uibinder_template' in result
        assert result['uibinder_template'] is not None

    def test_extract_template_filename(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test extraction of UiBinder template filename from @UiTemplate."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        template = result['uibinder_template']
        assert template['template_file'] == 'FlashAdministrationView.ui.xml'

    def test_detect_default_template_name(self, tmp_path):
        """Test detection of default template name (no @UiTemplate annotation)."""
        analyzer = GwtViewAnalyzer()

        content = """
        package com.example.client;

        import com.google.gwt.uibinder.client.UiBinder;
        import com.google.gwt.core.client.GWT;
        import com.google.gwt.user.client.ui.Composite;
        import com.google.gwt.user.client.ui.Widget;

        public class UserView extends Composite {
            interface UserViewUiBinder extends UiBinder<Widget, UserView> {}
            private static UserViewUiBinder uiBinder = GWT.create(UserViewUiBinder.class);

            public UserView() {
                initWidget(uiBinder.createAndBindUi(this));
            }
        }
        """

        file_path = tmp_path / "UserView.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        # Should infer default template name
        template = result['uibinder_template']
        assert template['template_file'] == 'UserView.ui.xml'

    def test_extract_ui_fields(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test extraction of @UiField bindings."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        assert 'ui_fields' in result
        ui_fields = result['ui_fields']

        assert len(ui_fields) >= 5  # dataTable, buttons, labels

        # Check field structure
        for field in ui_fields:
            assert 'field_name' in field
            assert 'field_type' in field

    def test_identify_field_types(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test that field types are correctly identified."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)
        ui_fields = result['ui_fields']

        # Find specific fields
        field_names = [f['field_name'] for f in ui_fields]
        assert 'dataTable' in field_names
        assert 'createButton' in field_names
        assert 'refreshButton' in field_names

        # Check button type
        button_field = next(f for f in ui_fields if f['field_name'] == 'createButton')
        assert button_field['field_type'] == 'Button'


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtViewAnalyzer not yet implemented")
class TestViewImplementsInterface:
    """Test detection of view implementing presenter interface."""

    def test_detect_implemented_interface(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test that view's implemented interface is detected."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        assert 'implements_interface' in result
        assert result['implements_interface'] == 'Display'

    def test_link_to_presenter(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test that link to presenter is established."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        assert 'presenter_interface' in result
        # Should reference FlashAdministrationPresenter.Display
        assert 'FlashAdministrationPresenter' in result['presenter_interface']


@pytest.mark.skipif(not ANALYZER_AVAILABLE, reason="GwtViewAnalyzer not yet implemented")
class TestViewAnalyzerIntegration:
    """Integration tests for complete view analysis."""

    def test_analyze_complete_view(self, gwt_fixtures_dir, flash_admin_view_content):
        """Test complete analysis of view."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        result = analyzer.analyze(file_path, flash_admin_view_content)

        # Check structure
        assert result['gwt_role'] == 'view'
        assert 'view_name' in result
        assert result['view_name'] == 'FlashAdministrationView'
        assert 'component_type' in result
        assert 'uibinder_template' in result
        assert 'ui_fields' in result
        assert 'implements_interface' in result

    def test_can_analyze_view_files(self, gwt_fixtures_dir):
        """Test that analyzer can identify view files."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashAdministrationView.java"

        assert analyzer.can_analyze(file_path) is True

    def test_cannot_analyze_non_view_files(self, gwt_fixtures_dir):
        """Test that analyzer rejects non-view files."""
        analyzer = GwtViewAnalyzer()
        file_path = gwt_fixtures_dir / "FlashInfoDTO.java"

        assert analyzer.can_analyze(file_path) is False

    def test_view_without_uibinder(self, tmp_path):
        """Test analysis of view without UiBinder."""
        analyzer = GwtViewAnalyzer()

        content = """
        package com.example.client;

        import com.google.gwt.user.client.ui.Composite;
        import com.google.gwt.user.client.ui.Button;
        import com.google.gwt.user.client.ui.VerticalPanel;

        public class SimpleView extends Composite {
            private Button okButton;
            private VerticalPanel panel;

            public SimpleView() {
                panel = new VerticalPanel();
                okButton = new Button("OK");
                panel.add(okButton);
                initWidget(panel);
            }
        }
        """

        file_path = tmp_path / "SimpleView.java"
        file_path.write_text(content)

        result = analyzer.analyze(file_path, content)

        # Should still analyze, just without UiBinder info
        assert result is not None
        assert result['gwt_role'] == 'view'
        assert result['uibinder_template'] is None
