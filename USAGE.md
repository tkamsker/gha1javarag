# Java/JSP/GWT/JS → PRD Pipeline Usage Guide

## Quick Start

### Step 1: Initial Setup (Run Once)
```bash
# Activate virtual environment
source venv/bin/activate

# Run initial setup
./step1_setup.sh
```

This will:
- Check virtual environment
- Install Python dependencies
- Check Ollama installation and pull required models
- Start Weaviate with vectorization enabled
- Update configuration for semantic search

### Step 2: Process Your Code (Run Often)
```bash
# Activate virtual environment
source venv/bin/activate

# Run complete pipeline
./step2_fetch.sh all <project_name> <include_frontend>

# Examples:
./step2_fetch.sh all 20251008_1034 true
./step2_fetch.sh all my-project false
```

## Available Commands

### Step 2 Script Commands
```bash
# Complete pipeline
./step2_fetch.sh all <project> <frontend>

# Individual steps
./step2_fetch.sh discover <project> <frontend>
./step2_fetch.sh extract <project> <frontend>
./step2_fetch.sh index <project>
./step2_fetch.sh list <project>

# Search and analysis
./step2_fetch.sh search <project> <query> [limit]
./step2_fetch.sh prd <project>

# Help
./step2_fetch.sh help
```

### Direct Python Commands
```bash
# Discovery
python main.py discover --project <project> --include-frontend

# Extraction
python main.py extract --project <project> --include-frontend

# Indexing
python main.py index --project <project>

# Search
python main.py search --query "product administration" --project <project> --frontend --limit 10

# PRD Generation
python main.py prd --project <project> --frontend
```

## Examples

### Example 1: Complete Pipeline
```bash
# Setup (run once)
./step1_setup.sh

# Process code with frontend analysis
./step2_fetch.sh all my-java-project true

# Search for specific functionality
./step2_fetch.sh search my-java-project "user authentication" 5

# Generate PRD
./step2_fetch.sh prd my-java-project
```

### Example 2: Backend Only
```bash
# Process code without frontend analysis
./step2_fetch.sh all my-java-project false

# List what was indexed
./step2_fetch.sh list my-java-project
```

### Example 3: Incremental Updates
```bash
# After code changes, just re-index
./step2_fetch.sh index my-java-project

# Check what's indexed
./step2_fetch.sh list my-java-project
```

## Configuration

### Environment Variables (.env)
```bash
# Java source directory
JAVA_SOURCE_DIR=/path/to/your/java/project

# File patterns to include
JAVA_INCLUDE_GLOBS=**/*.java
JSP_INCLUDE_GLOBS=**/*.jsp
JS_INCLUDE_GLOBS=**/*.js
GWT_INCLUDE_GLOBS=**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java

# Weaviate configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=

# Ollama configuration
OLLAMA_MODEL_NAME=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Active**
   ```bash
   source venv/bin/activate
   ```

2. **Weaviate Not Running**
   ```bash
   ./docker-weaviate.sh start
   ```

3. **Ollama Not Running**
   ```bash
   ollama serve
   ```

4. **Missing Models**
   ```bash
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text
   ```

5. **Permission Denied**
   ```bash
   chmod +x step1_setup.sh step2_fetch.sh
   ```

### Reset Everything
```bash
# Stop services
./docker-weaviate.sh stop
pkill ollama

# Restart setup
./step1_setup.sh
```

## Output Files

- **Discovery**: `data/discover/` - Lists of discovered files
- **Extraction**: `data/build/` - Extracted artifacts as JSON
- **Indexing**: Weaviate database with vectorized artifacts
- **PRD**: `data/prd/` - Generated Product Requirements Documents

## Next Steps

After running the pipeline:

1. **Review Discovered Files**: Check `data/discover/` for file lists
2. **Examine Extracted Artifacts**: Look at `data/build/` for extracted data
3. **Search Your Codebase**: Use search commands to find specific functionality
4. **Generate PRDs**: Create comprehensive documentation
5. **Iterate**: Re-run as your codebase evolves
