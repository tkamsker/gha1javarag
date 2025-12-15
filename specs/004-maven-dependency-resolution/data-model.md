# Data Model: Maven Dependency Resolution and DTO Analysis

**Feature**: 004-maven-dependency-resolution
**Created**: 2025-12-15
**Source**: Extracted from [spec.md](./spec.md) Key Entities section

## Overview

This document defines the data models for Maven dependency resolution and DTO pattern recognition. Models are implemented as Python dataclasses with type hints and validation rules.

## Core Models

### 1. MavenDependency

Represents a single Maven dependency declaration extracted from pom.xml.

**Fields**:
```python
@dataclass
class MavenDependency:
    """Maven dependency from pom.xml."""

    # Required fields (from pom.xml)
    group_id: str                    # e.g., "at.a1ta.cuco"
    artifact_id: str                 # e.g., "cuco-cct-core"

    # Optional fields (may be absent in pom.xml)
    version: Optional[str] = None    # e.g., "1.0.0", can be property reference
    scope: str = "compile"           # compile, test, provided, runtime, system

    # Resolution fields (computed during discovery)
    resolved_path: Optional[Path] = None  # Absolute path to artifact directory
    resolution_status: str = "pending"    # pending, resolved, not_found, circular

    # Metadata
    declared_in: Optional[Path] = None    # Path to pom.xml where declared
    depth: int = 0                        # Dependency depth (0=direct, 1=transitive)
```

**Validation Rules**:
- `group_id` and `artifact_id` are required (non-empty strings)
- `scope` must be one of: compile, test, provided, runtime, system
- `resolution_status` must be one of: pending, resolved, not_found, circular
- `depth` must be >= 0

**State Transitions**:
```
pending → resolved      (artifact directory found)
pending → not_found     (artifact directory not in JAVA_SOURCE_DIR)
pending → circular      (circular dependency detected during resolution)
```

**Usage**:
```python
dep = MavenDependency(
    group_id="at.a1ta.cuco",
    artifact_id="cuco-cct-core",
    version="1.0.0",
    scope="compile",
    declared_in=Path("/workspace/cuco-ui-admin/pom.xml"),
    depth=0
)

# After resolution
dep.resolved_path = Path("/workspace/cuco-cct-core")
dep.resolution_status = "resolved"
```

---

### 2. DtoArtifact

Represents a Data Transfer Object extracted from Java source code.

**Fields**:
```python
@dataclass
class DtoField:
    """Individual field within a DTO."""
    name: str                              # e.g., "userId"
    field_type: str                        # e.g., "String", "Long", "List<AddressDTO>"
    modifiers: List[str]                   # e.g., ["private", "final"]
    validation_annotations: List[Dict[str, any]]  # JSR-303 annotations
    is_nested_dto: bool = False            # True if field_type is another DTO

@dataclass
class DtoArtifact:
    """Data Transfer Object artifact."""

    # Identification (required)
    artifact_id: str                       # Canonical ID: project:path:classname
    class_name: str                        # Simple name, e.g., "UserDTO"
    package_name: str                      # Fully qualified, e.g., "com.example.dto"
    source_path: Path                      # Relative to JAVA_SOURCE_DIR
    project: str                           # Project name for filtering

    # DTO structure (required)
    fields: List[DtoField]                 # Field definitions with types and annotations

    # Classification metadata
    classification_confidence: int = 0     # 0-100 confidence score
    classification_signals: List[str] = field(default_factory=list)  # Reasons for classification

    # Validation & serialization (optional)
    validation_rules: Dict[str, List[Dict[str, any]]] = field(default_factory=dict)  # field_name → annotations
    serialization_markers: List[str] = field(default_factory=list)  # ["Serializable", "IsSerializable"]

    # Relationships (optional)
    nested_dtos: List[str] = field(default_factory=list)  # Class names of nested DTOs
    inner_classes: List[str] = field(default_factory=list)  # Inner class names
    is_shared: bool = False                # True if in .shared package (GWT)

    # Standard fields
    language: str = "java"
    framework: Optional[str] = None        # "GWT", "Spring", "JAX-RS" if detected
    content_summary: Optional[str] = None  # AI-generated summary
```

**Validation Rules**:
- `artifact_id` must follow pattern: `{project}:{path}:{class_name}`
- `class_name` must be valid Java identifier
- `package_name` must be valid Java package name
- `classification_confidence` must be 0-100
- `fields` must not be empty for valid DTO (at least 1 field)

**Classification Signals** (recorded in `classification_signals`):
- `"naming_pattern_match:*DTO"` - Class name matches *DTO.java
- `"naming_pattern_match:*Request"` - Class name matches *Request.java
- `"structural_analysis:field_ratio=5.0"` - High field-to-method ratio
- `"serialization_marker:Serializable"` - Implements Serializable
- `"package_location:.dto."` - Located in .dto. package
- `"no_entity_annotations"` - No @Entity annotation found

**Usage**:
```python
dto = DtoArtifact(
    artifact_id="cuco-ui-admin:com/example/dto/UserDTO.java:UserDTO",
    class_name="UserDTO",
    package_name="com.example.dto",
    source_path=Path("com/example/dto/UserDTO.java"),
    project="cuco-ui-admin",
    fields=[
        DtoField(
            name="userId",
            field_type="Long",
            modifiers=["private"],
            validation_annotations=[
                {"name": "NotNull", "parameters": {}},
                {"name": "Min", "parameters": {"value": "1"}}
            ]
        ),
        DtoField(
            name="email",
            field_type="String",
            modifiers=["private"],
            validation_annotations=[
                {"name": "Email", "parameters": {}},
                {"name": "NotBlank", "parameters": {}}
            ]
        )
    ],
    classification_confidence=95,
    classification_signals=[
        "naming_pattern_match:*DTO",
        "package_location:.dto.",
        "serialization_marker:Serializable"
    ],
    serialization_markers=["Serializable"],
    is_shared=False
)
```

---

### 3. DependencyGraph

Represents the resolved dependency tree for a project.

**Fields**:
```python
@dataclass
class DependencyNode:
    """Node in the dependency graph."""
    dependency: MavenDependency          # The dependency itself
    children: List['DependencyNode']     # Direct dependencies of this artifact
    parent: Optional['DependencyNode']   # Parent node (None for root)

@dataclass
class DependencyGraph:
    """Complete dependency resolution graph for a project."""

    # Root project
    project_name: str                    # e.g., "cuco-ui-admin"
    root_pom: Path                       # Path to root pom.xml
    root_node: DependencyNode            # Root of dependency tree

    # Resolution metadata
    total_dependencies: int = 0          # Total number of dependencies discovered
    resolved_count: int = 0              # Successfully resolved dependencies
    not_found_count: int = 0             # Dependencies not found in JAVA_SOURCE_DIR
    circular_count: int = 0              # Circular dependencies detected
    max_depth: int = 0                   # Maximum dependency depth in tree

    # Resolution history
    resolution_errors: List[str] = field(default_factory=list)  # Error messages
    circular_paths: List[List[str]] = field(default_factory=list)  # Detected cycles

    # Timing
    resolution_start: Optional[datetime] = None
    resolution_end: Optional[datetime] = None
```

**Validation Rules**:
- `root_node` must have depth=0
- `total_dependencies` = `resolved_count + not_found_count + circular_count`
- `max_depth` must be >= 0

**Graph Operations**:
```python
def get_all_dependencies(graph: DependencyGraph) -> List[MavenDependency]:
    """Flatten dependency tree to list."""
    pass

def find_dependency(graph: DependencyGraph, artifact_id: str) -> Optional[DependencyNode]:
    """Find node by artifact_id."""
    pass

def get_dependencies_at_depth(graph: DependencyGraph, depth: int) -> List[MavenDependency]:
    """Get all dependencies at specific depth level."""
    pass
```

**Usage**:
```python
graph = DependencyGraph(
    project_name="cuco-ui-admin",
    root_pom=Path("/workspace/cuco-ui-admin/pom.xml"),
    root_node=DependencyNode(
        dependency=MavenDependency(
            group_id="at.a1ta.cuco",
            artifact_id="cuco-ui-admin",
            depth=0
        ),
        children=[...],
        parent=None
    ),
    total_dependencies=15,
    resolved_count=14,
    not_found_count=1,
    circular_count=0,
    max_depth=2
)
```

---

### 4. ProjectConfiguration

Represents configuration for dependency resolution and discovery.

**Fields**:
```python
@dataclass
class ProjectConfiguration:
    """Configuration for Maven dependency resolution and discovery."""

    # Base paths (required)
    java_source_dir: Path                # From JAVA_SOURCE_DIR env var
    project_subdirectory: Optional[str] = None  # From --project parameter

    # Computed paths
    effective_base_dir: Path = field(init=False)  # java_source_dir / project_subdirectory

    # Dependency resolution settings
    dependency_depth: int = 1            # Max depth for transitive dependencies
    resolve_transitive: bool = True      # Resolve beyond direct dependencies

    # Error handling
    continue_on_error: bool = True       # Continue if dependency not found
    log_level: str = "INFO"              # Logging verbosity

    # Output paths
    output_dir: Path = Path("./output")  # For discovery/extraction results

    def __post_init__(self):
        """Compute effective base directory after initialization."""
        if self.project_subdirectory:
            self.effective_base_dir = self.java_source_dir / self.project_subdirectory
        else:
            self.effective_base_dir = self.java_source_dir

        # Validate paths exist
        if not self.java_source_dir.exists():
            raise ValueError(f"JAVA_SOURCE_DIR does not exist: {self.java_source_dir}")

        if self.project_subdirectory and not self.effective_base_dir.exists():
            raise ValueError(f"Project directory does not exist: {self.effective_base_dir}")
```

**Validation Rules**:
- `java_source_dir` must exist and be a directory
- `effective_base_dir` must exist and be a directory (if project_subdirectory specified)
- `dependency_depth` must be >= 0
- `log_level` must be one of: DEBUG, INFO, WARNING, ERROR

**Usage**:
```python
config = ProjectConfiguration(
    java_source_dir=Path("/workspace"),
    project_subdirectory="cuco-ui-admin",
    dependency_depth=2,
    output_dir=Path("./output")
)

# effective_base_dir is computed automatically
assert config.effective_base_dir == Path("/workspace/cuco-ui-admin")
```

---

## Relationships

```
ProjectConfiguration
  ↓ (configures)
DependencyGraph
  ↓ (contains)
DependencyNode
  ↓ (wraps)
MavenDependency
  ↓ (resolved to directory containing)
DtoArtifact (many)
```

**Workflow**:
1. Load `ProjectConfiguration` from CLI args and environment
2. Parse root pom.xml to extract `MavenDependency` list
3. Resolve each dependency to build `DependencyGraph`
4. Discover Java files in resolved dependency directories
5. Classify discovered files, creating `DtoArtifact` for DTOs
6. Index `DtoArtifact` instances in Weaviate

## Persistence

### Weaviate Schema

**DtoArtifact** is persisted in Weaviate with the following schema:

```python
{
    "class": "DtoArtifact",
    "description": "Data Transfer Object extracted from Java codebase",
    "properties": [
        {"name": "artifact_id", "dataType": ["text"]},
        {"name": "class_name", "dataType": ["text"]},
        {"name": "package_name", "dataType": ["text"]},
        {"name": "source_path", "dataType": ["text"]},
        {"name": "project", "dataType": ["text"]},
        {"name": "fields", "dataType": ["object[]"]},  # Array of DtoField objects
        {"name": "validation_rules", "dataType": ["object"]},  # Dict field_name → annotations
        {"name": "serialization_markers", "dataType": ["text[]"]},
        {"name": "nested_dtos", "dataType": ["text[]"]},
        {"name": "is_shared", "dataType": ["boolean"]},
        {"name": "inner_classes", "dataType": ["text[]"]},
        {"name": "language", "dataType": ["text"]},
        {"name": "framework", "dataType": ["text"]},
        {"name": "content_summary", "dataType": ["text"]},
    ],
    "vectorizer": "text2vec-transformers",
    "moduleConfig": {
        "text2vec-transformers": {
            "vectorizeClassName": False,
            "vectorizePropertyName": False,
            "properties": {
                "content_summary": {"vectorizePropertyName": True}
            }
        }
    }
}
```

**MavenDependency** is NOT persisted directly in Weaviate (transient resolution metadata).

**DependencyGraph** is NOT persisted directly in Weaviate (can be reconstructed from pom.xml).

### JSONL Output

Intermediate results are stored in JSONL format:

**discovery-inventory.jsonl**:
```json
{"path": "com/example/dto/UserDTO.java", "type": "java", "project": "cuco-ui-admin", "dependency": "cuco-cct-core"}
```

**extraction-results.jsonl**:
```json
{
  "artifact_id": "cuco-ui-admin:com/example/dto/UserDTO.java:UserDTO",
  "artifact_type": "dto",
  "class_name": "UserDTO",
  "fields": [{"name": "userId", "type": "Long", "annotations": [{"name": "NotNull"}]}],
  "serialization_markers": ["Serializable"]
}
```

## Testing Strategy

### Unit Tests

- **MavenDependency**: Validation, state transitions, equality
- **DtoArtifact**: Field validation, classification confidence calculation
- **DependencyGraph**: Tree traversal, circular detection, depth calculation
- **ProjectConfiguration**: Path resolution, validation errors

### Integration Tests

- End-to-end dependency resolution with test fixtures
- Weaviate schema creation and DTO indexing
- JSONL serialization and deserialization

### Test Fixtures

Located in `tests/fixtures/`:
- `pom-files/simple.xml` - Single dependency
- `pom-files/multi-module.xml` - Multiple dependencies
- `pom-files/circular-deps.xml` - Circular dependency
- `dto-classes/standard-dto.java` - Standard DTO with JSR-303
- `dto-classes/nested-dto.java` - DTO with nested DTO fields
- `dto-classes/entity-vs-dto.java` - Entity with @Entity annotation

## Implementation Notes

- All models use Python `dataclasses` with type hints
- Validation logic in `__post_init__` methods
- Immutable fields where appropriate (use `frozen=True` for value objects)
- JSON serialization via `dataclasses.asdict()` and custom encoders for Path
- Weaviate mapping via dedicated schema definition files
