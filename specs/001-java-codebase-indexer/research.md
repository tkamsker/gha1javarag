# Research: Java Codebase Indexer Pipeline

**Feature**: 001-java-codebase-indexer
**Date**: 2025-12-12
**Phase**: Phase 0 - Technology Research & Decisions

## Overview

This document captures key technology decisions and research findings for implementing the Java Codebase Indexer Pipeline. All decisions prioritize local execution, simplicity for AI-assisted development, and constitutional compliance.

## Technology Decisions

### 1. CLI Framework: Click 8.x

**Decision**: Use Click for CLI implementation

**Rationale**:
- Industry-standard Python CLI framework with excellent documentation
- Declarative command definition with decorators matches constitution's code quality requirements
- Built-in help generation, parameter validation, and type conversion
- Sub-command support perfect for pipeline stages (discover, extract, index, search, status)
- Progress bar support via click.progressbar() for user experience requirement
- Environment variable integration for configuration hierarchy

**Alternatives Considered**:
- argparse (stdlib): More verbose, manual help text, no progress bars
- typer: Newer, less ecosystem support, similar to Click but adds complexity
- fire: Too magical, harder to maintain for AI-assisted development

### 2. Vector Database Client: weaviate-client 4.x

**Decision**: Use weaviate-client v4 Python client

**Rationale**:
- Official Python client for Weaviate with type hints (constitution requirement)
- v4 introduces improved batch operations (performance requirement: 50+ objects/batch)
- Built-in connection pooling and error handling
- Schema management API for Project and CodeArtifact classes
- Supports filtering queries by project ID (multi-project requirement)
- Native vector search with hybrid capabilities

**Alternatives Considered**:
- Direct REST API calls: More code, manual connection handling, no type safety
- weaviate-client v3: Older API, less efficient batching
- Other vector DBs (Pinecone, Qdrant): Require different deployment, not already chosen per spec

**Implementation Notes**:
- Use `client.batch.configure()` for batch size configuration
- Implement connection health checks before operations (constitution gate requirement)
- Use context managers for proper connection cleanup

### 3. Ollama Communication: httpx

**Decision**: Use httpx for Ollama HTTP API communication

**Rationale**:
- Modern HTTP client with async support (future scalability)
- Type hints throughout (constitution requirement)
- Connection pooling built-in (rate limiting requirement: 10 concurrent)
- Timeout configuration for long AI operations
- Better error messages than requests library
- HTTP/2 support for future optimization

**Alternatives Considered**:
- requests: Synchronous only, no connection limit built-in
- aiohttp: Async-first complicates initial implementation
- urllib3: Too low-level, more boilerplate

**Implementation Notes**:
- Create client with `limits=httpx.Limits(max_connections=10)` for rate limiting
- Set appropriate timeouts (connect=10s, read=300s for AI operations)
- Implement retry decorator for transient failures

### 4. POM Parsing: lxml

**Decision**: Use lxml for XML/POM parsing

**Rationale**:
- Fast C-based parser (performance requirement: 1000+ files/second)
- XPath support for extracting Maven coordinates
- Handles malformed XML gracefully (edge case requirement)
- Well-documented, industry standard
- Memory-efficient streaming parser available for large POMs

**Alternatives Considered**:
- xml.etree (stdlib): Slower, less robust with malformed XML
- BeautifulSoup: Overkill, designed for HTML not structured XML
- xmltodict: Converts to dict but loses structure, harder to query

**Implementation Notes**:
- Use `etree.parse()` with error handling for malformed files
- XPath queries like `//groupId/text()` for Maven coordinates
- Fall back to manual parsing if XPath fails

### 5. Configuration Management: python-dotenv

**Decision**: Use python-dotenv for .env file loading

**Rationale**:
- Simple, focused library for .env file parsing
- Doesn't override existing environment variables (respects hierarchy)
- Zero dependencies, minimal attack surface
- Industry standard pattern

**Alternatives Considered**:
- Manual file parsing: More code, error-prone
- pydantic-settings: Overkill for simple config, adds dependency weight
- ConfigParser: INI format not as common as .env

**Implementation Notes**:
- Load early in CLI entry point with `load_dotenv(override=False)`
- Create .env.example with documented variables
- Validate required variables at startup (JAVA_SOURCE_DIR, etc.)

### 6. Testing Framework: pytest

**Decision**: Use pytest with fixtures for all test types

**Rationale**:
- Industry standard with excellent plugin ecosystem
- Fixture system perfect for test isolation (constitution requirement)
- Markers for slow tests (`@pytest.mark.slow`)
- Parameterized tests for edge cases
- Coverage reporting integration (>80% requirement)
- Mock/patch support via pytest-mock

**Alternatives Considered**:
- unittest (stdlib): More verbose, less flexible fixtures
- nose: Unmaintained
- pytest is already project standard per existing conftest.py

**Implementation Notes**:
- Use fixtures for mock Ollama responses, test Weaviate collections
- Separate fixture files for unit, integration, e2e
- Configure pytest.ini with markers and coverage thresholds

### 7. Progress Tracking: Rich (or click.progressbar)

**Decision**: Start with click.progressbar, evaluate Rich later

**Rationale**:
- click.progressbar() built into Click framework (minimal dependencies)
- Meets requirement: progress updates every 10 seconds
- Can show percentage, ETA, items processed
- Rich adds beautiful formatting but increases complexity

**Alternatives Considered**:
- tqdm: Another dependency, similar to click.progressbar
- Rich: Full TUI framework, may be overkill for phase 1
- Manual progress logging: Harder to format consistently

**Implementation Notes**:
- Wrap file iteration with `click.progressbar(files, label="Processing")`
- Update every N items processed (configurable, default 100)
- Include elapsed time and ETA in output

### 8. File System Operations: pathlib + os.walk

**Decision**: Use pathlib for paths, os.walk for discovery

**Rationale**:
- pathlib provides type-safe path operations (constitution requirement)
- os.walk is fastest for recursive directory traversal (performance requirement)
- Both stdlib, no dependencies
- Cross-platform (Windows, macOS, Linux)

**Alternatives Considered**:
- glob.glob recursive: Slower than os.walk for deep trees
- scandir: Lower-level, more code
- third-party like pathtools: Unnecessary dependency

**Implementation Notes**:
- Use `os.walk()` for discovery, convert to `Path` objects for processing
- Filter by extension early to avoid stat() calls on irrelevant files
- Stream results rather than building full list (memory requirement)

### 9. Concurrency: Threading with Semaphore

**Decision**: Use threading with Semaphore for AI request rate limiting

**Rationale**:
- Python threading sufficient for I/O-bound operations (AI calls, Weaviate)
- Semaphore provides clean rate limiting (max 10 concurrent)
- Simpler than asyncio for phase 1
- GIL not a bottleneck for network I/O

**Alternatives Considered**:
- asyncio: More complex, bigger refactor if needed later
- multiprocessing: Overkill for I/O, process overhead
- No concurrency: Too slow for 50+ files/minute requirement

**Implementation Notes**:
- ThreadPoolExecutor with max_workers=10 (configurable via env)
- Semaphore(10) for Ollama request limiting
- Queue for batching Weaviate operations across threads

### 10. Project Locking: filelock

**Decision**: Use filelock library for per-project locking

**Rationale**:
- Simple file-based locking (works across process boundaries)
- Supports timeout and non-blocking acquire
- Cross-platform (NFS-safe on POSIX, works on Windows)
- Small, focused library

**Alternatives Considered**:
- Manual lock files: Race conditions, cleanup issues
- Database-based locking: Requires shared DB, overengineered
- No locking: Data corruption risk per clarification

**Implementation Notes**:
- Lock file: `.codeindex-{project_id}.lock` in temp directory
- Context manager usage: `with FileLock(lock_path, timeout=5)`
- Clear error message if lock acquisition fails

## Architecture Patterns

### Streaming Architecture

**Pattern**: Generator-based processing pipeline

**Rationale**:
- Memory requirement: <2GB for 100k files
- Discovery yields file paths incrementally
- Extraction processes in batches, doesn't accumulate all results
- Indexing batches objects to Weaviate without holding all in memory

**Implementation**:
```python
def discover_files(root_dir: Path) -> Generator[Path, None, None]:
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if is_relevant_extension(filename):
                yield Path(dirpath) / filename
```

### Retry Logic Pattern

**Pattern**: Exponential backoff decorator

**Rationale**:
- Constitution requirement: retry with exponential backoff
- Centralized retry logic reduces duplication
- Configurable max attempts and delays

**Implementation**:
```python
@retry(max_attempts=3, base_delay=1.0, max_delay=30.0)
def call_ollama(prompt: str) -> dict:
    response = httpx_client.post(...)
    response.raise_for_status()
    return response.json()
```

### Idempotent Indexing Pattern

**Pattern**: Deterministic UUID generation for Weaviate objects

**Rationale**:
- Requirement: idempotent indexing (FR-012)
- UUID v5 (deterministic) from project_id + file_path + content_hash
- Weaviate upserts based on UUID

**Implementation**:
```python
import uuid
def generate_artifact_id(project_id: str, path: str, hash: str) -> str:
    namespace = uuid.UUID('00000000-0000-0000-0000-000000000001')
    key = f"{project_id}:{path}:{hash}"
    return str(uuid.uuid5(namespace, key))
```

## Unresolved Items

None - all technical decisions resolved based on feature spec and clarifications.

## Next Steps

Proceed to Phase 1:
1. Design detailed data model (data-model.md)
2. Define Weaviate schema contracts (contracts/weaviate-schema.yaml)
3. Define CLI interface contracts (contracts/cli-interface.md)
4. Create quickstart guide (quickstart.md)
5. Update agent context (CLAUDE.md)
