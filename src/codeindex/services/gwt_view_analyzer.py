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
                'implements_interface': implemented_interface,
                'presenter_interface': presenter_interface
            }

            self.logger.info(
                f"Extracted view metadata from {file_path.name}: "
                f"type={component_type}, "
                f"uibinder={uibinder_template is not None}, "
                f"fields={len(ui_fields)}"
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
        extends = class_info.get('extends', '')

        # Check base class
        if 'Composite' in extends:
            return 'Composite'
        elif 'PopupPanel' in extends or 'DialogBox' in extends:
            return 'PopupPanel'
        elif 'Panel' in extends:
            # Further classify panel types
            if 'VerticalPanel' in extends:
                return 'VerticalPanel'
            elif 'HorizontalPanel' in extends:
                return 'HorizontalPanel'
            elif 'FlowPanel' in extends:
                return 'FlowPanel'
            else:
                return 'Panel'
        elif 'Widget' in extends:
            return 'Widget'

        # Check if it's a portlet by name
        if 'Portlet' in class_info.get('class_name', ''):
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
