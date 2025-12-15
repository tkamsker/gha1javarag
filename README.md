# Java Codebase Indexer & PRD Generator

A Python-based pipeline that analyzes Java/JSP/GWT/JavaScript codebases, extracts structured information using AI, indexes artifacts in a vector database, and generates comprehensive Product Requirements Documents (PRDs) from existing code.

## Features

### Core Pipeline

- **🔍 Discovery**: Recursively scan source directories to find Java, JSP, GWT, JavaScript, XML, and SQL files
- **🧠 AI Extraction**: Use Ollama LLM (Gemma 3:12b) to understand code semantics and extract structured information
- **📊 Vector Indexing**: Store artifacts in Weaviate with embeddings for semantic search
- **🔎 Semantic Search**: Natural language queries over your entire codebase
- **📈 Status Monitoring**: View indexing statistics and project health

### PRD Generation (Feature 002)

Generate comprehensive Product Requirements Documents from your indexed codebase:

- **📄 Database Layer Documentation**: Extract database schemas, entities, relationships, and constraints
- **⚙️ Service Layer Documentation**: Document backend services, API endpoints, and business logic
- **🎨 Frontend Layer Documentation**: Catalog UI forms, components, and user interactions
- **📋 Master PRD Synthesis**: Combine all layers into a comprehensive master document with cross-layer mappings

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (for Weaviate)
- Ollama with gemma3:12b model

### Installation

```bash
# Clone the repository
git clone https://github.com/tkamsker/gha1javarag.git
cd gha1javarag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Setup Services

```bash
# Start Ollama (in separate terminal)
ollama serve

# Pull the model
ollama pull gemma3:12b

# Start Weaviate (auto-detects macOS/Linux)
./docker-weaviate.sh start

# Verify services
./docker-weaviate.sh status
```

### Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and set your source directory
JAVA_SOURCE_DIR=/path/to/your/java/source
```

## Usage

### Basic Pipeline

```bash
# 1. Discover source files
codeindex discover --source-dir /path/to/source --project myapp

# 2. Extract structured information with AI
codeindex extract --project myapp

# 3. Index artifacts in Weaviate
codeindex index --project myapp

# 4. Search your codebase
codeindex search "user authentication" --project myapp

# 5. View indexing status
codeindex status --project myapp
```

### PRD Generation

Generate comprehensive documentation from your indexed codebase:

#### Generate Full PRD (All Layers + Master)

```bash
codeindex prd full \
  --project myapp \
  --source-dir /path/to/source \
  --output-dir ./docs/prd
```

This generates:
- `database_prd.md` - Database schema documentation
- `service_prd.md` - Backend service documentation
- `frontend_prd.md` - Frontend component documentation
- `master_prd.md` - Comprehensive master PRD with cross-layer insights

#### Generate Specific Layer

```bash
# Database layer only
codeindex prd database --project myapp --output-dir ./docs

# Service layer only
codeindex prd services --project myapp --output-dir ./docs

# Frontend layer only
codeindex prd frontend --project myapp --output-dir ./docs
```

#### Advanced Options

```bash
# Force refresh (re-analyze all files)
codeindex prd full --force-refresh --project myapp

# Custom LLM settings
codeindex prd full \
  --llm-timeout 180 \
  --parallel 20 \
  --llm-retries 5 \
  --project myapp

# Filter by domain
codeindex prd full \
  --domain-filter authentication \
  --project myapp

# Quiet mode (for automation)
codeindex prd full --quiet --project myapp
```

### PRD Output Structure

```
output/myapp/
├── master_prd.md                    # Master PRD synthesizing all layers
├── prd/
│   ├── database_prd.md              # Database schema documentation
│   ├── service_prd.md               # Service layer documentation
│   └── frontend_prd.md              # Frontend layer documentation
├── database/
│   ├── entities/                    # Individual entity JSON files
│   └── index.md                     # Database entity index
├── services/
│   ├── definitions/                 # Individual service JSON files
│   ├── endpoints/                   # Individual endpoint JSON files
│   └── index.md                     # Service index
├── frontend/
│   ├── forms/                       # Individual form JSON files
│   ├── components/                  # Individual component JSON files
│   └── index.md                     # Frontend index
├── business_rules/
│   └── rules_by_layer.json         # Business rules catalog
└── .visit_log.jsonl                # Incremental processing log
```

## PRD Features

### Database Layer Analysis

Extracts and documents:
- JPA entity annotations
- iBATIS SQL mappings
- Liquibase migrations
- Table schemas with columns, types, constraints
- Foreign key relationships
- Indexes and performance considerations
- Database-level business rules

### Service Layer Analysis

Extracts and documents:
- Spring service classes and methods
- REST/SOAP API endpoints with full specifications
- Service dependencies and injection patterns
- Transactional boundaries
- Service-level business rules
- Data flow analysis

### Frontend Layer Analysis

Extracts and documents:
- JSP form definitions
- GWT UI components and modules
- Form fields with validation rules
- Form-to-backend endpoint mappings
- Navigation flows
- UI component hierarchies

### Master PRD Synthesis

Generates comprehensive documentation with:
- Executive summary with system statistics
- Technology stack detection (Spring, JPA, JSP, GWT, etc.)
- Business domain categorization
- Architecture overview (layered design)
- Cross-layer integration mappings (Form → API → Database)
- Comprehensive business rules catalog
- Links to detailed layer-specific documentation

## GWT (Google Web Toolkit) Support

**Full GWT application analysis** with specialized analyzers for GWT patterns and MVP architecture.

### GWT Features

The tool provides deep analysis of GWT applications with:

- ✅ **MVP Pattern Recognition**: Automatic detection of Presenter-View-Model patterns
- ✅ **RPC Servlet Analysis**: Extract service methods, async interfaces, and client-server contracts
- ✅ **UiBinder Template Parsing**: Extract form fields, widgets, and UI structure from XML templates
- ✅ **DTO Analysis**: Document shared data transfer objects with serialization patterns
- ✅ **View Component Analysis**: Catalog UI components, widgets, and event handlers
- ✅ **Navigation Flow Mapping**: Track application flow and presenter navigation
- ✅ **GWT Module Detection**: Identify and document GWT module configurations

### GWT Artifact Types

The system recognizes and analyzes these GWT-specific artifacts:

| Type | Pattern | Analysis |
|------|---------|----------|
| **Presenter** | `*Presenter.java` | View binding, event handlers, navigation logic, RPC calls |
| **View** | `*View.java` | Component type, UI fields, UiBinder integration |
| **UiBinder** | `*.ui.xml` | Form fields, widgets, labels, validation |
| **DTO** | `*DTO.java` in shared | Fields, serialization, nested DTOs, inner classes |
| **RPC Servlet** | `*ServletImpl.java` | Service methods, async interface, error handling |
| **GWT Module** | `*.gwt.xml` | Entry points, source paths, dependencies |

### GWT Analysis Example

```bash
# Discover GWT application
codeindex discover --source-dir /path/to/gwt-app --project myapp

# Extract with GWT analyzers
codeindex extract --project myapp

# Index GWT artifacts
codeindex index --project myapp

# Search GWT components
codeindex search "user authentication presenter" --project myapp
codeindex search "form validation" --project myapp
```

### GWT PRD Output

When analyzing GWT applications, PRDs include:

**Presenter Analysis**:
- View interface bindings with confidence scores
- Event handlers (click, change, etc.) and their actions
- Navigation targets and application flow
- RPC service calls with parameters
- MVP binding patterns (Display interface, separate interface, naming convention)

**View Analysis**:
- Component type (Composite, Widget, Panel, PopupPanel)
- UI fields with widget types
- UiBinder template paths
- Event registrations

**DTO Analysis**:
- Field definitions with types
- Validation rules (@NotNull, @Size, @Pattern, etc.)
- Serialization markers (GWT IsSerializable, Java Serializable)
- Nested DTO references
- Inner class definitions

**RPC Servlet Analysis**:
- Service method signatures
- Async interface patterns
- Parameter and return types
- Service inheritance hierarchy

### GWT Testing

The GWT support includes comprehensive test coverage:

- **38 Integration Tests**: Presenter, View, DTO, Servlet, UiBinder analysis
- **Real-world Validation**: Tested on 183-file production GWT codebase
- **Pattern Recognition**: 19 classifier tests for GWT file patterns
- **Weaviate Compatibility**: JSON serialization validation

### GWT Best Practices

**For optimal GWT analysis**:

1. **Standard Package Structure**: Use `client`, `server`, `shared` packages
2. **Naming Conventions**: Follow `*Presenter`, `*View`, `*DTO` patterns
3. **UiBinder Templates**: Co-locate `.ui.xml` with view classes
4. **Serialization**: Use GWT `IsSerializable` or Java `Serializable`
5. **MVP Binding**: Use Display interfaces or clear naming conventions

### GWT Troubleshooting

**Issue: GWT files not detected**
```bash
# Verify file patterns
find /path/to/source -name "*Presenter.java" -o -name "*.ui.xml"

# Check discovery results
grep "gwt_" output/discovery-inventory.jsonl
```

**Issue: UiBinder extraction fails**
```bash
# Validate XML structure
xmllint --noout path/to/file.ui.xml

# Check for GWT namespaces
grep "urn:ui:com.google.gwt.uibinder" path/to/file.ui.xml
```

**Issue: DTO not recognized as shared**
```bash
# Verify serialization markers
grep -E "IsSerializable|implements Serializable" path/to/DTO.java

# Check package structure
# Should contain .shared. or have serialization markers
```

## Integration with Spec Kit

Generated PRDs are designed for use with [GitHub Spec Kit](https://github.com/github/spec-kit):

```bash
# Initialize Spec Kit
specify init . --ai claude

# Create project principles
/speckit.constitution

# Place generated PRD in Spec Kit structure
cp output/myapp/master_prd.md specs/myfeature/prd.md

# Generate specification from PRD
/speckit.specify

# Generate implementation plan
/speckit.plan

# Break down into tasks
/speckit.tasks
```

## Architecture

### Pipeline Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Discovery  │────▶│ Extraction  │────▶│   Indexing  │────▶│   Search    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │                    │
   File scan          AI analysis         Vector store         Semantic query
   Maven POMs         Ollama LLM          Weaviate            Natural language

                                              ▼
                                    ┌─────────────────┐
                                    │ PRD Generation  │
                                    └─────────────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                  ┌──────────┐       ┌──────────┐       ┌──────────┐
                  │ Database │       │ Services │       │ Frontend │
                  │   Layer  │       │   Layer  │       │   Layer  │
                  └──────────┘       └──────────┘       └──────────┘
                        └───────────────────┬───────────────────┘
                                            ▼
                                    ┌───────────────┐
                                    │  Master PRD   │
                                    └───────────────┘
```

### Key Components

- **Discovery Service**: Scans directory trees, identifies file types, parses Maven POMs
- **Extraction Service**: Coordinates AI-powered semantic extraction
- **Parsers**: Java, JSP, XML, SQL specialized parsers
- **Ollama Client**: LLM integration with retry logic and rate limiting
- **Weaviate Store**: Vector database operations with batching
- **Indexing Service**: Artifact storage and retrieval
- **PRD Generators**: Layer-specific and master PRD generation
- **Visit Log**: Incremental processing with content hash tracking

## Configuration

All configuration via environment variables or CLI arguments:

| Variable | Default | Description |
|----------|---------|-------------|
| `JAVA_SOURCE_DIR` | - | Root source directory (required) |
| `WEAVIATE_URL` | http://localhost:8080 | Weaviate endpoint |
| `OLLAMA_URL` | http://localhost:11434 | Ollama endpoint |
| `OLLAMA_MODEL_NAME` | gemma3:12b | LLM model to use |
| `MAX_CONCURRENT_AI_CALLS` | 10 | Parallel LLM requests |
| `BATCH_SIZE` | 50 | Weaviate batch size |
| `LOG_LEVEL` | INFO | Logging verbosity |
| `OUTPUT_DIR` | ./data | Output directory |

## Testing

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/unit/ --cov=src/codeindex --cov-report=html

# Run specific test suite
pytest tests/unit/test_visit_log.py -v

# Test PRD generation
python test_enhanced_prd.py
```

**Test Results**: 321 unit tests passing
- Parsers: Java, JSP, XML, SQL - 100% tested
- Services: Discovery, extraction, classification
- Models: All data models validated
- Visit Log: Incremental processing verified

## CLI Reference

### Discover Command

```bash
codeindex discover [OPTIONS]

Options:
  --source-dir PATH     Source directory to scan (required)
  --project TEXT        Project name/ID
  --output-dir PATH     Output directory for inventory (default: ./data)
  --include-tests       Include test files
  --exclude-generated   Exclude auto-generated code (default: true)
  -v, --verbose         Enable verbose logging
```

### Extract Command

```bash
codeindex extract [OPTIONS]

Options:
  --source-dir PATH     Source directory (overrides JAVA_SOURCE_DIR)
  --project TEXT        Project name/ID
  --parallel INT        Number of parallel LLM tasks (default: 10)
  --force-refresh       Re-extract all files
  -v, --verbose         Enable verbose logging
```

### Index Command

```bash
codeindex index [OPTIONS]

Options:
  --input PATH          Input file/directory with artifacts
  --project TEXT        Project name/ID
  --reset               Clear existing data before indexing
  --batch-size INT      Batch size for indexing (default: 50)
  -v, --verbose         Enable verbose logging
```

### Search Command

```bash
codeindex search QUERY [OPTIONS]

Options:
  --project TEXT        Filter by project
  --limit INT           Maximum results (default: 10)
  --type TEXT           Filter by artifact type
  -v, --verbose         Enable verbose logging
```

### PRD Command

```bash
codeindex prd [LAYER] [OPTIONS]

Arguments:
  LAYER                 Layer to analyze: database|services|frontend|full

Options:
  --project TEXT        Project name/ID to analyze
  --source-dir PATH     Source directory (overrides JAVA_SOURCE_DIR)
  --output-dir PATH     Output directory for PRDs (default: ./output)
  --force-refresh       Re-analyze all files
  --parallel INT        Parallel LLM tasks (default: 10)
  --llm-timeout INT     LLM timeout in seconds (default: 120)
  --llm-retries INT     LLM retry attempts (default: 3)
  --llm-model TEXT      Ollama model to use
  --domain-filter TEXT  Only analyze specific domain
  --skip-database       Skip database layer (with full)
  --skip-services       Skip service layer (with full)
  --skip-frontend       Skip frontend layer (with full)
  -q, --quiet           Suppress progress output
  -v, --verbose         Enable verbose logging
```

## Troubleshooting

### Services Not Running

```bash
# Check Ollama
curl -s http://localhost:11434/api/tags

# Check Weaviate
curl -s http://localhost:8080/v1/meta

# View Weaviate logs
./docker-weaviate.sh logs

# Restart services
./docker-weaviate.sh restart
```

### Empty Search Results

```bash
# Check what's indexed
./weaviate_stats.py

# Verify project name
codeindex status --project myapp

# Re-index with reset
codeindex index --project myapp --reset
```

### PRD Generation Issues

```bash
# Check Ollama is running with correct model
ollama list

# Increase timeout for large files
codeindex prd full --llm-timeout 300 --project myapp

# Force refresh to re-analyze
codeindex prd full --force-refresh --project myapp

# Run with verbose logging
codeindex prd full -v --project myapp
```

## Docker Management

```bash
# Start Weaviate (auto-detects OS)
./docker-weaviate.sh start

# Stop Weaviate
./docker-weaviate.sh stop

# Restart Weaviate
./docker-weaviate.sh restart

# View logs
./docker-weaviate.sh logs

# Clean data (removes all indexed data)
./docker-weaviate.sh clean

# Check status
./docker-weaviate.sh status
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest tests/unit/ -v`
5. Commit changes: `git commit -m "feat: description"`
6. Push to branch: `git push origin feature-name`
7. Open a pull request

## Project Structure

```
gha1javarag/
├── src/codeindex/           # Main application
│   ├── cli/                 # CLI commands
│   ├── models/              # Data models
│   ├── parsers/             # Language-specific parsers
│   ├── services/            # Business logic
│   ├── schemas/             # Weaviate schemas
│   └── utils/               # Utilities
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   ├── e2e/                 # End-to-end tests
│   └── fixtures/            # Test data
├── specs/                   # Spec Kit feature specs
├── .specify/                # Spec Kit configuration
├── docker-weaviate.sh       # Weaviate management script
├── weaviate_stats.py        # Diagnostic tool
└── test_enhanced_prd.py     # PRD generation validation
```

## License

[Your License Here]

## Acknowledgments

- Built with [Weaviate](https://weaviate.io/) for vector search
- Powered by [Ollama](https://ollama.ai/) for local LLM inference
- Integrates with [GitHub Spec Kit](https://github.com/github/spec-kit) for specification-driven development
- Uses Gemma 3:12b model for code understanding

## Support

- **Issues**: https://github.com/tkamsker/gha1javarag/issues
- **Documentation**: See CLAUDE.md for detailed instructions
- **Setup Guide**: See SETUP.md for environment-specific setup

---

🤖 *Enhanced with AI-powered code understanding and PRD generation*
