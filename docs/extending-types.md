# Extending Artifact Types

**Last Updated**: 2025-12-14
**Audience**: Developers adding new file classifications

## Overview

This guide explains how to extend the Java Codebase Indexer Pipeline with new artifact type classifications. Artifact types categorize files by their purpose and enable filtered semantic search.

### When to Add a New Type

Add a new artifact type when:
- You're analyzing a new file format that serves a distinct purpose (e.g., Docker configs, GraphQL schemas)
- The file type requires different search semantics than existing types
- You need to filter search results by this specific file category

### What Artifact Types Do

Artifact types serve two main purposes:

1. **Classification**: Categorize files by purpose (source code, tests, configs, views, etc.)
2. **Search Filtering**: Enable users to search within specific file categories

For example:
```bash
# Search only in JSP view files
codeindex search "user login form" --type jsp_view

# Search only in database schemas
codeindex search "user table" --type sql_schema
```

---

## Architecture Overview

The artifact type system has three main components:

### 1. Type Enumeration

**File**: `src/codeindex/models/__init__.py`

Defines the controlled vocabulary of artifact types:

```python
class ArtifactType(str, Enum):
    """Artifact type enumeration."""
    JAVA_SOURCE = "java_source"
    JAVA_TEST = "java_test"
    JSP_VIEW = "jsp_view"
    # ... more types
```

### 2. File Classifier

**File**: `src/codeindex/services/classifier.py`

Determines artifact type based on file extension, path, and naming patterns:

```python
def get_artifact_type(path: Path) -> ArtifactType:
    """Determine artifact type for a file."""
    if is_java_test(path):
        return ArtifactType.JAVA_TEST
    if is_java_source(path):
        return ArtifactType.JAVA_SOURCE
    # ... more checks
```

### 3. Weaviate Schema

**File**: `src/codeindex/schemas/weaviate.py`

Defines how artifact types are stored and indexed in Weaviate for semantic search.

---

## Step-by-Step Implementation

### Step 1: Add Type to Enumeration

Edit `src/codeindex/models/__init__.py`:

```python
class ArtifactType(str, Enum):
    """
    Artifact type enumeration.

    Defines the semantic types for code artifacts based on file purpose.
    """
    # Existing types
    JAVA_SOURCE = "java_source"
    JAVA_TEST = "java_test"
    JSP_VIEW = "jsp_view"
    # ... other types

    # Your new type
    DOCKERFILE = "dockerfile"              # Docker configuration files
    GRAPHQL_SCHEMA = "graphql_schema"      # GraphQL schema definitions
    TERRAFORM_CONFIG = "terraform_config"  # Infrastructure as Code
    # Add clear, descriptive comments
```

**Naming Convention**:
- Use lowercase with underscores: `snake_case`
- Be specific: `graphql_schema` not just `schema`
- Use purpose-based names: `sql_schema` (what it defines) not `ddl_file` (how it's implemented)

### Step 2: Add Classification Logic

Edit `src/codeindex/services/classifier.py`:

#### 2a. Add Detection Function

```python
def is_dockerfile(path: Path) -> bool:
    """
    Check if file is a Dockerfile.

    Args:
        path: File path to check

    Returns:
        True if Dockerfile
    """
    # Check filename patterns
    if path.name.lower() in ['dockerfile', 'dockerfile.dev', 'dockerfile.prod']:
        return True

    # Check for Dockerfile with extension
    if path.stem.lower() == 'dockerfile' and path.suffix:
        return True

    return False


def is_graphql_schema(path: Path) -> bool:
    """
    Check if file is a GraphQL schema definition.

    Args:
        path: File path to check

    Returns:
        True if GraphQL schema file
    """
    if path.suffix.lower() not in ['.graphql', '.gql']:
        return False

    # Check for schema keywords in path or filename
    schema_keywords = ['schema', 'type', 'query', 'mutation']
    filename_lower = path.stem.lower()

    for keyword in schema_keywords:
        if keyword in filename_lower:
            return True

    # Check if in schema directory
    if 'schema' in str(path).lower():
        return True

    return False


def is_terraform_config(path: Path) -> bool:
    """
    Check if file is a Terraform configuration.

    Args:
        path: File path to check

    Returns:
        True if Terraform config file
    """
    return path.suffix.lower() == '.tf'
```

#### 2b. Update `get_artifact_type()` Function

```python
def get_artifact_type(path: Path) -> ArtifactType:
    """
    Determine artifact type for a file.

    Args:
        path: File path to classify

    Returns:
        ArtifactType enum value
    """
    # Check in order of specificity (most specific first)

    # Your new types (add near the top for higher priority)
    if is_dockerfile(path):
        return ArtifactType.DOCKERFILE

    if is_graphql_schema(path):
        return ArtifactType.GRAPHQL_SCHEMA

    if is_terraform_config(path):
        return ArtifactType.TERRAFORM_CONFIG

    # Existing types
    if is_java_test(path):
        return ArtifactType.JAVA_TEST

    if is_java_source(path):
        return ArtifactType.JAVA_SOURCE

    # ... rest of existing checks

    # Default fallback
    return ArtifactType.OTHER_TEXT
```

**Order Matters**: Place more specific checks before general ones. For example, check for `JAVA_TEST` before `JAVA_SOURCE` because test files are also Java files.

### Step 3: Create Unit Tests

Create `tests/unit/test_classifier_extensions.py`:

```python
"""
Unit tests for artifact type classification extensions.
"""
import pytest
from pathlib import Path
from codeindex.services.classifier import (
    get_artifact_type,
    is_dockerfile,
    is_graphql_schema,
    is_terraform_config
)
from codeindex.models import ArtifactType


class TestDockerfileDetection:
    """Tests for Dockerfile detection."""

    def test_standard_dockerfile(self):
        """Test standard Dockerfile."""
        path = Path("/project/Dockerfile")
        assert is_dockerfile(path) is True
        assert get_artifact_type(path) == ArtifactType.DOCKERFILE

    def test_dockerfile_with_suffix(self):
        """Test Dockerfile with suffix (Dockerfile.dev)."""
        path = Path("/project/Dockerfile.dev")
        assert is_dockerfile(path) is True

    def test_dockerfile_case_insensitive(self):
        """Test case insensitivity."""
        path = Path("/project/dockerfile")
        assert is_dockerfile(path) is True

    def test_not_dockerfile(self):
        """Test non-Dockerfile files."""
        path = Path("/project/docker-compose.yml")
        assert is_dockerfile(path) is False


class TestGraphQLSchemaDetection:
    """Tests for GraphQL schema detection."""

    def test_graphql_schema_extension(self):
        """Test .graphql extension."""
        path = Path("/project/schema.graphql")
        assert is_graphql_schema(path) is True
        assert get_artifact_type(path) == ArtifactType.GRAPHQL_SCHEMA

    def test_gql_extension(self):
        """Test .gql extension."""
        path = Path("/project/types.gql")
        assert is_graphql_schema(path) is True

    def test_schema_in_path(self):
        """Test schema directory detection."""
        path = Path("/project/schemas/user.graphql")
        assert is_graphql_schema(path) is True

    def test_not_graphql_schema(self):
        """Test non-GraphQL files."""
        path = Path("/project/query.sql")
        assert is_graphql_schema(path) is False


class TestTerraformConfigDetection:
    """Tests for Terraform config detection."""

    def test_terraform_extension(self):
        """Test .tf extension."""
        path = Path("/infra/main.tf")
        assert is_terraform_config(path) is True
        assert get_artifact_type(path) == ArtifactType.TERRAFORM_CONFIG

    def test_not_terraform_config(self):
        """Test non-Terraform files."""
        path = Path("/project/config.yaml")
        assert is_terraform_config(path) is False
```

Run tests:
```bash
pytest tests/unit/test_classifier_extensions.py -v
```

### Step 4: Update Discovery to Include New Types

The discovery service should automatically include your new file types if they match the file extension patterns. Verify by running discovery:

```bash
# Test discovery with new file types
codeindex discover --source-dir /path/to/project/with/new/types
```

If your new types aren't being discovered, check the exclusion patterns in `src/codeindex/services/discovery.py`:

```python
# Ensure your file patterns aren't excluded
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    # Make sure your new file types aren't in this list
]
```

---

## Real-World Example: Adding Kotlin Support

Here's a complete example showing how to add Kotlin source files as a new artifact type.

### Step 1: Add to Enumeration

```python
# src/codeindex/models/__init__.py

class ArtifactType(str, Enum):
    # ... existing types
    KOTLIN_SOURCE = "kotlin_source"  # Kotlin source files
    KOTLIN_TEST = "kotlin_test"      # Kotlin test files
```

### Step 2: Add Classification Logic

```python
# src/codeindex/services/classifier.py

def is_kotlin_source(path: Path) -> bool:
    """
    Check if file is a Kotlin source file (not test).

    Args:
        path: File path to check

    Returns:
        True if Kotlin source file
    """
    if path.suffix.lower() != '.kt':
        return False

    # Exclude test files
    if is_kotlin_test(path):
        return False

    return True


def is_kotlin_test(path: Path) -> bool:
    """
    Check if file is a Kotlin test file.

    Args:
        path: File path to check

    Returns:
        True if Kotlin test file
    """
    if path.suffix.lower() != '.kt':
        return False

    # Check for test path patterns
    test_patterns = [
        r'(^|/)src/test/',
        r'(^|/)src/androidTest/',
        r'(^|\\)src\\test\\',
        r'(^|\\)src\\androidTest\\',
    ]

    path_str = str(path)
    for pattern in test_patterns:
        if re.search(pattern, path_str):
            return True

    # Check for test file naming conventions
    stem = path.stem
    if stem.endswith('Test') or stem.endswith('Tests'):
        return True

    return False


def get_artifact_type(path: Path) -> ArtifactType:
    """Determine artifact type for a file."""

    # Add Kotlin checks (before general checks)
    if is_kotlin_test(path):
        return ArtifactType.KOTLIN_TEST

    if is_kotlin_source(path):
        return ArtifactType.KOTLIN_SOURCE

    # ... existing checks
```

### Step 3: Create Tests

```python
# tests/unit/test_kotlin_classifier.py

import pytest
from pathlib import Path
from codeindex.services.classifier import get_artifact_type, is_kotlin_source, is_kotlin_test
from codeindex.models import ArtifactType


class TestKotlinSourceDetection:
    """Tests for Kotlin source file detection."""

    def test_kotlin_source_file(self):
        """Test standard Kotlin source file."""
        path = Path("/project/src/main/kotlin/com/example/App.kt")
        assert is_kotlin_source(path) is True
        assert get_artifact_type(path) == ArtifactType.KOTLIN_SOURCE

    def test_kotlin_test_not_source(self):
        """Test that Kotlin test files are not classified as source."""
        path = Path("/project/src/test/kotlin/com/example/AppTest.kt")
        assert is_kotlin_source(path) is False
        assert is_kotlin_test(path) is True


class TestKotlinTestDetection:
    """Tests for Kotlin test file detection."""

    def test_kotlin_test_in_test_directory(self):
        """Test Kotlin test file in test directory."""
        path = Path("/project/src/test/kotlin/com/example/AppTest.kt")
        assert is_kotlin_test(path) is True
        assert get_artifact_type(path) == ArtifactType.KOTLIN_TEST

    def test_kotlin_test_with_test_suffix(self):
        """Test Kotlin file ending with Test."""
        path = Path("/project/src/main/kotlin/utils/StringUtilsTest.kt")
        assert is_kotlin_test(path) is True

    def test_kotlin_source_not_test(self):
        """Test that Kotlin source files are not classified as tests."""
        path = Path("/project/src/main/kotlin/com/example/App.kt")
        assert is_kotlin_test(path) is False
```

### Step 4: Verify End-to-End

Test with a real project:

```bash
# Create test Kotlin project
mkdir -p /tmp/kotlin-test/src/main/kotlin/com/example
mkdir -p /tmp/kotlin-test/src/test/kotlin/com/example

cat > /tmp/kotlin-test/src/main/kotlin/com/example/App.kt << 'EOF'
package com.example

fun main() {
    println("Hello, Kotlin!")
}
EOF

cat > /tmp/kotlin-test/src/test/kotlin/com/example/AppTest.kt << 'EOF'
package com.example

import org.junit.Test

class AppTest {
    @Test
    fun testMain() {
        // Test code
    }
}
EOF

# Run discovery
codeindex discover --source-dir /tmp/kotlin-test

# Expected output should include:
# Files by type:
#   kotlin_source: 1
#   kotlin_test: 1
```

---

## Classification Patterns

### Pattern 1: Extension-Based Detection

Simple file extension matching:

```python
def is_python_source(path: Path) -> bool:
    """Check if file is a Python source file."""
    return path.suffix.lower() == '.py'
```

### Pattern 2: Path-Based Detection

Check file location in directory structure:

```python
def is_test_file(path: Path) -> bool:
    """Check if file is in a test directory."""
    test_patterns = [
        r'(^|/)src/test/',
        r'(^|/)tests/',
        r'(^|\\)src\\test\\',
        r'(^|\\)tests\\',
    ]

    path_str = str(path)
    for pattern in test_patterns:
        if re.search(pattern, path_str):
            return True

    return False
```

### Pattern 3: Filename Pattern Detection

Check filename conventions:

```python
def is_config_file(path: Path) -> bool:
    """Check if file is a configuration file."""
    config_patterns = [
        'config',
        'settings',
        'configuration',
        '.env',
    ]

    filename_lower = path.name.lower()
    for pattern in config_patterns:
        if pattern in filename_lower:
            return True

    return False
```

### Pattern 4: Content-Based Detection

Read file content to determine type (use sparingly for performance):

```python
def is_spring_config(path: Path) -> bool:
    """Check if XML file is a Spring configuration."""
    if path.suffix.lower() != '.xml':
        return False

    try:
        # Read first few lines to check for Spring namespace
        with open(path, 'r', encoding='utf-8') as f:
            header = ''.join(f.readlines()[:10])
            if 'springframework' in header:
                return True
    except Exception:
        pass

    return False
```

### Pattern 5: Combined Detection

Use multiple criteria for robust classification:

```python
def is_sql_schema(path: Path) -> bool:
    """Check if SQL file is a schema/DDL file."""
    # Must be SQL file
    if path.suffix.lower() != '.sql':
        return False

    # Check filename for schema keywords
    schema_keywords = ['schema', 'create', 'ddl', 'migration']
    filename_lower = path.stem.lower()

    for keyword in schema_keywords:
        if keyword in filename_lower:
            return True

    # Check if in migrations directory
    if 'migrations' in str(path).lower():
        return True

    return False
```

---

## Best Practices

### 1. Maintain Order of Specificity

Place more specific checks before general ones in `get_artifact_type()`:

```python
def get_artifact_type(path: Path) -> ArtifactType:
    # CORRECT: Check test files before source files
    if is_java_test(path):
        return ArtifactType.JAVA_TEST
    if is_java_source(path):
        return ArtifactType.JAVA_SOURCE

    # INCORRECT: Source check would match test files first
    # if is_java_source(path):  # This includes tests!
    #     return ArtifactType.JAVA_SOURCE
    # if is_java_test(path):
    #     return ArtifactType.JAVA_TEST
```

### 2. Use Clear, Descriptive Names

**Good**:
- `GRAPHQL_SCHEMA` (clear purpose)
- `KOTLIN_TEST` (language + purpose)
- `SQL_MIGRATION` (type + purpose)

**Bad**:
- `GQL` (unclear abbreviation)
- `TEST` (too vague)
- `DDL_FILE` (implementation detail, not purpose)

### 3. Document Detection Logic

```python
def is_gwt_module(path: Path) -> bool:
    """
    Check if file is a GWT module XML.

    GWT modules are identified by:
    - .xml extension
    - Filename ending with .gwt.xml (e.g., App.gwt.xml)

    Args:
        path: File path to check

    Returns:
        True if GWT module file
    """
    if path.suffix.lower() != '.xml':
        return False

    # GWT modules end with .gwt.xml
    return '.gwt.xml' in path.name.lower()
```

### 4. Handle Edge Cases

Test with:
- Case variations (Dockerfile, dockerfile, DOCKERFILE)
- Files without extensions (Dockerfile, Makefile)
- Files with multiple dots (schema.graphql.backup)
- Windows vs Unix paths

```python
def is_dockerfile(path: Path) -> bool:
    """Check if file is a Dockerfile."""
    # Case-insensitive check
    name_lower = path.name.lower()

    # Handle exact match
    if name_lower == 'dockerfile':
        return True

    # Handle variations (Dockerfile.dev, Dockerfile.prod)
    if name_lower.startswith('dockerfile.'):
        return True

    return False
```

### 5. Write Comprehensive Tests

Cover all detection scenarios:

```python
def test_dockerfile_detection():
    """Test all Dockerfile variations."""
    test_cases = [
        ("Dockerfile", True),
        ("dockerfile", True),
        ("DOCKERFILE", True),
        ("Dockerfile.dev", True),
        ("Dockerfile.prod", True),
        ("docker-compose.yml", False),
        ("DockerfileBackup", False),
    ]

    for filename, expected in test_cases:
        path = Path(f"/project/{filename}")
        assert is_dockerfile(path) == expected, f"Failed for {filename}"
```

---

## Integration with Search

Once your new artifact type is defined, users can filter searches:

```bash
# Search only in Dockerfiles
codeindex search "expose port" --type dockerfile

# Search in GraphQL schemas
codeindex search "user type" --type graphql_schema

# Search in Terraform configs
codeindex search "s3 bucket" --type terraform_config
```

The search filtering is automatically supported once the artifact type is indexed in Weaviate.

---

## Troubleshooting

### New Type Not Appearing in Discovery

**Problem**: Files aren't being classified with your new type

**Solution**:
1. Verify `get_artifact_type()` includes your check
2. Check order of checks (specific before general)
3. Test detection function in isolation
4. Check file isn't excluded by discovery patterns

```python
# Test classification directly
from pathlib import Path
from codeindex.services.classifier import get_artifact_type

path = Path("/project/Dockerfile")
artifact_type = get_artifact_type(path)
print(f"Detected type: {artifact_type}")  # Should print: DOCKERFILE
```

### Search Filtering Not Working

**Problem**: `--type your_type` filter returns no results

**Solution**:
1. Verify files were indexed (check `codeindex status`)
2. Ensure type name matches exactly (case-sensitive)
3. Re-index project after adding new type
4. Check Weaviate schema includes new type

```bash
# Check if files are indexed
codeindex status --project "your-project-id"

# Should show:
# Files by type:
#   your_new_type: X files
```

### Classification Conflicts

**Problem**: Files are classified as wrong type

**Solution**:
1. Check order in `get_artifact_type()` (specific first)
2. Add more specific detection criteria
3. Test with edge cases

```python
# Example: JSON files being classified as XML_CONFIG
# Fix: Add JSON-specific detection before XML check

def is_json_config(path: Path) -> bool:
    return path.suffix.lower() == '.json'

def get_artifact_type(path: Path) -> ArtifactType:
    # Check JSON before XML (more specific)
    if is_json_config(path):
        return ArtifactType.JSON_CONFIG

    if is_xml_config(path):
        return ArtifactType.XML_CONFIG
```

---

## Performance Considerations

### Fast Checks First

Order checks by performance:

```python
def get_artifact_type(path: Path) -> ArtifactType:
    # Fast: Extension check (no I/O)
    if path.suffix.lower() == '.py':
        return ArtifactType.PYTHON_SOURCE

    # Medium: Path pattern matching
    if _matches_pattern(path, TEST_PATTERNS):
        return ArtifactType.TEST_FILE

    # Slow: Content inspection (avoid if possible)
    if _check_file_content(path):
        return ArtifactType.SPECIAL_FILE
```

### Avoid File I/O in Classification

Only read file content when absolutely necessary:

```python
# BAD: Reading file for every classification
def is_spring_config(path: Path) -> bool:
    content = path.read_text()  # Expensive!
    return 'springframework' in content

# GOOD: Use filename/path patterns instead
def is_spring_config(path: Path) -> bool:
    if path.suffix.lower() != '.xml':
        return False

    # Check filename patterns
    config_names = ['applicationcontext', 'spring', 'beans']
    filename_lower = path.stem.lower()

    return any(name in filename_lower for name in config_names)
```

---

## Next Steps

After adding your artifact type:

1. **Create parser**: If structural extraction is needed, see [Adding Parsers](adding-parsers.md)
2. **Test discovery**: Run `codeindex discover` on sample project
3. **Test end-to-end**: Index and search with new type
4. **Update documentation**: Add examples to quickstart.md

---

## Additional Resources

- **Classifier Implementation**: `src/codeindex/services/classifier.py` (380 lines)
- **ArtifactType Enum**: `src/codeindex/models/__init__.py` (lines 20-41)
- **Unit Tests**: `tests/unit/test_classifier.py` (comprehensive examples)
- **Discovery Service**: `src/codeindex/services/discovery.py` (integration)
