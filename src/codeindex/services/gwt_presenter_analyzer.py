"""
GWT Presenter Analyzer

Analyzes GWT Presenter implementations to extract:
- View bindings with confidence scoring (Display interface, separate interface, naming convention)
- Event handlers (ClickHandler, ChangeHandler, etc.)
- Navigation logic (Place navigation, URL navigation)
- RPC service calls

Implements FR-005 from the specification.
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from codeindex.parsers.hybrid_java_parser import HybridJavaParser
from codeindex.utils.gwt_patterns import GwtRole


logger = logging.getLogger(__name__)


class GwtPresenterAnalyzer:
    """
    Analyzer for GWT Presenter implementations.

    Identifies MVP pattern relationships and extracts presenter metadata
    including view bindings, event handlers, and navigation logic.
    """

    def __init__(self):
        """Initialize GWT Presenter analyzer."""
        self.logger = logging.getLogger(__name__)
        self.parser = HybridJavaParser()

    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this analyzer can handle the file.

        Args:
            file_path: Path to Java file

        Returns:
            True if file is a GWT Presenter
        """
        # Check file name pattern
        file_name = file_path.name
        if not file_name.endswith('Presenter.java'):
            return False

        # Quick content check
        try:
            content = file_path.read_text(encoding='utf-8')
            # Look for common presenter patterns
            return any([
                'interface Display' in content,
                'View view' in content or 'IView' in content or 'Display view' in content,
                'ClickHandler' in content,
                'PlaceController' in content
            ])
        except Exception:
            return False

    def get_gwt_role(self) -> GwtRole:
        """
        Return the GWT role this analyzer produces.

        Returns:
            GwtRole.PRESENTER
        """
        return GwtRole.PRESENTER

    def analyze(
        self,
        file_path: Path,
        content: str,
        semantic_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze GWT Presenter and extract metadata.

        Args:
            file_path: Path to presenter file
            content: Java source code
            semantic_data: Optional LLM-extracted semantic data

        Returns:
            Dictionary with GWT presenter metadata
        """
        self.logger.debug(f"Analyzing GWT Presenter: {file_path.name}")

        try:
            # Extract class information
            class_info = self.parser.extract_class_info(content)

            # Detect view binding with confidence scoring
            view_binding = self.detect_view_binding(file_path, content, class_info)

            # Extract event handlers
            event_handlers = self.extract_event_handlers(content)

            # Extract navigation logic
            navigation_logic = self.extract_navigation_logic(content)

            # Extract RPC calls
            rpc_calls = self.extract_rpc_calls(content)

            # Build metadata
            metadata = {
                'gwt_role': GwtRole.PRESENTER.value,
                'presenter_name': class_info.get('class_name', file_path.stem),
                'package': class_info.get('package', ''),
                'view_binding': view_binding,
                'event_handlers': event_handlers,
                'navigation_logic': navigation_logic,
                'rpc_calls': rpc_calls
            }

            # Add validation warnings for low confidence bindings
            if view_binding and view_binding.get('confidence', 0) < 0.7:
                metadata['warnings'] = [f"Low confidence view binding: {view_binding['confidence']:.0%}"]

            self.logger.info(
                f"Extracted presenter metadata from {file_path.name}: "
                f"view_binding={view_binding is not None}, "
                f"handlers={len(event_handlers)}, "
                f"navigation={len(navigation_logic)}"
            )

            return metadata

        except Exception as e:
            self.logger.error(f"Error analyzing GWT Presenter {file_path}: {e}", exc_info=True)
            return {
                'gwt_role': GwtRole.PRESENTER.value,
                'presenter_name': file_path.stem,
                'view_binding': None,
                'event_handlers': [],
                'navigation_logic': [],
                'rpc_calls': [],
                'error': str(e)
            }

    def detect_view_binding(
        self,
        file_path: Path,
        content: str,
        class_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect view binding using 4 strategies with confidence scoring.

        Strategy 1: @Presenter annotation (95% confidence)
        Strategy 2: Nested Display/View interface (90% confidence)
        Strategy 3: Separate interface (85% confidence)
        Strategy 4: Naming convention (70% confidence)

        Args:
            file_path: Path to presenter file
            content: Java source code
            class_info: Parsed class information

        Returns:
            View binding dictionary with confidence score, or None
        """
        # Strategy 1: @Presenter annotation with view parameter (95% confidence)
        annotation_binding = self._detect_presenter_annotation(content, class_info)
        if annotation_binding:
            return annotation_binding

        # Strategy 2: Nested Display or View interface (90% confidence)
        display_binding = self._detect_nested_display(content, class_info)
        if display_binding:
            return display_binding

        # Strategy 3: Separate interface (85% confidence)
        separate_binding = self._detect_separate_interface(content, class_info)
        if separate_binding:
            return separate_binding

        # Strategy 4: Naming convention (70% confidence)
        naming_binding = self._detect_naming_convention(file_path, content, class_info)
        if naming_binding:
            return naming_binding

        self.logger.warning(f"Could not detect view binding for {file_path.name}")
        return None

    def _detect_nested_display(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect nested Display interface pattern (90% confidence).

        Pattern: public interface Display { ... }

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            View binding with 90% confidence, or None
        """
        # Look for nested Display interface
        display_pattern = r'public\s+interface\s+Display\s*\{'
        if not re.search(display_pattern, content):
            return None

        # Find Display field and constructor param
        view_field, constructor_param = self._find_view_field_and_param(content, 'Display')

        if view_field:
            self.logger.debug("Detected nested Display interface pattern (90% confidence)")
            return {
                'strategy': 'nested_display_interface',
                'confidence': 0.90,
                'view_interface': 'Display',
                'view_field': view_field,
                'constructor_param': constructor_param
            }

        return None

    def _detect_separate_interface(
        self,
        content: str,
        class_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect separate view interface pattern (85% confidence).

        Pattern: Constructor takes interface starting with 'I' or ending with 'View'

        Args:
            content: Java source code
            class_info: Parsed class information

        Returns:
            View binding with 85% confidence, or None
        """
        # Look for imports of view interfaces
        import_pattern = r'import\s+[\w.]+\.(I\w+(?:View)?);'
        imports = re.findall(import_pattern, content)

        for view_interface in imports:
            view_field, constructor_param = self._find_view_field_and_param(content, view_interface)

            if view_field:
                self.logger.debug(f"Detected separate interface pattern: {view_interface} (85% confidence)")
                return {
                    'strategy': 'separate_interface',
                    'confidence': 0.85,
                    'view_interface': view_interface,
                    'view_field': view_field,
                    'constructor_param': constructor_param
                }

        return None

    def _detect_naming_convention(
        self,
        file_path: Path,
        content: str,
        class_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect view by naming convention (70% confidence).

        Pattern: FlashInfoPresenter → FlashInfoView

        Args:
            file_path: Path to presenter file
            content: Java source code
            class_info: Parsed class information

        Returns:
            View binding with 70% confidence, or None
        """
        presenter_name = class_info.get('class_name') or ''
        if not presenter_name or not presenter_name.endswith('Presenter'):
            return None

        # Derive view name
        view_base = presenter_name[:-9]  # Remove 'Presenter'
        view_name = f"{view_base}View"

        # Check if this view class is referenced
        view_field, constructor_param = self._find_view_field_and_param(content, view_name)

        if view_field:
            self.logger.debug(f"Detected naming convention: {view_name} (70% confidence)")
            return {
                'strategy': 'naming_convention',
                'confidence': 0.70,
                'view_interface': view_name,
                'view_field': view_field,
                'constructor_param': constructor_param
            }

        return None

    def _find_view_field_and_param(
        self,
        content: str,
        view_type: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Find view field and constructor parameter.

        Args:
            content: Java source code
            view_type: View type/interface name

        Returns:
            Tuple of (field_name, constructor_param_name)
        """
        # Find field: private final Display view;
        field_pattern = rf'private\s+(?:final\s+)?{re.escape(view_type)}\s+(\w+)\s*;'
        field_match = re.search(field_pattern, content)
        field_name = field_match.group(1) if field_match else None

        # Find constructor param: public Presenter(Display view)
        param_pattern = rf'{re.escape(view_type)}\s+(\w+)\s*[,)]'
        param_match = re.search(param_pattern, content)
        param_name = param_match.group(1) if param_match else None

        return field_name, param_name

    def extract_event_handlers(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract event handlers from presenter.

        Finds ClickHandler, ChangeHandler, etc. registrations.

        Args:
            content: Java source code

        Returns:
            List of event handler dictionaries
        """
        handlers = []

        # Pattern: view.getXxxButton().addClickHandler(new ClickHandler() { ... onClick(...) { methodCall(); }})
        handler_pattern = r'view\.get(\w+)\(\)\.add(\w+Handler)\s*\(new\s+(\w+Handler)\s*\(\)\s*\{[^}]*?onClick[^}]*?\{[^}]*?(\w+)\('

        for match in re.finditer(handler_pattern, content, re.DOTALL):
            widget_getter = match.group(1)
            add_method = match.group(2)
            handler_type = match.group(3)
            action_method = match.group(4)

            handlers.append({
                'widget_getter': widget_getter,
                'handler_type': handler_type,
                'action_method': action_method
            })

        self.logger.debug(f"Extracted {len(handlers)} event handlers")
        return handlers

    def extract_navigation_logic(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract navigation logic from presenter.

        Finds PlaceController.goTo() calls and navigateTo() calls.

        Args:
            content: Java source code

        Returns:
            List of navigation dictionaries
        """
        navigation = []

        # Pattern 1: PlaceController.goTo(new SomePlace(...))
        place_pattern = r'\.goTo\s*\(\s*new\s+([\w.]+Place)'
        for match in re.finditer(place_pattern, content):
            place_name = match.group(1)
            # Extract just the class name if fully qualified
            if '.' in place_name:
                place_name = place_name.split('.')[-1]

            # Find source method
            source_method = self._find_containing_method(content, match.start())

            navigation.append({
                'navigation_type': 'place',
                'target': place_name,
                'source_method': source_method
            })

        # Pattern 2: view.navigateTo("/some/url") or navigateTo() with string concatenation
        # Matches: navigateTo("/url"), navigateTo("/url" + var), navigateTo("/url/" + var)
        url_pattern = r'navigateTo\s*\(\s*"([^"]+)"'
        for match in re.finditer(url_pattern, content):
            url = match.group(1)

            source_method = self._find_containing_method(content, match.start())

            navigation.append({
                'navigation_type': 'url',
                'target': url,
                'source_method': source_method
            })

        self.logger.debug(f"Extracted {len(navigation)} navigation calls")
        return navigation

    def extract_rpc_calls(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract RPC service calls from presenter.

        Args:
            content: Java source code

        Returns:
            List of RPC call dictionaries
        """
        rpc_calls = []

        # Pattern: rpcService.methodName(params, new AsyncCallback<Type>() { ... })
        rpc_pattern = r'(\w+Service)\.(\w+)\s*\([^)]*new\s+AsyncCallback<([^>]+)>'

        for match in re.finditer(rpc_pattern, content):
            service_name = match.group(1)
            method_name = match.group(2)
            return_type = match.group(3)

            rpc_calls.append({
                'service': service_name,
                'method': method_name,
                'return_type': return_type
            })

        self.logger.debug(f"Extracted {len(rpc_calls)} RPC calls")
        return rpc_calls

    def _find_containing_method(self, content: str, position: int) -> str:
        """
        Find the method containing a given position in source code.

        Args:
            content: Java source code
            position: Position in content

        Returns:
            Method name or 'unknown'
        """
        # Look backwards for method signature
        before = content[:position]

        # Find last method declaration before position
        method_pattern = r'(?:private|public|protected)\s+\w+\s+(\w+)\s*\('
        matches = list(re.finditer(method_pattern, before))

        if matches:
            return matches[-1].group(1)

        return 'unknown'
