# Running the Pipeline

## Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Validate Setup
```bash
python validate_setup.py
```

### 3. Dry Run (Preview What Will Be Processed)
```bash
python dry_run.py
```

### 4. Run Full Pipeline
```bash
python main.py
```

## Important Notes

### Configuration
Before running, ensure your `.env` file is configured:
- `JAVA_SOURCE_DIR` - Points to your source code directory
- `OLLAMA_BASE_URL` - Ollama service URL (default: http://localhost:11434)
- `WEAVIATE_URL` - Weaviate service URL (default: http://localhost:8080)

### Prerequisites
- Ollama must be running with models: `gemma3:12b` and `nomic-embed-text`
- Weaviate must be running (Docker container)
- Virtual environment activated

### Output Location
Results will be in `data/output/{project_name}/`:
- `requirements.md` - Detailed requirements document
- `requirements_json.json` - Structured JSON data
- `mapping.md` - Next.js/NestJS migration mapping

### Monitoring
Watch progress in real-time:
```bash
tail -f data/output/logs/pipeline.log
```

