# Quickstart Guide: Maven Dependency Resolution and DTO Analysis

**Feature**: 004-maven-dependency-resolution
**Created**: 2025-12-15
**Target Audience**: Developers implementing this feature

## Overview

This guide provides step-by-step instructions for implementing Maven dependency resolution and DTO pattern recognition in the Java Codebase Indexer pipeline.

**Prerequisites**:
- Feature 001 (Java Codebase Indexer) fully implemented
- Python 3.8+ environment with virtual environment activated
- Weaviate running on localhost:8080
- Ollama running on localhost:11434

## Implementation Phases

### Phase 0: Setup and Testing Infrastructure

**Duration**: ~1-2 hours

#### 1. Create Test Fixtures

```bash
# Create fixture directories
mkdir -p tests/fixtures/pom-files
mkdir -p tests/fixtures/dto-classes

# Create simple pom.xml fixture
cat > tests/fixtures/pom-files/simple.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>at.a1ta.cuco</groupId>
            <artifactId>cuco-cct-core</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
EOF

# Create standard DTO fixture
cat > tests/fixtures/dto-classes/standard-dto.java <<'EOF'
package com.example.dto;

import java.io.Serializable;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.validation.constraints.Email;

public class UserDTO implements Serializable {
    @NotNull
    private Long userId;

    @NotNull
    @Size(min = 3, max = 50)
    private String username;

    @Email
    @NotNull
    private String email;

    // Getters and setters omitted for brevity
}
EOF
```

#### 2. Set Up Testing Environment

```bash
# Verify Weaviate is running
curl -s http://localhost:8080/v1/meta | jq .

# Verify Ollama is running
curl -s http://localhost:11434/api/tags | jq .

# Run existing tests to ensure baseline
pytest tests/unit/ -v

# Expected: All existing tests pass
```

### Phase 1: Maven Parser Implementation

**Duration**: ~2-3 hours

#### 1. Create MavenDependency Model

```bash
# Create new model file
touch src/codeindex/models/maven_dependency.py
```

```python
# src/codeindex/models/maven_dependency.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class MavenDependency:
    """Maven dependency from pom.xml."""

    # Required fields
    group_id: str
    artifact_id: str

    # Optional fields
    version: Optional[str] = None
    scope: str = "compile"

    # Resolution fields
    resolved_path: Optional[Path] = None
    resolution_status: str = "pending"

    # Metadata
    declared_in: Optional[Path] = None
    depth: int = 0

    def __post_init__(self):
        """Validate fields after initialization."""
        if not self.group_id or not self.artifact_id:
            raise ValueError("group_id and artifact_id are required")

        valid_scopes = {"compile", "test", "provided", "runtime", "system"}
        if self.scope not in valid_scopes:
            raise ValueError(f"Invalid scope: {self.scope}")

        valid_statuses = {"pending", "resolved", "not_found", "circular"}
        if self.resolution_status not in valid_statuses:
            raise ValueError(f"Invalid resolution_status: {self.resolution_status}")
```

#### 2. Create Maven Parser Service

```bash
# Create parser service
touch src/codeindex/services/maven_parser.py
```

```python
# src/codeindex/services/maven_parser.py
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
import logging

from ..models.maven_dependency import MavenDependency

log = logging.getLogger(__name__)

def parse_pom(pom_path: Path, depth: int = 0) -> List[MavenDependency]:
    """
    Parse Maven pom.xml and extract dependency declarations.

    Args:
        pom_path: Absolute path to pom.xml file
        depth: Current dependency depth (0=direct, 1+=transitive)

    Returns:
        List of MavenDependency objects

    Raises:
        FileNotFoundError: If pom.xml doesn't exist
        ET.ParseError: If XML is malformed
    """
    if not pom_path.exists():
        raise FileNotFoundError(f"pom.xml not found: {pom_path}")

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # Maven namespace
        ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}

        dependencies = []

        # Find all <dependency> elements
        for dep_elem in root.findall(".//mvn:dependency", ns):
            group_id_elem = dep_elem.find("mvn:groupId", ns)
            artifact_id_elem = dep_elem.find("mvn:artifactId", ns)
            version_elem = dep_elem.find("mvn:version", ns)
            scope_elem = dep_elem.find("mvn:scope", ns)

            if group_id_elem is None or artifact_id_elem is None:
                log.warning(f"Incomplete dependency in {pom_path}: missing groupId or artifactId")
                continue

            dependency = MavenDependency(
                group_id=group_id_elem.text,
                artifact_id=artifact_id_elem.text,
                version=version_elem.text if version_elem is not None else None,
                scope=scope_elem.text if scope_elem is not None else "compile",
                declared_in=pom_path,
                depth=depth
            )

            dependencies.append(dependency)

        log.info(f"Parsed {len(dependencies)} dependencies from {pom_path}")
        return dependencies

    except ET.ParseError as e:
        log.error(f"XML parse error in {pom_path}: {e}")
        raise
```

#### 3. Write Unit Tests

```python
# tests/unit/test_maven_parser.py
import pytest
from pathlib import Path
from codeindex.services.maven_parser import parse_pom
from codeindex.models.maven_dependency import MavenDependency

def test_parse_simple_pom():
    """Test parsing simple pom.xml with single dependency."""
    pom_path = Path("tests/fixtures/pom-files/simple.xml")
    dependencies = parse_pom(pom_path)

    assert len(dependencies) == 1
    assert dependencies[0].group_id == "at.a1ta.cuco"
    assert dependencies[0].artifact_id == "cuco-cct-core"
    assert dependencies[0].version == "1.0.0"
    assert dependencies[0].scope == "compile"
    assert dependencies[0].depth == 0

def test_parse_nonexistent_pom():
    """Test parsing non-existent pom.xml raises error."""
    with pytest.raises(FileNotFoundError):
        parse_pom(Path("/nonexistent/pom.xml"))

def test_maven_dependency_validation():
    """Test MavenDependency field validation."""
    # Valid dependency
    dep = MavenDependency(group_id="com.example", artifact_id="test")
    assert dep.scope == "compile"  # default

    # Invalid scope
    with pytest.raises(ValueError):
        MavenDependency(group_id="com.example", artifact_id="test", scope="invalid")
```

```bash
# Run tests
pytest tests/unit/test_maven_parser.py -v

# Expected: All tests pass
```

### Phase 2: Path Resolution and Dependency Graph

**Duration**: ~2-3 hours

#### 1. Create Path Resolver Utility

```python
# src/codeindex/utils/path_resolver.py
from pathlib import Path
from typing import Optional
import logging

log = logging.getLogger(__name__)

def resolve_artifact_path(
    artifact_id: str,
    base_dir: Path,
    group_id: Optional[str] = None
) -> Optional[Path]:
    """
    Resolve Maven artifact to directory path.

    Resolution: base_dir / artifact_id

    Args:
        artifact_id: Maven artifactId (e.g., "cuco-cct-core")
        base_dir: Base directory (JAVA_SOURCE_DIR or JAVA_SOURCE_DIR/project)
        group_id: Maven groupId (not used in path resolution per Assumption 1)

    Returns:
        Resolved path if directory exists, None otherwise
    """
    artifact_path = base_dir / artifact_id

    if artifact_path.exists() and artifact_path.is_dir():
        log.debug(f"Resolved artifact {artifact_id} to {artifact_path}")
        return artifact_path
    else:
        log.warning(f"Artifact directory not found: {artifact_path}")
        if group_id:
            log.warning(f"  groupId: {group_id}, artifactId: {artifact_id}")
        log.warning(f"  Expected at: {artifact_path}")
        log.warning(f"  Searched from base: {base_dir}")
        return None
```

#### 2. Create Dependency Resolver Service

```python
# src/codeindex/services/dependency_resolver.py
from pathlib import Path
from typing import Set, List, Optional
import logging

from ..models.maven_dependency import MavenDependency
from ..models.dependency_graph import DependencyGraph, DependencyNode
from .maven_parser import parse_pom
from ..utils.path_resolver import resolve_artifact_path

log = logging.getLogger(__name__)

def resolve_dependencies(
    root_pom: Path,
    base_dir: Path,
    max_depth: int = 1,
    project_name: Optional[str] = None
) -> DependencyGraph:
    """
    Resolve dependency graph with circular detection.

    Args:
        root_pom: Path to root pom.xml
        base_dir: Base directory for artifact resolution
        max_depth: Maximum dependency depth to resolve
        project_name: Project name for graph metadata

    Returns:
        Complete dependency graph
    """
    visited: Set[str] = set()
    circular_paths: List[List[str]] = []

    def resolve_recursive(
        pom_path: Path,
        depth: int,
        path: List[str]
    ) -> List[DependencyNode]:
        """Recursively resolve dependencies."""
        if depth > max_depth:
            return []

        dependencies = parse_pom(pom_path, depth)
        nodes = []

        for dep in dependencies:
            # Circular dependency detection
            if dep.artifact_id in visited:
                cycle = path + [dep.artifact_id]
                log.warning(f"Circular dependency detected: {' → '.join(cycle)}")
                dep.resolution_status = "circular"
                circular_paths.append(cycle)
                continue

            visited.add(dep.artifact_id)

            # Resolve artifact path
            resolved = resolve_artifact_path(dep.artifact_id, base_dir, dep.group_id)
            if resolved:
                dep.resolved_path = resolved
                dep.resolution_status = "resolved"

                # Recurse into dependency's pom.xml if within depth limit
                child_pom = resolved / "pom.xml"
                children = []
                if child_pom.exists() and depth < max_depth:
                    children = resolve_recursive(
                        child_pom,
                        depth + 1,
                        path + [dep.artifact_id]
                    )

                nodes.append(DependencyNode(
                    dependency=dep,
                    children=children,
                    parent=None
                ))
            else:
                dep.resolution_status = "not_found"
                nodes.append(DependencyNode(
                    dependency=dep,
                    children=[],
                    parent=None
                ))

        return nodes

    # Start resolution
    root_dependencies = resolve_recursive(root_pom, 0, [])

    # Build graph
    graph = DependencyGraph(
        project_name=project_name or "unknown",
        root_pom=root_pom,
        root_node=DependencyNode(
            dependency=MavenDependency(
                group_id="",
                artifact_id=project_name or "root",
                depth=-1
            ),
            children=root_dependencies,
            parent=None
        )
    )

    # Compute statistics
    all_deps = _flatten_graph(graph.root_node)
    graph.total_dependencies = len(all_deps)
    graph.resolved_count = sum(1 for d in all_deps if d.resolution_status == "resolved")
    graph.not_found_count = sum(1 for d in all_deps if d.resolution_status == "not_found")
    graph.circular_count = len(circular_paths)
    graph.max_depth = max(d.depth for d in all_deps) if all_deps else 0
    graph.circular_paths = circular_paths

    return graph

def _flatten_graph(node: DependencyNode) -> List[MavenDependency]:
    """Flatten dependency tree to list."""
    deps = [node.dependency] if node.dependency.depth >= 0 else []
    for child in node.children:
        deps.extend(_flatten_graph(child))
    return deps
```

#### 3. Run Integration Tests

```bash
# Create integration test
# tests/integration/test_dependency_resolution.py

pytest tests/integration/test_dependency_resolution.py -v
```

### Phase 3: DTO Classification

**Duration**: ~3-4 hours

#### 1. Implement DTO Classifier

```python
# src/codeindex/services/classifier.py (extend existing)

def classify_dto(
    java_source: str,
    file_path: Path,
    class_name: str
) -> ClassificationResult:
    """
    Classify Java class as DTO or not using multi-phase algorithm.

    See contracts/dto-classifier-api.yaml for detailed specification.
    """
    confidence = 0
    signals = []

    # Phase 1: Naming pattern match
    dto_patterns = ["DTO", "Request", "Response", "Command", "Query", "Event"]
    if any(class_name.endswith(pattern) for pattern in dto_patterns):
        confidence += 80
        signals.append(f"naming_pattern_match:*{class_name[-10:]}")

    # Phase 2: Entity exclusion
    entity_annotations = ["@Entity", "@Table", "@Document", "@Embeddable"]
    if any(annotation in java_source for annotation in entity_annotations):
        return ClassificationResult(
            is_dto=False,
            confidence=0,
            signals=[],
            rejection_reason="entity_annotation_present"
        )

    # Phase 3: Structural analysis
    field_count = len(re.findall(r'^\s*private\s+\w+\s+\w+\s*;', java_source, re.MULTILINE))
    method_count = len(re.findall(r'^\s*(?:public|private|protected)\s+\w+\s+\w+\s*\(', java_source, re.MULTILINE))
    # Exclude getters/setters/toString/equals/hashCode
    business_methods = method_count - (field_count * 2) - 3  # rough estimate
    if business_methods < 0:
        business_methods = 0

    if field_count > 0 and field_count / max(business_methods, 1) > 3.0:
        confidence += 30
        signals.append(f"structural_analysis:field_ratio={field_count}/{business_methods}")

    # Phase 4: Serialization markers
    if "implements Serializable" in java_source or "implements IsSerializable" in java_source:
        confidence += 10
        signals.append("serialization_marker:Serializable")

    # Phase 5: Package location
    package_indicators = [".dto.", ".shared.", ".model.", ".transfer.", ".command.", ".query."]
    if any(indicator in str(file_path) for indicator in package_indicators):
        confidence += 15
        signals.append("package_location:" + next(ind for ind in package_indicators if ind in str(file_path)))

    # Threshold decision
    is_dto = confidence >= 70

    return ClassificationResult(
        is_dto=is_dto,
        confidence=confidence,
        signals=signals,
        rejection_reason=None if is_dto else "confidence_below_threshold"
    )
```

### Phase 4: Integration with Discovery Pipeline

**Duration**: ~2-3 hours

#### 1. Extend Discovery CLI

```python
# src/codeindex/cli/discover.py (extend existing)

@click.option(
    "--project",
    type=str,
    default=None,
    help="Project subdirectory within JAVA_SOURCE_DIR"
)
@click.option(
    "--dependency-depth",
    type=int,
    default=1,
    help="Maximum dependency depth to resolve (default: 1)"
)
def discover(source_dir, output, project, dependency_depth):
    """Discover source files with Maven dependency resolution."""
    # ... existing code ...

    # Resolve dependencies if pom.xml exists
    pom_path = source_path / "pom.xml"
    if pom_path.exists():
        log.info(f"Resolving Maven dependencies from {pom_path}")
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=source_path,
            max_depth=dependency_depth,
            project_name=project
        )

        # Log resolution statistics
        log.info(f"Dependency resolution complete:")
        log.info(f"  Total: {graph.total_dependencies}")
        log.info(f"  Resolved: {graph.resolved_count}")
        log.info(f"  Not found: {graph.not_found_count}")
        log.info(f"  Circular: {graph.circular_count}")

        # Add resolved dependency directories to discovery
        for dep in _flatten_graph(graph.root_node):
            if dep.resolved_path:
                discover_in_directory(dep.resolved_path, inventory)
```

### Phase 5: Weaviate Schema and Indexing

**Duration**: ~1-2 hours

#### 1. Create DtoArtifact Schema

```python
# src/codeindex/schemas/dto_artifact_schema.py

DTO_ARTIFACT_SCHEMA = {
    "class": "DtoArtifact",
    "description": "Data Transfer Object extracted from Java codebase",
    "properties": [
        {"name": "artifact_id", "dataType": ["text"]},
        {"name": "class_name", "dataType": ["text"]},
        {"name": "package_name", "dataType": ["text"]},
        {"name": "source_path", "dataType": ["text"]},
        {"name": "project", "dataType": ["text"]},
        {"name": "fields", "dataType": ["object[]"]},
        {"name": "validation_rules", "dataType": ["object"]},
        {"name": "serialization_markers", "dataType": ["text[]"]},
        {"name": "nested_dtos", "dataType": ["text[]"]},
        {"name": "is_shared", "dataType": ["boolean"]},
        {"name": "language", "dataType": ["text"]},
        {"name": "framework", "dataType": ["text"]},
        {"name": "content_summary", "dataType": ["text"]},
    ],
    "vectorizer": "text2vec-transformers"
}
```

## Testing Checklist

Before proceeding to `/speckit.tasks`:

- [ ] All unit tests pass (`pytest tests/unit/`)
- [ ] All integration tests pass (`pytest tests/integration/`)
- [ ] Test coverage >80% for maven_parser, dependency_resolver, dto_classifier
- [ ] Manual test: Run discovery on real project with pom.xml
- [ ] Manual test: Verify DTO classification on sample DTOs
- [ ] Weaviate schema created successfully
- [ ] Sample DTOs indexed and searchable in Weaviate

## Next Steps

Once implementation is complete:

1. Run `/speckit.tasks` to generate task breakdown
2. Create GitHub issues from tasks using `/speckit.taskstoissues`
3. Begin implementation following tasks.md

## Common Issues

**Issue**: `xml.etree.ElementTree.ParseError: no element found`
**Solution**: Check pom.xml file is valid XML. Use `xmllint pom.xml` to validate.

**Issue**: Dependencies not resolving (all "not_found")
**Solution**: Verify JAVA_SOURCE_DIR is correct and artifact directories exist at base_dir/artifact_id

**Issue**: DTO classification false positives (Services classified as DTOs)
**Solution**: Tune confidence threshold or add exclusion patterns for service classes

## Resources

- [Feature Specification](./spec.md)
- [Research Document](./research.md)
- [Data Model](./data-model.md)
- [Maven Parser API Contract](./contracts/maven-parser-api.yaml)
- [DTO Classifier API Contract](./contracts/dto-classifier-api.yaml)
