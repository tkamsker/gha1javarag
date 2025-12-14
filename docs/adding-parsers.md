# Adding New Parsers

**Last Updated**: 2025-12-14
**Audience**: Developers extending language support

## Overview

This guide walks you through adding support for a new programming language or file type to the Java Codebase Indexer Pipeline. Parsers extract structural information from source files, which is then enhanced with AI-generated semantic understanding.

### When to Add a Parser

Add a new parser when:
- You need to analyze a new programming language (e.g., Python, Kotlin, Groovy)
- You want to extract structured data from a specific file format (e.g., YAML configs, Thymeleaf templates)
- The existing parsers don't provide the structural information you need

### What Parsers Do

Parsers extract **structural information** from source files:
- Language constructs (classes, methods, functions)
- Imports and dependencies
- Annotations and decorators
- File-specific patterns (JSP tags, SQL statements, XML elements)

This structural data is combined with AI-generated semantic understanding to create rich, searchable code artifacts.

---

## Parser Architecture Pattern

All parsers follow a consistent pattern for maintainability and testability.

### Required Components

1. **Parser Class** - Main parsing logic
2. **Regular Expressions** - Patterns for structural extraction
3. **Parse Method** - Returns structured dictionary
4. **Error Handling** - Graceful degradation on parse errors
5. **Convenience Functions** - Standalone functions for common operations

### File Location

```
src/codeindex/parsers/
├── __init__.py              # Export new parser
├── java_parser.py           # Existing: Java parser
├── jsp_parser.py            # Existing: JSP parser
├── xml_parser.py            # Existing: XML parser
├── sql_parser.py            # Existing: SQL parser
└── your_parser.py           # New: Your parser
```

---

## Step-by-Step Implementation

### Step 1: Create Parser File

Create `src/codeindex/parsers/your_parser.py`:

```python
"""
Your Language Parser.

Extracts structural information from YOUR_LANGUAGE files including:
- List the key elements you'll extract
- Be specific about what structural data you capture
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


# ==============================================================================
# Regular Expressions
# ==============================================================================

# Define regex patterns for the language constructs you need to extract
# Example: Function definition pattern
FUNCTION_PATTERN = re.compile(
    r'^\s*def\s+(\w+)\s*\(([^)]*)\)',  # Python function example
    re.MULTILINE
)


# ==============================================================================
# YourLanguageParser Class
# ==============================================================================

class YourLanguageParser:
    """
    Parser for YOUR_LANGUAGE files.

    Extracts structural information using regex patterns.
    """

    def __init__(self):
        """Initialize parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a YOUR_LANGUAGE file.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with parsed elements

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse source code.

        Args:
            content: Source code as string

        Returns:
            Dictionary with structural information
        """
        try:
            # Remove comments to avoid false matches (if applicable)
            cleaned_content = self._remove_comments(content)

            # Extract all structural elements
            result = {
                'functions': self.extract_functions(cleaned_content),
                'classes': self.extract_classes(cleaned_content),
                'imports': self.extract_imports(cleaned_content),
                # Add more extraction methods as needed
            }

            return result

        except Exception as e:
            self.logger.error(f"Error parsing code: {e}", exc_info=True)
            # Return minimal result on error - NEVER fail completely
            return {
                'functions': [],
                'classes': [],
                'imports': [],
                'parse_error': str(e)
            }

    def _remove_comments(self, content: str) -> str:
        """
        Remove comments from code (customize for your language).

        Args:
            content: Source code

        Returns:
            Code without comments
        """
        # Example: Remove Python-style comments
        # Single-line comments
        content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)
        # Add more comment patterns as needed
        return content

    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract function/method declarations.

        Args:
            content: Source code

        Returns:
            List of function information
        """
        functions = []

        for match in FUNCTION_PATTERN.finditer(content):
            function_name = match.group(1)
            parameters_str = match.group(2) or ''

            function_info = {
                'name': function_name,
                'parameters': [p.strip() for p in parameters_str.split(',') if p.strip()],
            }

            functions.append(function_info)

        return functions

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract class declarations.

        Args:
            content: Source code

        Returns:
            List of class information
        """
        # Implement class extraction for your language
        return []

    def extract_imports(self, content: str) -> List[str]:
        """
        Extract import/include statements.

        Args:
            content: Source code

        Returns:
            List of imported modules/packages
        """
        # Implement import extraction for your language
        return []


# ==============================================================================
# Standalone Functions (for convenience)
# ==============================================================================

def parse_your_language_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a YOUR_LANGUAGE file (convenience function).

    Args:
        file_path: Path to file

    Returns:
        Dictionary with parsed elements
    """
    parser = YourLanguageParser()
    return parser.parse_file(file_path)
```

### Step 2: Add Parser to Package

Edit `src/codeindex/parsers/__init__.py`:

```python
"""
Parsers package.
"""
from .java_parser import JavaParser, parse_java_file
from .jsp_parser import JSPParser, parse_jsp_file
from .xml_parser import XMLParser, parse_xml_file
from .sql_parser import SQLParser, parse_sql_file
from .your_parser import YourLanguageParser, parse_your_language_file  # Add this

__all__ = [
    'JavaParser',
    'JSPParser',
    'XMLParser',
    'SQLParser',
    'YourLanguageParser',  # Add this
    'parse_java_file',
    'parse_jsp_file',
    'parse_xml_file',
    'parse_sql_file',
    'parse_your_language_file',  # Add this
]
```

### Step 3: Integrate with Extraction Service

Edit `src/codeindex/services/extraction.py` to use your parser:

```python
# Import your parser
from codeindex.parsers import YourLanguageParser

class ExtractionService:
    def __init__(self):
        self.java_parser = JavaParser()
        self.jsp_parser = JSPParser()
        self.xml_parser = XMLParser()
        self.sql_parser = SQLParser()
        self.your_language_parser = YourLanguageParser()  # Add this

    def _extract_structural(self, file_path: Path, artifact_type: ArtifactType) -> dict:
        """Extract structural information based on file type."""

        # Add your language type
        if artifact_type == ArtifactType.YOUR_LANGUAGE_SOURCE:
            return self.your_language_parser.parse_file(file_path)

        # Existing parsers...
        elif artifact_type == ArtifactType.JAVA_SOURCE:
            return self.java_parser.parse_file(file_path)
        # ... other types
```

### Step 4: Create Unit Tests

Create `tests/unit/test_your_parser.py`:

```python
"""
Unit tests for YOUR_LANGUAGE parser.
"""
import pytest
from pathlib import Path
from codeindex.parsers import YourLanguageParser


@pytest.fixture
def parser():
    """Create parser instance."""
    return YourLanguageParser()


def test_parse_simple_function(parser):
    """Test parsing a simple function."""
    code = """
    def greet(name):
        return f"Hello, {name}"
    """

    result = parser.parse(code)

    assert len(result['functions']) == 1
    assert result['functions'][0]['name'] == 'greet'
    assert result['functions'][0]['parameters'] == ['name']


def test_parse_with_error(parser):
    """Test graceful error handling."""
    code = "invalid syntax that will fail"

    result = parser.parse(code)

    # Should return minimal result, not crash
    assert 'parse_error' in result
    assert isinstance(result['functions'], list)


def test_parse_empty_file(parser):
    """Test parsing empty file."""
    result = parser.parse("")

    assert result['functions'] == []
    assert result['classes'] == []
```

Run tests:
```bash
pytest tests/unit/test_your_parser.py -v
```

---

## Real-World Example: Python Parser

Here's a concrete example showing how to create a Python parser:

### Python Parser Implementation

```python
"""
Python source file parser.

Extracts structural information from Python files including:
- Function definitions
- Class definitions
- Import statements
- Decorators
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


# ==============================================================================
# Regular Expressions
# ==============================================================================

# Function definition: def function_name(params):
FUNCTION_PATTERN = re.compile(
    r'^\s*(?:((?:@\w+(?:\([^)]*\))?\s+)*))?'  # Optional decorators (group 1)
    r'def\s+'                                   # def keyword
    r'(\w+)\s*'                                 # Function name (group 2)
    r'\(([^)]*)\)',                             # Parameters (group 3)
    re.MULTILINE
)

# Class definition: class ClassName:
CLASS_PATTERN = re.compile(
    r'^\s*(?:((?:@\w+(?:\([^)]*\))?\s+)*))?'  # Optional decorators (group 1)
    r'class\s+'                                 # class keyword
    r'(\w+)'                                    # Class name (group 2)
    r'(?:\(([^)]*)\))?',                        # Optional base classes (group 3)
    re.MULTILINE
)

# Import statements
IMPORT_PATTERN = re.compile(
    r'^\s*(?:from\s+([\w.]+)\s+)?import\s+([\w.*]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.*]+(?:\s+as\s+\w+)?)*)',
    re.MULTILINE
)

# Decorators
DECORATOR_PATTERN = re.compile(
    r'@(\w+)(?:\([^)]*\))?',
    re.MULTILINE
)

# Comments
SINGLE_LINE_COMMENT = re.compile(r'#.*?$', re.MULTILINE)
DOCSTRING_PATTERN = re.compile(r'""".*?"""|\'\'\'.*?\'\'\'', re.DOTALL)


# ==============================================================================
# PythonParser Class
# ==============================================================================

class PythonParser:
    """Parser for Python source files."""

    def __init__(self):
        """Initialize parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a Python file."""
        if not file_path.exists():
            raise FileNotFoundError(f"Python file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """Parse Python source code."""
        try:
            # Remove comments but keep docstrings for now
            cleaned_content = SINGLE_LINE_COMMENT.sub('', content)

            result = {
                'functions': self.extract_functions(cleaned_content),
                'classes': self.extract_classes(cleaned_content),
                'imports': self.extract_imports(cleaned_content),
                'decorators': self.extract_decorators(content),
            }

            return result

        except Exception as e:
            self.logger.error(f"Error parsing Python code: {e}", exc_info=True)
            return {
                'functions': [],
                'classes': [],
                'imports': [],
                'decorators': [],
                'parse_error': str(e)
            }

    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions."""
        functions = []

        for match in FUNCTION_PATTERN.finditer(content):
            decorators_str = match.group(1) or ''
            function_name = match.group(2)
            parameters_str = match.group(3) or ''

            # Parse decorators
            decorators = DECORATOR_PATTERN.findall(decorators_str)

            # Parse parameters
            parameters = []
            if parameters_str.strip():
                params = parameters_str.split(',')
                for param in params:
                    param = param.strip()
                    if param:
                        parameters.append(param)

            function_info = {
                'name': function_name,
                'parameters': parameters,
                'decorators': decorators,
            }

            functions.append(function_info)

        return functions

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions."""
        classes = []

        for match in CLASS_PATTERN.finditer(content):
            decorators_str = match.group(1) or ''
            class_name = match.group(2)
            bases_str = match.group(3) or ''

            # Parse decorators
            decorators = DECORATOR_PATTERN.findall(decorators_str)

            # Parse base classes
            bases = []
            if bases_str.strip():
                bases = [b.strip() for b in bases_str.split(',') if b.strip()]

            class_info = {
                'name': class_name,
                'bases': bases,
                'decorators': decorators,
            }

            classes.append(class_info)

        return classes

    def extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract import statements."""
        imports = []

        for match in IMPORT_PATTERN.finditer(content):
            from_module = match.group(1)  # May be None
            import_names = match.group(2)

            import_info = {
                'from': from_module,
                'imports': [i.strip() for i in import_names.split(',')]
            }

            imports.append(import_info)

        return imports

    def extract_decorators(self, content: str) -> List[str]:
        """Extract all decorators."""
        decorators = []
        seen = set()

        for match in DECORATOR_PATTERN.finditer(content):
            decorator = match.group(1)
            if decorator not in seen:
                seen.add(decorator)
                decorators.append(decorator)

        return decorators


# Convenience function
def parse_python_file(file_path: Path) -> Dict[str, Any]:
    """Parse a Python file (convenience function)."""
    parser = PythonParser()
    return parser.parse_file(file_path)
```

---

## Testing Your Parser

### Unit Test Structure

```python
import pytest
from codeindex.parsers import PythonParser

@pytest.fixture
def parser():
    return PythonParser()

def test_parse_function_with_decorator(parser):
    code = """
    @staticmethod
    def calculate(x, y):
        return x + y
    """

    result = parser.parse(code)

    assert len(result['functions']) == 1
    func = result['functions'][0]
    assert func['name'] == 'calculate'
    assert func['parameters'] == ['x', 'y']
    assert 'staticmethod' in func['decorators']

def test_parse_class_with_inheritance(parser):
    code = """
    class Child(Parent, Mixin):
        pass
    """

    result = parser.parse(code)

    assert len(result['classes']) == 1
    cls = result['classes'][0]
    assert cls['name'] == 'Child'
    assert cls['bases'] == ['Parent', 'Mixin']
```

### Integration Testing

Test with real files:

```bash
# Create test fixture
mkdir -p tests/fixtures/python
cat > tests/fixtures/python/sample.py << 'EOF'
from typing import List
import os

class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

def main():
    calc = Calculator()
    print(calc.add(1, 2))
EOF

# Run parser
python -m pytest tests/unit/test_python_parser.py -v
```

---

## Best Practices

### 1. Graceful Error Handling

Always return a valid dictionary, even on errors:

```python
try:
    # Parsing logic
    return {'functions': [...], 'classes': [...]}
except Exception as e:
    logger.error(f"Parse error: {e}")
    return {
        'functions': [],
        'classes': [],
        'parse_error': str(e)  # Include error for debugging
    }
```

### 2. Comment Removal

Remove comments before parsing to avoid false matches:

```python
def _remove_comments(self, content: str) -> str:
    # Language-specific comment patterns
    content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)  # Python
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)  # Java/JS
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Multi-line
    return content
```

### 3. Regex Performance

Use compiled patterns at module level:

```python
# At module level (compiled once)
FUNCTION_PATTERN = re.compile(r'...')

# In method (reuse compiled pattern)
def extract_functions(self, content: str):
    for match in FUNCTION_PATTERN.finditer(content):
        ...
```

### 4. Handle Edge Cases

Test with:
- Empty files
- Files with only comments
- Files with syntax errors
- Very large files (memory efficiency)
- Unicode and special characters

### 5. Document Regex Patterns

```python
# Function definition with optional decorators
# Example: @staticmethod\n    def func(x, y):
FUNCTION_PATTERN = re.compile(
    r'^\s*'                                   # Leading whitespace
    r'(?:((?:@\w+(?:\([^)]*\))?\s+)*))?'    # Optional decorators
    r'def\s+'                                 # def keyword
    r'(\w+)\s*'                               # Function name
    r'\(([^)]*)\)',                           # Parameters
    re.MULTILINE
)
```

---

## Performance Considerations

### Streaming for Large Files

For files >100k lines, consider chunking:

```python
def parse_large_file(self, file_path: Path, chunk_size: int = 1000) -> List[Dict]:
    """Parse large file in chunks."""
    results = []

    with open(file_path, 'r') as f:
        chunk = []
        for i, line in enumerate(f):
            chunk.append(line)
            if i % chunk_size == 0 and i > 0:
                content = ''.join(chunk)
                results.append(self.parse(content))
                chunk = []

    return results
```

### Regex Optimization

- Use `finditer()` instead of `findall()` for memory efficiency
- Avoid excessive backtracking in patterns
- Consider using a proper parser library for complex grammars (e.g., `tree-sitter`)

---

## Troubleshooting

### Parser Returns Empty Results

1. **Check regex patterns**: Test patterns in isolation with test strings
2. **Verify file encoding**: Ensure UTF-8 encoding
3. **Check for comment removal issues**: Make sure comments aren't breaking patterns

### Performance Issues

1. **Profile regex patterns**: Use `re.DEBUG` flag to see pattern compilation
2. **Consider AST parsing**: For complex languages, use language-specific parsers (e.g., `ast` for Python)
3. **Implement caching**: Cache parsed results if files are parsed multiple times

### False Matches

1. **Remove comments first**: Comments can trigger false positives
2. **Use stricter patterns**: Add more context to regex patterns
3. **Validate matches**: Add post-processing to filter invalid matches

---

## Next Steps

After creating your parser:

1. **Add artifact type**: See [Extending Artifact Types](extending-types.md) guide
2. **Update CLI**: Ensure new file types are discovered
3. **Test end-to-end**: Run full pipeline with new file type
4. **Document usage**: Update quickstart.md with examples

---

## Additional Resources

- **JavaParser Example**: `src/codeindex/parsers/java_parser.py` (400+ lines, comprehensive)
- **JSPParser Example**: `src/codeindex/parsers/jsp_parser.py` (simpler, 450 lines)
- **Unit Tests**: `tests/unit/test_parsers.py` (105 tests)
- **Regex Testing**: https://regex101.com (test patterns online)
