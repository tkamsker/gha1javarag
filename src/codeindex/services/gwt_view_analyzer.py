"""
GWT View Analyzer

Analyzes GWT View implementations to extract:
- Component type (Composite, PopupPanel, Panel, Widget)
- UiBinder template references
- @UiField bindings
- Implemented presenter interfaces

Implements FR-005 from the specification.
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from codeindex.parsers.hybrid_java_parser import HybridJavaParser
from codeindex.utils.gwt_patterns import GwtRole


logger = logging.getLogger(__name__)


class GwtViewAnalyzer:
    """
    Analyzer for GWT View implementations.

    Extracts UI structure, UiBinder templates, and presenter interface implementations.
    """

    def __init__(self):
        """Initialize GWT View analyzer."""
        self.logger = logging.getLogger(__name__)
        self.parser = HybridJavaParser()

    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this analyzer can handle the file.

        Args:
            file_path: Path to Java file

        Returns:
            True if file is a GWT View
        """
        # Check file name pattern
        file_name = file_path.name
        if not file_name.endswith('View.java'):
            return False

        # Quick content check for view indicators
        try:
            content = file_path.read_text(encoding='utf-8')
            return any([
                'extends Composite' in content,
                'extends PopupPanel' in content,
                'extends DialogBox' in content,
                'extends Panel' in content,
                'extends Widget' in content,
                '@UiField' in content,
                'UiBinder' in content,
                'implements Display' in content
            ])
        except Exception:
            return False

    def get_gwt_role(self) -> GwtRole:
        """
        Return the GWT role this analyzer produces.

        Returns:
            GwtRole.VIEW
        """
        return GwtRole.VIEW

    def analyze(
        self,
        file_path: Path,
        content: str,
        semantic_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze GWT View and extract metadata.

        Args:
            file_path: Path to view file
            content: Java source code
            semantic_data: Optional LLM-extracted semantic data

        Returns:
            Dictionary with GWT view metadata
        """
        self.logger.debug(f"Analyzing GWT View: {file_path.name}")

        try:
            # Extract class information
            class_info = self.parser.extract_class_info(content)

            # Detect component type
            component_type = self.detect_component_type(content, class_info)

            # Find UiBinder template
            uibinder_template = self.find_uibinder_template(file_path, content)

            # Extract UI field bindings
            ui_fields = self.extract_ui_field_bindings(content)

            # Extract navigation widgets (T064)
            navigation_widgets = self.extract_navigation_widgets(content)

            # Detect implemented interface (Display, etc.)
            implemented_interface = self._detect_implemented_interface(content, class_info)

            # Find presenter reference
            presenter_interface = self._find_presenter_reference(content)

            # Build metadata
            metadata = {
                'gwt_role': GwtRole.VIEW.value,
                'view_name': class_info.get('class_name', file_path.stem),
                'package': class_info.get('package', ''),
                'component_type': component_type,
                'uibinder_template': uibinder_template,
                'ui_fields': ui_fields,
                'navigation_widgets': navigation_widgets,
                'implements_interface': implemented_interface,
                'presenter_interface': presenter_interface
            }

            self.logger.info(
                f"Extracted view metadata from {file_path.name}: "
                f"type={component_type}, "
                f"uibinder={uibinder_template is not None}, "
                f"fields={len(ui_fields)}, "
                f"navigation_widgets={len(navigation_widgets)}"
            )

            return metadata

        except Exception as e:
            self.logger.error(f"Error analyzing GWT View {file_path}: {e}", exc_info=True)
            return {
                'gwt_role': GwtRole.VIEW.value,
                'view_name': file_path.stem,
                'component_type': 'Unknown',
                'uibinder_template': None,
                'ui_fields': [],
                'navigation_widgets': [],
                'implements_interface': None,
                'presenter_interface': None,
                'error': str(e)
            }

    def detect_component_type(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> str:
        """
        Detect GWT component type (Composite, PopupPanel, Panel, Widget).

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            Component type string
        """
        extends = class_info.get('extends') or ''

        # Check base class
        if extends and 'Composite' in extends:
            return 'Composite'
        elif extends and ('PopupPanel' in extends or 'DialogBox' in extends):
            return 'PopupPanel'
        elif extends and 'Panel' in extends:
            # Further classify panel types
            if extends and 'VerticalPanel' in extends:
                return 'VerticalPanel'
            elif extends and 'HorizontalPanel' in extends:
                return 'HorizontalPanel'
            elif extends and 'FlowPanel' in extends:
                return 'FlowPanel'
            else:
                return 'Panel'
        elif extends and 'Widget' in extends:
            return 'Widget'

        # Check if it's a portlet by name
        class_name = class_info.get('class_name') or ''
        if class_name and 'Portlet' in class_name:
            return 'Portlet'

        return 'Unknown'

    def find_uibinder_template(
        self,
        file_path: Path,
        content: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find UiBinder template reference with @UiTemplate detection.

        Args:
            file_path: Path to view file
            content: Java source code

        Returns:
            UiBinder template info or None
        """
        # Check if UiBinder is used
        if 'UiBinder' not in content:
            return None

        template_info = {}

        # Look for @UiTemplate annotation
        template_annotation_pattern = r'@UiTemplate\s*\(\s*"([^"]+)"\s*\)'
        template_match = re.search(template_annotation_pattern, content)

        if template_match:
            template_info['template_file'] = template_match.group(1)
            template_info['explicit'] = True
        else:
            # Infer default template name: ViewName.java → ViewName.ui.xml
            view_name = file_path.stem
            template_info['template_file'] = f"{view_name}.ui.xml"
            template_info['explicit'] = False

        # Look for UiBinder interface definition
        uibinder_pattern = r'interface\s+(\w+)\s+extends\s+UiBinder<'
        uibinder_match = re.search(uibinder_pattern, content)
        if uibinder_match:
            template_info['uibinder_interface'] = uibinder_match.group(1)

        self.logger.debug(f"Found UiBinder template: {template_info.get('template_file')}")
        return template_info

    def extract_ui_field_bindings(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract @UiField annotations and bindings.

        Args:
            content: Java source code

        Returns:
            List of UI field dictionaries
        """
        ui_fields = []

        # Pattern: @UiField Type fieldName;
        ui_field_pattern = r'@UiField\s+(\w+(?:<[^>]+>)?)\s+(\w+)\s*;'

        for match in re.finditer(ui_field_pattern, content):
            field_type = match.group(1)
            field_name = match.group(2)

            ui_fields.append({
                'field_name': field_name,
                'field_type': field_type
            })

        self.logger.debug(f"Extracted {len(ui_fields)} @UiField bindings")
        return ui_fields

    def extract_navigation_widgets(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract navigation-related widgets from view.

        Implements T064 - Navigation widget extraction.

        Finds:
        - Buttons with navigation-related names (save, cancel, submit, etc.)
        - Anchor/Link widgets
        - Menu items that trigger navigation
        - Widgets with "get" methods suggesting click handlers

        Args:
            content: Java source code

        Returns:
            List of navigation widget dictionaries
        """
        widgets = []

        # Pattern 1: Navigation-related button fields
        # @UiField Button saveButton, @UiField Button cancelButton, etc.
        nav_button_pattern = r'@UiField\s+Button\s+(\w*(?:save|cancel|submit|ok|close|back|next|delete|add|edit|create|update|view|details|go)(?:Btn|Button)?)\s*;'
        for match in re.finditer(nav_button_pattern, content, re.IGNORECASE):
            widget_name = match.group(1)
            widgets.append({
                'widget_name': widget_name,
                'widget_type': 'Button',
                'navigation_hint': 'action_button',
                'getter_method': f"get{widget_name[0].upper()}{widget_name[1:]}"
            })

        # Pattern 2: Anchor/Link widgets
        anchor_pattern = r'@UiField\s+Anchor\s+(\w+)\s*;'
        for match in re.finditer(anchor_pattern, content):
            widget_name = match.group(1)
            widgets.append({
                'widget_name': widget_name,
                'widget_type': 'Anchor',
                'navigation_hint': 'link',
                'getter_method': f"get{widget_name[0].upper()}{widget_name[1:]}"
            })

        # Pattern 3: Hyperlink widgets
        hyperlink_pattern = r'@UiField\s+Hyperlink\s+(\w+)\s*;'
        for match in re.finditer(hyperlink_pattern, content):
            widget_name = match.group(1)
            widgets.append({
                'widget_name': widget_name,
                'widget_type': 'Hyperlink',
                'navigation_hint': 'link',
                'getter_method': f"get{widget_name[0].upper()}{widget_name[1:]}"
            })

        # Pattern 4: Menu items (MenuItem, MenuBar)
        menuitem_pattern = r'@UiField\s+MenuItem\s+(\w+)\s*;'
        for match in re.finditer(menuitem_pattern, content):
            widget_name = match.group(1)
            widgets.append({
                'widget_name': widget_name,
                'widget_type': 'MenuItem',
                'navigation_hint': 'menu',
                'getter_method': f"get{widget_name[0].upper()}{widget_name[1:]}"
            })

        # Pattern 5: Getter methods for widgets (indicates potential click handler)
        # public Button getSaveButton() or getSaveButton() in Display interface
        getter_pattern = r'(?:public\s+)?(?:Button|Anchor|Hyperlink|MenuItem|HasClickHandlers)\s+get(\w+(?:Button|Btn|Link)?)\s*\(\s*\)'
        for match in re.finditer(getter_pattern, content):
            widget_name = match.group(1)

            # Skip if already found via @UiField
            if any(w['widget_name'].lower() == widget_name.lower() for w in widgets):
                continue

            widgets.append({
                'widget_name': widget_name,
                'widget_type': 'Unknown',
                'navigation_hint': 'getter_method',
                'getter_method': f"get{widget_name}"
            })

        self.logger.debug(f"Extracted {len(widgets)} navigation widgets")
        return widgets

    def _detect_implemented_interface(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> Optional[str]:
        """
        Detect implemented presenter interface.

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            Interface name or None
        """
        implements = class_info.get('implements', [])

        # Filter out standard GWT interfaces
        gwt_interfaces = {'HasWidgets', 'IsWidget', 'EventHandler'}

        for interface in implements:
            # Skip standard GWT interfaces
            if interface in gwt_interfaces:
                continue

            # Return first non-standard interface (likely Display or view contract)
            return interface

        return None

    def _find_presenter_reference(self, content: str) -> Optional[str]:
        """
        Find reference to presenter class.

        Looks for imports or qualified names like "FlashAdministrationPresenter.Display"

        Args:
            content: Java source code

        Returns:
            Presenter class name or None
        """
        # Look for qualified interface reference: SomePresenter.Display
        qualified_pattern = r'(\w+Presenter)\.Display'
        match = re.search(qualified_pattern, content)

        if match:
            return match.group(1)

        # Look for import of presenter
        import_pattern = r'import\s+[\w.]+\.(\w+Presenter);'
        match = re.search(import_pattern, content)

        if match:
            return match.group(1)

        return None
