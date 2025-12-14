"""
Unit tests for GWT UiBinder Parser.

Tests:
- T028: UiBinder XML parsing with HTML entities
- T029: Form field extraction (TextBox, TextArea, CheckBox)
- T030: Label matching heuristic
- T031: ListBox options extraction
"""

import pytest
from pathlib import Path

# These imports will fail initially until GwtUiBinderParser is implemented
try:
    from codeindex.parsers.uibinder_parser import GwtUiBinderParser
    PARSER_AVAILABLE = True
except ImportError:
    PARSER_AVAILABLE = False


@pytest.fixture
def gwt_fixtures_dir():
    """Get path to GWT test fixtures."""
    return Path(__file__).parent.parent / "fixtures" / "gwt"


@pytest.fixture
def uibinder_content(gwt_fixtures_dir):
    """Load FlashInfoEditView.ui.xml content."""
    file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"
    return file_path.read_text(encoding='utf-8')


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="GwtUiBinderParser not yet implemented")
class TestUiBinderXmlParsing:
    """T028: Test UiBinder XML parsing with HTML entities."""

    def test_parse_valid_uibinder_xml(self, gwt_fixtures_dir, uibinder_content):
        """Test that parser can parse valid UiBinder XML."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)

        assert result is not None
        assert 'form_fields' in result
        assert isinstance(result['form_fields'], list)

    def test_handle_html_entities(self, gwt_fixtures_dir, uibinder_content):
        """Test that parser handles HTML entities like &nbsp; correctly."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)

        # Should not crash on &nbsp; and other entities
        assert result is not None
        # Check that labels with &nbsp; were parsed
        labels = [field.get('label', '') for field in result['form_fields']]
        # Should have successfully extracted labels even with HTML entities
        assert any('Title' in label for label in labels)

    def test_parse_malformed_xml(self, tmp_path):
        """Test that parser handles malformed XML gracefully."""
        parser = GwtUiBinderParser()

        # Create malformed XML (unclosed tag)
        malformed_xml = """
        <ui:UiBinder xmlns:ui="urn:ui:com.google.gwt.uibinder"
                     xmlns:g="urn:import:com.google.gwt.user.client.ui">
            <g:HTMLPanel>
                <g:TextBox ui:field="testField"
            </g:HTMLPanel>
        </ui:UiBinder>
        """

        file_path = tmp_path / "malformed.ui.xml"
        file_path.write_text(malformed_xml)

        # Should return minimal valid result, not crash
        result = parser.parse(file_path, malformed_xml)

        assert result is not None
        assert 'form_fields' in result
        assert 'error' in result or len(result['form_fields']) == 0


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="GwtUiBinderParser not yet implemented")
class TestFormFieldExtraction:
    """T029: Test form field extraction (TextBox, TextArea, CheckBox)."""

    def test_extract_textbox_fields(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of TextBox fields."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find TextBox fields
        textboxes = [f for f in form_fields if f['widget_type'] == 'TextBox']

        assert len(textboxes) >= 2  # titleTextBox, authorTextBox
        field_names = [f['field_name'] for f in textboxes]
        assert 'titleTextBox' in field_names
        assert 'authorTextBox' in field_names

    def test_extract_textarea_fields(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of TextArea fields."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find TextArea fields
        textareas = [f for f in form_fields if f['widget_type'] == 'TextArea']

        assert len(textareas) >= 1  # descriptionTextArea
        textarea = textareas[0]
        assert textarea['field_name'] == 'descriptionTextArea'

    def test_extract_checkbox_fields(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of CheckBox fields."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find CheckBox fields
        checkboxes = [f for f in form_fields if f['widget_type'] == 'CheckBox']

        assert len(checkboxes) >= 2  # activeCheckBox, notifyCheckBox
        field_names = [f['field_name'] for f in checkboxes]
        assert 'activeCheckBox' in field_names
        assert 'notifyCheckBox' in field_names

    def test_extract_datebox_fields(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of DateBox fields."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find DateBox fields
        dateboxes = [f for f in form_fields if f['widget_type'] == 'DateBox']

        assert len(dateboxes) >= 1  # expirationDateBox
        datebox = dateboxes[0]
        assert datebox['field_name'] == 'expirationDateBox'

    def test_extract_button_fields(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of Button fields."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find Button fields
        buttons = [f for f in form_fields if f['widget_type'] == 'Button']

        assert len(buttons) >= 2  # saveButton, cancelButton
        field_names = [f['field_name'] for f in buttons]
        assert 'saveButton' in field_names
        assert 'cancelButton' in field_names

    def test_field_structure(self, gwt_fixtures_dir, uibinder_content):
        """Test that extracted fields have required structure."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        assert len(form_fields) > 0

        # Check first field has required attributes
        field = form_fields[0]
        assert 'field_name' in field
        assert 'widget_type' in field
        assert 'label' in field  # May be empty string if no label found


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="GwtUiBinderParser not yet implemented")
class TestLabelMatching:
    """T030: Test label matching heuristic."""

    def test_match_explicit_label_widget(self, gwt_fixtures_dir, uibinder_content):
        """Test matching labels defined with g:Label widget."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find titleTextBox - should have matched titleLabel
        title_field = next((f for f in form_fields if f['field_name'] == 'titleTextBox'), None)

        assert title_field is not None
        assert title_field['label'] is not None
        assert 'Title' in title_field['label']

    def test_match_label_by_proximity(self, gwt_fixtures_dir, uibinder_content):
        """Test matching labels in same table row."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find descriptionTextArea - should have matched descriptionLabel
        desc_field = next((f for f in form_fields if f['field_name'] == 'descriptionTextArea'), None)

        assert desc_field is not None
        assert desc_field['label'] is not None
        assert 'Description' in desc_field['label']

    def test_match_label_by_text_content(self, gwt_fixtures_dir, uibinder_content):
        """Test matching labels by plain text in same row."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find authorTextBox - has plain text "Author:" in same row
        author_field = next((f for f in form_fields if f['field_name'] == 'authorTextBox'), None)

        assert author_field is not None
        # Should have extracted label from text content
        assert author_field['label'] is not None
        assert 'Author' in author_field['label']

    def test_checkbox_label_from_text_content(self, gwt_fixtures_dir, uibinder_content):
        """Test that CheckBox labels come from their text content."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find activeCheckBox - has inline text "Active (visible to users)"
        active_checkbox = next((f for f in form_fields if f['field_name'] == 'activeCheckBox'), None)

        assert active_checkbox is not None
        assert active_checkbox['label'] is not None
        assert 'Active' in active_checkbox['label']

    def test_button_label_from_text_content(self, gwt_fixtures_dir, uibinder_content):
        """Test that Button labels come from their text content."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find saveButton - has text "Save"
        save_button = next((f for f in form_fields if f['field_name'] == 'saveButton'), None)

        assert save_button is not None
        assert save_button['label'] == 'Save'


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="GwtUiBinderParser not yet implemented")
class TestListBoxOptionsExtraction:
    """T031: Test ListBox options extraction."""

    def test_extract_listbox_options(self, gwt_fixtures_dir, uibinder_content):
        """Test extraction of ListBox options."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find ListBox fields
        listboxes = [f for f in form_fields if f['widget_type'] == 'ListBox']

        assert len(listboxes) >= 2  # categoryListBox, priorityListBox

    def test_category_listbox_options(self, gwt_fixtures_dir, uibinder_content):
        """Test that category ListBox has correct options."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find categoryListBox
        category_listbox = next((f for f in form_fields if f['field_name'] == 'categoryListBox'), None)

        assert category_listbox is not None
        assert 'options' in category_listbox
        options = category_listbox['options']

        # Should have 4 options
        assert len(options) == 4

        # Check option values and labels
        option_values = [opt['value'] for opt in options]
        option_labels = [opt['label'] for opt in options]

        assert 'NEWS' in option_values
        assert 'ALERT' in option_values
        assert 'INFO' in option_values
        assert 'WARNING' in option_values

        assert 'News' in option_labels
        assert 'Alert' in option_labels

    def test_priority_listbox_options(self, gwt_fixtures_dir, uibinder_content):
        """Test that priority ListBox has correct options."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find priorityListBox
        priority_listbox = next((f for f in form_fields if f['field_name'] == 'priorityListBox'), None)

        assert priority_listbox is not None
        assert 'options' in priority_listbox
        options = priority_listbox['options']

        # Should have 4 options
        assert len(options) == 4

        # Check option values
        option_values = [opt['value'] for opt in options]
        assert 'LOW' in option_values
        assert 'MEDIUM' in option_values
        assert 'HIGH' in option_values
        assert 'CRITICAL' in option_values

    def test_listbox_option_structure(self, gwt_fixtures_dir, uibinder_content):
        """Test that ListBox options have correct structure."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)
        form_fields = result['form_fields']

        # Find any ListBox
        listbox = next((f for f in form_fields if f['widget_type'] == 'ListBox'), None)

        assert listbox is not None
        assert 'options' in listbox
        assert isinstance(listbox['options'], list)

        if listbox['options']:
            option = listbox['options'][0]
            assert 'value' in option
            assert 'label' in option


@pytest.mark.skipif(not PARSER_AVAILABLE, reason="GwtUiBinderParser not yet implemented")
class TestUiBinderParserIntegration:
    """Integration tests for complete UiBinder parser workflow."""

    def test_parse_complete_form(self, gwt_fixtures_dir, uibinder_content):
        """Test complete parsing of realistic UiBinder form."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        result = parser.parse(file_path, uibinder_content)

        # Should extract all form fields
        form_fields = result['form_fields']

        # Should have at least:
        # - 2 TextBox (title, author)
        # - 1 TextArea (description)
        # - 2 ListBox (category, priority)
        # - 2 CheckBox (active, notify)
        # - 1 DateBox (expiration)
        # - 2 Button (save, cancel)
        assert len(form_fields) >= 10

        # Check widget type distribution
        widget_types = [f['widget_type'] for f in form_fields]
        assert 'TextBox' in widget_types
        assert 'TextArea' in widget_types
        assert 'ListBox' in widget_types
        assert 'CheckBox' in widget_types
        assert 'DateBox' in widget_types
        assert 'Button' in widget_types

    def test_can_analyze_uibinder_files(self, gwt_fixtures_dir):
        """Test that parser can identify UiBinder files."""
        parser = GwtUiBinderParser()
        file_path = gwt_fixtures_dir / "FlashInfoEditView.ui.xml"

        assert parser.can_analyze(file_path) is True

    def test_cannot_analyze_non_uibinder_files(self, tmp_path):
        """Test that parser rejects non-UiBinder files."""
        parser = GwtUiBinderParser()

        # Create a non-UiBinder XML file
        regular_xml = tmp_path / "config.xml"
        regular_xml.write_text("<config><setting>value</setting></config>")

        assert parser.can_analyze(regular_xml) is False

        # Create a Java file
        java_file = tmp_path / "Test.java"
        java_file.write_text("public class Test {}")

        assert parser.can_analyze(java_file) is False

    def test_validation_warns_missing_ui_field(self, tmp_path):
        """Test validation warns about widgets without ui:field attribute."""
        parser = GwtUiBinderParser()

        # Create UiBinder with field missing ui:field
        content = """
        <ui:UiBinder xmlns:ui="urn:ui:com.google.gwt.uibinder"
                     xmlns:g="urn:import:com.google.gwt.user.client.ui">
            <g:HTMLPanel>
                <g:TextBox width="200px"/>
            </g:HTMLPanel>
        </ui:UiBinder>
        """

        file_path = tmp_path / "test.ui.xml"
        file_path.write_text(content)

        result = parser.parse(file_path, content)

        # Should have warnings about missing ui:field
        assert 'warnings' in result
        assert len(result['warnings']) > 0
        assert any('ui:field' in w for w in result['warnings'])
