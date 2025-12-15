"""
GWT UiBinder XML Parser

Parses UiBinder XML templates to extract:
- Form fields (TextBox, TextArea, ListBox, CheckBox, etc.)
- Widget types and ui:field bindings
- Labels and associated text
- ListBox options

Implements FR-004 from the specification.
"""

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional


logger = logging.getLogger(__name__)


class GwtUiBinderParser:
    """
    Parser for GWT UiBinder XML templates.

    Extracts form fields, widget bindings, and UI structure
    from UiBinder XML files.
    """

    # Namespace mapping for GWT UiBinder
    NAMESPACES = {
        'ui': 'urn:ui:com.google.gwt.uibinder',
        'g': 'urn:import:com.google.gwt.user.client.ui'
    }

    # Widget types we care about for forms
    FORM_WIDGET_TYPES = {
        'TextBox', 'TextArea', 'PasswordTextBox', 'IntegerBox', 'DoubleBox',
        'ListBox', 'CheckBox', 'RadioButton',
        'DateBox', 'DatePicker',
        'Button', 'SubmitButton', 'ResetButton',
        'Label', 'HTML', 'HTMLPanel'
    }

    def __init__(self):
        """Initialize UiBinder parser."""
        self.logger = logging.getLogger(__name__)

    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this parser can handle the file.

        Args:
            file_path: Path to file

        Returns:
            True if file is a UiBinder XML template
        """
        # Check file extension
        if not str(file_path).endswith('.ui.xml'):
            return False

        # Quick content check
        try:
            content = file_path.read_text(encoding='utf-8')
            return 'ui:UiBinder' in content
        except Exception:
            return False

    def analyze(self, file_path: Path, content: str, semantic_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze UiBinder XML template and extract GWT metadata.

        This is the main entry point called by the GWT analyzer registry.
        Wraps the parse() method and adds GWT-specific metadata.

        Args:
            file_path: Path to .ui.xml file
            content: XML content
            semantic_data: Optional AI-generated semantic data (not used for UiBinder)

        Returns:
            Dictionary with GWT UiBinder metadata including form fields
        """
        from codeindex.utils.gwt_patterns import GwtRole

        # Use the parse method to extract fields
        parse_result = self.parse(file_path, content)

        # Add GWT-specific metadata
        result = {
            'gwt_role': GwtRole.UI_BINDER.value,
            'template_name': parse_result['template_name'],
            'template_path': parse_result['template_path'],
            'form_fields': parse_result['form_fields'],
            'field_count': parse_result['field_count'],
            'warnings': parse_result.get('warnings', [])
        }

        # Include error if present
        if 'error' in parse_result:
            result['error'] = parse_result['error']

        return result

    def parse(self, file_path: Path, content: str) -> Dict[str, Any]:
        """
        Parse UiBinder XML template and extract form fields.

        Args:
            file_path: Path to .ui.xml file
            content: XML content

        Returns:
            Dictionary with form fields, labels, and metadata
        """
        self.logger.debug(f"Parsing UiBinder template: {file_path.name}")

        try:
            # Parse XML with HTML entity support
            root = self._parse_xml_with_entities(content)

            if root is None:
                return self._error_result("Failed to parse XML")

            # Extract form fields
            form_fields = self.parse_form_fields(root, content)

            # Extract metadata
            result = {
                'template_name': file_path.stem,
                'template_path': str(file_path),
                'form_fields': form_fields,
                'field_count': len(form_fields),
                'warnings': []
            }

            # Validate and add warnings
            warnings = self._validate_form_fields(form_fields, content)
            result['warnings'] = warnings

            self.logger.info(
                f"Extracted {len(form_fields)} form fields from {file_path.name}"
            )

            return result

        except Exception as e:
            self.logger.error(f"Error parsing UiBinder template {file_path}: {e}", exc_info=True)
            return self._error_result(str(e))

    def parse_form_fields(self, root: ET.Element, content: str) -> List[Dict[str, Any]]:
        """
        Extract all form fields from UiBinder XML.

        Args:
            root: XML root element
            content: Original XML content for label matching

        Returns:
            List of form field dictionaries
        """
        form_fields = []

        # Find all widgets with ui:field attribute
        for widget in root.iter():
            # Get tag name without namespace
            tag_name = self._strip_namespace(widget.tag)

            # Check if this is a form widget
            if tag_name not in self.FORM_WIDGET_TYPES:
                continue

            # Get ui:field attribute
            ui_field = widget.get('{urn:ui:com.google.gwt.uibinder}field')

            if not ui_field:
                continue

            # Build field data
            field_data = {
                'field_name': ui_field,
                'widget_type': tag_name,
                'label': self.find_associated_labels(widget, ui_field, content),
                'attributes': dict(widget.attrib)
            }

            # Extract ListBox options if applicable
            if tag_name == 'ListBox':
                field_data['options'] = self.extract_select_options(widget)

            form_fields.append(field_data)

        return form_fields

    def extract_select_options(self, listbox_element: ET.Element) -> List[Dict[str, str]]:
        """
        Extract options from a ListBox widget.

        Args:
            listbox_element: ListBox XML element

        Returns:
            List of option dictionaries with value and label
        """
        options = []

        # Find all g:item children
        for item in listbox_element:
            tag_name = self._strip_namespace(item.tag)

            if tag_name == 'item':
                value = item.get('value', '')
                label = item.text or ''

                options.append({
                    'value': value,
                    'label': label.strip()
                })

        return options

    def find_associated_labels(
        self,
        widget: ET.Element,
        field_name: str,
        content: str
    ) -> Optional[str]:
        """
        Find label associated with a widget using heuristics.

        Strategy:
        1. For CheckBox/Button: Use inline text content
        2. Look for g:Label with ui:field matching pattern (fieldLabel)
        3. Look for Label in same table row
        4. Look for plain text in same table row

        Args:
            widget: Widget XML element
            field_name: ui:field name
            content: Full XML content

        Returns:
            Label text or None
        """
        widget_type = self._strip_namespace(widget.tag)

        # Strategy 1: For CheckBox and Button, use inline text
        if widget_type in ['CheckBox', 'RadioButton', 'Button', 'SubmitButton', 'ResetButton']:
            text = self._get_element_text(widget)
            if text:
                return text.strip()

        # Strategy 2: Look for explicit Label widget with matching ui:field
        # e.g., titleTextBox → titleLabel
        label_field_name = field_name.replace('TextBox', 'Label').replace('TextArea', 'Label') \
                                     .replace('ListBox', 'Label').replace('DateBox', 'Label') \
                                     .replace('CheckBox', 'Label')

        if label_field_name != field_name:
            # Search for Label with this ui:field in content
            # More flexible pattern to handle content across lines and with nested tags
            label_pattern = rf'<g:Label\s+ui:field="{label_field_name}"[^>]*>(.*?)</g:Label>'
            match = re.search(label_pattern, content, re.DOTALL)
            if match:
                label_text = match.group(1)
                # Clean up HTML entities and extra whitespace
                label_text = self._clean_label_text(label_text)
                if label_text:
                    return label_text

        # Strategy 3: Look for Label in same table row
        # Find parent <tr> and look for any Label
        parent = self._find_parent_tr(widget, content)
        if parent:
            label_pattern = r'<g:Label[^>]*>(.*?)</g:Label>'
            matches = re.finditer(label_pattern, parent, re.DOTALL)
            for match in matches:
                label_text = self._clean_label_text(match.group(1))
                if label_text:
                    return label_text

        # Strategy 4: Look for plain text in same <td> before widget
        # This is a fallback for simple cases like <td>Author:</td>
        widget_pattern = rf'ui:field="{re.escape(field_name)}"'
        widget_pos = content.find(widget_pattern)
        if widget_pos > 0:
            # Find the <tr> containing this widget
            tr_start = content.rfind('<tr', 0, widget_pos)
            if tr_start >= 0:
                tr_end = content.find('</tr>', widget_pos)
                if tr_end > 0:
                    row_content = content[tr_start:tr_end]

                    # Look for plain text in <td> cells
                    # Pattern: <td>...text...</td> before our widget
                    td_pattern = r'<td[^>]*>(.*?)</td>'
                    td_matches = re.finditer(td_pattern, row_content, re.DOTALL)

                    for td_match in td_matches:
                        td_content = td_match.group(1)

                        # Skip if this <td> contains our widget
                        if field_name in td_content:
                            continue

                        # Extract text without tags
                        text = re.sub(r'<[^>]+>', '', td_content)
                        text = self._clean_label_text(text)

                        # Return if we found meaningful text
                        if text and len(text) > 0 and len(text) < 50:
                            return text

        return ''  # Return empty string instead of None for consistency

    def _parse_xml_with_entities(self, content: str) -> Optional[ET.Element]:
        """
        Parse XML content with HTML entity support.

        Handles entities like &nbsp;, &lt;, &gt;, etc.

        Args:
            content: XML string

        Returns:
            Root element or None on error
        """
        try:
            # Replace HTML entities that might not be in XML
            # Common entities in UiBinder templates
            content = content.replace('&nbsp;', ' ')
            content = content.replace('&mdash;', '—')
            content = content.replace('&ldquo;', '"')
            content = content.replace('&rdquo;', '"')

            # Parse XML
            root = ET.fromstring(content)
            return root

        except ET.ParseError as e:
            self.logger.warning(f"XML parse error: {e}")
            # Try to recover by parsing as much as possible
            try:
                # Remove problematic parts and try again
                content = re.sub(r'<!DOCTYPE[^>]+>', '', content)
                root = ET.fromstring(content)
                return root
            except Exception:
                return None

    def _strip_namespace(self, tag: str) -> str:
        """
        Remove namespace from XML tag.

        Args:
            tag: Tag with namespace like {urn:import:...}TextBox

        Returns:
            Tag without namespace like TextBox
        """
        if '}' in tag:
            return tag.split('}', 1)[1]
        return tag

    def _get_element_text(self, element: ET.Element) -> str:
        """
        Get all text content from element and children.

        Args:
            element: XML element

        Returns:
            Concatenated text content
        """
        texts = []

        if element.text:
            texts.append(element.text)

        for child in element:
            texts.append(self._get_element_text(child))
            if child.tail:
                texts.append(child.tail)

        return ' '.join(texts)

    def _clean_label_text(self, text: str) -> str:
        """
        Clean label text by removing HTML entities, extra whitespace, etc.

        Args:
            text: Raw label text

        Returns:
            Cleaned label text
        """
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')

        # Remove asterisks and colons (common label decorations)
        text = re.sub(r'[*:]+$', '', text)

        # Remove content in parentheses (like class names)
        text = re.sub(r'\{[^}]+\}', '', text)

        # Remove span tags and content
        text = re.sub(r'<span[^>]*>.*?</span>', '', text)

        # Remove all remaining tags
        text = re.sub(r'<[^>]+>', '', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text.strip()

    def _find_parent_tr(self, widget: ET.Element, content: str) -> Optional[str]:
        """
        Find parent <tr> element content in raw XML.

        This is a fallback when element tree navigation doesn't work.

        Args:
            widget: Widget element
            content: Full XML content

        Returns:
            <tr> content or None
        """
        # Get ui:field to locate widget in content
        ui_field = widget.get('{urn:ui:com.google.gwt.uibinder}field')
        if not ui_field:
            return None

        # Find widget in content
        widget_pattern = rf'ui:field="{ui_field}"'
        widget_pos = content.find(widget_pattern)

        if widget_pos < 0:
            return None

        # Find enclosing <tr>
        tr_start = content.rfind('<tr', 0, widget_pos)
        if tr_start < 0:
            return None

        tr_end = content.find('</tr>', widget_pos)
        if tr_end < 0:
            return None

        return content[tr_start:tr_end + 5]

    def _validate_form_fields(self, form_fields: List[Dict[str, Any]], content: str) -> List[str]:
        """
        Validate form fields and return warnings.

        Args:
            form_fields: Extracted form fields
            content: XML content

        Returns:
            List of warning messages
        """
        warnings = []

        # Check for widgets without ui:field
        widget_pattern = r'<g:(\w+)'
        widgets = re.findall(widget_pattern, content)

        form_widgets_in_content = [w for w in widgets if w in self.FORM_WIDGET_TYPES]
        fields_found = len(form_fields)

        if len(form_widgets_in_content) > fields_found:
            diff = len(form_widgets_in_content) - fields_found
            warnings.append(
                f"Found {diff} form widget(s) without ui:field attribute. "
                f"These widgets cannot be accessed from Java code."
            )

        # Check for fields without labels
        unlabeled = [f for f in form_fields if not f.get('label')]
        if unlabeled and len(unlabeled) > 0:
            unlabeled_names = [f['field_name'] for f in unlabeled[:3]]
            if len(unlabeled) > 3:
                unlabeled_names.append(f"and {len(unlabeled) - 3} more")
            warnings.append(
                f"Found {len(unlabeled)} field(s) without associated labels: "
                f"{', '.join(unlabeled_names)}"
            )

        return warnings

    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """
        Create error result dictionary.

        Args:
            error_message: Error message

        Returns:
            Minimal valid result with error
        """
        return {
            'template_name': '',
            'template_path': '',
            'form_fields': [],
            'field_count': 0,
            'warnings': [],
            'error': error_message
        }
