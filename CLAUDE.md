# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Java JSP Application Reverse Engineering Tool that uses AI-powered analysis to extract requirements, data structures, and business rules from Java/JSP codebases. The tool leverages **Enhanced Weaviate** for vector storage with advanced data structure discovery and supports multiple AI providers (OpenAI, Anthropic, Ollama).

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
# Enhanced Weaviate Processing Pipeline
# Step 1: Process and analyze files with enhanced Weaviate storage
./Step1_Enhanced_Weaviate.sh [test|production|emergency]

# Step 2: Generate requirements documentation with Weaviate
./Step2_Enhanced_Weaviate.sh [test|production|emergency]

# Step 3: Generate additional documentation with Weaviate
./Step3_Enhanced_Weaviate.sh [test|production|emergency]

# Note: Legacy ChromaDB-based scripts moved to archive/ directory
```

### Web Interface
```bash
# Start web interface with Weaviate integration
./start_web.sh

# Note: Legacy FastAPI/Flask web servers moved to archive/ directory
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

**Enhanced Weaviate Integration (`src/weaviate_connector.py`, `src/weaviate_schemas.py`)**
- Advanced data structure discovery and entity relationship mapping
- Vector storage with metadata for file paths, functions, classes, and data structures
- Semantic search capabilities with enhanced architectural classification
- Intelligent schema management for different code artifacts

**Enhanced Processing Pipeline**
1. **File Processing** (`src/file_processor.py`) - Scans and extracts metadata
2. **AI Analysis** (`src/ai_analyzer.py`) - Batch processing with rate limiting
3. **Enhanced Weaviate Processing** (`src/enhanced_weaviate_processor.py`) - Data structure discovery
4. **Requirements Generation** (`src/weaviate_requirements_generator.py`) - Structured documentation
5. **Weaviate Storage** - Vector embeddings with architectural classification and data structure insights

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

**Enhanced Data Structure Discovery**
- Automatic entity and DTO identification from Java code
- Relationship mapping between data structures
- Data flow analysis across architectural layers
- Business rule extraction from validation logic

**Enhanced Weaviate Features**
- Schema-aware vector storage for different code artifacts
- Intelligent metadata classification (controllers, services, entities, etc.)
- Cross-reference analysis for architectural dependencies
- Advanced querying capabilities for semantic code search

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
WEAVIATE_DIR=./data/weaviate

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_COLLECTION_PREFIX=java_codebase
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

**Enhanced Web Interface**
- Chat-based interface for querying processed documentation
- Real-time Weaviate querying with AI-powered responses
- Advanced semantic search across data structures and architectural components

**StrictDoc Integration**
- Generates formal requirements documentation
- Converts markdown to StrictDoc format with proper structure
- Maintains document hierarchy and relationships

## Important Notes

- Always use the Enhanced Weaviate shell scripts (Step1_Enhanced_Weaviate.sh, etc.) rather than calling Python directly
- The system automatically handles API quota limits and provides helpful error messages
- Weaviate collections are persistent - processing builds upon previous runs with enhanced data structure analysis
- Debug mode processes only files listed in the debug file, useful for incremental development
- The web interface provides real-time access to processed documentation via semantic search with Weaviate

## Archive Information

**Legacy Components**: Non-enhanced scripts and ChromaDB-based components have been moved to the `archive/` directory including:
- Original Step1.sh, Step2.sh, Step3.sh (ChromaDB-based)
- ChromaDB connectors and processors
- Legacy web interface components (FastAPI/Flask implementations)
- Old test files and documentation

**Focus**: The codebase now focuses exclusively on Enhanced Weaviate implementation with advanced data structure discovery and architectural analysis.