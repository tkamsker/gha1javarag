# GWT PRD Generation Implementation Plan

**Goal**: Fix T083 validation failure by making PRD generator consume GWT metadata from Weaviate

**Current Coverage**: 13.4% (16/119 components)
**Target Coverage**: >80% (96/119 components)

## Problem Analysis

### Current Architecture
1. **PRD Analyzers** (`db_analyzer.py`, `service_analyzer.py`, `frontend_analyzer.py`):
   - Scan source filesystem for files
   - Use LLM to extract metadata
   - Save as JSON files in `output/<layer>/`

2. **PRD Generator** (`prd_generator.py`):
   - Loads JSON files from `output/<layer>/`
   - Synthesizes into master PRD markdown

3. **GWT Extraction** (Already Working):
   - Discovery finds GWT files
   - Extraction analyzes with specialized parsers
   - **Metadata stored in Weaviate** with fields:
     - `gwt_role`: presenter, view, ui_binder, rpc_servlet, shared_dto
     - Presenter: `presenter_name`, `view_binding`, `event_handlers`, `navigation_logic`, `rpc_calls`
     - View: `view_name`, `component_type`, `ui_fields`
     - UiBinder: `template_name`, `form_fields` (with widget types, labels, options)
     - RPC: `service_class`, `rpc_methods`

### The Gap
- **Frontend Analyzer** only looks for "forms" using regex patterns
- Doesn't query Weaviate for GWT artifacts
- Missing 103 GWT components (40 Presenters + 30 Views + 33 UiBinder)
- Only captures 16 RPC servlets via service analyzer

## Solution Strategy

### Approach: Query Weaviate from Frontend Analyzer

**Why This Approach:**
1. GWT metadata is already complete and high-quality in Weaviate
2. Avoid duplicate LLM analysis (faster, cheaper)
3. No changes to extraction pipeline (already working perfectly)
4. No changes to PRD generator structure

**Implementation Steps:**

### Step 1: Add Weaviate Query to Frontend Analyzer ✓ TODO

**File**: `src/codeindex/services/frontend_analyzer.py`

Add new method:
```python
def _query_gwt_artifacts_from_weaviate(
    self,
    config,
    project_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Query Weaviate for GWT artifacts.

    Returns:
        List of GWT artifacts with semantic_data.gwt_role in:
        - presenter
        - view
        - ui_binder
        - rpc_servlet (may already be captured by service analyzer)
    """
    from codeindex.services.weaviate_store import WeaviateStore

    store = WeaviateStore(config=config)

    # Query for GWT artifacts
    # WHERE semantic_data.gwt_role IN [presenter, view, ui_binder]
    # AND project = project_name (if specified)

    # Return artifacts
```

### Step 2: Convert GWT Artifacts to PRD Models ✓ TODO

**File**: `src/codeindex/services/frontend_analyzer.py`

Add conversion methods:
```python
def _convert_gwt_presenter_to_ui_component(
    self,
    artifact: Dict[str, Any]
) -> UIComponent:
    """Convert GWT Presenter to UIComponent model."""
    semantic = artifact['semantic_data']

    return UIComponent(
        name=semantic.get('presenter_name', ''),
        component_type=ComponentType.GWT_PRESENTER,
        file_path=artifact['file_path'],
        description=semantic.get('summary', ''),
        events=[...],  # from event_handlers
        data_bindings=[...],  # from rpc_calls
        navigation_targets=[...]  # from navigation_logic
    )

def _convert_gwt_view_to_ui_component(
    self,
    artifact: Dict[str, Any]
) -> UIComponent:
    """Convert GWT View to UIComponent model."""
    # Similar structure

def _convert_uibinder_to_form_definition(
    self,
    artifact: Dict[str, Any]
) -> FormDefinition:
    """Convert UiBinder to FormDefinition model."""
    semantic = artifact['semantic_data']

    fields = []
    for field_data in semantic.get('form_fields', []):
        fields.append(FormField(
            name=field_data.get('field_name', ''),
            type=_map_widget_to_field_type(field_data.get('widget_type')),
            label=field_data.get('label', ''),
            required=field_data.get('required', False),
            validation=[...]
        ))

    return FormDefinition(
        name=semantic.get('template_name', ''),
        form_type=FormType.GWT_FORM,
        fields=fields,
        # ...
    )
```

### Step 3: Integrate with Existing Analysis ✓ TODO

**File**: `src/codeindex/services/frontend_analyzer.py`

Modify `analyze()` method:
```python
def analyze(self, project_name: Optional[str] = None):
    """Analyze frontend layer."""

    # Existing filesystem analysis
    frontend_files = self.find_frontend_files()

    # Analyze files with LLM (existing code)
    forms_from_files = self._analyze_files_with_llm(frontend_files)

    # NEW: Query Weaviate for GWT artifacts
    gwt_artifacts = self._query_gwt_artifacts_from_weaviate(
        config=self.config,  # Need to pass config to __init__
        project_name=project_name
    )

    # NEW: Convert GWT artifacts to PRD models
    for artifact in gwt_artifacts:
        gwt_role = artifact['semantic_data'].get('gwt_role')

        if gwt_role == 'presenter':
            component = self._convert_gwt_presenter_to_ui_component(artifact)
            self._save_ui_component(component)

        elif gwt_role == 'view':
            component = self._convert_gwt_view_to_ui_component(artifact)
            self._save_ui_component(component)

        elif gwt_role == 'ui_binder':
            form = self._convert_uibinder_to_form_definition(artifact)
            self._save_form_definition(form)

    # Continue with existing code...
```

### Step 4: Add GWT Sections to PRD Template ✓ TODO

**File**: `src/codeindex/services/prd_generator.py`

Modify `generate_master_prd()` to add GWT-specific sections:

```markdown
## Frontend Layer

### UI Components

#### GWT Presenters (40)
| Presenter | View Binding | Event Handlers | Navigation |
|-----------|--------------|----------------|------------|
| UserListPresenter | UserListView | onEdit, onDelete | -> UserEditView |
| ... | ... | ... | ... |

#### GWT Views (30)
| View | Component Type | UI Fields | Template |
|------|----------------|-----------|----------|
| UserListView | Composite | table, searchBox | UserListView.ui.xml |
| ... | ... | ... | ... |

#### GWT Forms (33)
| Form | Fields | Validation | Submission |
|------|--------|------------|------------|
| UserEditView.ui.xml | firstName, lastName, email | required, email format | UserService.saveUser() |
| ... | ... | ... | ... |
```

### Step 5: Update PRD Models ✓ TODO

**File**: `src/codeindex/models/prd.py`

Add GWT-specific component types:
```python
class ComponentType(Enum):
    GWT_PRESENTER = "gwt_presenter"
    GWT_VIEW = "gwt_view"
    GWT_WIDGET = "gwt_widget"
    GWT_ACTIVITY = "gwt_activity"
    # ... existing types
```

## Testing Strategy

1. **Unit Test**: Test Weaviate query and conversion methods
2. **Integration Test**: Run PRD generation on cuco-ui-admin
3. **Validation**: Re-run T083 coverage calculation

### Expected Coverage After Fix

- **Presenters**: 40/40 (100%)
- **Views**: 30/30 (100%)
- **UiBinder**: 33/33 (100%)
- **RPC Servlets**: 16/16 (already working)
- **Total**: 119/119 (100%)

## Files to Modify

1. `src/codeindex/services/frontend_analyzer.py` - Add Weaviate query and conversion
2. `src/codeindex/models/prd.py` - Add GWT component types
3. `src/codeindex/services/prd_generator.py` - Add GWT sections to template
4. `tests/integration/test_gwt_prd_generation.py` - Add integration test

## Implementation Order

1. ✓ Explore architecture (DONE)
2. ⏳ Implement Weaviate query method
3. ⏳ Implement GWT-to-PRD conversion methods
4. ⏳ Update PRD generator templates
5. ⏳ Add GWT component types to models
6. ⏳ Integration test
7. ⏳ Re-run T083 validation

## Success Criteria

- T083 coverage >80% (currently 13.4%)
- PRD shows all 40 Presenters
- PRD shows all 30 Views
- PRD shows all 33 UiBinder forms
- No breaking changes to existing non-GWT PRD generation
- T082 timing improved or maintained (<14min)
