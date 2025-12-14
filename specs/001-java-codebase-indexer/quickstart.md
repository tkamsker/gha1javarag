# Quickstart Guide: Java Codebase Indexer Pipeline

**Feature**: 001-java-codebase-indexer
**Date**: 2025-12-12
**Audience**: Developers implementing or using the indexer

## Prerequisites

### Required Services

1. **Ollama with gemma3:12b model**
   ```bash
   # Install Ollama (if not installed)
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull the gemma3:12b model
   ollama pull gemma3:12b

   # Start Ollama server
   ollama serve

   # Verify (in another terminal)
   curl http://localhost:11434/api/tags
   ```

2. **Weaviate in Docker**
   ```bash
   # Use the project's existing docker-weaviate.sh script
   ./docker-weaviate.sh start

   # Or use docker-compose directly
   docker-compose up -d

   # Verify
   curl http://localhost:8080/v1/meta
   ```

3. **Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

### Development Environment Setup

```bash
# 1. Clone repository (or navigate to project root)
cd /path/to/gha1javarag

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install package in development mode
pip install -e .

# 5. Create configuration file
cp .env.example .env
```

### Configuration

Edit `.env` file with your settings:

```bash
# Required: Path to Java source code to analyze
JAVA_SOURCE_DIR=/path/to/your/java/codebase

# Optional: Service URLs (defaults shown)
WEAVIATE_URL=http://localhost:8080
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b

# Optional: Performance tuning
MAX_CONCURRENT_AI_CALLS=10
BATCH_SIZE=50

# Optional: Logging
LOG_LEVEL=INFO

# Optional: Output directories
OUTPUT_DIR=./data
```

## First-Time Usage

### Step 1: Discover Projects

Scan your Java codebase to find all Maven projects:

```bash
# Using command or module syntax
codeindex discover --source-dir /path/to/java/source --output ./output/discovery-inventory.jsonl

# Or with Python module
python -m codeindex discover --source-dir /path/to/java/source
```

Expected output:
```
Discovering Maven projects in /path/to/java/source...

============================================================
Discovery Results
============================================================
Root directory: /path/to/java/source
Scan timestamp: 2025-12-13 18:00:00
Duration: 0.15s

Projects found: 3
Total files: 6,750

Files by type:
  java_source         :   4,200
  xml_config          :   1,100
  static_asset        :   1,200
  jsp_view            :     250

Projects:
  • my-app                       v1.0.0           (2,450 files)
  • my-lib                       v1.0.0           (1,200 files)
  • my-web                       v2.0.0           (3,100 files)

✓ Inventory saved to: ./output/discovery-inventory.jsonl
```

**What this does**:
- Recursively walks source directory
- Finds all directories containing `pom.xml`
- Parses Maven coordinates from POMs
- Classifies files by type (Java, JSP, XML, etc.)
- Saves inventory to JSONL file for next step

**Troubleshooting**:
- "No Maven projects found": Check JAVA_SOURCE_DIR points to correct location
- Permission errors: Ensure read access to source directory
- Slow scanning: This is normal for large codebases (100k+ files)

### Step 2: Extract Semantic Information

Use AI to understand what each file does:

```bash
# Extract using the inventory
codeindex extract --inventory ./output/discovery-inventory.jsonl --output ./output/extraction-results.jsonl

# Or use default paths
codeindex extract
```

Expected output:
```
Loading inventory from ./output/discovery-inventory.jsonl...
Found 6,750 files to extract
Processing batch 1 (10 files)...
Processing batch 2 (10 files)...
...
  Progress: 6,750/6,750 files

============================================================
Extraction Summary
============================================================
Total files: 6,750

Files by type:
  java_source         :   4,200
  xml_config          :   1,100
  static_asset        :   1,200
  jsp_view            :     250

Frameworks detected: Spring, GWT, Hibernate, Maven, MyBatis, JUnit

✓ Results saved to: ./output/extraction-results.jsonl
```

**What this does**:
- Sends each file to Ollama gemma3:12b model
- AI generates natural language summaries
- Identifies entities (classes, methods, tables)
- Tags files by layer, domain, frameworks, concerns
- Saves extraction results for indexing

**Troubleshooting**:
- "Ollama unavailable": Ensure `ollama serve` is running
- Slow extraction: Normal! Expect ~50 files/minute
- Timeouts: Increase timeout in code if files are very large
- High memory: Extraction streams files, should stay under 2GB

### Step 3: Index to Weaviate

Store artifacts in vector database for semantic search:

```bash
# Index with inventory and extraction results
codeindex index --inventory ./output/discovery-inventory.jsonl --extraction ./output/extraction-results.jsonl

# Add --create-schema flag if first time
codeindex index --inventory ./output/discovery-inventory.jsonl --extraction ./output/extraction-results.jsonl --create-schema
```

Expected output:
```
Checking Weaviate at http://localhost:8080...
✓ Weaviate is available

Indexing from:
  Inventory:  ./output/discovery-inventory.jsonl
  Extraction: ./output/extraction-results.jsonl
  Batch size: 50


============================================================
Indexing Summary
============================================================
Projects indexed:   3
Artifacts indexed:  6,750
Artifacts errors:   0
Total files:        6,750

✓ Indexing complete
```

**What this does**:
- Creates Weaviate schema (Project, CodeArtifact classes)
- Generates vector embeddings for summaries
- Stores projects and artifacts with metadata
- Uses deterministic UUIDs for idempotent updates

**Troubleshooting**:
- "Weaviate unavailable": Check `docker ps` and `./docker-weaviate.sh status`
- Schema mismatch: Use `--reset` flag or delete Weaviate data volume
- Slow indexing: Check Weaviate logs, ensure Docker has enough resources

### Step 4: Verify Indexing

Check what was indexed:

```bash
python -m codeindex status
```

Expected output:
```
Weaviate Status: Connected
Ollama Status: Connected

Indexed Projects: 3

com.example:my-app:1.0.0
  Files: 2,438 artifacts
  Last Indexed: 2025-12-12 10:45:30
  Types: java_source (1,200), jsp_view (450), xml_config (300), ...
```

### Step 5: Search Semantically

Find code by what it does, not just keywords:

```bash
python -m codeindex search "user authentication logic"
```

Expected output:
```
Searching for: "user authentication logic"

Results (15 matches):

1. [Score: 0.94] src/main/java/com/example/auth/AuthService.java
   Summary: Handles user authentication using JWT tokens...

2. [Score: 0.89] src/main/java/com/example/auth/AuthFilter.java
   Summary: Servlet filter that validates authentication...
```

**Search Examples**:
```bash
# Find database persistence code
codeindex search "database queries" --layer persistence

# Find frontend forms
codeindex search "user input forms" --type jsp_view

# Find security-related code
codeindex search "validation" --layer backend

# Search specific project
codeindex search "billing logic" --project "com.example:my-app:1.0.0"
```

## Common Workflows

### Analyzing a New Project

```bash
# Full pipeline for a new project
export JAVA_SOURCE_DIR=/path/to/new/project

codeindex discover
codeindex extract
codeindex index
codeindex status
```

### Re-indexing After Code Changes

```bash
# Discover to capture new/changed files
codeindex discover --force

# Extract only changed files (automatically skips unchanged via hash)
codeindex extract

# Update index (idempotent - updates existing records)
codeindex index
```

### Analyzing Specific Project

```bash
# Set project filter
export PROJECT="com.example:my-app:1.0.0"

# Run pipeline for single project
codeindex discover --project $PROJECT
codeindex extract --project $PROJECT
codeindex index --project $PROJECT
```

### Resetting Project Data

```bash
# Clear all data for a project and re-index
codeindex index --project "com.example:my-app:1.0.0" --reset

# Then re-run extraction and indexing
codeindex extract --project "com.example:my-app:1.0.0" --force
codeindex index --project "com.example:my-app:1.0.0"
```

### Performance Tuning

```bash
# Increase concurrent AI calls (if Ollama can handle it)
export MAX_CONCURRENT_AI_CALLS=20
codeindex extract

# Increase batch size for faster indexing
codeindex index --batch-size 100

# Enable verbose output for debugging
codeindex discover --verbose
```

## Development Workflows

### Running Tests

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/              # Fast unit tests
pytest tests/integration/        # Integration tests (require services)
pytest tests/e2e/               # End-to-end pipeline tests

# Run with coverage
pytest --cov=src/codeindex --cov-report=html

# Run only fast tests (exclude slow E2E)
pytest -m "not slow"
```

### Creating Test Fixtures

```bash
# Sample Java code for testing
mkdir -p tests/fixtures/sample_java
cat > tests/fixtures/sample_java/SampleClass.java << 'EOF'
package com.example;

public class SampleClass {
    public String greet(String name) {
        return "Hello, " + name;
    }
}
EOF

# Sample POM for testing
cat > tests/fixtures/sample_pom.xml << 'EOF'
<project>
  <groupId>com.example</groupId>
  <artifactId>test-project</artifactId>
  <version>1.0.0</version>
</project>
EOF
```

### Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
codeindex discover

# Or use --log-level flag
codeindex extract --log-level DEBUG

# Check service health manually
curl http://localhost:8080/v1/meta  # Weaviate
curl http://localhost:11434/api/tags  # Ollama

# View Weaviate data directly
curl http://localhost:8080/v1/objects?class=Project | jq
```

### Monitoring Long-Running Operations

```bash
# Run extraction in background
codeindex extract > extract.log 2>&1 &

# Monitor progress
tail -f extract.log

# Check lock files (if operation seems stuck)
ls -la /tmp/.codeindex-*.lock
```

## Troubleshooting

### Services Not Running

**Problem**: "Connection refused" errors

**Solution**:
```bash
# Check Ollama
systemctl status ollama  # Linux
ps aux | grep ollama    # macOS

# Restart if needed
ollama serve

# Check Weaviate
docker ps | grep weaviate
./docker-weaviate.sh status
./docker-weaviate.sh restart
```

### Out of Memory

**Problem**: "MemoryError" during extraction or indexing

**Solution**:
- Streaming architecture should prevent this, but if it happens:
- Process one project at a time with `--project` flag
- Reduce `MAX_CONCURRENT_AI_CALLS` to 5 or lower
- Increase Docker memory limit for Weaviate

### Slow Performance

**Problem**: Extraction taking hours

**Solution**:
- This is normal for large codebases (expect ~50 files/minute)
- Increase `MAX_CONCURRENT_AI_CALLS` if Ollama can handle it
- Run overnight for very large codebases (100k+ files)
- Consider upgrading Ollama hardware (GPU acceleration)

### Empty Search Results

**Problem**: Search returns no results even after indexing

**Solution**:
```bash
# Verify data was indexed
codeindex status --project "your-project-id"

# Check if project ID matches
codeindex status  # List all project IDs

# Try broader search
codeindex search "java class"

# Check Weaviate directly
curl http://localhost:8080/v1/objects?class=CodeArtifact | jq
```

### Project Locked Error

**Problem**: "Project is currently being processed"

**Solution**:
- Another process is running on this project
- Wait for it to complete, or
- If process is stuck/dead, manually remove lock:
  ```bash
  rm /tmp/.codeindex-{project-id}.lock
  ```

## Next Steps

After completing the quickstart:

1. **Explore the codebase**: Try various semantic searches
2. **Analyze patterns**: Use status command to understand your codebase composition
3. **Integrate with workflows**: Automate indexing in CI/CD pipelines
4. **Extend the system**: Add new artifact types or parsers (see development docs)
5. **Generate PRDs**: Use indexed data for downstream PRD generation (future phase)

## Additional Resources

- Full CLI documentation: `specs/001-java-codebase-indexer/contracts/cli-interface.md`
- Data model: `specs/001-java-codebase-indexer/data-model.md`
- Weaviate schema: `specs/001-java-codebase-indexer/contracts/weaviate-schema.yaml`
- Project CLAUDE.md: Repository root (implementation guidance)

