# Research: GWT Application Support Implementation

**Date**: 2025-12-14
**Feature**: 001-gwt-prd-support
**Purpose**: Technical research for implementing GWT pattern detection and analysis

## Executive Summary

This research establishes the technical foundation for implementing GWT (Google Web Toolkit) support in the PRD generation system. Key findings inform decisions on Java parsing libraries, GWT pattern detection strategies, and MVP relationship mapping.

## 1. Java Parsing Library Selection

### Decision: javalang (Primary) + Regex (Fallback)

**Rationale**:
- **javalang** provides sufficient AST parsing for Java 8 codebases (most GWT projects)
- Easy integration: `pip install javalang`, pure Python, no C dependencies
- Good balance of features vs. complexity for method signature extraction
- Existing regex parser serves as robust fallback for edge cases

**Alternatives Considered**:
- **tree-sitter-java**: Faster but more complex setup, overkill for current needs
- **Regex only**: Too fragile for nested structures and generic types
- **ANTLR4**: Full-featured but heavyweight dependency chain

**Implementation Approach**:
```python
class HybridJavaParser:
    # Try javalang first, fall back to regex
    def parse(file_path):
        if javalang_available:
            try: return parse_with_javalang(file_path)
            except: pass
        return parse_with_regex(file_path)
```

## 2. GWT RPC Servlet Detection

### Pattern Recognition

**Key Indicators**:
1. **Server-side Implementation**: Extends `RemoteServiceServlet`
2. **Service Interface**: Extends `RemoteService`
3. **Async Interface**: Name ends with `Async`, methods return `void` with `AsyncCallback<T>` parameter

**Naming Conventions** (descending confidence):
- `*ServletImpl.java` (95% confidence - standard GWT naming)
- `*Servlet.java` (85% confidence - alternative naming)
- `*Service.java` in `*.server.*` package (80% confidence - package-based)

**Detection Strategy**:
```python
def is_gwt_rpc_servlet(parsed_java):
    return (
        parsed_java['extends'] == 'RemoteServiceServlet' and
        'RemoteService' in parsed_java['implements'] and
        any('server' in pkg or 'servlet' in pkg
            for pkg in parsed_java['packages'])
    )
```

### RPC Method Extraction

**Method Signature Requirements**:
- Public visibility
- Declared in service interface
- Parameters and return types are serializable
- May throw `RemoteException` or custom exceptions

**Extraction with javalang**:
```python
for method in tree.filter(javalang.tree.MethodDeclaration):
    if 'public' in method.modifiers:
        rpc_methods.append({
            'name': method.name,
            'return_type': method.return_type.name,
            'parameters': [(p.type.name, p.name) for p in method.parameters],
            'exceptions': [e.name for e in method.throws]
        })
```

## 3. UiBinder XML Parsing

### Widget Type Mapping

| GWT Widget | Form Field Type | XML Pattern |
|------------|-----------------|-------------|
| `<g:TextBox>` | text | `{gwt_ns}TextBox` |
| `<g:TextArea>` | textarea | `{gwt_ns}TextArea` |
| `<g:PasswordTextBox>` | password | `{gwt_ns}PasswordTextBox` |
| `<g:CheckBox>` | checkbox | `{gwt_ns}CheckBox` |
| `<g:ListBox>` | select | `{gwt_ns}ListBox` |
| `<g:DatePicker>` | date | `{gwt_ns}DatePicker` |
| `<g:FileUpload>` | file | `{gwt_ns}FileUpload` |

**Namespace URIs**:
- UI Binder: `urn:ui:com.google.gwt.uibinder`
- Widgets: `urn:import:com.google.gwt.user.client.ui`

### Field Extraction Strategy

**Algorithm**:
1. Parse XML with lxml (recover mode for HTML entities)
2. Find all form widgets with `ui:field` attribute
3. Extract `name` attribute (HTML form name)
4. Heuristically match associated labels (previous sibling `<g:Label>`)
5. For `<g:ListBox>`, extract `<g:item>` options

**Label Matching Heuristic**:
```python
def find_associated_label(widget_element):
    parent = widget_element.getparent()
    widget_index = list(parent).index(widget_element)
    if widget_index > 0:
        prev = list(parent)[widget_index - 1]
        if prev.tag.endswith('Label'):
            return prev.text
    return None
```

## 4. MVP Pattern Detection

### Three Detection Strategies

#### Strategy 1: Inner Display Interface (Confidence: 90%)
```java
public class UserListPresenter {
    public interface Display {
        HasClickHandlers getAddButton();
        void setData(List<User> users);
    }
    private final Display view;
}
```

**Detection**: Search for `interface Display` within presenter class

#### Strategy 2: Separate View Interface (Confidence: 85%)
```java
public class UserListPresenter implements UserListView.Presenter {
    private final UserListView view;
}
```

**Detection**: Extract view type from field declaration or constructor parameter

#### Strategy 3: Naming Convention (Confidence: 70%)
```
UserListPresenter -> UserListView
FlashAdministrationPresenter -> FlashAdministrationView
```

**Detection**: Replace `Presenter` with `View` in class name, search file system

### Implementation Priority

1. **Display Interface** (P1): Highest confidence, most explicit binding
2. **Separate Interface** (P2): Medium confidence, requires interface resolution
3. **Naming Convention** (P3): Lowest confidence but useful for incomplete patterns

## 5. Performance Considerations

### Benchmarks (Estimated)

| Operation | Current | With javalang | Target |
|-----------|---------|---------------|--------|
| Java file parsing | 50 files/sec | 40 files/sec | >30 files/sec |
| UiBinder XML parsing | N/A (0) | 100 files/sec | >50 files/sec |
| MVP detection | N/A (0) | 20 files/sec | >10 files/sec |
| End-to-end (184 files) | 8 min | 10 min | <10 min ✓ |

**Memory Impact**:
- javalang AST: ~50KB per file
- 184 files: ~9MB additional memory
- Well under 2GB constraint ✓

### Optimization Strategies

1. **Lazy Loading**: Only parse Java when needed (RPC detection first via regex)
2. **Caching**: Cache parsed ASTs if file hasn't changed
3. **Parallel Processing**: Parse files concurrently (existing batch system)
4. **Fallback Fast Path**: Use regex for simple cases, javalang for complex

## 6. Error Handling

### Known Edge Cases

1. **Malformed UiBinder XML**:
   - Solution: lxml recover mode (already implemented for HTML entities)
   - Fallback: Skip file, log warning, continue

2. **Java Syntax Errors**:
   - Solution: Try regex fallback if javalang fails
   - Log parsing errors at DEBUG level

3. **Missing MVP Bindings**:
   - Solution: Report relationship with confidence score
   - PRD generation continues with partial data

4. **Generic Type Parameters**:
   - Example: `AsyncCallback<List<UserDTO>>`
   - Solution: Extract type recursively from javalang AST

## 7. Integration Points

### Existing Codebase Modifications

**Files to Extend**:
1. `src/codeindex/services/classifier.py` - Add GWT file patterns
2. `src/codeindex/services/extraction.py` - Route to GWT analyzers
3. `src/codeindex/services/frontend_analyzer.py` - Add UiBinder parsing
4. `src/codeindex/schemas/weaviate_schema.py` - Add GWT metadata fields

**Files to Create**:
1. `src/codeindex/parsers/hybrid_java_parser.py` - Java parsing
2. `src/codeindex/parsers/uibinder_parser.py` - UiBinder XML parsing
3. `src/codeindex/services/gwt_rpc_analyzer.py` - RPC servlet analysis
4. `src/codeindex/services/mvp_detector.py` - MVP pattern detection
5. `src/codeindex/utils/gwt_patterns.py` - Pattern matching utilities

## 8. Testing Strategy

### Test Fixtures Required

Create `tests/fixtures/gwt/` with:
1. **FlashInfoServletImpl.java** - RPC servlet with multiple methods
2. **FlashInfoService.java** - RPC service interface
3. **FlashInfoServiceAsync.java** - Async RPC interface
4. **FlashAdministrationPresenter.java** - Presenter with Display interface
5. **FlashAdministrationView.java** - View implementing Display
6. **FlashInfoEditView.ui.xml** - UiBinder with form fields (including `&nbsp;`)
7. **FlashInfoDTO.java** - Shared DTO with fields

### Test Coverage Goals

- **Unit Tests**:
  - GWT pattern detection: 100%
  - javalang + regex fallback: 100%
  - UiBinder field extraction: >90%
  - MVP detection (all 3 strategies): >85%

- **Integration Tests**:
  - E2E PRD generation on cuco-ui-admin: 1 test
  - Weaviate queries for GWT artifacts: >80%

## 9. Dependencies

### New Dependencies

```python
# requirements.txt additions
javalang==0.13.0  # Java AST parsing (optional - graceful fallback)
```

**Justification**: Single pure-Python dependency, no transitive dependencies, <500KB installed size.

### Optional Dependencies

- `tree-sitter-languages`: Consider for future performance optimization
- `tree-sitter`: If adopting tree-sitter parser

## 10. Risk Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| javalang fails on modern Java | Medium | Medium | Regex fallback, log warning |
| UiBinder parsing errors | Medium | Low | Recover mode, skip file |
| MVP detection false positives | Low | Low | Confidence scoring, manual review |
| Performance regression | Low | Medium | Benchmark tests, optimize hot paths |

### Backward Compatibility

- All new analyzers are additive
- Existing Java EE analysis unchanged
- Zero breaking changes to API or CLI

## 11. Implementation Sequence

### Phase Order (from plan.md)

**Phase 1**: Core Java parsing (javalang + hybrid parser)
**Phase 2**: GWT RPC detection and servlet analysis
**Phase 3**: UiBinder XML parsing and form extraction
**Phase 4**: MVP pattern detection and relationship mapping

**Rationale**: Bottom-up approach ensures each layer has solid foundation before building next.

## References

- [GWT RPC Documentation](https://www.gwtproject.org/doc/latest/tutorial/RPC.html)
- [javalang GitHub](https://github.com/c2nes/javalang)
- [GWT UiBinder Guide](https://www.gwtproject.org/doc/latest/DevGuideUiBinder.html)
- [GWT MVP Architecture](https://www.gwtproject.org/articles/mvp-architecture.html)
- PRD_FIX_PLAN.md (original problem analysis)
- Agent research output (detailed patterns and code examples)
