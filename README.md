# CrewAI Requirements Extraction Pipeline

A multi-step, agent-driven pipeline for extracting comprehensive requirements from legacy Java/JSP/GWT projects and generating migration documentation for Next.js/NestJS architectures.

## Overview

This pipeline uses CrewAI agents orchestrated across three steps to:
1. **Discover and extract** information from source files using AI
2. **Structure and analyze** projects to understand relationships
3. **Synthesize requirements** and create migration mappings

## Features

- ✅ Automatic project boundary detection (via `pom.xml` or directory structure)
- ✅ AI-powered semantic extraction using local Ollama LLM
- ✅ Vector database storage with Weaviate for efficient retrieval
- ✅ Comprehensive analysis of DAOs, DTOs, Services, and UI components
- ✅ Cross-reference resolution between frontend and backend
- ✅ Detailed requirements documentation in Markdown
- ✅ Migration mapping to Next.js/NestJS microservices architecture

## Prerequisites

### 1. Ollama
Install and start Ollama, then pull the required models:

```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama
ollama serve

# Pull required models (in another terminal)
ollama pull gemma3:12b
ollama pull nomic-embed-text
```

### 2. Weaviate
Run Weaviate using Docker:

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

### 3. Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. **Create `.env` file** from the template:
   ```bash
   cp .env.example .env
   ```

2. **Update configuration** in `.env`:
   - `JAVA_SOURCE_DIR`: Path to your source code directory
   - `OLLAMA_BASE_URL`: Ollama service URL (default: `http://host.docker.internal:11434`)
   - `WEAVIATE_URL`: Weaviate service URL (default: `http://localhost:8080`)
   - Adjust other settings as needed

## Usage

### Basic Usage

Run the complete pipeline:

```bash
python main.py
```

The pipeline will:
1. Discover all source files in `JAVA_SOURCE_DIR`
2. Extract information using AI and store in Weaviate
3. Structure projects and analyze relationships
4. Generate requirements and migration documents

### Output Structure

```
data/
  output/
    {project_name}/
      requirements.md          # Detailed requirements document
      requirements_json.json   # Structured JSON data
      mapping.md              # Next.js/NestJS migration mapping
    logs/
      pipeline.log           # Execution logs
  build/
    step1_processed.json     # Step 1 processing log
```

### Pipeline Steps

#### Step 1: Source Discovery & AI Extraction
- Discovers all source files matching configured patterns
- Determines project boundaries
- Extracts structured information from each file using Ollama LLM
- Stores enriched metadata in Weaviate

#### Step 2: Project Structuring & Deep Analysis
- Organizes files by type (DAO, DTO, Service, Controller, UI)
- Analyzes data models, constraints, and business rules
- Maps service dependencies
- Analyzes frontend forms and UI components
- Resolves cross-references between frontend and backend

#### Step 3: Requirements Synthesis & Target Solution Mapping
- Generates comprehensive requirements documents
- Creates migration mapping to Next.js/NestJS architecture
- Reviews and validates completeness

## Architecture

### Agents

**Step 1 Agents:**
- `SourceReaderAgent`: Discovers files and project boundaries
- `FileExtractorAgent`: Extracts information using AI
- `DataStoreAgent`: Stores data in Weaviate

**Step 2 Agents:**
- `ProjectStructurerAgent`: Organizes project structure
- `DAODTOAnalyzerAgent`: Analyzes data layer
- `ServiceLinkerAgent`: Maps service dependencies
- `FrontendAnalyzerAgent`: Analyzes UI components
- `LinkageAgent`: Resolves cross-references

**Step 3 Agents:**
- `RequirementsWriterAgent`: Generates requirements docs
- `SolutionMappingAgent`: Creates migration mappings
- `ReviewAgent`: Quality assurance

### Components

- `src/config.py`: Configuration management
- `src/utils/logger.py`: Logging system
- `src/utils/ollama_client.py`: Ollama LLM integration
- `src/utils/weaviate_client.py`: Weaviate vector database client
- `src/pipeline.py`: Main pipeline orchestrator

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in `.env`
- Verify models are installed: `ollama list`

### Weaviate Connection Issues
- Ensure Weaviate is running: `docker ps | grep weaviate`
- Check `WEAVIATE_URL` in `.env`
- Verify ports 8080 and 50051 are available

### Large Codebase Processing
- Processing large codebases may take significant time
- Monitor logs in `data/output/logs/pipeline.log`
- Consider processing projects separately by updating `JAVA_SOURCE_DIR`

## Customization

### Adding File Types
Update glob patterns in `.env`:
```env
CUSTOM_INCLUDE_GLOBS=**/*.custom
```

Then update `Config.get_all_globs()` in `src/config.py` to include the new pattern.

### Customizing AI Prompts
Modify prompts in:
- `src/utils/ollama_client.py`: File extraction prompts
- `src/agents/step3_agents.py`: Requirements and mapping prompts

### Extending Agents
Add new agents by:
1. Creating tools in the appropriate `step*_agents.py` file
2. Creating CrewAI agents with the tools
3. Adding them to the pipeline in `src/pipeline.py`

## Limitations

1. **LLM Processing Time**: Large files may take time to process
2. **Memory Usage**: Processing very large codebases may require optimization
3. **Error Recovery**: Limited automatic retry logic
4. **Weaviate Version**: May need adjustments based on Weaviate client version

## Contributing

See `IMPLEMENTATION_PLAN.md` for detailed architecture and implementation notes.

## License

[Your License Here]


## 2025.10.29 Iteration 18 
# nohup
nohup ./scripts/run_full.sh > "log_full_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &


#  2025.11.03 Middle 

nohup python scripts/run_middle.py   --dir1 /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-core/src/main/java/at/a1ta/cuco/core/dao   --dir2 /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-core/src/main/java/at/a1ta/cuco/core/service   --count 100   --project cuco-core   --preview 5  > frznbrnf.log &