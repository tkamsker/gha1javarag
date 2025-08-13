# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Java JSP Application Reverse Engineering Tool that uses AI-powered analysis to extract requirements, data structures, and business rules from Java/JSP codebases. The tool leverages ChromaDB for vector storage and supports multiple AI providers (OpenAI, Anthropic, Ollama).

## Common Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env
# Edit .env with your API keys and configuration
```

### Core Processing Steps
```bash
# Step 1: Process and analyze files (with rate limiting)
./Step1.sh [test|production|emergency]

# Step 2: Generate requirements documentation
./Step2.sh [test|production|emergency]

# Step 3: Generate additional documentation
./Step3.sh [test|production|emergency]

# Combined processing (legacy)
./Lofalassn.sh [test|production|emergency]
```

### Web Interface
```bash
# Start web interface (auto-detects FastAPI/Flask)
./start_web.sh

# Or start specific web server
./run_fastapi.sh
./run_flask.sh
```

### Testing
```bash
# Test AI providers
python src/test_ai_providers.py

# Test ChromaDB functionality
python test_chromadb.py
python test_chromadb_functionality.py

# Test rate limiting
python src/test_rate_limiter.py

# Test specific features
python test_debug_feature.py
python test_enhanced_chunking.py
```

### StrictDoc Documentation
```bash
# Generate StrictDoc documentation
cd strictdoc
./Web.sh
```

## Architecture Overview

### Core Components

**AI Provider System (`src/ai_providers.py`)**
- Abstract base class with implementations for OpenAI, Anthropic, and Ollama
- Factory pattern for provider selection via `AI_PROVIDER` environment variable
- Built-in rate limiting and error handling

**ChromaDB Integration (`src/chromadb_connector.py`)**
- Enhanced chunking for intelligent code segmentation
- Vector storage with metadata for file paths, functions, classes
- Semantic search capabilities for code and documentation

**Processing Pipeline**
1. **File Processing** (`src/file_processor.py`) - Scans and extracts metadata
2. **AI Analysis** (`src/ai_analyzer.py`) - Batch processing with rate limiting
3. **Requirements Generation** (`src/requirements_analyzer.py`) - Structured documentation
4. **ChromaDB Storage** - Vector embeddings with intelligent chunking

**Rate Limiting System (`src/rate_limiter.py`)**
- Configurable rate limits per AI provider
- Exponential backoff with retry logic
- Quota monitoring and automatic fallback

### Key Patterns

**Batch Processing**
- Files processed in batches (default: 3 files per API call)
- Priority-based file selection (Java → JSP → XML → others)
- Intelligent file filtering to skip binary/compiled files

**Multi-Provider Support**
- Environment variable switching between AI providers
- Provider-specific rate limiting and error handling
- Graceful fallback between providers

**Enhanced Chunking**
- Function-level code chunking for better semantic search
- Metadata extraction (class names, function signatures)
- Complexity scoring for prioritization

## Environment Configuration

### Required Variables
```bash
# AI Provider Selection
AI_PROVIDER=openai|anthropic|ollama

# Provider-specific API keys
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=deepseek-r1:32b
OLLAMA_TIMEOUT=240  # Timeout in seconds (overrides config file)

# Rate Limiting
RATE_LIMIT_ENV=test|production|emergency

# Paths
OUTPUT_DIR=./output
CHROMADB_DIR=./data/chromadb
```

### Rate Limiting Modes
- **test**: 10 req/min, 500 req/hour, 8s delays, 180s timeout
- **production**: 15 req/min, 800 req/hour, 4s delays, 240s timeout
- **emergency**: 5 req/min, 200 req/hour, 10s delays, 120s timeout

### Ollama Timeout Configuration
The `OLLAMA_TIMEOUT` environment variable overrides config file timeouts:
- **240-300s**: Recommended for large models (deepseek-r1:70b, etc.)
- **180-240s**: Recommended for medium models 
- **120-180s**: Recommended for small models
- Set in `.env` file: `OLLAMA_TIMEOUT=300`

## Key Features

**Debug Mode**
- Set `DEBUGFILE` environment variable to process specific files
- Useful for testing changes on subset of codebase

**Web Interface**
- Chat-based interface for querying processed documentation
- Supports both FastAPI and Flask backends
- Real-time ChromaDB querying with AI-powered responses

**StrictDoc Integration**
- Generates formal requirements documentation
- Converts markdown to StrictDoc format with proper structure
- Maintains document hierarchy and relationships

## Important Notes

- Always use the shell scripts (Step1.sh, Step2.sh, etc.) rather than calling Python directly
- The system automatically handles API quota limits and provides helpful error messages
- ChromaDB collections are persistent - processing builds upon previous runs
- Debug mode processes only files listed in the debug file, useful for incremental development
- The web interface provides real-time access to processed documentation via semantic search