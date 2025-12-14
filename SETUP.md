# Setup Guide: Java Codebase Indexer Pipeline

Quick setup guide for getting started with the Java Codebase Indexer.

## Prerequisites

- **Python 3.8+** installed
- **Docker** (for Weaviate)
- **Ollama** with gemma3:12b model

## Quick Start (3 Steps)

### 1️⃣ Setup Virtual Environment

Run the setup script to create a virtual environment and install dependencies:

```bash
./step1.sh
```

This script will:
- ✅ Check Python version (requires 3.8+)
- ✅ Create `.venv` virtual environment
- ✅ Install all dependencies from `requirements.txt`
- ✅ Install `codeindex` CLI in development mode
- ✅ Verify installation

**Note**: Safe to run multiple times - will reuse existing venv.

### 2️⃣ Configure Environment

Copy the example configuration and edit with your settings:

```bash
cp .env.example .env
# Edit .env and set at minimum:
# - JAVA_SOURCE_DIR=/path/to/your/java/source
```

### 3️⃣ Start Services

Start Weaviate (vector database):

```bash
./docker-weaviate.sh start
```

Verify Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

## Usage Scripts

### step1.sh - Virtual Environment Setup

```bash
./step1.sh
```

**When to use**:
- First time setup
- After pulling new dependencies
- To reinstall/update packages

**Safe to run multiple times** - idempotent.

### with-venv.sh - Run Commands in Virtual Environment

```bash
./with-venv.sh <command> [args...]
```

**Examples**:

```bash
# Run CLI commands
./with-venv.sh codeindex --help
./with-venv.sh codeindex discover --source-dir /path/to/java

# Run tests
./with-venv.sh pytest tests/unit/
./with-venv.sh pytest --cov=src/codeindex

# Run Python scripts
./with-venv.sh python my_script.py
```

**When to use**:
- When you want to run a command without manually activating venv
- In scripts and automation
- One-off commands

### run.sh - Full Pipeline Runner

```bash
./run.sh [project-name]
```

**Examples**:

```bash
# Run full pipeline on all projects
./run.sh

# Run full pipeline on specific project
./run.sh "com.example:myapp:1.0.0"
```

**What it does**:
1. Activates virtual environment
2. Runs `codeindex discover` (finds Maven projects)
3. Runs `codeindex extract` (AI semantic analysis) - *Phase 4*
4. Runs `codeindex index` (store in Weaviate) - *Phase 5*
5. Runs `codeindex status` (show results)

**Note**: Currently only discover and status work (Phase 2 complete).

### docker-weaviate.sh - Weaviate Management

```bash
./docker-weaviate.sh <command>
```

**Commands**:
- `start` - Start Weaviate container
- `stop` - Stop Weaviate container
- `restart` - Restart Weaviate
- `status` - Show container status
- `logs` - View container logs
- `clean` - Stop and remove data

**Auto-detects OS** (macOS/Linux) and uses appropriate Docker Compose file.

## Manual Virtual Environment Activation

If you prefer to activate the virtual environment manually:

```bash
# Activate
source .venv/bin/activate

# Use CLI directly
codeindex --help
codeindex discover --source-dir /path/to/java

# Run tests
pytest tests/unit/

# Deactivate when done
deactivate
```

## Development Workflow

### Daily Development

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Run tests during development
pytest tests/unit/test_config.py -v

# 3. Run CLI commands
codeindex --help

# 4. Deactivate when done
deactivate
```

### Running Tests

```bash
# All tests
./with-venv.sh pytest

# Unit tests only (fast)
./with-venv.sh pytest tests/unit/

# With coverage
./with-venv.sh pytest --cov=src/codeindex --cov-report=html

# Specific test file
./with-venv.sh pytest tests/unit/test_config.py -v
```

### Code Quality

```bash
# Type checking (if mypy installed)
./with-venv.sh mypy src/codeindex

# Linting (if ruff installed)
./with-venv.sh ruff check src/codeindex
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `./step1.sh` fails with Python version error

**Solution**: Install Python 3.8 or higher:
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv
```

**Problem**: `codeindex` command not found after setup

**Solution**: Make sure you're using the virtual environment:
```bash
source .venv/bin/activate
which codeindex  # Should show .venv/bin/codeindex
```

### Docker/Weaviate Issues

**Problem**: `./docker-weaviate.sh start` fails

**Solution**: Check Docker is running:
```bash
docker ps
# If Docker daemon not running, start Docker Desktop
```

**Problem**: Weaviate port conflict (8080 already in use)

**Solution**: Edit `.env` and change `WEAVIATE_URL`:
```bash
WEAVIATE_URL=http://localhost:8081
```

Then update docker-compose files to use port 8081.

### Ollama Issues

**Problem**: Cannot connect to Ollama

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve

# Pull model if needed
ollama pull gemma3:12b
```

## Script Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `step1.sh` | Setup venv + install deps | `./step1.sh` |
| `with-venv.sh` | Run command in venv | `./with-venv.sh <cmd>` |
| `run.sh` | Full pipeline execution | `./run.sh [project]` |
| `docker-weaviate.sh` | Manage Weaviate | `./docker-weaviate.sh start` |
| `weaviate_stats.sh` | Show Weaviate stats | `./weaviate_stats.sh` |

## Next Steps

After setup is complete:

1. **Verify installation**: `./with-venv.sh codeindex --help`
2. **Configure .env**: Set `JAVA_SOURCE_DIR` and other settings
3. **Start services**: `./docker-weaviate.sh start`
4. **Run discovery**: `./with-venv.sh codeindex discover`
5. **Check documentation**: `src/codeindex/README.md`

## Additional Resources

- **Project README**: `src/codeindex/README.md`
- **CLI Reference**: `specs/001-java-codebase-indexer/contracts/cli-interface.md`
- **Quickstart Guide**: `specs/001-java-codebase-indexer/quickstart.md`
- **Implementation Status**: `specs/001-java-codebase-indexer/IMPLEMENTATION_CHECKPOINT.md`
- **Development Guide**: `CLAUDE.md`
