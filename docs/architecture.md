# Java Codebase Indexer - Architecture Documentation

**Version**: 1.0
**Last Updated**: 2025-12-14
**Status**: Production Ready

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Principles](#design-principles)

---

## System Overview

The Java Codebase Indexer is a production-ready pipeline that analyzes Java/JSP/GWT codebases, extracts semantic information using AI (Ollama), and enables natural language search over code artifacts through vector embeddings (Weaviate).

### Key Capabilities

- **Discover**: Scan directory trees, identify Maven projects, classify 6,750+ files
- **Extract**: AI-powered semantic understanding via Ollama (gemma3:12b)
- **Index**: Vector embeddings in Weaviate for semantic search
- **Search**: Natural language queries returning contextually relevant code
- **Monitor**: Health checks and statistics via status command

### Performance Characteristics

- **Discovery**: 17,967 files/second
- **Extraction**: ~50 files/minute (AI-limited)
- **Indexing**: ~975 artifacts/minute
- **Search**: <2 second response times
- **Memory**: <2GB for 100k files (streaming architecture)

---

## Architecture Layers

The system follows a clean, layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer                            │
│  (discover, extract, index, search, status commands)    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                  Service Layer                           │
│  - DiscoveryService    - ExtractionService              │
│  - IndexingService     - WeaviateStore                  │
│  - OllamaClient        - MavenParser                    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                  Parser Layer                            │
│  - JavaParser    - JSPParser                            │
│  - XMLParser     - SQLParser                            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                  Model Layer                             │
│  - Project       - CodeArtifact                         │
│  - Inventory     - ExtractionResult                     │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Infrastructure Layer                        │
│  - Config        - Logging                              │
│  - Retry         - Locking                              │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**CLI Layer** (`src/codeindex/cli/`)
- Command-line interface using Click framework
- Input validation and argument parsing
- Progress indicators and user feedback
- Output formatting (text and JSON)

**Service Layer** (`src/codeindex/services/`)
- Business logic orchestration
- External service integration (Weaviate, Ollama)
- Batch processing and concurrency management
- Error handling and retry logic

**Parser Layer** (`src/codeindex/parsers/`)
- File-type specific parsing logic
- Structural extraction (classes, methods, imports)
- Pattern matching with regex
- Framework detection

**Model Layer** (`src/codeindex/models/`)
- Domain entities (Project, CodeArtifact)
- Data transfer objects (Inventory, ExtractionResult)
- Enumerations (ArtifactType, LayerTag)
- Serialization/deserialization

**Infrastructure Layer** (`src/codeindex/utils/`)
- Cross-cutting concerns
- Configuration management
- Logging setup
- Retry decorators
- File locking

---

## Core Components

### 1. Discovery Service

**Purpose**: Scan directory trees and identify Maven projects

**Key Features**:
- Recursive directory traversal with exclusion patterns
- Maven POM parsing with fallback ID generation
- File classification by extension and path patterns
- Streaming architecture (generator-based)
- JSONL output format

**Class**: `DiscoveryService` in `src/codeindex/services/discovery.py`

**Main Methods**:
- `discover_projects()`: Find Maven projects in directory tree
- `scan_and_classify()`: Classify files by artifact type
- `generate_inventory()`: Create complete discovery inventory

**Performance**: 17,967 files/second on typical hardware

### 2. Extraction Service

**Purpose**: Extract semantic information using AI

**Key Features**:
- Ollama integration for AI summaries
- Concurrent processing with ThreadPoolExecutor
- Rate limiting (configurable MAX_CONCURRENT_AI_CALLS)
- Chunking support for large files (>100k lines)
- Graceful degradation if Ollama unavailable

**Class**: `ExtractionService` in `src/codeindex/services/extraction.py`

**Main Methods**:
- `extract_file()`: Extract single file
- `extract_batch()`: Process multiple files concurrently
- `_extract_structural()`: Parse file structure
- `_extract_semantic()`: Get AI-generated metadata

**Performance**: ~50 files/minute (Ollama-limited)

### 3. Indexing Service

**Purpose**: Store artifacts in Weaviate with vector embeddings

**Key Features**:
- Deterministic UUID generation (idempotent indexing)
- Batch operations (configurable batch size)
- Per-project locking (prevents concurrent modification)
- Schema validation and creation
- Error aggregation and reporting

**Class**: `IndexingService` in `src/codeindex/services/indexing.py`

**Main Methods**:
- `index_projects()`: Index project metadata
- `index_artifacts()`: Index code artifacts with embeddings
- `_dict_to_project()`: Convert inventory to Project model

**Performance**: ~975 artifacts/minute

### 4. Weaviate Store

**Purpose**: Vector database abstraction layer

**Key Features**:
- Connection pooling and health checks
- Schema management (Project, CodeArtifact classes)
- Batch operations with automatic commit
- Query builder for semantic search
- Statistics aggregation

**Class**: `WeaviateStore` in `src/codeindex/services/weaviate_store.py`

**Main Methods**:
- `connect()`: Establish connection with health check
- `create_schema()`: Deploy Project and CodeArtifact classes
- `index_artifacts_batch()`: Batch upsert with error handling
- `search()`: Semantic search with filters
- `get_statistics()`: Aggregate project/artifact counts

### 5. Ollama Client

**Purpose**: HTTP client for Ollama AI service

**Key Features**:
- Connection pooling (limits=10)
- Configurable timeouts (connect=10s, read=300s)
- Automatic retry with exponential backoff
- Rate limiting with semaphore
- JSON response parsing

**Class**: `OllamaClient` in `src/codeindex/services/ollama_client.py`

**Main Methods**:
- `generate()`: Get AI completion for prompt
- `health_check()`: Verify service availability
- `_call_with_retry()`: Retry wrapper with backoff

---

## Data Flow

### Complete Pipeline Flow

```
┌─────────────┐
│  User runs  │
│  discover   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Discovery Phase                                       │
│                                                          │
│  Source Directory                                        │
│       │                                                  │
│       ├─→ Find pom.xml files                            │
│       ├─→ Parse Maven coordinates                       │
│       ├─→ Classify files by type                        │
│       └─→ Generate inventory.jsonl                      │
│                                                          │
│  Output: discovery-inventory.jsonl                      │
│  Format: Line 1: Metadata                               │
│          Line 2+: Project records with file lists       │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Extraction Phase                                      │
│                                                          │
│  inventory.jsonl                                         │
│       │                                                  │
│       ├─→ For each file:                                │
│       │    ├─→ Read file content                        │
│       │    ├─→ Parse structure (classes, methods)       │
│       │    ├─→ Send to Ollama for AI summary           │
│       │    ├─→ Extract entities and tags                │
│       │    └─→ Detect frameworks                        │
│       │                                                  │
│       └─→ Generate extraction-results.jsonl             │
│                                                          │
│  Output: extraction-results.jsonl                       │
│  Format: Line 1: Metadata                               │
│          Line 2+: ExtractionResult per file             │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Indexing Phase                                        │
│                                                          │
│  inventory.jsonl + extraction-results.jsonl             │
│       │                                                  │
│       ├─→ Create Weaviate schema (if needed)            │
│       ├─→ For each project:                             │
│       │    └─→ Upsert Project record                    │
│       │                                                  │
│       └─→ For each artifact:                            │
│            ├─→ Generate deterministic UUID              │
│            ├─→ Create vector embedding                  │
│            └─→ Batch upsert to Weaviate                 │
│                                                          │
│  Output: Data in Weaviate                               │
│  Classes: Project, CodeArtifact                         │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Search Phase                                          │
│                                                          │
│  User query: "user authentication logic"                │
│       │                                                  │
│       ├─→ Convert query to vector embedding             │
│       ├─→ Semantic search in Weaviate                   │
│       ├─→ Apply filters (project, type, layer)          │
│       ├─→ Rank by similarity score                      │
│       └─→ Return top N results                          │
│                                                          │
│  Output: Ranked list of matching artifacts              │
└─────────────────────────────────────────────────────────┘
```

### Data Formats

**Discovery Inventory (JSONL)**
```json
{"scan_timestamp": "2025-12-14T10:00:00", "total_files": 539, ...}
{"project_id": "com.example:app:1.0", "files": [...], ...}
```

**Extraction Results (JSONL)**
```json
{"extraction_timestamp": "2025-12-14T10:05:00", "total_files": 539}
{"file_path": "/path/to/File.java", "summary": "...", "entities": [...], ...}
```

**Weaviate Schema**
- **Project**: Metadata about Maven project
- **CodeArtifact**: Individual file with vector embedding

---

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.8+ | Implementation |
| CLI Framework | Click | 8.0+ | Command-line interface |
| Vector DB | Weaviate | 1.32 | Semantic search |
| AI Model | Ollama/gemma3:12b | Latest | Semantic extraction |
| HTTP Client | httpx | 0.24+ | Ollama communication |
| XML Parser | lxml | 4.9+ | POM parsing |
| Testing | pytest | 7.4+ | Test framework |

### External Services

**Weaviate** (Port 8080)
- Deployed via Docker Compose
- Configured with text2vec-ollama module
- Persistent storage in weaviate-data/

**Ollama** (Port 11434)
- Local LLM inference
- gemma3:12b model (12B parameters)
- GPU acceleration recommended

### Development Tools

- **filelock**: Per-project locking
- **python-dotenv**: Configuration management
- **pytest-cov**: Code coverage reports
- **pytest-mock**: Test mocking

---

## Design Principles

### 1. Streaming Architecture

**Problem**: Large codebases (100k+ files) cause memory issues

**Solution**: Generator-based processing throughout
- Discovery yields files incrementally
- Extraction processes in batches
- Indexing uses streaming JSONL format

**Benefit**: <2GB memory usage regardless of codebase size

### 2. Idempotent Operations

**Problem**: Re-indexing creates duplicates

**Solution**: Deterministic UUIDs from content hashes
```python
uuid.uuid5(namespace, f"{project_id}:{file_path}:{content_hash}")
```

**Benefit**: Safe to re-run pipeline without data duplication

### 3. Graceful Degradation

**Problem**: External services (Ollama, Weaviate) may be unavailable

**Solution**: Fallback behavior at each layer
- Discovery: Works without any services
- Extraction: Falls back to structural parsing if Ollama down
- Indexing: Clear error messages with remediation steps

**Benefit**: Partial functionality always available

### 4. Configurable Concurrency

**Problem**: Different hardware capabilities

**Solution**: Tunable parameters
- `MAX_CONCURRENT_AI_CALLS`: Ollama concurrency (default: 10)
- `WEAVIATE_BATCH_SIZE`: Indexing batch size (default: 50)

**Benefit**: Adapts to available resources

### 5. Progress Transparency

**Problem**: Long-running operations appear stuck

**Solution**: Real-time progress indicators
- File counts and rates
- ETA calculations
- Batch progress tracking

**Benefit**: User confidence during long operations

### 6. Error Resilience

**Problem**: One bad file shouldn't fail entire pipeline

**Solution**: Continue-on-error with aggregation
- Log errors but continue processing
- Aggregate error counts by type
- Report summary at end

**Benefit**: Maximum data extraction even with some failures

---

## Project Structure

```
gha1javarag/
├── src/codeindex/           # Main package
│   ├── __main__.py          # CLI entry point
│   ├── cli/                 # Command implementations
│   │   ├── discover.py      # Discovery command
│   │   ├── extract.py       # Extraction command
│   │   ├── index.py         # Indexing command
│   │   ├── search.py        # Search command
│   │   └── status.py        # Status command
│   ├── services/            # Business logic
│   │   ├── discovery.py     # Directory scanning
│   │   ├── extraction.py    # AI semantic extraction
│   │   ├── indexing.py      # Weaviate indexing
│   │   ├── weaviate_store.py # Vector DB abstraction
│   │   ├── ollama_client.py # AI client
│   │   ├── maven.py         # POM parser
│   │   └── classifier.py    # File type detection
│   ├── parsers/             # Language parsers
│   │   ├── java_parser.py   # Java code parser
│   │   ├── jsp_parser.py    # JSP parser
│   │   ├── xml_parser.py    # XML config parser
│   │   └── sql_parser.py    # SQL parser
│   ├── models/              # Domain models
│   │   ├── project.py       # Project entity
│   │   ├── artifact.py      # CodeArtifact entity
│   │   ├── inventory.py     # Discovery result
│   │   └── extraction.py    # Extraction result
│   ├── schemas/             # Weaviate schemas
│   │   └── weaviate.py      # Schema definitions
│   └── utils/               # Utilities
│       ├── config.py        # Configuration
│       ├── logging.py       # Logging setup
│       ├── retry.py         # Retry decorator
│       ├── locking.py       # File locking
│       └── progress.py      # Progress indicators
├── tests/                   # Test suite
│   ├── unit/                # Unit tests (105 tests)
│   ├── integration/         # Integration tests
│   ├── e2e/                 # End-to-end tests
│   └── fixtures/            # Test data
├── docs/                    # Documentation
│   ├── architecture.md      # This file
│   ├── adding-parsers.md    # Parser development guide
│   └── extending-types.md   # Type extension guide
├── specs/                   # Feature specifications
│   └── 001-java-codebase-indexer/
│       ├── plan.md          # Technical plan
│       ├── tasks.md         # Task breakdown
│       └── data-model.md    # Data model
├── .env.example             # Configuration template
├── requirements.txt         # Python dependencies
├── docker-weaviate.sh       # Weaviate management
└── run.sh                   # Pipeline runner
```

---

## Next Steps

After understanding the architecture:

1. **Read [Adding New Parsers](adding-parsers.md)** to extend language support
2. **Read [Extending Artifact Types](extending-types.md)** to add new classifications
3. **Review [quickstart.md](../specs/001-java-codebase-indexer/quickstart.md)** for usage examples
4. **Explore [data-model.md](../specs/001-java-codebase-indexer/data-model.md)** for entity details

---

## Additional Resources

- **CLAUDE.md**: Implementation guidance and troubleshooting
- **Constitution**: `.specify/memory/constitution.md` - Development standards
- **Weaviate Schema**: `specs/001-java-codebase-indexer/contracts/weaviate-schema.yaml`
- **CLI Interface**: `specs/001-java-codebase-indexer/contracts/cli-interface.md`
