# Refactoring Plan: Multi-Directory Maven Dependency Resolution

## Problem Statement

The current dependency resolver only looks for Maven dependencies as subdirectories of the analyzed project. However, in real-world scenarios, dependencies exist as **sibling directories** in a shared workspace.

### Current Behavior (WRONG)
```
Analyzing: /playground/java/cuco-ui-admin
Looks for: /playground/java/cuco-ui-admin/administration.ui  ❌
```

### Expected Behavior (CORRECT)
```
Analyzing: /playground/java/cuco-ui-admin
Looks for: /playground/java/administration.ui  ✅ (sibling directory)
```

## Architecture Overview

### Current Structure
```
/playground/java/
├── cuco-ui-admin/           ← Main project (analyzing)
│   ├── pom.xml              (depends on: administration.ui, cuco-cct-core, ...)
│   ├── src/main/java/...
│   └── ...
├── administration.ui/        ← Dependency (sibling)
│   ├── pom.xml
│   └── src/main/java/...
├── cuco-cct-core/           ← Dependency (sibling)
│   ├── pom.xml
│   └── src/main/java/...
├── cuco-ui-common/          ← Dependency (sibling)
└── ...
```

## Phase 1: Path Resolver Enhancement

### 1.1 Current Implementation Issues

**File**: `src/codeindex/utils/path_resolver.py`

Current logic:
1. Takes `base_dir` (project directory)
2. Looks for `base_dir/artifactId/`
3. Only searches subdirectories (monorepo pattern)

**Problems:**
- Doesn't search parent directory for siblings
- Doesn't search parent's parent (multi-level workspaces)
- No fallback search strategy

### 1.2 New Search Strategy

**Search Order** (stop at first match):
1. **Subdirectory search** (current monorepo pattern)
   - `{base_dir}/{artifactId}/`
   - Example: `/playground/java/cuco-ui-admin/administration.ui/`

2. **Sibling directory search** (NEW - workspace pattern)
   - `{base_dir}/../{artifactId}/`
   - Example: `/playground/java/administration.ui/`

3. **Workspace root search** (NEW - multi-level pattern)
   - Search up to 3 levels for common workspace root
   - Look for sibling directories at each level
   - Example: `/playground/java/{artifactId}/`

4. **Maven local repository** (FUTURE - optional)
   - `~/.m2/repository/{groupId}/{artifactId}/{version}/`
   - Only if source code needed (not just compiled JARs)

### 1.3 Implementation Plan

**New Function**: `resolve_artifact_path_with_siblings()`

```python
def resolve_artifact_path_with_siblings(
    base_dir: Path,
    artifact_id: str,
    group_id: str,
    search_levels: int = 3
) -> Optional[Path]:
    """
    Resolve artifact path with multi-level sibling search.

    Args:
        base_dir: Starting directory (project being analyzed)
        artifact_id: Maven artifact ID
        group_id: Maven group ID
        search_levels: How many parent levels to search (default: 3)

    Returns:
        Path to artifact directory, or None if not found

    Search Strategy:
        1. Check subdirectory: base_dir/artifact_id/
        2. Check sibling: base_dir/../artifact_id/
        3. Check parent siblings: base_dir/../../artifact_id/
        4. Continue up to search_levels
    """
```

**Validation**:
- Check if directory exists
- Check if pom.xml exists in directory
- Verify groupId/artifactId match in pom.xml

## Phase 2: Dependency Resolver Enhancement

### 2.1 Current Implementation Issues

**File**: `src/codeindex/services/dependency_resolver.py`

Current behavior:
- Uses path_resolver to find dependencies
- Only resolves if path exists
- Marks as "not found" if not in subdirectory

**Problems:**
- Doesn't retry with different search strategies
- No caching of resolved paths
- No workspace root detection

### 2.2 New Features

**2.2.1 Workspace Root Detection**

Detect the workspace root by looking for:
- Multiple pom.xml files at the same level
- `.m2/` directory
- `.mvn/` directory
- Common parent with multiple Maven projects

**2.2.2 Dependency Graph Enhancement**

Store additional metadata:
- Dependency resolution strategy used (subdirectory/sibling/workspace)
- Full path to dependency source
- Whether dependency is local or external
- Dependency chain (transitive dependencies)

**2.2.3 Caching**

Cache resolved paths to avoid repeated filesystem searches:
```python
_artifact_path_cache: Dict[str, Path] = {}
```

## Phase 3: Discovery Service Integration

### 3.1 Changes Required

**File**: `src/codeindex/services/discovery.py`

**Add workspace detection**:
```python
def detect_workspace_root(project_dir: Path) -> Path:
    """
    Detect the workspace root directory containing multiple projects.

    Strategy:
    1. Look for parent directories with multiple pom.xml files
    2. Check for .mvn/ or .m2/ directories
    3. Default to parent if multiple Maven projects found
    """
```

**Update discovery to pass workspace root**:
```python
workspace_root = detect_workspace_root(source_dir)
dependencies = resolve_dependencies(
    project,
    depth=dependency_depth,
    workspace_root=workspace_root  # NEW parameter
)
```

## Phase 4: CLI Enhancement

### 4.1 New CLI Parameters

**Add to discover command**:
```bash
codeindex discover \
  --source-dir /playground/java/cuco-ui-admin \
  --workspace-root /playground/java \        # NEW: explicit workspace root
  --dependency-depth 1 \
  --search-siblings                          # NEW: enable sibling search
```

**Default behavior**:
- If `--workspace-root` not provided: auto-detect (go up 1 level)
- If `--search-siblings` not provided: default to True
- Backwards compatible: existing behavior still works for monorepos

### 4.2 Configuration Options

**Add to config.py**:
```python
# Dependency resolution configuration
DEPENDENCY_SEARCH_SIBLINGS = True          # Search sibling directories
DEPENDENCY_SEARCH_LEVELS = 3               # How many parent levels to search
DEPENDENCY_WORKSPACE_ROOT = None           # Explicit workspace root (optional)
DEPENDENCY_REQUIRE_POM_VALIDATION = True   # Validate pom.xml in resolved paths
```

## Phase 5: Testing Strategy

### 5.1 Test Scenarios

**Test Case 1: Sibling Dependencies**
```
workspace/
├── project-a/  (depends on project-b, project-c)
├── project-b/
└── project-c/
```
Expected: Resolve project-b and project-c from workspace/

**Test Case 2: Multi-Level Workspace**
```
root/
├── backend/
│   ├── api/  (depends on backend/common)
│   └── common/
└── shared/
    └── models/  (depends on nothing)
```
Expected: Resolve backend/common from root/backend/

**Test Case 3: Mixed Dependencies**
```
workspace/
├── main-app/  (depends on local-lib, external-lib)
├── local-lib/  (found as sibling)
└── external-lib NOT PRESENT (should be marked as not found)
```
Expected: Resolve local-lib, mark external-lib as not found

**Test Case 4: Backwards Compatibility**
```
monorepo/
├── pom.xml (parent)
├── module-a/
└── module-b/  (depends on module-a)
```
Expected: Resolve module-a as subdirectory (existing behavior)

### 5.2 Test Files

Create test fixtures:
```
tests/fixtures/workspaces/
├── sibling-deps/
│   ├── main/
│   ├── dep1/
│   └── dep2/
├── multi-level/
│   └── ...
└── mixed/
    └── ...
```

### 5.3 Integration Tests

**New test file**: `tests/integration/test_sibling_dependency_resolution.py`

Test scenarios:
- Sibling discovery
- Multi-level search
- Workspace root detection
- Path caching
- Error handling (circular deps, missing deps)

## Phase 6: Documentation Updates

### 6.1 CLAUDE.md Updates

Add section: "Multi-Directory Dependency Resolution"

Document:
- Workspace patterns (sibling, multi-level)
- How search works
- Configuration options
- Examples for different project structures

### 6.2 run-cuco.sh Updates

Update script to:
```bash
# Detect workspace root
WORKSPACE_ROOT=$(dirname "$SOURCE_DIR")

# Run discovery with workspace root
codeindex discover \
  --source-dir "$SOURCE_DIR" \
  --workspace-root "$WORKSPACE_ROOT" \
  --dependency-depth 1 \
  --search-siblings
```

### 6.3 CUCO-QUICKSTART.md Updates

Add section: "Multi-Project Workspace Setup"

Document:
- Directory structure requirements
- How dependencies are resolved
- Troubleshooting missing dependencies
- Performance implications

## Phase 7: Performance Considerations

### 7.1 Optimization Strategies

**Caching**:
- Cache resolved artifact paths
- Cache workspace root detection
- Cache pom.xml parsing results

**Parallel Search**:
- Search multiple parent levels in parallel
- Use concurrent filesystem operations

**Early Termination**:
- Stop search once artifact found
- Skip unnecessary pom.xml validation if path confirmed

### 7.2 Performance Targets

- Sibling search overhead: < 5ms per dependency
- Workspace root detection: < 10ms per project
- Total dependency resolution: < 500ms for 20 dependencies

## Phase 8: Migration Path

### 8.1 Backwards Compatibility

**Ensure existing behavior works**:
- Monorepo projects (subdirectory dependencies)
- Single projects (no dependencies)
- Projects with --dependency-depth 0

**Configuration flags**:
```python
# Disable sibling search for backwards compatibility
export DEPENDENCY_SEARCH_SIBLINGS=false
```

### 8.2 Deprecation Warnings

No deprecations needed - this is purely additive functionality.

### 8.3 Feature Flags

```python
# Enable/disable new features independently
FEATURE_SIBLING_SEARCH = True       # Search sibling directories
FEATURE_WORKSPACE_DETECTION = True  # Auto-detect workspace root
FEATURE_MULTI_LEVEL_SEARCH = True   # Search multiple parent levels
```

## Implementation Order

### Priority 1: Core Functionality
1. ✅ Phase 1: Path resolver enhancement (sibling search)
2. ✅ Phase 2: Dependency resolver integration
3. ✅ Phase 3: Discovery service updates

### Priority 2: Testing & Validation
4. ✅ Phase 5: Test scenarios and fixtures
5. ✅ Phase 5: Integration tests

### Priority 3: User Experience
6. ✅ Phase 4: CLI enhancements
7. ✅ Phase 6: Documentation updates
8. ✅ Phase 8: Migration & backwards compatibility

### Priority 4: Optimization
9. ⏳ Phase 7: Performance optimizations (can be done later)

## Success Criteria

### Functional Requirements
- ✅ Resolve dependencies in sibling directories
- ✅ Auto-detect workspace root
- ✅ Maintain backwards compatibility with monorepo pattern
- ✅ Clear error messages for missing dependencies
- ✅ Support multi-level directory structures (up to 3 levels)

### Non-Functional Requirements
- ✅ Performance: < 500ms for 20 dependencies
- ✅ Test coverage: > 80% for new code
- ✅ Documentation: Complete examples and troubleshooting
- ✅ User experience: Works without manual configuration

### Acceptance Tests
1. Run pipeline on cuco-ui-admin with sibling dependencies
2. Verify all local dependencies are resolved (no warnings)
3. Verify dependency information indexed in Weaviate
4. Verify search can find code across dependencies
5. Verify existing monorepo projects still work

## Risk Assessment

### High Risk
- **Breaking existing behavior**: Mitigated by feature flags and testing
- **Performance degradation**: Mitigated by caching and early termination

### Medium Risk
- **Complex directory structures**: May need additional search strategies
- **Circular dependencies**: Already handled by existing code

### Low Risk
- **Documentation gaps**: Can be addressed incrementally
- **Edge cases**: Can be discovered through testing

## Next Steps

1. Review and approve this plan
2. Create feature branch: `005-multi-directory-dependencies`
3. Implement Phase 1 (path resolver)
4. Write tests for Phase 1
5. Iterate through remaining phases
6. Final testing with real cuco-ui-admin project
7. Merge to main

## Questions for Clarification

1. **Directory depth**: Is 3 levels sufficient, or should it be configurable?
2. **Maven repository**: Should we also search ~/.m2/repository/?
3. **Validation**: Should we strictly validate groupId/artifactId in pom.xml?
4. **Performance**: Is 500ms target acceptable for 20 dependencies?
5. **Caching**: Should cache persist across runs (file cache)?

---

**Status**: 📋 PLANNING - Ready for review and implementation
**Estimated effort**: 8-12 hours of development + testing
**Target release**: Feature 005
