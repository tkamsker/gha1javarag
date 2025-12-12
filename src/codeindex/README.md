# Java Codebase Indexer Pipeline

Python CLI pipeline for discovering, analyzing, and indexing Java codebases with AI-powered semantic understanding.

## Module Structure

```
codeindex/
├── __init__.py           # Package initialization
├── __main__.py           # CLI entry point (main command group)
├── cli/                  # CLI command implementations
│   ├── discover.py       # Discover Maven projects and create inventory
│   ├── extract.py        # Extract semantic understanding with AI
│   ├── index.py          # Index artifacts to Weaviate
│   ├── search.py         # Semantic search over indexed data
│   └── status.py         # Show indexing status and statistics
├── models/               # Data models and entities
│   ├── project.py        # Project entity
│   ├── artifact.py       # CodeArtifact entity
│   ├── inventory.py      # DiscoveryInventory
│   └── extraction.py     # ExtractionResult
├── services/             # Business logic services
│   ├── discovery.py      # File discovery and Maven project detection
│   ├── maven.py          # POM parser
│   ├── classifier.py     # File type classification
│   ├── extractor.py      # Extraction orchestration
│   ├── ollama_client.py  # Ollama HTTP client
│   ├── indexer.py        # Indexing orchestration
│   └── weaviate_store.py # Weaviate operations
├── parsers/              # File parsers for extraction
│   ├── java_parser.py    # Java source parsing
│   ├── jsp_parser.py     # JSP parsing
│   ├── xml_parser.py     # XML configuration parsing
│   └── sql_parser.py     # SQL parsing
├── utils/                # Utility functions
│   ├── config.py         # Configuration management
│   ├── logging.py        # Structured logging setup
│   ├── retry.py          # Retry logic with backoff
│   ├── progress.py       # Progress indicators
│   └── locking.py        # Per-project file locking
└── schemas/              # Weaviate schema definitions
    └── weaviate.py       # Project and CodeArtifact schemas
```

## Usage

### Installation

```bash
# Install in development mode
pip install -e .

# Verify installation
codeindex --help
```

### Commands

```bash
# Discover Maven projects
codeindex discover --source-dir /path/to/java/source

# Extract semantic understanding
codeindex extract

# Index to Weaviate
codeindex index

# Search semantically
codeindex search "authentication logic"

# Check status
codeindex status
```

### Configuration

Copy `.env.example` to `.env` and configure:

```bash
JAVA_SOURCE_DIR=/path/to/java/source
WEAVIATE_URL=http://localhost:8080
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
LOG_LEVEL=INFO
MAX_CONCURRENT_AI_CALLS=10
```

## Development

### Running Tests

```bash
# All tests
pytest

# Unit tests only (fast)
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests (slow)
pytest tests/e2e/

# With coverage
pytest --cov=src/codeindex --cov-report=html
```

### Code Quality

```bash
# Type checking
mypy src/codeindex

# Linting
ruff check src/codeindex

# Format code
ruff format src/codeindex
```

## Architecture

### Pipeline Phases

1. **Discovery**: Scan file system, find Maven projects, classify files
2. **Extraction**: Use Ollama AI to generate summaries and semantic tags
3. **Indexing**: Store artifacts in Weaviate with vector embeddings
4. **Search**: Semantic search over indexed codebase

### Key Patterns

- **Streaming Architecture**: Process large codebases without loading all into memory
- **Idempotent Indexing**: Deterministic UUIDs (UUID v5) enable update-not-duplicate behavior
- **Rate Limiting**: Configurable concurrent AI requests using threading.Semaphore
- **Retry Logic**: Exponential backoff for transient failures
- **Per-Project Locking**: File-based locks prevent concurrent operations on same project

## More Information

- Full specification: `/specs/001-java-codebase-indexer/spec.md`
- Implementation plan: `/specs/001-java-codebase-indexer/plan.md`
- Data model: `/specs/001-java-codebase-indexer/data-model.md`
- CLI reference: `/specs/001-java-codebase-indexer/contracts/cli-interface.md`
- Quickstart guide: `/specs/001-java-codebase-indexer/quickstart.md`
- Project documentation: `/CLAUDE.md`
