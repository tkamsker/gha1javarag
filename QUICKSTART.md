# Quick Start Guide

## Prerequisites Check

Run the validation script to ensure everything is set up:

```bash
python validate_setup.py
```

This will check:
- ✓ All required packages are installed
- ✓ Configuration is correct
- ✓ External services (Ollama, Weaviate) are accessible
- ✓ Code structure is complete

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` and update:
- `JAVA_SOURCE_DIR` - Path to your Java source code
- Other settings as needed

### 3. Start External Services

**Ollama:**
```bash
# Start Ollama server
ollama serve

# In another terminal, pull required models
ollama pull gemma3:12b
ollama pull nomic-embed-text
```

**Weaviate:**
```bash
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

### 4. Validate Setup

```bash
python validate_setup.py
```

### 5. Run Pipeline

```bash
python main.py
```

## Pipeline Execution Flow

### Step 1: Source Discovery & AI Extraction
- Discovers all source files
- Extracts information using AI
- Stores in Weaviate vector database

**Duration:** Depends on number of files (can take hours for large codebases)

### Step 2: Project Structuring & Analysis
- Organizes files by type
- Analyzes relationships
- Builds structured JSON

**Duration:** Minutes to tens of minutes

### Step 3: Requirements Generation
- Generates requirements documents
- Creates migration mappings
- Performs quality review

**Duration:** Minutes per project

## Output Files

After completion, check `data/output/`:

```
data/output/
  {project_name}/
    requirements.md          # Detailed requirements
    requirements_json.json   # Structured data
    mapping.md              # Next.js/NestJS migration guide
  logs/
    pipeline.log           # Full execution log
```

## Monitoring Progress

Watch the logs in real-time:
```bash
tail -f data/output/logs/pipeline.log
```

Or check processing status:
```bash
cat data/build/step1_processed.json
```

## Troubleshooting

### Pipeline stops or fails
- Check logs: `data/output/logs/pipeline.log`
- Verify services: `python validate_setup.py`
- Check disk space (vector database can grow large)

### Slow processing
- Normal for large codebases
- Each file requires AI processing
- Consider processing smaller projects first

### Memory issues
- Reduce batch size in `src/pipeline.py`
- Process projects separately
- Ensure sufficient RAM (8GB+ recommended)

## Next Steps After Pipeline Completion

1. **Review Requirements**: Check `requirements.md` for each project
2. **Review Mappings**: Check `mapping.md` for migration guidance
3. **Validate**: Review generated JSON structure in `requirements_json.json`
4. **Iterate**: Re-run with improved prompts if needed

## Tips

- Start with a small project to test
- Monitor logs during first run
- Keep Ollama and Weaviate running during execution
- Save processing logs for later analysis

