# Internal API Contracts

**Feature**: 007-gwt-navigation-and-error-fixes
**Purpose**: Document internal API contracts for new parsers and services

## Overview

This feature introduces new internal services and parsers for timeout handling, FK extraction, and GWT navigation analysis. These are **internal APIs** (not REST endpoints) used within the codeindex Python package.

## Key Internal Contracts

### 1. OllamaClient.extract_with_timeout()

**Purpose**: Extract semantic metadata from code using Ollama LLM with adaptive timeout and fallback.

**Contract**:
```python
async def extract_with_timeout(
    file_path: str,
    file_content: str,
    artifact_type: str,
    file_lines: int
) -> ExtractionResult:
    """
    Extract metadata with adaptive timeout and fallback.

    Args:
        file_path: Absolute path to source file
        file_content: Full source code content
        artifact_type: Type of artifact (service, dao, presenter, etc.)
        file_lines: Number of lines in file (for timeout calculation)

    Returns:
        ExtractionResult with metadata or fallback indicators

    Raises:
        ExtractionError: If both LLM and fallback fail
    """
```

**Behavior**:
- Calculate timeout: `base_timeout * (1 + file_lines / 1000)`
- Retry on timeout: 3 attempts with delays [5s, 15s, 45s]
- Fallback: Use StructuralAnalyzer if all retries fail
- Log metrics: timeout_duration, retry_count, fallback_used

---

### 2. StructuralAnalyzer.extract_basic_metadata()

**Purpose**: Extract basic structural metadata using Java AST parsing (no LLM).

**Contract**:
```python
def extract_basic_metadata(
    file_path: str,
    file_content: str
) -> Dict[str, Any]:
    """
    Extract structural metadata without LLM.

    Args:
        file_path: Absolute path to source file
        file_content: Full Java source code content

    Returns:
        Dict with basic metadata:
        - class_name: str
        - package: str
        - imports: List[str]
        - methods: List[str]
        - annotations: List[str]
        - super_class: Optional[str]
        - interfaces: List[str]

    Raises:
        ParseError: If Java AST parsing fails
    """
```

**Behavior**:
- Parse Java code using javalang library
- Extract only structural facts (no semantics)
- Fast (<100ms per file)
- No external dependencies (no Ollama required)

---

### 3. DBAnalyzer.extract_foreign_keys()

**Purpose**: Extract foreign key relationships from multiple sources with validation.

**Contract**:
```python
def extract_foreign_keys(
    dao_file_path: str,
    dao_content: str,
    ibatis_xml_path: Optional[str] = None
) -> List[ForeignKeyRelationship]:
    """
    Extract FK from Java annotations, iBATIS XML, and SQL JOIN statements.

    Args:
        dao_file_path: Absolute path to DAO Java file
        dao_content: Full DAO source code
        ibatis_xml_path: Optional path to iBATIS XML file

    Returns:
        List of ForeignKeyRelationship with source tracking

    Behavior:
        1. Collect all columns from Java annotations
        2. Extract FK from @JoinColumn annotations
        3. If iBATIS XML provided: Extract FK from <association> tags
        4. Parse SQL queries for JOIN ON clauses
        5. Validate FK columns exist in collected columns
        6. Merge FK from all sources (priority: Java > iBATIS > SQL)
        7. Return with source field (Java/iBATIS/SQL)
    """
```

**Validation Rules**:
- FK column must exist in collected columns
- Target column must exist (if known)
- Missing FK logs warning, doesn't fail analysis

---

### 4. IndexParser.extract_gwt_modules()

**Purpose**: Parse index.html/jsp files to extract GWT module references.

**Contract**:
```python
def extract_gwt_modules(
    index_file_path: str
) -> List[str]:
    """
    Extract GWT module references from index.html/jsp.

    Args:
        index_file_path: Absolute path to index.html or index.jsp

    Returns:
        List of GWT module names (e.g., ["app", "admin"])

    Behavior:
        1. Parse HTML using lxml.html (handles malformed HTML)
        2. XPath query: //script[@src] to find script tags
        3. Extract module name from src (e.g., app/app.nocache.js → "app")
        4. Regex fallback: Search for inline __gwt_activeModules
        5. JSP support: Parse <%@ include %> directives
    """
```

**Edge Cases**:
- Multiple modules: Return all found
- Malformed HTML: lxml recovery mode
- JSP variables: Extract pattern, log variable

---

### 5. GWTModuleParser.parse_module()

**Purpose**: Parse *.gwt.xml module descriptors using lxml XML parser.

**Contract**:
```python
def parse_module(
    module_xml_path: str
) -> GWTModule:
    """
    Parse GWT module descriptor XML file.

    Args:
        module_xml_path: Absolute path to *.gwt.xml file

    Returns:
        GWTModule with entry_points, inherits, source_paths

    Raises:
        ParseError: If XML is invalid

    Behavior:
        1. Parse XML using lxml.etree with namespaces
        2. XPath queries:
           - //entry-point/@class → entry point classes
           - //inherits/@name → inherited modules
           - //source/@path → source paths
        3. Handle missing elements gracefully (library modules may lack entry-point)
    """
```

**Edge Cases**:
- No entry-point: Library module (valid)
- Circular inherits: Caller must track visited
- Conditional inherits: Parse all, filter later

---

### 6. GWTNavigationAnalyzer.build_navigation_graph()

**Purpose**: Build complete navigation graph from index.html entry points.

**Contract**:
```python
def build_navigation_graph(
    index_file_path: str,
    source_dir: str
) -> NavigationGraph:
    """
    Build complete GWT navigation graph via BFS traversal.

    Args:
        index_file_path: Path to index.html/jsp
        source_dir: Root directory for source file resolution

    Returns:
        NavigationGraph with nodes and edges

    Behavior:
        1. Parse index.html → extract GWT module names
        2. For each module: Parse *.gwt.xml → extract entry-points
        3. BFS traversal:
           a. Dequeue current node (Presenter/Activity)
           b. If visited: skip (circular dependency)
           c. Mark visited
           d. Analyze node → extract navigation targets
           e. Extract bound View (Display pattern)
           f. Create NavigationNodes for targets
           g. Add edges (current → targets)
           h. Enqueue targets
        4. Return complete NavigationGraph
    """
```

**Performance**:
- In-memory LRU cache for parsed GWT modules (maxsize=256)
- Streaming node output (yield as discovered)
- Bounded memory: ~1MB peak

---

## Success Criteria

All contracts must:
- Use type hints for all parameters and return types
- Raise specific exceptions (not generic Exception)
- Log errors at appropriate levels (ERROR/WARNING/INFO/DEBUG)
- Include docstrings with Args, Returns, Raises, Behavior sections
- Handle edge cases gracefully (log warnings, don't crash)
- Be independently testable with unit tests

## Testing Requirements

Each contract must have:
- Unit tests for happy path
- Unit tests for edge cases (malformed input, missing files)
- Integration tests for end-to-end workflows
- Mock external dependencies (Ollama, file I/O) in unit tests
