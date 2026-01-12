"""
HTML Form Parser.

Extracts form structures from static HTML files using lxml.html.

Feature 008 T010: Parse HTML forms for frontend analysis.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from lxml import html, etree

logger = logging.getLogger(__name__)


class HtmlFormParser:
    """
    Parser for HTML forms in static HTML files.

    Supports:
    - Standard HTML forms (<form>, <input>, <button>)
    - Field label detection (adjacent text, <label> tags)
    - Multi-page forms (fieldset, form wizard)
    - Textarea, select, and button elements

    Uses lxml.html for robust HTML parsing.
    """

    def __init__(self):
        """Initialize HTML form parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse HTML file and extract forms.

        Args:
            file_path: Path to HTML file

        Returns:
            Dictionary with parsed forms

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"HTML file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse HTML content and extract forms.

        Args:
            content: HTML source code

        Returns:
            Dictionary with form information
        """
        try:
            doc = html.fromstring(content)
            forms = []

            for form_element in doc.xpath('//form'):
                forms.append(self._extract_form(form_element))

            return {
                'forms': forms,
                'form_count': len(forms),
            }

        except etree.ParserError as e:
            self.logger.error(f"HTML parsing error: {e}")
            return {
                'forms': [],
                'form_count': 0,
                'parse_error': str(e)
            }
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {e}", exc_info=True)
            return {
                'forms': [],
                'form_count': 0,
                'parse_error': str(e)
            }

    def _extract_form(self, form_element) -> Dict[str, Any]:
        """
        Extract structure from form element.

        Args:
            form_element: lxml form element

        Returns:
            Dictionary with form information
        """
        fields = []

        # Extract input fields
        for input_elem in form_element.xpath('.//input'):
            field = self._extract_input_field(input_elem)
            if field['name'] or field['id']:  # Only add if has name or id
                fields.append(field)

        # Extract textarea fields
        for textarea_elem in form_element.xpath('.//textarea'):
            field = self._extract_textarea_field(textarea_elem)
            if field['name'] or field['id']:
                fields.append(field)

        # Extract select fields
        for select_elem in form_element.xpath('.//select'):
            field = self._extract_select_field(select_elem)
            if field['name'] or field['id']:
                fields.append(field)

        # Extract buttons
        buttons = []
        for button_elem in form_element.xpath('.//button | .//input[@type="submit"] | .//input[@type="reset"]'):
            button = self._extract_button(button_elem)
            buttons.append(button)

        # Extract fieldsets (for multi-page forms)
        fieldsets = []
        for fieldset_elem in form_element.xpath('.//fieldset'):
            fieldsets.append(self._extract_fieldset(fieldset_elem))

        return {
            'id': form_element.get('id', ''),
            'name': form_element.get('name', ''),
            'action': form_element.get('action', ''),
            'method': (form_element.get('method') or 'GET').upper(),
            'enctype': form_element.get('enctype', ''),
            'fields': fields,
            'buttons': buttons,
            'fieldsets': fieldsets,
            'field_count': len(fields),
            'button_count': len(buttons),
            'fieldset_count': len(fieldsets),
        }

    def _extract_input_field(self, input_elem) -> Dict[str, Any]:
        """
        Extract input field information.

        Args:
            input_elem: lxml input element

        Returns:
            Dictionary with field information
        """
        input_type = input_elem.get('type', 'text')
        name = input_elem.get('name', '')
        field_id = input_elem.get('id', '')

        # Find label
        label = self._find_label_for_field(input_elem, field_id)

        return {
            'type': 'input',
            'input_type': input_type,
            'name': name,
            'id': field_id,
            'value': input_elem.get('value', ''),
            'placeholder': input_elem.get('placeholder', ''),
            'label': label,
            'required': input_elem.get('required') is not None,
            'pattern': input_elem.get('pattern', ''),
            'min': input_elem.get('min', ''),
            'max': input_elem.get('max', ''),
            'maxlength': input_elem.get('maxlength', ''),
            'disabled': input_elem.get('disabled') is not None,
            'readonly': input_elem.get('readonly') is not None,
        }

    def _extract_textarea_field(self, textarea_elem) -> Dict[str, Any]:
        """
        Extract textarea field information.

        Args:
            textarea_elem: lxml textarea element

        Returns:
            Dictionary with field information
        """
        name = textarea_elem.get('name', '')
        field_id = textarea_elem.get('id', '')

        # Find label
        label = self._find_label_for_field(textarea_elem, field_id)

        return {
            'type': 'textarea',
            'name': name,
            'id': field_id,
            'placeholder': textarea_elem.get('placeholder', ''),
            'label': label,
            'required': textarea_elem.get('required') is not None,
            'rows': textarea_elem.get('rows', ''),
            'cols': textarea_elem.get('cols', ''),
            'maxlength': textarea_elem.get('maxlength', ''),
            'disabled': textarea_elem.get('disabled') is not None,
            'readonly': textarea_elem.get('readonly') is not None,
            'default_value': textarea_elem.text_content().strip() if textarea_elem.text_content() else '',
        }

    def _extract_select_field(self, select_elem) -> Dict[str, Any]:
        """
        Extract select/dropdown field information.

        Args:
            select_elem: lxml select element

        Returns:
            Dictionary with field information
        """
        name = select_elem.get('name', '')
        field_id = select_elem.get('id', '')

        # Find label
        label = self._find_label_for_field(select_elem, field_id)

        # Extract options
        options = []
        for option_elem in select_elem.xpath('.//option'):
            option_value = option_elem.get('value', option_elem.text_content().strip())
            option_text = option_elem.text_content().strip()
            options.append({
                'value': option_value,
                'label': option_text,
                'selected': option_elem.get('selected') is not None,
            })

        return {
            'type': 'select',
            'name': name,
            'id': field_id,
            'label': label,
            'required': select_elem.get('required') is not None,
            'multiple': select_elem.get('multiple') is not None,
            'disabled': select_elem.get('disabled') is not None,
            'options': options,
            'option_count': len(options),
        }

    def _extract_button(self, button_elem) -> Dict[str, Any]:
        """
        Extract button information.

        Args:
            button_elem: lxml button or input element

        Returns:
            Dictionary with button information
        """
        button_type = 'button'
        text = ''

        if button_elem.tag == 'button':
            button_type = button_elem.get('type', 'button')
            text = button_elem.text_content().strip()
        elif button_elem.tag == 'input':
            button_type = button_elem.get('type', 'button')
            text = button_elem.get('value', '')

        return {
            'type': button_type,
            'name': button_elem.get('name', ''),
            'id': button_elem.get('id', ''),
            'text': text,
            'onclick': button_elem.get('onclick', ''),
            'disabled': button_elem.get('disabled') is not None,
        }

    def _extract_fieldset(self, fieldset_elem) -> Dict[str, Any]:
        """
        Extract fieldset information (for multi-page forms).

        Args:
            fieldset_elem: lxml fieldset element

        Returns:
            Dictionary with fieldset information
        """
        # Find legend (fieldset title)
        legend = ''
        legend_elem = fieldset_elem.find('.//legend')
        if legend_elem is not None:
            legend = legend_elem.text_content().strip()

        # Count fields within fieldset
        field_count = (
            len(fieldset_elem.xpath('.//input')) +
            len(fieldset_elem.xpath('.//textarea')) +
            len(fieldset_elem.xpath('.//select'))
        )

        return {
            'id': fieldset_elem.get('id', ''),
            'legend': legend,
            'field_count': field_count,
            'disabled': fieldset_elem.get('disabled') is not None,
        }

    def _find_label_for_field(self, field_elem, field_id: str) -> str:
        """
        Find label for form field using multiple strategies.

        Feature 008 T010: Label detection for better field documentation.

        Strategies:
        1. <label for="field_id"> (explicit association)
        2. <label> wrapping the field (implicit association)
        3. Adjacent text in parent container
        4. Placeholder attribute as fallback

        Args:
            field_elem: lxml field element
            field_id: Field ID attribute

        Returns:
            Label text or empty string
        """
        # Strategy 1: <label for="field_id">
        if field_id:
            root = field_elem.getroottree().getroot()
            label_elem = root.xpath(f'//label[@for="{field_id}"]')
            if label_elem:
                return label_elem[0].text_content().strip()

        # Strategy 2: <label> wrapping the field
        parent = field_elem.getparent()
        if parent is not None and parent.tag == 'label':
            # Get label text excluding field text
            label_text = parent.text_content().strip()
            field_text = field_elem.tail or ''
            # Remove field placeholder from label
            label_text = label_text.replace(field_text, '').strip()
            if label_text:
                return label_text

        # Strategy 3: Adjacent text in parent container
        if parent is not None:
            # Look for text before the field
            if parent.text:
                text = parent.text.strip()
                # Check if it looks like a label (ends with : or is short)
                if text and (text.endswith(':') or len(text) < 50):
                    return text.rstrip(':').strip()

            # Look for preceding sibling text
            prev = field_elem.getprevious()
            if prev is not None:
                if prev.tag in ['span', 'div', 'p', 'strong', 'b']:
                    text = prev.text_content().strip()
                    if text and len(text) < 50:
                        return text.rstrip(':').strip()

        # Strategy 4: No label found
        return ''


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_html_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse HTML file and extract forms (convenience function).

    Args:
        file_path: Path to HTML file

    Returns:
        Dictionary with parsed forms
    """
    parser = HtmlFormParser()
    return parser.parse_file(file_path)


def parse_html(content: str) -> Dict[str, Any]:
    """
    Parse HTML content and extract forms (convenience function).

    Args:
        content: HTML source code

    Returns:
        Dictionary with parsed forms
    """
    parser = HtmlFormParser()
    return parser.parse(content)
