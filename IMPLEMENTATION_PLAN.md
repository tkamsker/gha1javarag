# Implementation Plan: CrewAI Requirements Extraction Pipeline

## Overview
This document outlines the step-by-step implementation of the Multi-Step CrewAI Requirements Extraction Pipeline as specified in Iteration18.md.

## Architecture

### Components
1. **Configuration System** (`src/config.py`)
   - Loads environment variables from `.env`
   - Manages all pipeline configuration
   - Provides helper methods for directory setup

2. **Utility Modules** (`src/utils/`)
   - `logger.py`: Centralized logging system
   - `ollama_client.py`: LLM integration for semantic extraction
   - `weaviate_client.py`: Vector database integration

3. **CrewAI Agents** (`src/agents/`)
   - **Step 1** (`step1_agents.py`): Source discovery and extraction
   - **Step 2** (`step2_agents.py`): Project structuring and analysis
   - **Step 3** (`step3_agents.py`): Requirements synthesis and mapping

4. **Pipeline Orchestrator** (`src/pipeline.py`)
   - Coordinates all three steps
   - Manages workflow and data flow
   - Handles error recovery

5. **Main Entry Point** (`main.py`)
   - CLI interface
   - Pipeline execution

## Implementation Steps

### ✅ Step 1: Project Setup
- [x] Create `.env.example` file with configuration template
- [x] Create `requirements.txt` with dependencies
- [x] Set up project structure (`src/` directory)
- [x] Create configuration management (`src/config.py`)

### ✅ Step 2: Utility Modules
- [x] Implement logging system
- [x] Implement Ollama client for LLM interactions
- [x] Implement Weaviate client for vector storage

### ✅ Step 3: Step 1 Agents (Source Discovery & AI Extraction)
- [x] `SourceReaderAgent`: File discovery and project industry detection
- [x] `FileExtractorAgent`: AI-powered file information extraction
- [x] `DataStoreAgent`: Weaviate storage management

### ✅ Step 4: Step 2 Agents (Project Structuring & Deep Analysis)
- [x] `ProjectStructurerAgent`: Organize files by type (DAO, DTO, Service, UI)
- [x] `DAODTOAnalyzerAgent`: Extract data models and constraints
- [x] `ServiceLinkerAgent`: Map service dependencies
- [x] `FrontendAnalyzerAgent`: Analyze UI files and forms
- [x] `LinkageAgent`: Resolve cross-references

### ✅ Step 5: Step 3 Agents (Requirements Synthesis)
- [x] `RequirementsWriterAgent`: Generate Markdown requirements
- [x] `SolutionMappingAgent`: Map to Next.js/NestJS architecture
- [x] `ReviewAgent`: Quality assurance and completeness check

### ✅ Step 6: Pipeline Orchestrator
- [x] Implement `RequirementsExtractionPipeline` class
- [x] Implement `run_step1()`, `run_step2()`, `run_step3()` methods
- [x] Implement main `run()` method

### ✅ Step 7: Main Entry Point
- [x] Create `main.py` with CLI interface
- [x] Add error handling and logging

## Usage

### Prerequisites
1. **Ollama**: Must be running with the specified model
   ```bash
   ollama pull gemma3:12b
   ollama pull nomic-embed-text
   ```

2. **Weaviate**: Must be running on localhost:8080
   ```bash
   docker run -d -p 8080:8080 -p 50051:50051 semitechnologies/weaviate
   ```

3. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Copy `.env.example` to `.env`
2. Update `JAVA_SOURCE_DIR` to point to your source code
3. Adjust other configuration as needed

### Running the Pipeline
```bash
python main.py
```

## Output Structure

```
data/output/
  {project}/
    requirements.md          # Detailed requirements document
    requirements_json.json   # Structured JSON data
    mapping.md              # Migration mapping to Next.js/NestJS
  logs/
    pipeline.log           # Execution logs
```

## Next Steps / Improvements

1. **Error Handling**: Add retry logic for LLM calls and Weaviate operations
2. **Caching**: Implement caching for LLM responses to speed up re-runs
3. **Parallel Processing**: Process multiple files concurrently
4. **Progress Tracking**: Add progress bars and status updates
5. **Validation**: Add validation for configuration and prerequisites
6. **Testing**: Add unit tests for agents and tools
7. **Documentation**: Generate API documentation

## Known Limitations

1. **Weaviate Connection**: The client may need adjustment based on Weaviate version
2. **LLM Timeout**: Large files may timeout; consider chunking
3. **Memory Usage**: Processing large codebases may require memory optimization
4. **Error Recovery**: Limited retry logic; manual recovery may be needed

