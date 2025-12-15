# Implementation Contracts: GWT Application Support

**Feature**: 001-gwt-prd-support
**Created**: 2025-12-14
**Purpose**: Define interfaces and schemas for GWT analyzer implementation

## Overview

This directory contains contract definitions that implementation code must adhere to:

1. **gwt_analyzer_interface.py** - Abstract base classes for all GWT analyzers
2. **weaviate_schema_extension.py** - Weaviate schema additions and query helpers

## Contract Files

### gwt_analyzer_interface.py

**Purpose**: Defines abstract interfaces that all GWT analyzers must implement

**Key Interfaces**:
- `GwtAnalyzer` - Base class for all GWT analyzers
- `GwtRpcAnalyzer` - RPC servlet analysis (FR-002, FR-003)
- `GwtPresenterAnalyzer` - MVP presenter analysis (FR-006, FR-009)
- `GwtViewAnalyzer` - MVP view analysis (FR-007)
- `GwtUiBinderParser` - UiBinder XML parsing (FR-004, FR-005)
- `GwtModelAnalyzer` - DTO extraction (FR-008)

**Supporting Classes**:
- `GwtAnalyzerRegistry` - Analyzer registration and routing
- `GwtPatternDetector` - GWT application detection (FR-001)

**Data Classes**:
- `RpcMethod` - RPC method signature representation
- `MvpBinding` - Presenter-view binding metadata
- `FormField` - UiBinder form field representation
- `DtoField` - DTO field definition

**Enums**:
- `GwtRole` - Artifact role classification
- `MvpBindingType` - Binding detection strategy

**Usage**:
```python
from specs.contracts.gwt_analyzer_interface import GwtRpcAnalyzer, RpcMethod

class FlashInfoServletAnalyzer(GwtRpcAnalyzer):
    def can_analyze(self, file_path: Path) -> bool:
        return file_path.name.endswith("ServletImpl.java")

    def analyze(self, file_path: Path, content: str, semantic_data=None) -> Dict[str, Any]:
        # Implementation here
        pass

    def get_gwt_role(self) -> GwtRole:
        return GwtRole.RPC_SERVLET
```

---

### weaviate_schema_extension.py

**Purpose**: Defines Weaviate schema additions for GWT metadata storage

**Schema Extensions**:
- 10 new properties added to `CodeArtifact` class
- All properties support filtering and querying
- Complex objects (arrays, nested structures) stored as JSON

**New Properties**:
| Property | Type | Description |
|----------|------|-------------|
| `gwt_role` | text | Artifact role (rpc_servlet, presenter, view, ui_binder, shared_dto) |
| `rpc_methods` | object[] | RPC method signatures |
| `presenter_view_binding` | object | MVP binding metadata with confidence |
| `ui_components` | object[] | Form fields and widgets |
| `dto_fields` | object[] | DTO field definitions |
| `gwt_framework_version` | text | Detected GWT version |
| `referenced_dtos` | text[] | DTO class names |
| `event_handlers` | object[] | Presenter event handlers |
| `navigation_logic` | object[] | Presenter navigation |
| `has_html_entities` | boolean | UiBinder HTML entity flag |

**Query Helpers**:
```python
from specs.contracts.weaviate_schema_extension import build_gwt_filter

# Find all RPC servlets in project
filter = build_gwt_filter("cuco-ui-admin", gwt_role="rpc_servlet")

# Find high-confidence presenter-view pairs
filter = build_gwt_filter("cuco-ui-admin", gwt_role="presenter", min_confidence=0.85)

# Find servlets using specific DTO
filter = build_dto_usage_query("cuco-ui-admin", "FlashInfoDTO")
```

**Validation Helpers**:
```python
from specs.contracts.weaviate_schema_extension import validate_gwt_metadata

artifact = {
    "gwt_role": "rpc_servlet",
    "rpc_methods": [...],
    "referenced_dtos": [...]
}

errors = validate_gwt_metadata(artifact)
if errors:
    print(f"Validation failed: {errors}")
```

**Sample Data**:
- `SAMPLE_RPC_SERVLET_METADATA` - Example RPC servlet artifact
- `SAMPLE_PRESENTER_METADATA` - Example presenter artifact
- `SAMPLE_UIBINDER_METADATA` - Example UiBinder artifact

---

## Implementation Guidelines

### 1. Analyzer Implementation Pattern

All analyzers follow this pattern:

```python
class MyGwtAnalyzer(GwtAnalyzer):
    """Docstring explaining what this analyzer does."""

    def can_analyze(self, file_path: Path) -> bool:
        """Check if file matches this analyzer's patterns."""
        # File pattern matching logic
        pass

    def analyze(self, file_path: Path, content: str, semantic_data=None) -> Dict[str, Any]:
        """Extract GWT metadata from file."""
        # Step 1: Use semantic data if available (LLM-extracted)
        # Step 2: Fall back to structural parsing (javalang/regex)
        # Step 3: Merge results
        # Step 4: Return dict matching data-model.md schema
        pass

    def get_gwt_role(self) -> GwtRole:
        """Return the GWT role this analyzer handles."""
        return GwtRole.RPC_SERVLET  # or PRESENTER, VIEW, etc.
```

### 2. Integration with Existing Codebase

**File**: `src/codeindex/services/extraction.py`

Modify the extraction service to route GWT files to appropriate analyzers:

```python
from codeindex.services.gwt_rpc_analyzer import GwtRpcAnalyzer
from codeindex.services.gwt_presenter_analyzer import GwtPresenterAnalyzer
from codeindex.services.gwt_view_analyzer import GwtViewAnalyzer

def _extract_semantic(self, file_path: Path, artifact_type: ArtifactType, pom_context=None):
    # Existing logic...

    # Add GWT routing
    if artifact_type == ArtifactType.JAVA_SOURCE:
        if file_path.name.endswith("ServletImpl.java"):
            analyzer = GwtRpcAnalyzer()
            if analyzer.can_analyze(file_path):
                content = file_path.read_text(encoding='utf-8')
                return analyzer.analyze(file_path, content, semantic_data)

        elif file_path.name.endswith("Presenter.java"):
            analyzer = GwtPresenterAnalyzer()
            # ... similar logic
```

**File**: `src/codeindex/schemas/weaviate_schema.py`

Add GWT schema extensions when creating schema:

```python
from specs.contracts.weaviate_schema_extension import GWT_SCHEMA_EXTENSION

def create_schema(client):
    # Existing schema creation...

    # Add GWT properties
    for prop in GWT_SCHEMA_EXTENSION["properties"]:
        client.schema.property.create("CodeArtifact", prop)
```

### 3. Hybrid Parsing Strategy

All analyzers should implement hybrid parsing:

```python
def extract_rpc_methods(self, file_path: Path, content: str) -> List[RpcMethod]:
    """Extract RPC methods using hybrid approach."""
    try:
        # Try javalang first (preferred)
        import javalang
        tree = javalang.parse.parse(content)
        return self._extract_with_javalang(tree)
    except Exception as e:
        # Fall back to regex
        self.logger.debug(f"javalang failed, using regex fallback: {e}")
        return self._extract_with_regex(content)
```

### 4. Confidence Scoring

Presenter-view bindings must include confidence scores:

```python
def detect_view_binding(self, file_path: Path, content: str) -> MvpBinding:
    """Detect view binding with confidence scoring."""

    # Strategy 1: Display interface (90% confidence)
    if "interface Display" in content:
        return MvpBinding(
            view_class=self._extract_display_usage(content),
            binding_type=MvpBindingType.DISPLAY_INTERFACE,
            confidence=0.9
        )

    # Strategy 2: Separate interface (85% confidence)
    view_class = self._extract_view_field(content)
    if view_class:
        return MvpBinding(
            view_class=view_class,
            binding_type=MvpBindingType.SEPARATE_INTERFACE,
            confidence=0.85
        )

    # Strategy 3: Naming convention (70% confidence)
    presenter_name = file_path.stem
    view_name = presenter_name.replace("Presenter", "View")
    return MvpBinding(
        view_class=view_name,
        binding_type=MvpBindingType.NAMING_CONVENTION,
        confidence=0.7
    )
```

### 5. Error Handling

All analyzers must handle errors gracefully:

```python
def analyze(self, file_path: Path, content: str, semantic_data=None) -> Dict[str, Any]:
    """Analyze GWT file with error handling."""
    try:
        # Analysis logic
        result = self._perform_analysis(file_path, content)

        # Validate result
        errors = validate_gwt_metadata(result)
        if errors:
            self.logger.warning(f"Validation errors in {file_path}: {errors}")

        return result

    except Exception as e:
        self.logger.error(f"Failed to analyze {file_path}: {e}")
        # Return minimal valid structure
        return create_gwt_metadata_template(self.get_gwt_role())
```

---

## Testing Requirements

### Unit Tests

Each analyzer must have unit tests covering:

1. **File Pattern Matching**
   ```python
   def test_can_analyze_rpc_servlet():
       analyzer = GwtRpcAnalyzer()
       assert analyzer.can_analyze(Path("FlashInfoServletImpl.java"))
       assert not analyzer.can_analyze(Path("FlashInfoDTO.java"))
   ```

2. **Method Extraction**
   ```python
   def test_extract_rpc_methods():
       analyzer = GwtRpcAnalyzer()
       content = load_fixture("FlashInfoServletImpl.java")
       methods = analyzer.extract_rpc_methods(Path("test.java"), content)
       assert len(methods) == 5
       assert methods[0].name == "createFlashInfo"
   ```

3. **Confidence Scoring**
   ```python
   def test_presenter_view_binding_confidence():
       analyzer = GwtPresenterAnalyzer()
       content = load_fixture("FlashAdministrationPresenter.java")
       binding = analyzer.detect_view_binding(Path("test.java"), content)
       assert binding.confidence >= 0.7
   ```

4. **Fallback Behavior**
   ```python
   def test_regex_fallback_on_malformed_java():
       analyzer = GwtRpcAnalyzer()
       malformed_content = "public class Foo { /* missing brace"
       methods = analyzer.extract_rpc_methods(Path("test.java"), malformed_content)
       # Should not raise exception, should return empty list
       assert methods == []
   ```

### Integration Tests

1. **Weaviate Schema Validation**
   ```python
   def test_gwt_schema_exists(weaviate_client):
       schema = weaviate_client.schema.get("CodeArtifact")
       assert "gwt_role" in [p["name"] for p in schema["properties"]]
   ```

2. **Query Helpers**
   ```python
   def test_build_gwt_filter():
       filter = build_gwt_filter("test-project", gwt_role="rpc_servlet")
       assert filter["operator"] == "And"
       assert len(filter["operands"]) == 2
   ```

3. **End-to-End Extraction**
   ```python
   def test_e2e_gwt_extraction():
       # Run full pipeline on test fixtures
       result = extract_gwt_project("tests/fixtures/gwt")
       assert result["rpc_servlets"] > 0
       assert result["presenters"] > 0
       assert result["views"] > 0
   ```

---

## Migration Path

### Phase 1: Core Infrastructure
1. Implement `GwtAnalyzerRegistry`
2. Add Weaviate schema extensions
3. Create hybrid Java parser (javalang + regex)

### Phase 2: RPC Analysis (P1)
1. Implement `GwtRpcAnalyzer`
2. Add RPC servlet classification to `classifier.py`
3. Test on sample servlets

### Phase 3: UI Parsing (P2)
1. Implement `GwtUiBinderParser`
2. Add UiBinder classification
3. Test on sample .ui.xml files

### Phase 4: MVP Detection (P3)
1. Implement `GwtPresenterAnalyzer` and `GwtViewAnalyzer`
2. Add confidence scoring
3. Test presenter-view binding

### Phase 5: DTO Extraction (P3)
1. Implement `GwtModelAnalyzer`
2. Add shared package detection
3. Test on sample DTOs

---

## FAQ

**Q: Why are interfaces abstract instead of concrete implementations?**
A: Contracts define "what" must be done, not "how". This allows flexibility in implementation while ensuring consistency.

**Q: Can I add additional methods to analyzer classes?**
A: Yes, but all abstract methods must be implemented. Additional helper methods are encouraged.

**Q: What happens if javalang is not installed?**
A: Analyzers must gracefully fall back to regex parsing. Installation is optional but recommended.

**Q: How do I test confidence scoring?**
A: Use test fixtures with known binding patterns and assert confidence values match expected thresholds.

**Q: Can I modify the Weaviate schema after indexing?**
A: Schema is additive only. New properties can be added without re-indexing existing data.

---

## References

- [data-model.md](../data-model.md) - Entity definitions and field schemas
- [research.md](../research.md) - Technical decisions and library selections
- [plan.md](../plan.md) - Implementation plan and constitution checks
- [spec.md](../spec.md) - Feature specification and requirements
