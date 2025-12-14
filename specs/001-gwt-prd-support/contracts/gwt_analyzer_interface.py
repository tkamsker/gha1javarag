"""
GWT Analyzer Interface Contracts

Defines abstract base classes and protocols for GWT-specific analyzers.
All GWT analyzers must implement these interfaces to ensure consistency
with the existing analyzer pattern (db_analyzer, service_analyzer, frontend_analyzer).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum


class GwtRole(str, Enum):
    """GWT-specific artifact roles."""
    RPC_SERVLET = "rpc_servlet"
    PRESENTER = "presenter"
    VIEW = "view"
    UI_BINDER = "ui_binder"
    SHARED_DTO = "shared_dto"


class MvpBindingType(str, Enum):
    """MVP presenter-view binding detection strategy."""
    DISPLAY_INTERFACE = "display_interface"      # 90% confidence
    SEPARATE_INTERFACE = "separate_interface"    # 85% confidence
    NAMING_CONVENTION = "naming_convention"      # 70% confidence


@dataclass
class RpcMethod:
    """Represents a GWT RPC method signature."""
    name: str
    return_type: str
    parameters: List[Dict[str, Any]]
    exceptions: List[str]
    description: str
    visibility: str = "public"


@dataclass
class MvpBinding:
    """Represents presenter-view binding metadata."""
    view_class: Optional[str]
    binding_type: MvpBindingType
    confidence: float  # 0.0 to 1.0


@dataclass
class FormField:
    """Represents a form field extracted from UiBinder."""
    ui_field_name: str
    widget_type: str
    html_name: Optional[str]
    label: Optional[str]
    required: Optional[bool]
    field_type: str  # text, textarea, checkbox, select, date, file


@dataclass
class DtoField:
    """Represents a field in a Data Transfer Object."""
    name: str
    type: str
    visibility: str
    has_getter: bool
    has_setter: bool
    validation_annotations: List[str]


class GwtAnalyzer(ABC):
    """
    Abstract base class for all GWT analyzers.

    Follows the same pattern as existing analyzers:
    - db_analyzer.py
    - service_analyzer.py
    - frontend_analyzer.py
    """

    @abstractmethod
    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this analyzer can handle the given file.

        Args:
            file_path: Path to the source file

        Returns:
            True if this analyzer can process the file
        """
        pass

    @abstractmethod
    def analyze(self, file_path: Path, content: str, semantic_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a GWT file and extract structured metadata.

        Args:
            file_path: Path to the source file
            content: File content as string
            semantic_data: Optional LLM-extracted semantic information

        Returns:
            Dictionary matching the semantic_data schema from data-model.md
        """
        pass

    @abstractmethod
    def get_gwt_role(self) -> GwtRole:
        """
        Return the GWT role this analyzer produces.

        Returns:
            GwtRole enum value
        """
        pass


class GwtRpcAnalyzer(GwtAnalyzer):
    """
    Analyzer for GWT RPC servlet implementations.

    Implements FR-002, FR-003:
    - Detect RPC servlet files (*Servlet.java, *ServletImpl.java)
    - Extract RPC method signatures
    - Identify referenced DTOs
    """

    @abstractmethod
    def extract_rpc_methods(self, file_path: Path, content: str) -> List[RpcMethod]:
        """
        Extract all public RPC methods from servlet implementation.

        Uses hybrid approach:
        1. Try javalang AST parsing (preferred)
        2. Fall back to regex parsing if javalang fails

        Args:
            file_path: Path to servlet file
            content: Java source code

        Returns:
            List of RpcMethod objects
        """
        pass

    @abstractmethod
    def identify_service_interface(self, file_path: Path, content: str) -> Optional[str]:
        """
        Identify the service interface this servlet implements.

        Args:
            file_path: Path to servlet file
            content: Java source code

        Returns:
            Fully qualified interface name or None
        """
        pass

    @abstractmethod
    def extract_referenced_dtos(self, rpc_methods: List[RpcMethod]) -> List[str]:
        """
        Extract all DTO class names used in RPC methods.

        Args:
            rpc_methods: List of extracted RPC methods

        Returns:
            List of DTO class names
        """
        pass


class GwtPresenterAnalyzer(GwtAnalyzer):
    """
    Analyzer for MVP presenter components.

    Implements FR-006, FR-009:
    - Detect presenter files (*Presenter.java)
    - Extract event handlers and business logic
    - Identify presenter-view bindings
    """

    @abstractmethod
    def detect_view_binding(self, file_path: Path, content: str) -> MvpBinding:
        """
        Detect presenter-view binding using three strategies.

        Priority order:
        1. Inner Display interface (90% confidence)
        2. Separate view interface (85% confidence)
        3. Naming convention (70% confidence)

        Args:
            file_path: Path to presenter file
            content: Java source code

        Returns:
            MvpBinding with detected view and confidence score
        """
        pass

    @abstractmethod
    def extract_event_handlers(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract event handler methods from presenter.

        Args:
            file_path: Path to presenter file
            content: Java source code

        Returns:
            List of event handler metadata (name, type, description, target)
        """
        pass

    @abstractmethod
    def extract_navigation_logic(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract navigation between presenters.

        Args:
            file_path: Path to presenter file
            content: Java source code

        Returns:
            List of navigation metadata (method, target presenter, description)
        """
        pass


class GwtViewAnalyzer(GwtAnalyzer):
    """
    Analyzer for MVP view components.

    Implements FR-007:
    - Detect view files (*View.java)
    - Extract UI component initialization
    - Link to UiBinder templates
    """

    @abstractmethod
    def find_uibinder_template(self, file_path: Path, content: str) -> Optional[Path]:
        """
        Find associated UiBinder XML template for this view.

        Strategies:
        1. Check for @UiTemplate annotation
        2. Look for .ui.xml file with same base name
        3. Search in same directory

        Args:
            file_path: Path to view file
            content: Java source code

        Returns:
            Path to .ui.xml file or None
        """
        pass

    @abstractmethod
    def extract_ui_field_bindings(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract @UiField annotated widget fields.

        Args:
            file_path: Path to view file
            content: Java source code

        Returns:
            List of widget metadata (field name, type, @UiField present)
        """
        pass

    @abstractmethod
    def detect_component_type(self, file_path: Path, content: str) -> str:
        """
        Classify view component type.

        Args:
            file_path: Path to view file
            content: Java source code

        Returns:
            Component type: "popup" | "portlet" | "panel" | "composite"
        """
        pass


class GwtUiBinderParser(GwtAnalyzer):
    """
    Parser for UiBinder XML templates.

    Implements FR-004, FR-005:
    - Parse UiBinder XML files (*.ui.xml)
    - Extract form fields and widgets
    - Handle HTML entities (&nbsp;, &lt;, &gt;)
    """

    @abstractmethod
    def parse_form_fields(self, file_path: Path) -> List[FormField]:
        """
        Extract all form fields from UiBinder template.

        Widget type mapping (see research.md):
        - <g:TextBox> → text
        - <g:TextArea> → textarea
        - <g:PasswordTextBox> → password
        - <g:CheckBox> → checkbox
        - <g:ListBox> → select
        - <g:DatePicker> → date
        - <g:FileUpload> → file

        Args:
            file_path: Path to .ui.xml file

        Returns:
            List of FormField objects
        """
        pass

    @abstractmethod
    def extract_select_options(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Extract options for ListBox widgets.

        Args:
            file_path: Path to .ui.xml file

        Returns:
            Dict mapping ui:field name to list of option values
        """
        pass

    @abstractmethod
    def find_associated_labels(self, file_path: Path) -> Dict[str, str]:
        """
        Heuristically match labels to form fields.

        Strategy (see research.md):
        - Check previous sibling for <g:Label>
        - Extract label text

        Args:
            file_path: Path to .ui.xml file

        Returns:
            Dict mapping ui:field name to label text
        """
        pass


class GwtModelAnalyzer(GwtAnalyzer):
    """
    Analyzer for shared Data Transfer Objects.

    Implements FR-008:
    - Detect DTOs in shared/ packages
    - Extract field definitions and types
    - Extract validation rules
    """

    @abstractmethod
    def extract_dto_fields(self, file_path: Path, content: str) -> List[DtoField]:
        """
        Extract all fields from DTO class.

        Args:
            file_path: Path to DTO file
            content: Java source code

        Returns:
            List of DtoField objects
        """
        pass

    @abstractmethod
    def extract_validation_rules(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract validation annotations from DTO.

        Common annotations:
        - @NotNull
        - @Size(min=X, max=Y)
        - @Pattern(regexp="...")
        - @Email

        Args:
            file_path: Path to DTO file
            content: Java source code

        Returns:
            List of validation rule metadata (field, rule, message)
        """
        pass

    @abstractmethod
    def check_gwt_serializable(self, file_path: Path, content: str) -> bool:
        """
        Verify DTO implements Serializable for GWT RPC.

        Args:
            file_path: Path to DTO file
            content: Java source code

        Returns:
            True if DTO is GWT-serializable
        """
        pass


# ============================================================================
# Integration Interfaces
# ============================================================================

class GwtAnalyzerRegistry:
    """
    Registry for all GWT analyzers.

    Integrates with existing extraction.py routing logic.
    """

    @abstractmethod
    def register(self, analyzer: GwtAnalyzer) -> None:
        """Register a GWT analyzer."""
        pass

    @abstractmethod
    def get_analyzer(self, file_path: Path) -> Optional[GwtAnalyzer]:
        """
        Get appropriate analyzer for file.

        Args:
            file_path: Path to file

        Returns:
            GwtAnalyzer instance or None
        """
        pass


class GwtPatternDetector:
    """
    Utility for detecting GWT patterns in codebases.

    Implements FR-001: GWT application detection.
    """

    @abstractmethod
    def is_gwt_application(self, source_dir: Path) -> bool:
        """
        Detect if codebase is a GWT application.

        Indicators:
        - Presence of *.gwt.xml module descriptors
        - GWT imports in Java files
        - client/server/shared directory structure

        Args:
            source_dir: Root of source directory

        Returns:
            True if GWT application detected
        """
        pass

    @abstractmethod
    def get_gwt_version(self, source_dir: Path) -> Optional[str]:
        """
        Detect GWT version from module descriptor or POM.

        Args:
            source_dir: Root of source directory

        Returns:
            GWT version string or None
        """
        pass
