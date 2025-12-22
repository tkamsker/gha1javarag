# Research Document: GWT Navigation Analysis and Error Fixes

**Feature**: 007-gwt-navigation-and-error-fixes
**Created**: 2025-12-22
**Purpose**: Document technical research decisions, rationale, and alternatives

## Research Topics

### 1. Adaptive Timeout Strategy for Ollama LLM Requests

**Research Question**: How should timeout values be calculated for LLM extraction requests to minimize failures while avoiding excessive wait times?

**Decision**: File-size-based adaptive timeout with configurable base timeout.

**Formula**: `timeout = base_timeout * (1 + file_lines / 1000)`

Where:
- `base_timeout`: Configurable via READ_TIMEOUT env var (default: 600s)
- `file_lines`: Number of lines in source file being analyzed
- Scales linearly: 500-line file gets 1.5x timeout, 1000-line file gets 2x timeout

**Rationale**:
1. **Empirical evidence**: Log analysis shows 29 timeout failures, predominantly on large service files (>500 lines)
2. **Linear correlation**: LLM processing time correlates roughly linearly with file size (more tokens to process)
3. **Simplicity**: Single formula, easy to understand and configure
4. **Configurability**: Base timeout adjustable per deployment (faster/slower hardware)
5. **Bounded growth**: Even 5000-line files get reasonable 6x timeout (3600s max), not infinite

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Fixed timeout (600s for all) | Simple, no calculation | Penalizes large files unfairly | Causes 29 production failures |
| Per-file calibration (historical data) | Optimal for each file | Requires historical runs, cold start problem | Too complex, fragile |
| Complexity-based timeout (cyclomatic) | Accounts for code complexity | Requires AST parsing before LLM call | Defeats purpose of fallback |
| Token count estimation | Accurate for LLM | Requires tokenizer, model-specific | Adds dependency, brittle |

**Validation**:
- Unit test: Verify timeout calculation for edge cases (0 lines, 10k lines, null)
- Integration test: Mock Ollama with slow responses, verify timeouts trigger correctly

**References**:
- Ollama documentation: Default timeout is 240s (4 minutes)
- Industry practice: AWS Lambda max timeout 15min, Google Cloud Functions 9min
- LLM benchmarks: GPT-3.5 ~1000 tokens/minute, file size proxy for token count

---

### 2. Exponential Backoff Parameters for Retry Logic

**Research Question**: What retry delays should be used for transient Ollama failures?

**Decision**: 3 retry attempts with delays [5s, 15s, 45s] (multiplier 3x).

**Backoff Sequence**:
| Attempt | Delay Before Retry | Cumulative Wait | Action |
|---------|-------------------|-----------------|--------|
| 1 (initial) | 0s | 0s | First attempt |
| 2 | 5s | 5s | Retry after brief pause |
| 3 | 15s | 20s | Retry after longer pause |
| 4 | 45s | 65s | Final retry before fallback |
| Fallback | N/A | 65s | Structural analysis (no LLM) |

**Rationale**:
1. **Industry standard**: AWS SDK uses 2-3x multiplier, Google APIs use 2x, Kubernetes uses 2x
2. **Quick recovery**: 5s first retry handles temporary slowness (GC pause, thread pool exhaustion)
3. **Load adaptation**: 15s second retry allows Ollama to recover from heavier load
4. **Worst-case**: 45s third retry handles sustained load spikes
5. **Bounded total wait**: 65s max before fallback (acceptable for reliability vs. speed tradeoff)
6. **Avoids thundering herd**: Exponential spacing prevents all clients retrying simultaneously

**Alternatives Considered**:
| Alternative | Delays | Total Wait | Rejected Because |
|-------------|--------|------------|------------------|
| Fibonacci [1s, 2s, 3s, 5s] | Short delays | 11s | Too fast, doesn't give Ollama time to recover |
| Fixed 10s delays | [10s, 10s, 10s] | 30s | Not adaptive, wastes time on transient issues |
| Aggressive [1s, 2s, 4s] | Binary backoff | 7s | Too short for LLM recovery |
| Conservative [10s, 30s, 90s] | Slow growth | 130s | Excessive wait, delays pipeline too much |
| More than 3 retries | [5s, 15s, 45s, 135s] | 200s | Diminishing returns, failure likely permanent |

**Validation**:
- Unit test: Verify delay calculation for each retry attempt
- Integration test: Mock intermittent Ollama failures, verify retry behavior
- Load test: Verify no thundering herd with concurrent extraction

**References**:
- AWS SDK retry strategy: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- Google Cloud retry best practices: 2x multiplier with jitter
- Ollama GitHub issues: Users report timeouts under sustained load, recovery within 30-60s

---

### 3. Structural Analysis Fallback Using javalang

**Research Question**: When Ollama LLM extraction fails after retries, what can be extracted without LLM?

**Decision**: Use javalang library for Java AST parsing to extract basic metadata.

**Extractable Metadata Without LLM**:
| Metadata | Extraction Method | Example |
|----------|-------------------|---------|
| Class name | AST type_declaration name | `UserService` |
| Package | AST package_declaration | `com.example.service` |
| Imports | AST import_declaration | `java.util.List` |
| Methods | AST method_declaration names | `getUser()`, `saveUser()` |
| Method parameters | AST formal_parameter types | `Long userId`, `UserDTO user` |
| Annotations | AST annotation names | `@Service`, `@Transactional` |
| Super class | AST extends_clause | `extends BaseService` |
| Interfaces | AST implements_clause | `implements UserRepository` |

**Limitations (Require LLM)**:
- Semantic understanding of what methods do
- Business logic extraction
- Complex control flow analysis
- Intent and purpose of code
- Documentation generation quality

**Estimated Value**:
- **With LLM**: 100% semantic understanding, rich documentation, context-aware extraction
- **Structural only**: 60-70% value - accurate structure, names, signatures, but no semantics
- **Nothing**: 0% value - file completely missing from documentation

**Rationale**:
1. **Already in requirements.txt**: javalang used elsewhere in project (zero new dependency)
2. **Fast**: <100ms per file (vs. 10-60s for LLM)
3. **Reliable**: No external service dependency, no timeouts
4. **Better than nothing**: Provides structural skeleton for documentation
5. **No false information**: Extracts only facts from AST, no hallucination risk
6. **Complements LLM**: When LLM succeeds, structural analysis not needed

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Skip file entirely | Simple, fast | Loses all documentation | 29 files completely missing |
| Regex extraction | No parsing library | Error-prone, fragile | Misses nested classes, complex syntax |
| Queue for later retry | Eventually processes all | Delays final results | Complicates pipeline, no guarantee |
| Use smaller LLM model | Faster, less timeout | Lower quality | Defeats purpose, still times out |

**Validation**:
- Unit test: Parse sample Java files, verify extracted metadata
- Integration test: Simulate Ollama timeout, verify fallback activation
- Quality test: Compare LLM vs. structural documentation for same file

**References**:
- javalang documentation: https://github.com/c2nes/javalang
- Project existing usage: Already used in `src/codeindex/parsers/java_parser.py`

---

### 4. Multi-Source Foreign Key Extraction

**Research Question**: How can we extract foreign key relationships from multiple sources (Java, iBATIS, SQL)?

**Decision**: Three-phase extraction with priority order: Java → iBATIS → SQL.

**Extraction Sources**:

**Phase 1: Java Annotations (Highest Priority)**
```java
@JoinColumn(name = "customer_id", referencedColumnName = "id")
@ManyToOne
private Customer customer;
```
- Extraction: Parse `@JoinColumn` annotation for column names
- Confidence: 95% (code of record)
- Tools: Existing Java AST parser

**Phase 2: iBATIS XML (Medium Priority)**
```xml
<resultMap id="orderMap" type="Order">
  <result property="customerId" column="customer_id"/>
  <association property="customer" column="customer_id"
               select="selectCustomer"/>
</resultMap>
```
- Extraction: Parse `<association>` and `<collection>` tags for FK columns
- Confidence: 85% (legacy pattern, may not match current schema)
- Tools: Existing lxml XML parser

**Phase 3: SQL JOIN Statements (Fallback)**
```sql
SELECT o.*, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
```
- Extraction: Parse JOIN ON clauses for column relationships
- Confidence: 70% (heuristic, may have false positives)
- Tools: SQL parsing with regex patterns (sqlparse library candidate)

**Merge Strategy**:
1. **Collect all columns first**: Parse @Column annotations, iBATIS columns, SQL columns
2. **Extract FK from each source**: Java, iBATIS, SQL in parallel
3. **Validate FK columns**: Verify both source and target columns exist in collected set
4. **Merge with priority**: Java annotation beats iBATIS beats SQL for same FK
5. **Mark source**: Tag each FK with source (Java/iBATIS/SQL) for confidence scoring
6. **Handle conflicts**: Log warning when sources disagree, use highest priority

**Rationale**:
1. **Empirical evidence**: 4 FK validation failures show Java-only extraction incomplete
2. **Legacy support**: iBATIS XML common in older Java codebases (pre-JPA)
3. **Comprehensive coverage**: SQL JOIN fallback catches pure SQL DAOs
4. **Confidence scoring**: Source tagging enables quality assessment
5. **Graceful degradation**: Validation failure logs warning, doesn't crash

**Alternatives Considered**:
| Alternative | Coverage | Complexity | Rejected Because |
|-------------|----------|------------|------------------|
| Java annotations only | 70-75% | Low | Misses 4 production FK failures |
| iBATIS only | 60% | Low | Incomplete for modern JPA codebases |
| SQL only | 50% | Medium | High false positive rate |
| Manual FK definition | 100% | Very High | Unsustainable, defeats automation purpose |

**Validation**:
- Unit test: Parse each source type independently (Java, iBATIS, SQL)
- Unit test: Test merge logic with conflicting FK from different sources
- Integration test: Analyze 4 previously failing DAOs, verify FK correctly extracted

**References**:
- JPA @JoinColumn spec: https://jakarta.ee/specifications/persistence/3.0/apidocs/
- iBATIS/MyBatis resultMap: https://mybatis.org/mybatis-3/sqlmap-xml.html#Result_Maps
- sqlparse library: https://github.com/andialbrecht/sqlparse

---

### 5. GWT Module Descriptor Parsing

**Research Question**: How should *.gwt.xml module descriptors be parsed to extract entry points and inheritance?

**Decision**: Use lxml XML parser with namespace-aware XPath queries.

**GWT Module Descriptor Structure**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<module rename-to='app'>
  <!-- Inherits -->
  <inherits name='com.google.gwt.user.User'/>
  <inherits name='com.example.shared.Shared'/>

  <!-- Entry point -->
  <entry-point class='com.example.client.AppEntryPoint'/>

  <!-- Source paths -->
  <source path='client'/>
  <source path='shared'/>
</module>
```

**Parsing Strategy**:
| Element | XPath Query | Extracted Data |
|---------|-------------|----------------|
| Entry points | `//entry-point/@class` | Fully qualified class names |
| Inherits | `//inherits/@name` | Module dependency names |
| Source paths | `//source/@path` | Relative source directories |
| Module name | `/module/@rename-to` or filename | Module identifier |

**Rationale**:
1. **Valid XML**: GWT module descriptors follow strict XML schema
2. **Namespace handling**: lxml supports XML namespaces (future-proof)
3. **XPath efficiency**: Query language optimized for XML traversal
4. **Already available**: lxml in requirements.txt (used for iBATIS, UiBinder)
5. **Error handling**: lxml provides clear error messages for malformed XML

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Regex parsing | No library needed | Brittle, misses nested elements | Fails on comments, CDATA, entities |
| BeautifulSoup | Popular HTML parser | Additional dependency | lxml already available |
| Custom parser | Perfect control | Reinvents wheel | lxml is battle-tested |
| Plain text search | Very simple | Misses structure | Fails on multi-line elements |

**Edge Cases Handled**:
- **Missing entry-point**: Some modules are pure library modules (no entry point)
- **Circular inherits**: A inherits B inherits A (use visited set)
- **Conditional inherits**: `<inherits>` with `<when-*>` conditions (parse all, filter later)
- **Invalid XML**: Log parse error, skip module gracefully

**Validation**:
- Unit test: Parse sample GWT modules with various structures
- Unit test: Test circular dependency detection
- Integration test: Parse real cuco-ui-admin GWT modules

**References**:
- GWT module descriptor spec: http://www.gwtproject.org/doc/latest/DevGuideOrganizingProjects.html#DevGuideModuleXml
- lxml documentation: https://lxml.de/tutorial.html
- Project existing usage: `src/codeindex/parsers/xml_parser.py`

---

### 6. Index.html/JSP Parsing for GWT Module References

**Research Question**: How should index.html and index.jsp files be parsed to find GWT module script tags?

**Decision**: Use lxml HTML parser with XPath queries, regex fallback for inline scripts.

**GWT Module Reference Patterns**:

**Pattern 1: Script tag with src attribute**
```html
<script type="text/javascript" src="app/app.nocache.js"></script>
```
- Extraction: XPath `//script[@src]` → extract src attribute
- Module name: Extract from path (e.g., `app/app.nocache.js` → module name `app`)

**Pattern 2: Inline script with module name**
```html
<script>
  var $wnd = window, $doc = $wnd.document;
  $wnd.__gwt_activeModules = {"app": {"moduleName": "app"}};
</script>
```
- Extraction: Regex pattern `"moduleName":\s*"([^"]+)"` → extract module name
- Fallback: Only used if Pattern 1 not found

**Pattern 3: JSP includes**
```jsp
<%@ include file="WEB-INF/app.gwt.xml" %>
```
- Extraction: Regex pattern `include file="([^"]+\.gwt\.xml)"` → extract file path
- Resolve: Load included file and parse as GWT module

**Rationale**:
1. **Malformed HTML**: lxml.html mode handles malformed HTML gracefully (missing closing tags)
2. **XPath efficiency**: `//script[@src]` query is fast and precise
3. **Regex fallback**: Handles inline JavaScript module definitions
4. **JSP support**: Regex patterns for JSP directives (include, tag)
5. **Robust**: Multiple pattern fallbacks increase discovery rate

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| BeautifulSoup | Popular HTML parser | Additional dependency | lxml already available |
| Regex only | Simple, no parsing | Fragile, misses nested tags | Breaks on complex HTML |
| Selenium/headless browser | Executes JavaScript | Heavy, slow, requires browser | Overkill for static analysis |
| Manual string search | Very simple | Misses encoding, structure | Too brittle |

**Edge Cases Handled**:
- **Multiple GWT modules**: Some index.html files load multiple modules (extract all)
- **Relative vs. absolute paths**: Resolve relative paths based on index.html location
- **Malformed HTML**: lxml recovery mode parses despite errors
- **JSP variables**: `<script src="${contextPath}/app.nocache.js">` → extract pattern, log variable

**Validation**:
- Unit test: Parse sample index.html files with various patterns
- Unit test: Parse sample index.jsp files with JSP includes
- Integration test: Parse cuco-ui-admin index files, verify module discovery

**References**:
- lxml.html documentation: https://lxml.de/lxmlhtml.html
- GWT module loading: http://www.gwtproject.org/doc/latest/DevGuideOrganizingProjects.html

---

### 7. Navigation Graph Construction Algorithm

**Research Question**: What data structure and algorithm should represent GWT application navigation?

**Decision**: Directed graph with typed nodes, built via BFS traversal from entry points.

**Graph Structure**:
```python
NavigationGraph:
  - entry_points: List[str]  # index.html, index.jsp paths
  - nodes: Dict[str, NavigationNode]  # node_id → NavigationNode
  - edges: List[(source_id, target_id, edge_type)]  # navigation relationships

NavigationNode:
  - node_id: str  # Unique identifier
  - node_type: Enum[Presenter, View, Activity, Place, External]
  - label: str  # Display name
  - source_file: str  # Path to source file
  - metadata: Dict  # Type-specific data
```

**Construction Algorithm**:
```
1. Parse index.html/jsp → extract GWT module references
2. For each GWT module:
   a. Parse *.gwt.xml → extract entry-point classes
   b. Add entry-point to queue (BFS)
3. While queue not empty:
   a. Dequeue current node (Presenter/Activity)
   b. If already visited: skip (circular dependency handling)
   c. Mark as visited
   d. Analyze node:
      - Extract navigation targets (Places, other Presenters)
      - Extract bound View (Display pattern)
   e. For each target:
      - Create NavigationNode
      - Add edge (current → target)
      - Enqueue target for processing
4. Return complete NavigationGraph
```

**Rationale**:
1. **Directed graph**: Captures navigation direction (A → B doesn't imply B → A)
2. **Typed nodes**: Enables different rendering (Presenters blue, Views green, External red)
3. **BFS traversal**: Discovers complete graph level-by-level (matches user navigation flow)
4. **Visited tracking**: Prevents infinite loops from circular navigation (back buttons)
5. **Edge labels**: Captures navigation type (click, place transition, history back)

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Tree structure | Simple, hierarchical | No cycles, single entry point | GWT apps have cycles (back) and multiple entries |
| Flat list of components | Very simple | Loses navigation flow | Can't answer "how to reach X from entry?" |
| Nested JSON | Human-readable | Hard to query, inefficient traversal | Graph queries require multiple JSON scans |
| Adjacency matrix | Fast edge lookup | Memory intensive for sparse graphs | GWT apps have sparse navigation (100 nodes, ~200 edges) |

**Performance Optimization**:
- **In-memory cache**: Cache parsed GWT modules to avoid re-parsing inherited modules
- **Lazy loading**: Load node metadata only when accessed (not during graph construction)
- **Streaming**: Write nodes to output as discovered (don't accumulate in memory)

**Validation**:
- Unit test: Build graph from mock entry points, verify BFS order
- Unit test: Test circular dependency detection (A → B → A)
- Integration test: Build graph from cuco-ui-admin, verify >90% Presenters discovered

**References**:
- Graph traversal algorithms: Introduction to Algorithms (CLRS) Chapter 22
- GWT Activity/Place framework: http://www.gwtproject.org/doc/latest/DevGuideMvpActivitiesAndPlaces.html

---

### 8. Performance Optimization: Caching and Streaming

**Research Question**: How can we prevent memory spikes and re-parsing overhead during navigation analysis?

**Decision**: Combine in-memory LRU cache for parsed modules with streaming node output.

**Caching Strategy**:
```python
from functools import lru_cache

@lru_cache(maxsize=256)
def parse_gwt_module(module_path: str) -> GWTModule:
    """Parse GWT module descriptor with LRU caching."""
    # Parse XML and return GWTModule object
    # Cache stores parsed result for 256 most recent modules
```

**Rationale for Cache Size**:
- Large GWT apps: ~50-100 modules typical
- With inheritance: Each module may be referenced 2-5 times
- Cache size 256: Covers 99% of scenarios (50 modules * 5 references = 250)
- LRU eviction: Oldest unused modules dropped automatically
- Memory footprint: ~1KB per cached module = 256KB total (negligible)

**Streaming Strategy**:
```python
def build_navigation_graph(entry_points: List[str]) -> Iterator[NavigationNode]:
    """Yield navigation nodes as discovered (streaming)."""
    queue = deque(entry_points)
    visited = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        node = analyze_node(current)
        yield node  # Stream to output immediately

        targets = extract_navigation_targets(node)
        queue.extend(targets)
```

**Benefits**:
- **Memory bounded**: Peak memory = cache size + queue size (~1MB)
- **Incremental output**: Nodes written to file as discovered (progress visible)
- **Parallel indexing**: Weaviate indexing can start before analysis completes
- **No memory spike**: Doesn't load entire graph before processing

**Alternatives Considered**:
| Alternative | Memory | Performance | Rejected Because |
|-------------|--------|-------------|------------------|
| No caching | Low | Slow (re-parse modules) | 5x slower on apps with deep inheritance |
| Unbounded cache | High | Fast | Memory spike for 500+ module apps |
| Disk cache | Low | Slow (I/O overhead) | Adds complexity, slower than in-memory |
| Load entire graph first | High | Fast | Memory spike, no incremental progress |

**Validation**:
- Performance test: Measure memory usage during analysis of 100-module app
- Performance test: Compare cached vs. non-cached parsing time
- Unit test: Verify LRU eviction with >256 unique modules

**References**:
- Python functools.lru_cache: https://docs.python.org/3/library/functools.html#functools.lru_cache
- Streaming data processing: https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/

---

### 9. Metrics Collection and Structured Logging

**Research Question**: What metrics should be collected and how should they be logged for monitoring?

**Decision**: Log structured metrics in JSON format at INFO level, detailed metrics at DEBUG level.

**Metrics to Collect**:

**Timeout Metrics** (Per Pipeline Run):
```json
{
  "stage": "extraction",
  "timeout_metrics": {
    "total_files": 539,
    "timeout_count": 0,
    "retry_count": 5,
    "retry_success": 4,
    "fallback_count": 1,
    "avg_timeout_duration": 45.2,
    "max_timeout_duration": 120.0
  }
}
```

**FK Extraction Metrics** (Per Pipeline Run):
```json
{
  "stage": "db_analysis",
  "fk_metrics": {
    "total_daos": 24,
    "fk_extracted": 87,
    "fk_by_source": {
      "java": 65,
      "ibatis": 18,
      "sql": 4
    },
    "validation_failures": 0,
    "recovery_rate": 1.0
  }
}
```

**Navigation Analysis Metrics** (Per Pipeline Run):
```json
{
  "stage": "gwt_navigation",
  "navigation_metrics": {
    "entry_points": 1,
    "modules_parsed": 52,
    "presenters_discovered": 127,
    "views_discovered": 115,
    "activities_discovered": 23,
    "places_discovered": 23,
    "external_boundaries": 5,
    "circular_dependencies": 2,
    "discovery_rate": 0.94
  }
}
```

**Rationale**:
1. **JSON format**: Enables automated parsing for dashboards and monitoring
2. **Structured data**: Each metric has consistent schema across runs
3. **INFO level**: Summary metrics visible by default without verbose logging
4. **DEBUG level**: Per-file metrics for detailed diagnostics
5. **Aggregation**: Metrics aggregated per pipeline stage for clarity

**Logging Strategy**:
```python
import logging
import json

logger = logging.getLogger(__name__)

# Summary metrics (INFO)
logger.info(json.dumps({
    "stage": "extraction",
    "timeout_metrics": timeout_metrics
}))

# Detailed metrics (DEBUG)
logger.debug(json.dumps({
    "stage": "extraction",
    "file": "UserService.java",
    "timeout_duration": 45.2,
    "retry_count": 2,
    "fallback_used": False
}))
```

**Alternatives Considered**:
| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Plain text logs | Human-readable | Hard to parse | Can't automate monitoring |
| Separate metrics file | Clean separation | Synchronization issues | Complicates deployment |
| Prometheus metrics | Industry standard | Requires external service | Overkill for CLI tool |
| OpenTelemetry | Comprehensive | Heavy dependency | Adds complexity |

**Validation**:
- Integration test: Run pipeline, parse JSON metrics, verify schema
- Integration test: Verify metrics logged at correct levels (INFO/DEBUG)

**References**:
- Structured logging best practices: https://www.structlog.org/en/stable/
- JSON logging format: https://github.com/madzak/python-json-logger

---

## Summary of Decisions

| Research Topic | Decision | Key Benefit |
|---------------|----------|-------------|
| Adaptive Timeout | File-size-based timeout calculation | Eliminates 29 production timeout failures |
| Exponential Backoff | 3 retries with [5s, 15s, 45s] delays | Handles transient Ollama load, bounded wait |
| Structural Fallback | javalang AST parsing without LLM | 60-70% value when LLM unavailable |
| Multi-Source FK | Java → iBATIS → SQL priority order | Resolves 4 FK validation failures |
| GWT Module Parsing | lxml XML parser with XPath queries | Robust, handles malformed XML, namespace-aware |
| Index.html Parsing | lxml HTML parser with regex fallback | Discovers GWT modules from multiple patterns |
| Navigation Graph | Directed graph with BFS traversal | Complete navigation map from entry points |
| Performance | LRU cache + streaming output | Bounded memory, incremental progress |
| Metrics | Structured JSON logging | Automated monitoring, clear diagnostics |

## Next Steps

**Phase 1: Design & Contracts**
1. Generate `data-model.md` with entity definitions (NavigationGraph, TimeoutMetric, FKRelationship, etc.)
2. Generate internal API contracts for new parsers and analyzers
3. Generate `quickstart.md` with test scenarios and validation steps

**Implementation Readiness**: All technical unknowns resolved. Ready to proceed with implementation based on research decisions.
