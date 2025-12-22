"""
GWT binding models for Presenter-View-UiBinder relationships.

This module defines dataclasses for representing MVP pattern bindings and
UiBinder widget hierarchies discovered during GWT analysis.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class PresenterViewBinding:
    """
    Maps Presenter → Display interface → View → UiBinder template.

    Represents the complete MVP binding chain discovered through pattern analysis
    (Display interface, separate interface, or naming convention).
    """

    presenter_class: str
    """Fully qualified Presenter class name"""

    display_interface: Optional[str] = None
    """Display interface name (inner interface or separate)"""

    view_class: Optional[str] = None
    """Concrete View implementation class name"""

    ui_binder_template: Optional[str] = None
    """Path to UiBinder XML template file"""

    confidence_score: float = 0.0
    """Confidence in this binding (0.0-1.0)"""

    binding_pattern: str = "unknown"
    """Pattern used to detect binding: 'inner_display', 'separate_interface', 'naming_convention'"""

    presenter_file: Optional[str] = None
    """Path to Presenter source file"""

    view_file: Optional[str] = None
    """Path to View source file"""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional binding metadata (event handlers, RPC calls, etc.)"""

    def __post_init__(self):
        """Validate presenter-view binding values"""
        if not self.presenter_class:
            raise ValueError("presenter_class cannot be empty")

        if self.confidence_score < 0.0 or self.confidence_score > 1.0:
            raise ValueError(f"confidence_score must be 0.0-1.0, got {self.confidence_score}")

        # Validate binding pattern
        valid_patterns = ['inner_display', 'separate_interface', 'naming_convention', 'unknown']
        if self.binding_pattern not in valid_patterns:
            raise ValueError(f"binding_pattern must be one of {valid_patterns}, got {self.binding_pattern}")

    def is_complete(self) -> bool:
        """
        Check if binding has all components (Presenter, View, UiBinder).

        Returns:
            True if all components are present
        """
        return (
            self.presenter_class is not None and
            self.view_class is not None and
            self.ui_binder_template is not None
        )

    def is_partial(self) -> bool:
        """
        Check if binding is partial (missing some components).

        Returns:
            True if Presenter exists but View or UiBinder is missing
        """
        return self.presenter_class is not None and not self.is_complete()

    def has_display_interface(self) -> bool:
        """
        Check if binding has Display interface defined.

        Returns:
            True if display_interface is set
        """
        return self.display_interface is not None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'presenter_class': self.presenter_class,
            'display_interface': self.display_interface,
            'view_class': self.view_class,
            'ui_binder_template': self.ui_binder_template,
            'confidence_score': self.confidence_score,
            'binding_pattern': self.binding_pattern,
            'presenter_file': self.presenter_file,
            'view_file': self.view_file,
            'metadata': self.metadata
        }


@dataclass
class UiBinderHierarchy:
    """
    Widget hierarchy extracted from UiBinder XML template.

    Represents the complete widget tree with parent-child relationships,
    UI fields, event handlers, and form structure.
    """

    template_path: str
    """Path to UiBinder XML template file"""

    root_widget_type: str
    """Type of root widget (e.g., 'VerticalPanel', 'Composite')"""

    widgets: List[Dict[str, Any]] = field(default_factory=list)
    """List of widget dictionaries with hierarchy information"""

    form_fields: List[Dict[str, str]] = field(default_factory=list)
    """List of form field dictionaries (name, type, label)"""

    buttons: List[Dict[str, str]] = field(default_factory=list)
    """List of button dictionaries (name, text, handler)"""

    event_handlers: List[str] = field(default_factory=list)
    """List of event handler method names from @UiHandler"""

    ui_fields: Dict[str, str] = field(default_factory=dict)
    """Map of @UiField name to widget type"""

    view_class: Optional[str] = None
    """Associated View class name if known"""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional hierarchy metadata"""

    def __post_init__(self):
        """Validate UiBinder hierarchy values"""
        if not self.template_path:
            raise ValueError("template_path cannot be empty")

        if not self.root_widget_type:
            raise ValueError("root_widget_type cannot be empty")

    def add_widget(self, widget_type: str, widget_name: Optional[str] = None,
                   parent: Optional[str] = None, attributes: Optional[Dict[str, str]] = None):
        """
        Add a widget to the hierarchy.

        Args:
            widget_type: Type of widget (e.g., 'Button', 'TextBox')
            widget_name: UI field name if @UiField annotated
            parent: Parent widget name/type
            attributes: Additional widget attributes
        """
        widget = {
            'type': widget_type,
            'name': widget_name,
            'parent': parent,
            'attributes': attributes or {}
        }
        self.widgets.append(widget)

        # Add to ui_fields if named
        if widget_name:
            self.ui_fields[widget_name] = widget_type

    def add_form_field(self, field_name: str, field_type: str, label: Optional[str] = None):
        """Add a form field to the hierarchy"""
        field = {
            'name': field_name,
            'type': field_type,
            'label': label
        }
        if field not in self.form_fields:
            self.form_fields.append(field)

    def add_button(self, button_name: str, button_text: str, handler: Optional[str] = None):
        """Add a button to the hierarchy"""
        button = {
            'name': button_name,
            'text': button_text,
            'handler': handler
        }
        if button not in self.buttons:
            self.buttons.append(button)

    def add_event_handler(self, handler_name: str):
        """Add an event handler method name"""
        if handler_name and handler_name not in self.event_handlers:
            self.event_handlers.append(handler_name)

    def get_widget_count(self) -> int:
        """Get total number of widgets in hierarchy"""
        return len(self.widgets)

    def get_form_field_count(self) -> int:
        """Get number of form fields"""
        return len(self.form_fields)

    def get_button_count(self) -> int:
        """Get number of buttons"""
        return len(self.buttons)

    def has_form_fields(self) -> bool:
        """Check if template contains form fields"""
        return len(self.form_fields) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'template_path': self.template_path,
            'root_widget_type': self.root_widget_type,
            'widgets': self.widgets,
            'form_fields': self.form_fields,
            'buttons': self.buttons,
            'event_handlers': self.event_handlers,
            'ui_fields': self.ui_fields,
            'view_class': self.view_class,
            'metadata': self.metadata
        }
