# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GEMINI Code Analysis and PRD Generator - A Python-based pipeline that analyzes Java/JSP/GWT/JavaScript codebases, extracts structured information, indexes artifacts in Weaviate vector database, and generates Product Requirements Documents (PRDs) using AI (Ollama/GEMINI).

The project integrates with GitHub Spec Kit for spec-driven development workflows.

## Architecture

### Core Pipeline Stages

The system operates through five main CLI stages (implemented as subcommands):

1. **discover** - Recursively scans `JAVA_SOURCE_DIR` for source files (.java, .jsp, .js, .xml, config files)
2. **extract** - Parses discovered files into structured artifacts (services, DAOs, endpoints, forms, GWT modules, DB schemas, iBATIS statements)
3. **index** - Generates vector embeddings and stores artifacts in Weaviate with project/type partitioning
4. **search** - Natural language semantic search over indexed artifacts
5. **prd** - Generates PRDs and requirements documents using Ollama LLM from indexed artifacts

### Key Artifact Types

The extractor creates typed artifacts stored in Weaviate:
- **Backend**: `DaoCall`, `IbatisStatement`, `BackendDoc`, `DbTable`, `GwtEndpoint`
- **Frontend**: `JspForm`, `GwtModule`, `GwtUiBinder`, `GwtActivityPlace`, `JsArtifact`

Each artifact includes: canonical ID, source path, language/framework type, and domain-specific metadata (endpoints, DTOs, DB schemas, form fields, navigation targets).

### External Dependencies

- **Weaviate** - Vector database running in Docker (port 8080), configured per OS (macOS/Ubuntu)
- **Ollama** - Local LLM service (port 11434) for embeddings and PRD generation
- **Spec Kit** - GitHub's spec-driven development toolkit integration via `.claude/` and `.specify/` directories

## Common Commands

### Environment Setup

```bash
# Create Python virtual environment
./setup_venv.sh

# Set required environment variable in .env
JAVA_SOURCE_DIR=/path/to/java/source/root

# Start Ollama (required before Weaviate)
ollama serve

# Start Weaviate with OS auto-detection
./docker-weaviate.sh start

# Or force specific OS configuration
./docker-weaviate.sh start macos
./docker-weaviate.sh start ubuntu

# Check service status
./docker-weaviate.sh status
```

### Pipeline Execution

```bash
# Run full pipeline for a project (with frontend extraction)
./run.sh <project-name>
# Default project name is "test" if not specified

# Or run via Python with explicit stages
export PYTHONPATH=$(pwd):$PYTHONPATH
python src/main.py discover --project myproject
python src/main.py extract --project myproject --include-frontend
python src/main.py index --project myproject
python src/main.py search --project myproject --query "database access"
python src/main.py prd --project myproject --frontend
```

### Weaviate Management

```bash
# Docker Compose operations (OS-aware)
./docker-weaviate.sh start     # Start container
./docker-weaviate.sh stop      # Stop container
./docker-weaviate.sh restart   # Restart container
./docker-weaviate.sh logs      # View logs
./docker-weaviate.sh clean     # Remove all data (confirmation required)

# View indexed statistics and diagnostics
./weaviate_stats.py
# Shows: object counts by class, projects, sample paths, search tests
```

### Testing

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit/
pytest tests/integration/

# Run individual test files
pytest tests/unit/test_discovery.py
pytest tests/unit/test_extraction.py
pytest tests/unit/test_prd_generation.py
pytest tests/integration/test_indexing.py
pytest tests/integration/test_search.py
```

### Spec Kit Integration

```bash
# Initialize Spec Kit (already done)
specify init . --ai claude

# Core Spec Kit workflow commands
/speckit.constitution  # Define project principles
/speckit.specify       # Create feature specifications
/speckit.plan          # Generate implementation plans
/speckit.tasks         # Break down into actionable tasks
/speckit.implement     # Execute implementation

# Enhancement commands
/speckit.clarify       # Ask clarifying questions (before planning)
/speckit.analyze       # Check cross-artifact consistency (after tasks)
/speckit.checklist     # Generate validation checklists
/speckit.taskstoissues # Convert tasks to GitHub issues
```

## Development Notes

### Configuration

All configuration is centralized but follows this priority:
1. CLI arguments (highest)
2. Environment variables
3. `.env` file (version-controlled, overridden by `.env.local` patterns)
4. `config/settings.py` defaults (lowest)

Critical environment variables:
- `JAVA_SOURCE_DIR` - Root of source tree to analyze (required)
- `LOG_LEVEL` - Logging verbosity
- Weaviate host configuration
- Ollama model parameters

### OS-Specific Behavior

The project auto-detects macOS vs Ubuntu/Linux and uses appropriate Docker Compose files:
- `docker-compose.macos.yml` - macOS configuration
- `docker-compose.ubuntu.yml` - Ubuntu/Linux configuration
- `docker-compose.yml` - Fallback/generic configuration

Weaviate uses `network_mode: host` to access local Ollama at `127.0.0.1:11434` (avoids IPv6 resolution issues).

### Project Structure Notes

- **src/** - Main source directory (currently empty, code may be at root level or archived)
- **tests/** - Unit and integration tests
- **archive/** - Old/deprecated code
- **data/** - Runtime data directory (gitignored)
- **output/** - Generated PRDs and artifacts (gitignored)
- **specs/** - Spec Kit feature specifications
- **weaviate-data/** - Persistent vector database storage (gitignored)
- **.claude/** - Claude Code slash commands
- **.specify/** - Spec Kit templates and memory
- **Iterations/** - Development iteration documentation

### Key Scripts

- `run.sh` - Convenience wrapper to run full pipeline with project name parameter
- `docker-weaviate.sh` - Comprehensive Weaviate Docker management (start/stop/clean/status/logs)
- `weaviate_stats.py` - Diagnostic tool showing indexed content with rich terminal output
- `setup_venv.sh` - Python virtual environment setup

### Weaviate Container Naming

Container uses name `weaviate-i19` (iteration 19), check `docker-weaviate.sh` status command for exact container grep pattern.

### Multi-Project Support

The system supports multiple projects in a shared Weaviate instance:
- Artifacts are tagged by `project` field
- Searches can filter by project
- Indexing is idempotent (re-indexing updates/upserts rather than duplicating)

### PRD Generation

Generated PRDs follow product requirements best practices:
- Objectives and stakeholders
- User stories
- Functional/non-functional requirements
- Out of scope items
- Structured for Spec Kit compatibility (`specs/<feature-id>/prd.md`)

Supports separate backend and frontend requirement generation via CLI flags.

## Integration with Spec Kit

Generated PRDs are designed to be consumed by Spec Kit:
1. Run pipeline to extract artifacts and generate PRDs
2. Place PRDs in `specs/<feature-id>/prd.md`
3. Use `/speckit.specify` to transform PRDs into specs
4. Use `/speckit.plan` and `/speckit.tasks` for implementation planning
5. Domain labels on artifacts help with feature breakdown

## Troubleshooting

### Services Not Running

```bash
# Check Ollama
curl -s http://localhost:11434/api/tags

# Check Weaviate
curl -s http://localhost:8080/v1/meta

# Use diagnostic script
./docker-weaviate.sh status
```

### Empty Search Results

```bash
# Check what's actually indexed
./weaviate_stats.py

# Verify project name matches
# Check that indexing completed without errors
```

### Container Issues

```bash
# View logs
./docker-weaviate.sh logs

# Clean restart
./docker-weaviate.sh clean
./docker-weaviate.sh start
```

### Missing src/main.py

Note: The `run.sh` script expects `src/main.py` but the src directory may be empty. Check if:
- Code is at project root level
- Code is in `archive/` directory
- Project structure is being reorganized


## Active Technologies
- Python 3.8+ (minimum version for type hints and modern async support) (001-java-codebase-indexer)

## Recent Changes
- 001-java-codebase-indexer: Added Python 3.8+ (minimum version for type hints and modern async support)
