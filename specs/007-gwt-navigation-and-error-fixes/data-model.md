# Data Model: GWT Navigation Analysis and Error Fixes

**Feature**: 007-gwt-navigation-and-error-fixes
**Created**: 2025-12-22

## Core Entities

### 1. NavigationGraph
Complete UI navigation structure from entry points (index.html, index.jsp) through GWT modules to all UI components.

**Key Fields**: project, graph_id, entry_points, nodes, edges, statistics

### 2. NavigationNode
Single node in navigation graph (Presenter/View/Activity/Place/Module/External).

**Key Fields**: node_id, node_type, label, source_file, outgoing_targets, confidence

### 3. GWTModule
Parsed GWT module descriptor (*.gwt.xml) with entry points and inheritance.

**Key Fields**: module_name, module_file, entry_point_classes, inherits, circular_inherits

### 4. PresenterViewBinding
Maps Presenter → Display interface → View → UiBinder template.

**Key Fields**: presenter_class, display_interface, view_class, ui_binder_template, confidence_score

### 5. UiBinderHierarchy
Widget hierarchy from UiBinder XML template.

**Key Fields**: template_path, root_widget_type, widgets, form_fields, buttons, event_handlers

### 6. ForeignKeyRelationship
Database FK with multi-source extraction (Java/iBATIS/SQL).

**Key Fields**: source_entity, source_column, target_entity, target_column, fk_source, confidence

### 7. TimeoutMetric
Ollama timeout event tracking with retry/fallback metadata.

**Key Fields**: file_path, timeout_threshold, retry_count, fallback_used, extraction_quality

## Implementation

All models use Python `dataclasses` with type hints (Python 3.8+) and Pydantic-style validation in `__post_init__` methods.

**Location**: 
- NavigationGraph, NavigationNode: `src/codeindex/models/navigation.py` (NEW)
- GWTModule: `src/codeindex/models/gwt_module.py` (NEW)
- PresenterViewBinding, UiBinderHierarchy: `src/codeindex/models/gwt_binding.py` (NEW)
- ForeignKeyRelationship: `src/codeindex/models/foreign_key.py` (NEW)
- TimeoutMetric: `src/codeindex/models/metrics.py` (NEW)

See [plan.md](./plan.md) for complete field definitions, validation rules, and usage examples.
