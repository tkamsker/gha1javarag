# Data Model: GWT Application Support

**Feature**: 001-gwt-prd-support
**Created**: 2025-12-14
**Purpose**: Define data entities and relationships for GWT artifact metadata

## Overview

This data model extends the existing `CodeArtifact` schema in Weaviate with GWT-specific metadata fields. All GWT artifacts inherit from the base artifact structure and add domain-specific properties for RPC servlets, MVP components, and UI definitions.

## Base Artifact Structure (Existing)

All GWT entities extend the existing artifact model:

```python
{
    "id": str,                    # Canonical ID
    "project": str,               # Project name
    "file_path": str,            # Source file path
    "artifact_type": str,        # ArtifactType enum value
    "language": str,             # "java" | "xml"
    "framework": List[str],      # ["GWT", "GWT-RPC", "GWT-MVP", ...]
    "domain_labels": List[str],  # Business domain tags
    "semantic_data": dict,       # Extracted semantic information
    "created_at": datetime,
    "updated_at": datetime
}
```

## GWT-Specific Entities

### 1. GWT RPC Servlet

Represents server-side RPC endpoint implementations.

**Artifact Type**: `JAVA_SOURCE`
**Framework Tags**: `["GWT", "GWT-RPC", "Backend"]`

**Semantic Data Schema**:
```python
{
    "gwt_role": "rpc_servlet",
    "servlet_name": str,                    # e.g., "FlashInfoServletImpl"
    "service_interface": str,               # e.g., "FlashInfoService"
    "async_interface": str,                 # e.g., "FlashInfoServiceAsync"
    "url_mapping": Optional[str],           # Servlet mapping path
    "base_class": "RemoteServiceServlet",
    "rpc_methods": [
        {
            "name": str,                     # Method name
            "return_type": str,              # Java return type
            "parameters": [
                {
                    "name": str,
                    "type": str,             # Parameter type
                    "is_dto": bool           # Whether it's a DTO
                }
            ],
            "exceptions": List[str],         # Thrown exceptions
            "description": str,              # LLM-extracted purpose
            "visibility": "public"
        }
    ],
    "referenced_dtos": List[str],           # DTO class names used
    "spring_annotations": List[str]         # Spring config if present
}
```

**Validation Rules** (from FR-002, FR-003):
- Must have at least one public method
- File name must match `*Servlet.java` or `*ServletImpl.java`
- `base_class` must be "RemoteServiceServlet" or implement RemoteService
- Each RPC method must have complete signature (name, return type, parameters)

**Relationships**:
- **References**: Shared DTOs (many-to-many)
- **Implements**: Service interface (one-to-one)

**State Transitions**: N/A (immutable once indexed)

---

### 2. MVP Presenter

Represents business logic controllers in the Model-View-Presenter pattern.

**Artifact Type**: `JAVA_SOURCE`
**Framework Tags**: `["GWT", "GWT-MVP", "Frontend"]`

**Semantic Data Schema**:
```python
{
    "gwt_role": "presenter",
    "presenter_name": str,                  # e.g., "FlashAdministrationPresenter"
    "view_binding": {
        "view_class": Optional[str],        # e.g., "FlashAdministrationView"
        "binding_type": str,                # "display_interface" | "separate_interface" | "naming_convention"
        "confidence": float                 # 0.7 to 1.0
    },
    "display_interface": Optional[dict],    # Inner Display interface if present
    "event_handlers": [
        {
            "handler_name": str,             # e.g., "onEditButtonClick"
            "event_type": str,               # e.g., "ClickHandler"
            "description": str,              # What the handler does
            "target_view_component": Optional[str]
        }
    ],
    "navigation_logic": [
        {
            "method_name": str,
            "target_presenter": str,         # Navigates to which presenter
            "description": str
        }
    ],
    "rpc_calls": [
        {
            "service": str,                  # RPC service name
            "method": str,                   # RPC method called
            "callback_logic": str            # What happens on success/failure
        }
    ],
    "constructor_params": List[str]         # Dependency injection
}
```

**Validation Rules** (from FR-006, FR-009):
- Must have file name ending with `*Presenter.java`
- Must have at least one event handler OR navigation method
- If `view_binding.confidence` < 0.7, issue warning in PRD
- `view_binding.binding_type` must be one of the three detection strategies

**Relationships**:
- **Controls**: MVP View (one-to-one, optional)
- **Calls**: GWT RPC Servlets (many-to-many)
- **Navigates To**: Other presenters (many-to-many)

**State Transitions**: N/A (immutable once indexed)

---

### 3. MVP View

Represents UI component implementations in the MVP pattern.

**Artifact Type**: `JAVA_SOURCE`
**Framework Tags**: `["GWT", "GWT-MVP", "Frontend"]`

**Semantic Data Schema**:
```python
{
    "gwt_role": "view",
    "view_name": str,                       # e.g., "FlashInfoEditView"
    "implements_interface": Optional[str],  # e.g., "FlashAdministrationPresenter.Display"
    "ui_binder_file": Optional[str],        # Associated .ui.xml file path
    "widgets": [
        {
            "field_name": str,               # @UiField annotated field
            "widget_type": str,              # e.g., "TextBox", "Button"
            "ui_field_annotation": bool      # Has @UiField annotation
        }
    ],
    "event_bindings": [
        {
            "widget_field": str,
            "event_type": str,               # e.g., "ClickEvent"
            "handler_method": str            # Method that handles event
        }
    ],
    "component_type": str                   # "popup" | "portlet" | "panel" | "composite"
}
```

**Validation Rules** (from FR-007):
- Must have file name ending with `*View.java`
- If `ui_binder_file` is present, file must exist and parse successfully
- Each widget must have a `widget_type` (cannot be null)

**Relationships**:
- **Controlled By**: MVP Presenter (one-to-one, optional)
- **Defined In**: UiBinder Template (one-to-one, optional)

**State Transitions**: N/A (immutable once indexed)

---

### 4. UiBinder Template

Represents declarative UI definitions in XML format.

**Artifact Type**: `GWT_UI_BINDER`
**Framework Tags**: `["GWT", "GWT-UiBinder", "Frontend"]`

**Semantic Data Schema**:
```python
{
    "gwt_role": "ui_binder",
    "template_name": str,                   # File name without extension
    "associated_view": Optional[str],       # Java class using this template
    "namespace_uri": str,                   # UiBinder namespace
    "form_fields": [
        {
            "ui_field_name": str,            # ui:field attribute value
            "widget_type": str,              # TextBox, TextArea, CheckBox, etc.
            "html_name": Optional[str],      # name attribute if present
            "label": Optional[str],          # Associated label text (heuristic)
            "required": Optional[bool],      # Inferred from validation
            "field_type": str                # "text" | "textarea" | "checkbox" | "select" | "date" | "file"
        }
    ],
    "panels": [
        {
            "type": str,                     # VerticalPanel, HorizontalPanel, etc.
            "child_count": int,
            "layout_hints": str              # Description of layout structure
        }
    ],
    "buttons": [
        {
            "ui_field_name": str,
            "text": str,                     # Button label
            "style_name": Optional[str]      # CSS class
        }
    ],
    "select_options": dict,                 # ListBox ui:field -> list of options
    "css_resources": List[str],             # Referenced CSS files
    "has_html_entities": bool               # Whether file contains &nbsp; etc.
}
```

**Validation Rules** (from FR-004, FR-005):
- Must parse successfully with lxml recover mode
- All `form_fields` must have non-empty `widget_type`
- `field_type` must map correctly from widget type (see research.md Table)
- If HTML entities are present, `has_html_entities` must be `true`

**Relationships**:
- **Used By**: MVP View (one-to-one, optional)

**State Transitions**: N/A (immutable once indexed)

---

### 5. Shared Data Transfer Object

Represents data structures shared between client and server.

**Artifact Type**: `JAVA_SOURCE`
**Framework Tags**: `["GWT", "GWT-Shared", "DTO"]`

**Semantic Data Schema**:
```python
{
    "gwt_role": "shared_dto",
    "class_name": str,                      # e.g., "FlashInfoDTO"
    "package": str,                         # Fully qualified package
    "implements_serializable": bool,        # Must be true for GWT RPC
    "fields": [
        {
            "name": str,
            "type": str,                     # Java type
            "visibility": str,               # "private" | "protected" | "public"
            "has_getter": bool,
            "has_setter": bool,
            "validation_annotations": List[str]  # @NotNull, @Size, etc.
        }
    ],
    "nested_dtos": List[str],               # References to other DTOs
    "validation_rules": [
        {
            "field": str,
            "rule": str,                     # e.g., "NotNull", "Size(min=1, max=100)"
            "message": Optional[str]         # Validation error message
        }
    ],
    "is_nested_in": Optional[str],          # Parent DTO if this is nested
    "default_constructor": bool             # Required for GWT serialization
}
```

**Validation Rules** (from FR-008):
- `implements_serializable` must be `true` for RPC usage
- Must have `default_constructor` for GWT serialization
- All fields should have getters and setters (warn if missing)
- If validation annotations present, extract to `validation_rules`

**Relationships**:
- **Used By**: GWT RPC Servlets (many-to-many)
- **Contains**: Other DTOs (many-to-many, for nested structures)

**State Transitions**: N/A (immutable once indexed)

---

## Weaviate Schema Extensions

### New Metadata Fields

Add to existing `CodeArtifact` class in Weaviate:

```python
{
    # Existing fields...

    # GWT-specific metadata
    "gwt_role": str,                        # "rpc_servlet" | "presenter" | "view" | "ui_binder" | "shared_dto"
    "rpc_methods": object,                  # JSON array of method signatures
    "presenter_view_binding": object,       # JSON object with binding metadata
    "ui_components": object,                # JSON array of form fields/widgets
    "dto_fields": object,                   # JSON array of DTO field definitions
    "gwt_framework_version": Optional[str]  # Detected GWT version
}
```

### Query Patterns

**Find all RPC servlets in a project**:
```python
where_filter = {
    "operator": "And",
    "operands": [
        {"path": ["project"], "operator": "Equal", "valueText": project_name},
        {"path": ["gwt_role"], "operator": "Equal", "valueText": "rpc_servlet"}
    ]
}
```

**Find presenter-view pairs with high confidence**:
```python
where_filter = {
    "operator": "And",
    "operands": [
        {"path": ["gwt_role"], "operator": "Equal", "valueText": "presenter"},
        {"path": ["presenter_view_binding.confidence"], "operator": "GreaterThan", "valueNumber": 0.85}
    ]
}
```

**Find all form fields across UiBinder templates**:
```python
where_filter = {
    "operator": "Equal",
    "path": ["gwt_role"],
    "valueText": "ui_binder"
}
# Then aggregate form_fields from ui_components
```

---

## Data Flow

### Extraction Phase
1. **Classifier** detects GWT files (FR-001)
2. **Semantic Extractor** uses Ollama to extract GWT patterns
3. **Structural Parser** (javalang/regex) extracts method signatures
4. **Hybrid Result** merges semantic + structural data

### Indexing Phase
1. Populate base `CodeArtifact` fields
2. Add GWT-specific metadata to `semantic_data`
3. Set `gwt_role` field for filtering
4. Generate vector embeddings
5. Store in Weaviate with project partition

### PRD Generation Phase
1. Query Weaviate by `gwt_role` and project
2. Group artifacts by type (servlets, presenters, views)
3. Resolve presenter-view relationships
4. Generate PRD sections using templates

---

## Cardinality Summary

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| Presenter → View | 1:0..1 | Presenter may control one view (optional) |
| View → UiBinder | 1:0..1 | View may use one UiBinder template (optional) |
| Presenter → RPC Servlet | M:N | Presenter can call multiple RPC services |
| RPC Servlet → DTO | M:N | Servlet methods use multiple DTOs |
| DTO → DTO | M:N | DTOs can nest other DTOs |
| Presenter → Presenter | M:N | Navigation between presenters |

---

## Migration Notes

**Existing Data Compatibility**:
- New `gwt_role` field defaults to `null` for non-GWT artifacts
- Existing Java EE artifacts unaffected
- No schema breaking changes - only additive fields

**Re-indexing Strategy**:
- Not required for existing projects
- GWT projects should be indexed fresh
- Mixed Java EE + GWT projects supported (FR-011)
