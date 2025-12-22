"""
GWT module model for parsed *.gwt.xml descriptors.

This module defines dataclasses for representing GWT module configurations
including entry points, inherited modules, and source paths.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class GWTModule:
    """
    Parsed GWT module descriptor from *.gwt.xml file.

    Represents the configuration of a GWT module including entry point classes,
    inherited modules, source paths, and other module-level settings.
    """

    module_name: str
    """Name of the GWT module (e.g., 'com.example.App')"""

    module_file: str
    """Path to the *.gwt.xml file"""

    entry_point_classes: List[str] = field(default_factory=list)
    """List of entry-point class names from <entry-point> elements"""

    inherits: List[str] = field(default_factory=list)
    """List of inherited module names from <inherits> elements"""

    source_paths: List[str] = field(default_factory=list)
    """List of source paths from <source> elements"""

    public_paths: List[str] = field(default_factory=list)
    """List of public resource paths from <public> elements"""

    rename_to: Optional[str] = None
    """Module rename-to attribute (compiled module name)"""

    circular_inherits: bool = False
    """Whether this module is part of a circular inheritance chain"""

    properties: Dict[str, str] = field(default_factory=dict)
    """Module properties from <set-property> elements"""

    stylesheets: List[str] = field(default_factory=list)
    """List of stylesheet references from <stylesheet> elements"""

    scripts: List[str] = field(default_factory=list)
    """List of script references from <script> elements"""

    def __post_init__(self):
        """Validate GWT module values"""
        if not self.module_name:
            raise ValueError("module_name cannot be empty")

        if not self.module_file:
            raise ValueError("module_file cannot be empty")

        # Validate entry point classes are fully qualified names
        for entry_point in self.entry_point_classes:
            if not entry_point or '.' not in entry_point:
                raise ValueError(f"Invalid entry point class name: {entry_point}")

    def is_library_module(self) -> bool:
        """
        Check if this is a library module (no entry points).

        Library modules are inherited by other modules but don't have their own entry points.

        Returns:
            True if this is a library module
        """
        return len(self.entry_point_classes) == 0

    def has_circular_dependency(self) -> bool:
        """
        Check if this module has circular dependency issues.

        Returns:
            True if circular_inherits flag is set
        """
        return self.circular_inherits

    def get_fully_qualified_entry_points(self) -> List[str]:
        """
        Get all entry point class names as fully qualified names.

        Returns:
            List of fully qualified entry point class names
        """
        return self.entry_point_classes

    def get_inherited_module_names(self) -> List[str]:
        """
        Get all inherited module names.

        Returns:
            List of inherited module names
        """
        return self.inherits

    def add_entry_point(self, class_name: str):
        """Add an entry point class to this module"""
        if class_name and class_name not in self.entry_point_classes:
            if '.' not in class_name:
                raise ValueError(f"Entry point must be fully qualified: {class_name}")
            self.entry_point_classes.append(class_name)

    def add_inherits(self, module_name: str):
        """Add an inherited module to this module"""
        if module_name and module_name not in self.inherits:
            self.inherits.append(module_name)

    def add_source_path(self, path: str):
        """Add a source path to this module"""
        if path and path not in self.source_paths:
            self.source_paths.append(path)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'module_name': self.module_name,
            'module_file': self.module_file,
            'entry_point_classes': self.entry_point_classes,
            'inherits': self.inherits,
            'source_paths': self.source_paths,
            'public_paths': self.public_paths,
            'rename_to': self.rename_to,
            'circular_inherits': self.circular_inherits,
            'properties': self.properties,
            'stylesheets': self.stylesheets,
            'scripts': self.scripts
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GWTModule':
        """Create GWTModule from dictionary"""
        return cls(
            module_name=data['module_name'],
            module_file=data['module_file'],
            entry_point_classes=data.get('entry_point_classes', []),
            inherits=data.get('inherits', []),
            source_paths=data.get('source_paths', []),
            public_paths=data.get('public_paths', []),
            rename_to=data.get('rename_to'),
            circular_inherits=data.get('circular_inherits', False),
            properties=data.get('properties', {}),
            stylesheets=data.get('stylesheets', []),
            scripts=data.get('scripts', [])
        )
