"""
Weaviate Schema Extension for GWT Support

Defines schema additions to the existing CodeArtifact class in Weaviate.
These fields store GWT-specific metadata extracted by GWT analyzers.

Integration Point: src/codeindex/schemas/weaviate_schema.py
"""

from typing import Dict, Any, List


# ============================================================================
# Schema Extension Definition
# ============================================================================

GWT_SCHEMA_EXTENSION = {
    "class": "CodeArtifact",  # Existing class - add these properties
    "properties": [
        {
            "name": "gwt_role",
            "dataType": ["text"],
            "description": "GWT-specific artifact role: rpc_servlet, presenter, view, ui_binder, shared_dto",
            "indexFilterable": True,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True  # Don't vectorize role (used for filtering)
                }
            }
        },
        {
            "name": "rpc_methods",
            "dataType": ["object[]"],
            "description": "Array of RPC method signatures with parameters, return types, exceptions",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True  # Complex object, skip vectorization
                }
            }
        },
        {
            "name": "presenter_view_binding",
            "dataType": ["object"],
            "description": "Presenter-view binding metadata with confidence score",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "ui_components",
            "dataType": ["object[]"],
            "description": "Array of UI widgets, form fields, and panels from UiBinder",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "dto_fields",
            "dataType": ["object[]"],
            "description": "Array of DTO field definitions with types and validation rules",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "gwt_framework_version",
            "dataType": ["text"],
            "description": "Detected GWT version (e.g., '2.8.2')",
            "indexFilterable": True,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "referenced_dtos",
            "dataType": ["text[]"],
            "description": "List of DTO class names referenced by RPC methods",
            "indexFilterable": True,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "event_handlers",
            "dataType": ["object[]"],
            "description": "Event handler methods in presenters",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "navigation_logic",
            "dataType": ["object[]"],
            "description": "Navigation between presenters",
            "indexFilterable": False,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        },
        {
            "name": "has_html_entities",
            "dataType": ["boolean"],
            "description": "Whether UiBinder template contains HTML entities",
            "indexFilterable": True,
            "indexSearchable": False,
            "moduleConfig": {
                "text2vec-ollama": {
                    "skip": True
                }
            }
        }
    ]
}


# ============================================================================
# Query Helpers
# ============================================================================

def build_gwt_filter(
    project: str,
    gwt_role: str = None,
    min_confidence: float = None
) -> Dict[str, Any]:
    """
    Build Weaviate where filter for GWT artifacts.

    Args:
        project: Project name
        gwt_role: Optional role filter (rpc_servlet, presenter, view, ui_binder, shared_dto)
        min_confidence: Optional minimum confidence for presenter-view bindings

    Returns:
        Weaviate where filter dict

    Example:
        >>> build_gwt_filter("cuco-ui-admin", gwt_role="rpc_servlet")
        {
            "operator": "And",
            "operands": [
                {"path": ["project"], "operator": "Equal", "valueText": "cuco-ui-admin"},
                {"path": ["gwt_role"], "operator": "Equal", "valueText": "rpc_servlet"}
            ]
        }
    """
    operands = [
        {"path": ["project"], "operator": "Equal", "valueText": project}
    ]

    if gwt_role:
        operands.append({
            "path": ["gwt_role"],
            "operator": "Equal",
            "valueText": gwt_role
        })

    if min_confidence is not None:
        operands.append({
            "path": ["presenter_view_binding", "confidence"],
            "operator": "GreaterThanEqual",
            "valueNumber": min_confidence
        })

    if len(operands) == 1:
        return operands[0]
    else:
        return {"operator": "And", "operands": operands}


def build_dto_usage_query(project: str, dto_class_name: str) -> Dict[str, Any]:
    """
    Find all RPC servlets that use a specific DTO.

    Args:
        project: Project name
        dto_class_name: DTO class name to search for

    Returns:
        Weaviate where filter dict

    Example:
        >>> build_dto_usage_query("cuco-ui-admin", "FlashInfoDTO")
        {
            "operator": "And",
            "operands": [
                {"path": ["project"], "operator": "Equal", "valueText": "cuco-ui-admin"},
                {"path": ["gwt_role"], "operator": "Equal", "valueText": "rpc_servlet"},
                {"path": ["referenced_dtos"], "operator": "ContainsAny", "valueText": ["FlashInfoDTO"]}
            ]
        }
    """
    return {
        "operator": "And",
        "operands": [
            {"path": ["project"], "operator": "Equal", "valueText": project},
            {"path": ["gwt_role"], "operator": "Equal", "valueText": "rpc_servlet"},
            {
                "path": ["referenced_dtos"],
                "operator": "ContainsAny",
                "valueText": [dto_class_name]
            }
        ]
    }


def build_presenter_view_pairs_query(project: str, min_confidence: float = 0.85) -> Dict[str, Any]:
    """
    Find presenter-view pairs with high confidence bindings.

    Args:
        project: Project name
        min_confidence: Minimum confidence threshold (default 0.85)

    Returns:
        Weaviate where filter dict
    """
    return build_gwt_filter(project, gwt_role="presenter", min_confidence=min_confidence)


# ============================================================================
# Migration Helpers
# ============================================================================

def create_gwt_metadata_template(gwt_role: str) -> Dict[str, Any]:
    """
    Create empty metadata template for GWT artifacts.

    Args:
        gwt_role: GWT role (rpc_servlet, presenter, view, ui_binder, shared_dto)

    Returns:
        Dictionary with default null values for GWT fields
    """
    template = {
        "gwt_role": gwt_role,
        "rpc_methods": None,
        "presenter_view_binding": None,
        "ui_components": None,
        "dto_fields": None,
        "gwt_framework_version": None,
        "referenced_dtos": None,
        "event_handlers": None,
        "navigation_logic": None,
        "has_html_entities": False
    }

    # Set role-specific fields to empty arrays instead of None
    if gwt_role == "rpc_servlet":
        template["rpc_methods"] = []
        template["referenced_dtos"] = []
    elif gwt_role == "presenter":
        template["event_handlers"] = []
        template["navigation_logic"] = []
        template["presenter_view_binding"] = {
            "view_class": None,
            "binding_type": None,
            "confidence": 0.0
        }
    elif gwt_role == "view":
        template["ui_components"] = []
    elif gwt_role == "ui_binder":
        template["ui_components"] = []
        template["has_html_entities"] = False
    elif gwt_role == "shared_dto":
        template["dto_fields"] = []

    return template


def validate_gwt_metadata(artifact: Dict[str, Any]) -> List[str]:
    """
    Validate GWT metadata for completeness.

    Args:
        artifact: CodeArtifact dictionary with GWT metadata

    Returns:
        List of validation errors (empty if valid)

    Example:
        >>> artifact = {"gwt_role": "rpc_servlet", "rpc_methods": []}
        >>> validate_gwt_metadata(artifact)
        ['RPC servlet must have at least one method']
    """
    errors = []
    gwt_role = artifact.get("gwt_role")

    if not gwt_role:
        return errors  # Not a GWT artifact

    # Role-specific validation
    if gwt_role == "rpc_servlet":
        rpc_methods = artifact.get("rpc_methods")
        if not rpc_methods or len(rpc_methods) == 0:
            errors.append("RPC servlet must have at least one method")

        referenced_dtos = artifact.get("referenced_dtos")
        if referenced_dtos is None:
            errors.append("RPC servlet must have referenced_dtos list (can be empty)")

    elif gwt_role == "presenter":
        binding = artifact.get("presenter_view_binding")
        if not binding:
            errors.append("Presenter must have presenter_view_binding object")
        elif binding.get("confidence", 0.0) < 0.7:
            errors.append(f"Presenter-view binding confidence too low: {binding.get('confidence')}")

        event_handlers = artifact.get("event_handlers")
        navigation = artifact.get("navigation_logic")
        if (not event_handlers or len(event_handlers) == 0) and (not navigation or len(navigation) == 0):
            errors.append("Presenter must have at least one event handler or navigation method")

    elif gwt_role == "view":
        ui_components = artifact.get("ui_components")
        if ui_components is None:
            errors.append("View must have ui_components list (can be empty)")

    elif gwt_role == "ui_binder":
        ui_components = artifact.get("ui_components")
        if not ui_components or len(ui_components) == 0:
            errors.append("UiBinder must have at least one UI component")

        if artifact.get("has_html_entities") is None:
            errors.append("UiBinder must have has_html_entities boolean")

    elif gwt_role == "shared_dto":
        dto_fields = artifact.get("dto_fields")
        if not dto_fields or len(dto_fields) == 0:
            errors.append("DTO must have at least one field")

    return errors


# ============================================================================
# Sample Data
# ============================================================================

SAMPLE_RPC_SERVLET_METADATA = {
    "gwt_role": "rpc_servlet",
    "rpc_methods": [
        {
            "name": "createFlashInfo",
            "return_type": "FlashInfoDTO",
            "parameters": [
                {"name": "dto", "type": "FlashInfoDTO", "is_dto": True}
            ],
            "exceptions": ["RemoteException"],
            "description": "Creates new flash info message",
            "visibility": "public"
        }
    ],
    "referenced_dtos": ["FlashInfoDTO"],
    "gwt_framework_version": "2.8.2",
    "presenter_view_binding": None,
    "ui_components": None,
    "dto_fields": None,
    "event_handlers": None,
    "navigation_logic": None,
    "has_html_entities": False
}

SAMPLE_PRESENTER_METADATA = {
    "gwt_role": "presenter",
    "presenter_view_binding": {
        "view_class": "FlashAdministrationView",
        "binding_type": "display_interface",
        "confidence": 0.9
    },
    "event_handlers": [
        {
            "handler_name": "onEditButtonClick",
            "event_type": "ClickHandler",
            "description": "Opens edit dialog for flash info",
            "target_view_component": "editButton"
        }
    ],
    "navigation_logic": [
        {
            "method_name": "goToAdminMain",
            "target_presenter": "AdminMainPresenter",
            "description": "Returns to admin main screen"
        }
    ],
    "gwt_framework_version": "2.8.2",
    "rpc_methods": None,
    "referenced_dtos": None,
    "ui_components": None,
    "dto_fields": None,
    "has_html_entities": False
}

SAMPLE_UIBINDER_METADATA = {
    "gwt_role": "ui_binder",
    "ui_components": [
        {
            "ui_field_name": "titleField",
            "widget_type": "TextBox",
            "html_name": "title",
            "label": "Title",
            "required": True,
            "field_type": "text"
        },
        {
            "ui_field_name": "messageField",
            "widget_type": "TextArea",
            "html_name": "message",
            "label": "Message",
            "required": True,
            "field_type": "textarea"
        }
    ],
    "has_html_entities": True,
    "gwt_framework_version": "2.8.2",
    "rpc_methods": None,
    "referenced_dtos": None,
    "presenter_view_binding": None,
    "dto_fields": None,
    "event_handlers": None,
    "navigation_logic": None
}
