# cuco-ui-admin Quick Start Guide

## Overview

This guide shows you how to run the codebase indexer pipeline for the cuco-ui-admin project in a separate terminal while you continue working.

## Prerequisites

1. **Ollama must be running** (in terminal 1):
   ```bash
   ollama serve
   ```

2. **Weaviate must be running** (in terminal 2):
   ```bash
   ./docker-weaviate.sh start
   ```

## Clear Weaviate Data (If Needed)

If you want to start fresh and remove all previously indexed data:

```bash
# Option 1: Using the clean command (asks for confirmation)
./docker-weaviate.sh clean

# Option 2: Manual cleanup
./docker-weaviate.sh stop
rm -rf weaviate-data/*
./docker-weaviate.sh start
```

## Run the Pipeline

### Terminal Setup (Recommended)

**Terminal 1**: Ollama
```bash
ollama serve
```

**Terminal 2**: Weaviate
```bash
./docker-weaviate.sh start
./docker-weaviate.sh logs  # Optional: watch logs
```

**Terminal 3**: Run the pipeline
```bash
# Make sure you're in the project directory
cd /path/to/gha1javarag

# Activate virtual environment (if not already active)
source .venv/bin/activate

# Run the pipeline for cuco-ui-admin
./run-cuco.sh /path/to/cuco-ui-admin
```

### Using .env Configuration

If you set `JAVA_SOURCE_DIR` in your `.env` file:

```bash
# .env file
JAVA_SOURCE_DIR=/path/to/cuco-ui-admin
```

Then you can simply run:

```bash
./run-cuco.sh
```

## Pipeline Steps

The script will automatically:

1. **Discover** source files (`.java`, `.jsp`, `.js`, `.xml`, config files)
2. **Extract** semantic information using AI (this takes 10-30 minutes for large codebases)
3. **Index** artifacts into Weaviate vector database
4. **Status** check to verify everything indexed correctly

## After Pipeline Completes

### Search Your Codebase

```bash
# Basic search
codeindex search "user authentication"

# Search with project filter
codeindex search "database access" --project cuco-ui-admin

# Limit results
codeindex search "form validation" --limit 10
```

### View Status

```bash
# See all indexed projects
codeindex status

# Filter by project
codeindex status --project cuco-ui-admin
```

### Generate PRD Documentation

```bash
# Generate frontend PRD
codeindex prd frontend --output-dir ./output/cuco-prd

# Generate backend PRD
codeindex prd backend --output-dir ./output/cuco-prd
```

### Generate Architecture Diagrams

```bash
# Generate component diagram
codeindex diagram component --output ./output/cuco-diagrams --format mermaid

# Generate GWT MVP diagram
codeindex diagram gwt \
  --extraction-file data/extraction-cuco-ui-admin.jsonl \
  --output ./output/cuco-diagrams \
  --format mermaid
```

## Monitoring Progress

While the pipeline runs, you can monitor progress in real-time:

```bash
# Watch discovery output
tail -f data/discovery-cuco-ui-admin.jsonl

# Watch extraction output
tail -f data/extraction-cuco-ui-admin.jsonl

# Watch extraction progress with pretty formatting
tail -f data/extraction-cuco-ui-admin.jsonl | jq -r '.file_path'
```

## Troubleshooting

### Dependency Resolution Warnings

If you see warnings like:
```
[WARNING] Artifact directory not found: .../administration.ui
[WARNING] Artifact not found: cuco-cct-core (groupId: at.a1ta.cuco)
```

**This is normal and harmless.** The dependency resolver is looking for local Maven modules, but cuco-ui-admin is a single project (not a monorepo), so these dependencies don't exist locally.

**Solution**: The script now disables dependency resolution by default since cuco-ui-admin doesn't need it.

**If you want dependency resolution** (for monorepo projects):
```bash
# Edit run-cuco.sh and add --dependency-depth 1 to the discover command
codeindex discover --source-dir "$SOURCE_DIR" --output "$DISCOVERY_FILE" --dependency-depth 1
```

### Ollama Not Running

```bash
# Check if Ollama is running
curl -s http://localhost:11434/api/tags

# Start Ollama (in separate terminal)
ollama serve
```

### Weaviate Not Running

```bash
# Check Weaviate status
./docker-weaviate.sh status

# Start Weaviate
./docker-weaviate.sh start

# Check Weaviate health
curl -s http://localhost:8080/v1/meta
```

### Pipeline Takes Too Long

The extraction step can take 10-30 minutes for large codebases like cuco-ui-admin (500+ files). This is normal because:
- Each file is analyzed using AI (Ollama)
- Semantic information is extracted from code
- GWT patterns are detected and analyzed

You can:
- Run it in a background terminal
- Use `--skip-ai` flag for faster extraction (structural analysis only):
  ```bash
  codeindex extract --inventory data/discovery-cuco-ui-admin.jsonl --skip-ai
  ```

### Out of Memory Errors

If you encounter memory issues:

```bash
# Reduce concurrent AI calls (default: 10)
export MAX_CONCURRENT_AI_CALLS=5

# Run the pipeline again
./run-cuco.sh
```

## Expected Output

For cuco-ui-admin (539 files), you should see approximately:
- **Discovery**: ~6 seconds
- **Extraction**: ~15-30 minutes (depending on hardware and AI model)
- **Indexing**: ~10-15 seconds
- **Total artifacts**: ~2,167 artifacts indexed

## Data Files

After running, you'll have:

```
data/
├── discovery-cuco-ui-admin.jsonl     # Discovered files and project structure
└── extraction-cuco-ui-admin.jsonl   # Extracted semantic information
```

These files are JSONL format (JSON Lines) - one JSON object per line.

## Performance Tips

1. **Use SSD**: Store the codebase on an SSD for faster file scanning
2. **Increase RAM**: Ollama performs better with more available RAM
3. **Use faster model**: Try `gemma2:2b` instead of `gemma3:12b` for faster extraction
4. **Parallel processing**: The default concurrency (10) works well for most systems

## Next Steps

After indexing cuco-ui-admin:
1. Search for specific functionality: `codeindex search "login"`
2. Generate PRD documentation for features you're working on
3. Create architecture diagrams to visualize the codebase structure
4. Use the indexed data to understand code dependencies and patterns
