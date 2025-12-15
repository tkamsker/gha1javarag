# Research: Maven Dependency Resolution and DTO Analysis

**Feature**: 004-maven-dependency-resolution
**Created**: 2025-12-15
**Status**: Complete

## Purpose

This document captures technical research and decisions for implementing Maven dependency resolution and DTO pattern recognition in the Java Codebase Indexer pipeline.

## Research Areas

### 1. XML Parsing for pom.xml

**Decision**: Use Python's built-in `xml.etree.ElementTree` for pom.xml parsing

**Rationale**:
- Standard library (no additional dependencies)
- Sufficient for simple XML navigation (groupId, artifactId, dependencies)
- Better security model than lxml (doesn't support external entities by default)
- Consistent with constitution principle: minimize external dependencies
- Performance adequate for typical pom.xml files (<100KB, <50 dependencies)

**Alternatives Considered**:
- **lxml**: More feature-rich, better XPath support, faster for large XML
  - Rejected: External dependency, overkill for simple dependency extraction
  - Note: Can revisit if complex Maven profiles or parent POM resolution needed
- **xml.dom.minidom**: DOM-based parsing
  - Rejected: More verbose API, higher memory usage for large files
- **BeautifulSoup with lxml backend**: HTML/XML parsing
  - Rejected: Heavy dependency for simple XML parsing

**Implementation Notes**:
- Use `xml.etree.ElementTree.parse()` for file-based parsing
- Use `xml.etree.ElementTree.fromstring()` for testing with string fixtures
- Namespace handling: Maven POM uses `http://maven.apache.org/POM/4.0.0` - use `{namespace}dependency` or `.//dependency` for simple queries
- Error handling: Catch `xml.etree.ElementTree.ParseError` for malformed XML

### 2. DTO Classification Algorithm

**Decision**: Multi-phase classification with naming patterns, structural analysis, and package location heuristics

**Rationale**:
- No single signal definitively identifies DTOs (unlike @Entity for JPA entities)
- Naming patterns (*DTO, *Request, *Response) cover ~80% of DTOs in enterprise Java
- Structural analysis (field-heavy, minimal logic) catches remaining ~20%
- Package location (.dto., .shared., .model.) provides additional context
- Prioritize precision over recall (avoid false positives)

**Algorithm**:
```
Phase 1: Naming Pattern Match (HIGH confidence)
  - Match: *DTO.java, *Request.java, *Response.java, *Command.java, *Query.java, *Event.java
  - If match → DTO (confidence: 95%)

Phase 2: Entity Exclusion (BLOCKER)
  - Check for JPA annotations: @Entity, @Table, @Document, @Embeddable
  - If present → NOT DTO (entity takes precedence)

Phase 3: Structural Analysis (MEDIUM confidence)
  - Count: private fields vs methods (exclude getters/setters/toString/equals/hashCode)
  - Ratio: fields / business_logic_methods > 3.0 → likely DTO
  - Presence of Serializable or IsSerializable → +10 confidence points
  - Located in .dto., .shared., .model., .transfer. packages → +15 confidence points

Phase 4: Threshold Decision
  - Confidence >= 70% → DTO
  - Confidence < 70% → POJO (default classification)
```

**Alternatives Considered**:
- **AST-only classification**: Parse Java AST and count field vs method ratios
  - Rejected: Misses naming context, lower accuracy without package info
- **Machine learning classifier**: Train on labeled DTO dataset
  - Rejected: Requires training data, maintenance burden, overkill for rule-based problem
- **Annotation-based only**: Require @Dto or similar annotation
  - Rejected: Most enterprise codebases don't use explicit DTO annotations

**Test Cases**:
- Standard DTO (UserDTO.java) → DTO
- Request/Response (LoginRequest.java, UserResponse.java) → DTO
- Entity with DTO name (UserDTO.java with @Entity) → Entity (not DTO)
- POJO in .shared package with Serializable → DTO
- Service class (UserService.java) → Not DTO
- Nested DTO (UserDTO with AddressDTO field) → Both classified as DTO

### 3. Circular Dependency Detection

**Decision**: Visited set tracking with path reconstruction for error messages

**Rationale**:
- Maven dependency graphs can have cycles (project A → B → A)
- Must detect cycles to prevent infinite resolution loops
- Constitution requires clear error messages with actionable guidance

**Algorithm**:
```python
def resolve_dependencies(artifact_id: str, visited: Set[str], path: List[str]) -> DependencyGraph:
    if artifact_id in visited:
        cycle_path = path + [artifact_id]
        log.warning(f"Circular dependency detected: {' → '.join(cycle_path)}")
        return None  # Stop recursion

    visited.add(artifact_id)
    path.append(artifact_id)

    # Resolve current artifact
    pom_path = resolve_pom(artifact_id)
    dependencies = parse_pom(pom_path)

    # Recursively resolve children (up to depth limit)
    for dep in dependencies:
        resolve_dependencies(dep.artifact_id, visited.copy(), path.copy())

    return dependency_graph
```

**Alternatives Considered**:
- **Topological sort**: Build full graph, then detect cycles via topological sort
  - Rejected: Requires loading full graph into memory, overkill for streaming resolution
- **DFS with colors**: White/gray/black node marking
  - Rejected: More complex, same result as visited set approach
- **Allow cycles**: Don't detect, rely on depth limit
  - Rejected: Confusing behavior, violates SC-005 (zero false positives)

**Error Message Format**:
```
WARNING: Circular dependency detected in project 'cuco-ui-admin'
  Path: cuco-core → cuco-utils → cuco-common → cuco-core
  Resolution: Dependency resolution stopped at 'cuco-common' to prevent infinite loop.
  Impact: Files in 'cuco-core' (second occurrence) will not be analyzed via this path.
  Recommendation: Review pom.xml files to break the circular dependency.
```

### 4. Weaviate Schema Design for DtoArtifact

**Decision**: Dedicated `DtoArtifact` class with nested object structure for fields and validation rules

**Schema**:
```python
{
    "class": "DtoArtifact",
    "description": "Data Transfer Object extracted from Java codebase",
    "properties": [
        {"name": "artifact_id", "dataType": ["text"], "description": "Canonical ID (project:path:classname)"},
        {"name": "class_name", "dataType": ["text"], "description": "Simple class name (e.g., UserDTO)"},
        {"name": "package_name", "dataType": ["text"], "description": "Fully qualified package"},
        {"name": "source_path", "dataType": ["text"], "description": "Relative file path"},
        {"name": "project", "dataType": ["text"], "description": "Project name for filtering"},

        # DTO-specific fields
        {"name": "fields", "dataType": ["object[]"], "description": "Field definitions with name, type, modifiers"},
        {"name": "validation_rules", "dataType": ["object[]"], "description": "JSR-303 annotations per field"},
        {"name": "serialization_markers", "dataType": ["text[]"], "description": "Serializable, IsSerializable, @Serializable"},
        {"name": "nested_dtos", "dataType": ["text[]"], "description": "Field types that are also DTOs"},
        {"name": "is_shared", "dataType": ["boolean"], "description": "Located in .shared package (GWT)"},
        {"name": "inner_classes", "dataType": ["text[]"], "description": "Nested inner class DTOs"},

        # Standard fields
        {"name": "language", "dataType": ["text"], "description": "Always 'java'"},
        {"name": "framework", "dataType": ["text"], "description": "GWT, Spring, JAX-RS if detected"},
        {"name": "content_summary", "dataType": ["text"], "description": "AI-generated summary of DTO purpose"},
    ],
    "vectorizer": "text2vec-transformers",  # Use Ollama embeddings
    "moduleConfig": {
        "text2vec-transformers": {
            "vectorizeClassName": False,
            "vectorizePropertyName": False,
        }
    }
}
```

**Rationale**:
- Separate class from generic `CodeArtifact` for specialized DTO queries
- `fields` as object array allows structured field metadata (name, type, annotations)
- `validation_rules` captures JSR-303 constraints for API documentation generation
- `is_shared` flag supports GWT frontend-backend shared DTO identification
- Consistent with existing artifact schema patterns (project, source_path, artifact_id)

**Alternatives Considered**:
- **Extend CodeArtifact**: Add DTO-specific properties to existing class
  - Rejected: Violates single responsibility, makes schema overly generic
- **Flatten fields**: Store fields as JSON text
  - Rejected: Loses structured queryability in Weaviate
- **Reference entity**: Store DTOs in separate collection, link to CodeArtifact
  - Rejected: Increases query complexity, Weaviate doesn't support strong foreign keys

### 5. JSR-303 Validation Annotation Extraction

**Decision**: Regex-based annotation extraction from Java source text

**Rationale**:
- JSR-303 annotations have consistent syntax: `@NotNull`, `@Size(min=1, max=100)`, `@Pattern(regexp="...")`
- Regex parsing sufficient for common cases (simpler than full Java AST parsing)
- Existing java_parser.py uses basic AST from Ollama - extend for annotation extraction
- Focus on common annotations: @NotNull, @NotEmpty, @NotBlank, @Size, @Min, @Max, @Pattern, @Email, @Valid

**Implementation**:
```python
import re
from typing import List, Dict

VALIDATION_ANNOTATIONS = [
    "NotNull", "NotEmpty", "NotBlank",
    "Size", "Min", "Max", "DecimalMin", "DecimalMax",
    "Pattern", "Email", "Past", "Future", "Valid"
]

def extract_validation_annotations(java_source: str, field_name: str) -> List[Dict[str, any]]:
    """Extract JSR-303 validation annotations for a specific field."""
    annotations = []

    # Pattern: @AnnotationName OR @AnnotationName(params)
    pattern = r'@(' + '|'.join(VALIDATION_ANNOTATIONS) + r')(?:\(([^)]+)\))?'

    # Find field declaration
    field_pattern = rf'(\s+@[\w.]+(?:\([^)]+\))?\s+)*\s*private\s+\w+\s+{field_name}\s*[;=]'
    field_match = re.search(field_pattern, java_source, re.MULTILINE | re.DOTALL)

    if field_match:
        field_text = field_match.group(0)
        for match in re.finditer(pattern, field_text):
            annotation_name = match.group(1)
            annotation_params = match.group(2) if match.group(2) else None
            annotations.append({
                "name": annotation_name,
                "parameters": parse_annotation_params(annotation_params)
            })

    return annotations

def parse_annotation_params(params_str: str) -> Dict[str, str]:
    """Parse annotation parameters like 'min=1, max=100' into dict."""
    if not params_str:
        return {}

    params = {}
    for param in params_str.split(','):
        if '=' in param:
            key, value = param.split('=', 1)
            params[key.strip()] = value.strip().strip('"')
    return params
```

**Alternatives Considered**:
- **Full Java AST parser (JavaParser, Eclipse JDT)**: Parse complete Java AST
  - Rejected: Heavy external dependency (Java tooling), requires JVM, complexity
- **ANTLR Java grammar**: Parse Java with ANTLR Python runtime
  - Rejected: Large dependency, overkill for annotation extraction
- **Ollama semantic extraction**: Ask Ollama to extract validation rules
  - Rejected: Already used for class-level extraction, regex faster for structured data

**Edge Cases**:
- Multi-line annotations: Handle with `re.DOTALL` flag
- Annotation inheritance: Only extract field-level annotations (not class-level)
- Custom validation annotations: Skip unless explicitly configured

### 6. Path Resolution Strategy

**Decision**: JAVA_SOURCE_DIR + project (optional) + artifactId for dependency resolution

**Algorithm**:
```python
def resolve_artifact_path(artifact_id: str, base_dir: Path, project: Optional[str]) -> Optional[Path]:
    """
    Resolve Maven artifact to directory path.

    Resolution order:
    1. If project specified: base_dir / project / artifact_id
    2. Otherwise: base_dir / artifact_id

    Returns None if directory doesn't exist (logged as warning).
    """
    if project:
        effective_base = base_dir / project
    else:
        effective_base = base_dir

    artifact_path = effective_base / artifact_id

    if artifact_path.exists() and artifact_path.is_dir():
        return artifact_path
    else:
        log.warning(f"Artifact directory not found: {artifact_path}")
        log.warning(f"  groupId: {group_id}, artifactId: {artifact_id}")
        log.warning(f"  Expected at: {artifact_path}")
        log.warning(f"  Searched from base: {effective_base}")
        return None
```

**Rationale**:
- Simple, predictable path resolution (no complex Maven conventions)
- Matches user's example: `cuco-cct-core` artifactId → `JAVA_SOURCE_DIR/cuco-cct-core/`
- Project parameter enables monorepo support without changing base directory
- Clear error messages when artifacts not found (Constitution: User Experience Consistency)

**Alternatives Considered**:
- **groupId + artifactId**: Map `at.a1ta.cuco:cuco-cct-core` → `at/a1ta/cuco/cuco-cct-core/`
  - Rejected: User example shows artifactId-only mapping
  - Note: Standard Maven repository layout, but not used for source trees
- **Maven settings.xml lookup**: Parse Maven settings for local repository
  - Rejected: Out of scope (no Maven integration per spec)
- **Symbolic link following**: Resolve symlinks to actual artifact locations
  - Rejected: Adds complexity, most enterprise projects use direct directories

**Edge Cases**:
- Artifact not found: Log warning with full expected path, continue processing other dependencies
- Multiple matches: If globbing needed, use first match and log warning
- Relative vs absolute project paths: Support both, normalize to absolute internally

## Summary

All technical decisions documented above resolve implementation details needed for Phase 1 design. Key technologies selected:
- **XML Parsing**: xml.etree.ElementTree (stdlib)
- **DTO Classification**: Multi-phase naming + structural + package heuristics
- **Circular Dependencies**: Visited set tracking with path reconstruction
- **Weaviate Schema**: Dedicated DtoArtifact class with nested field objects
- **Validation Extraction**: Regex-based annotation parsing
- **Path Resolution**: JAVA_SOURCE_DIR + project + artifactId (simple concatenation)

No external research or user clarification required. All decisions align with constitution principles (minimize dependencies, clear error handling, performance-conscious).

**Next Phase**: Proceed to Phase 1 - Generate data-model.md, contracts/, and quickstart.md based on research findings.
