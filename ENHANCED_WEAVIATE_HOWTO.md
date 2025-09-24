# Enhanced Weaviate HOWTO Guide

This comprehensive guide covers infrastructure setup, testing, and operation of the Enhanced Weaviate system for Java JSP Application Reverse Engineering.

## Table of Contents

1. [Infrastructure Setup](#infrastructure-setup)
2. [Prerequisites Check](#prerequisites-check)
3. [Environment Configuration](#environment-configuration)
4. [Infrastructure Validation](#infrastructure-validation)
5. [Enhanced Weaviate Processing](#enhanced-weaviate-processing)
6. [Testing Procedures](#testing-procedures)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Infrastructure Setup

### Quick Start (M3 Max Development)

For Apple Silicon M3 Max development environments:

```bash
# 1. Run the automated setup script
./scripts/setup-m3-dev.sh

# 2. Start the development environment
./start-dev.sh

# 3. Check status at http://localhost:8000
```

### Manual Infrastructure Setup

#### 1. Weaviate Setup

**Option A: Docker (Recommended)**

```bash
# Basic Weaviate with Ollama integration
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED='true' \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e ENABLE_MODULES='text2vec-ollama,generative-ollama' \
  -e OLLAMA_ORIGIN='http://host.docker.internal:11434' \
  -e TEXT2VEC_OLLAMA_DEFAULT_MODEL='nomic-embed-text' \
  -e GENERATIVE_OLLAMA_DEFAULT_MODEL='danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth' \
  -v weaviate_data:/var/lib/weaviate \
  cr.weaviate.io/semitechnologies/weaviate:1.32.9
```

**Option B: Docker Compose (Full Development Environment)**

```bash
# Use the provided M3 Max development configuration
docker-compose -f docker-compose.m3-dev.yml up -d
```

#### 2. Ollama Setup

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models (in separate terminal)
ollama pull nomic-embed-text                    # Embedding model
ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth  # Main model
```

---

## Prerequisites Check

### System Requirements

```bash
# Check Docker installation
docker --version
docker-compose --version

# Check available system memory (recommended: 32GB+ for M3 Max)
# macOS
sysctl -n hw.memsize | awk '{print int($0/1024/1024/1024)"GB"}'

# Linux
free -h
```

### Python Dependencies

```bash
# Option 1: Install all dependencies (includes legacy components)
pip install -r requirements.txt

# Option 2: Install minimal Enhanced Weaviate dependencies only (recommended)
pip install -r requirements-weaviate.txt

# Verify installation with compatibility check
./infrastructure-check.sh
```

### Weaviate Client Compatibility

If you encounter Weaviate client import errors, use the pinned compatible version:

```bash
# Uninstall current version
pip uninstall weaviate-client

# Install compatible version
pip install "weaviate-client>=4.5.0,<4.9.0"

# Verify compatibility
python3 -c "from weaviate.auth import AuthApiKey; print('✅ Compatible Weaviate client')"
```

---

## Environment Configuration

### 1. Create Environment File

```bash
# Copy example environment
cp env.example .env

# Edit configuration
nano .env
```

### 2. Required Environment Variables

```bash
# AI Provider Configuration
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
OLLAMA_TIMEOUT=300

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_COLLECTION_PREFIX=java_codebase

# Rate Limiting
RATE_LIMIT_ENV=production  # or test, emergency

# Paths
OUTPUT_DIR=./output
WEAVIATE_DIR=./data/weaviate
```

### 3. Optional AI Provider Keys

```bash
# For OpenAI (alternative)
OPENAI_API_KEY=your-openai-key-here

# For Anthropic (alternative)
ANTHROPIC_API_KEY=your-anthropic-key-here
```

---

## Infrastructure Validation

### 1. Automated Infrastructure Check

The Enhanced Weaviate scripts include built-in infrastructure validation:

```bash
# This check is automatically performed by Step1_Enhanced_Weaviate.sh
./Step1_Enhanced_Weaviate.sh test
```

### 2. Manual Validation Steps

```bash
# Check Weaviate health
curl -s http://localhost:8080/v1/meta
curl -s http://localhost:8080/v1/.well-known/ready

# Check Ollama availability
curl -s http://localhost:11434/api/tags

# Verify specific model availability
curl -s http://localhost:11434/api/tags | grep -i qwen3-coder

# Test AI provider connection
python3 src/test_ai_providers.py
```

### 3. Infrastructure Status Script

Create a quick status check script:

```bash
# Create infrastructure-check.sh
cat > infrastructure-check.sh << 'EOF'
#!/bin/bash

echo "🔍 Enhanced Weaviate Infrastructure Status Check"
echo "================================================"

# Check Weaviate
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "✅ Weaviate: Running on http://localhost:8080"
    WEAVIATE_VERSION=$(curl -s http://localhost:8080/v1/meta | jq -r .version 2>/dev/null || echo "unknown")
    echo "   Version: $WEAVIATE_VERSION"
else
    echo "❌ Weaviate: Not accessible on http://localhost:8080"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama: Running on http://localhost:11434"
    OLLAMA_MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models | length' 2>/dev/null || echo "unknown")
    echo "   Models available: $OLLAMA_MODELS"
    echo "   Required models:"
    
    # Check for embedding model
    if curl -s http://localhost:11434/api/tags | grep -q "nomic-embed-text"; then
        echo "   ✅ nomic-embed-text (embedding)"
    else
        echo "   ❌ nomic-embed-text (embedding) - Run: ollama pull nomic-embed-text"
    fi
    
    # Check for main model
    if curl -s http://localhost:11434/api/tags | grep -q "qwen3-coder"; then
        echo "   ✅ qwen3-coder-30b (main model)"
    else
        echo "   ❌ qwen3-coder-30b - Run: ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
    fi
else
    echo "❌ Ollama: Not accessible on http://localhost:11434"
    echo "   Start with: ollama serve"
fi

# Check Python dependencies
echo ""
echo "🐍 Python Dependencies:"
python3 -c "
try:
    import weaviate
    print('   ✅ weaviate-client:', weaviate.__version__)
except ImportError:
    print('   ❌ weaviate-client not installed')

try:
    import aiohttp
    print('   ✅ aiohttp:', aiohttp.__version__)
except ImportError:
    print('   ❌ aiohttp not installed')
"

echo ""
echo "💾 System Resources:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    MEMORY_GB=$(sysctl -n hw.memsize | awk '{print int($0/1024/1024/1024)}')
    echo "   Memory: ${MEMORY_GB}GB"
    if [ "$MEMORY_GB" -lt 32 ]; then
        echo "   ⚠️  Warning: Less than 32GB memory may cause performance issues"
    fi
fi

echo ""
echo "📁 Directory Structure:"
for dir in output data/weaviate logs; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❓ $dir/ (will be created automatically)"
    fi
done

EOF

chmod +x infrastructure-check.sh
```

---

## Enhanced Weaviate Processing

### 1. Step-by-Step Processing

```bash
# Step 1: Enhanced analysis with data structure discovery
./Step1_Enhanced_Weaviate.sh [test|production|emergency]

# Step 2: Traditional requirements generation
./Step2_Enhanced_Weaviate.sh [test|production|emergency]

# Step 3: Modern requirements generation
./Step3_Enhanced_Weaviate.sh [test|production|emergency]
```

### 2. Rate Limiting Modes

- **test**: 10 req/min, 500 req/hour, 8s delays, 180s timeout
- **production**: 15 req/min, 800 req/hour, 4s delays, 240s timeout
- **emergency**: 5 req/min, 200 req/hour, 10s delays, 120s timeout

### 3. Output Structure

After successful processing, expect these outputs:

```
output/
├── weaviate_metadata.json              # Core analysis results
├── data_structures_analysis.json       # Data structure discovery
├── enhanced_architecture_report.json   # Architecture analysis
├── analysis_summary.json              # Processing summary
└── requirements_weaviate/
    ├── by_layer/                       # Requirements by architectural layer
    ├── by_data_structure/              # Data-driven requirements
    └── analysis/                       # Detailed analysis reports
```

---

## Testing Procedures

### 1. AI Provider Testing

```bash
# Test all configured AI providers
python3 src/test_ai_providers.py

# Test specific rate limiting
python3 src/test_rate_limiter.py

# Test Ollama integration specifically
python3 src/test_ollama_debug.py
```

### 2. Enhanced Weaviate Integration Test

```bash
# Quick integration test (processes small subset)
DEBUGFILE=debug_files_example.txt ./Step1_Enhanced_Weaviate.sh test

# Full integration test
./infrastructure-check.sh && ./Step1_Enhanced_Weaviate.sh test
```

### 3. End-to-End Testing

```bash
# Complete pipeline test
./infrastructure-check.sh
./Step1_Enhanced_Weaviate.sh test
./Step2_Enhanced_Weaviate.sh test
./Step3_Enhanced_Weaviate.sh test

# Check outputs
ls -la output/
cat output/analysis_summary.json
```

### 4. Web Interface Testing

```bash
# Start web interface
./start_web.sh

# Test in browser: http://localhost:8000
# Health check endpoint: http://localhost:8000/api/health
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Weaviate Connection Issues

**Problem**: `❌ Error: Weaviate is not running on localhost:8080`

**Solutions**:
```bash
# Check if Docker is running
docker ps | grep weaviate

# Restart Weaviate
docker restart weaviate

# Check logs
docker logs weaviate

# Reset Weaviate data (if needed)
docker stop weaviate
docker rm weaviate
docker volume rm weaviate_data
# Then recreate with setup commands
```

#### 2. Weaviate Client Compatibility Issues

**Problem**: `TypeError: Too few arguments for <class 'weaviate.collections.data.executor._DataCollectionExecutor'>`

**Solutions**:
```bash
# Fix compatibility by using pinned version
pip uninstall weaviate-client
pip install "weaviate-client>=4.5.0,<4.9.0"

# Alternative: Clean install with Enhanced Weaviate requirements
pip install -r requirements-weaviate.txt

# Verify fix works
./infrastructure-check.sh
```

#### 3. Ollama Model Issues

**Problem**: Model not found or slow responses

**Solutions**:
```bash
# Check available models (note: your models show with capital letters)
ollama list

# Pull missing models if needed
ollama pull nomic-embed-text
ollama pull danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth

# Alternative smaller model for testing
ollama pull qwen2.5-coder:7b

# Increase timeout for large models
export OLLAMA_TIMEOUT=600

# Monitor resource usage
# macOS: Activity Monitor
# Linux: htop or top
```

#### 4. Memory Issues

**Problem**: Out of memory errors or slow processing

**Solutions**:
```bash
# Check memory usage
free -h  # Linux
vm_stat # macOS

# Use smaller model
export OLLAMA_MODEL_NAME=qwen2.5-coder:7b

# Reduce batch sizes (edit scripts)
# Restart Docker with more memory allocation
```

#### 4. Rate Limiting Issues

**Problem**: Too many API requests

**Solutions**:
```bash
# Use more conservative mode
./Step1_Enhanced_Weaviate.sh emergency

# Check rate limiting configuration
cat config/rate_limiting.yaml

# Wait and retry
sleep 300 && ./Step1_Enhanced_Weaviate.sh production
```

### 5. Debug Mode

Use debug mode for troubleshooting specific files:

```bash
# Create debug file list
echo "/path/to/specific/file.java" > debug_files.txt

# Run in debug mode
export DEBUGFILE=debug_files.txt
./Step1_Enhanced_Weaviate.sh test
```

---

## Advanced Configuration

### 1. Custom Weaviate Schema

Edit `src/weaviate_schemas.py` to customize:
- Collection names
- Property definitions
- Vector configurations
- Index settings

### 2. Ollama Model Configuration

```bash
# Create custom Modelfile
cat > Modelfile.custom << EOF
FROM qwen2.5-coder:7b

# Custom system prompt for Java analysis
SYSTEM """You are an expert Java enterprise application analyst..."""

# Adjust parameters
PARAMETER temperature 0.1
PARAMETER top_k 40
PARAMETER top_p 0.9
EOF

# Build custom model
ollama create java-analyzer -f Modelfile.custom

# Use in configuration
export OLLAMA_MODEL_NAME=java-analyzer
```

### 3. Performance Tuning

```bash
# Adjust batch sizes in processing scripts
# Edit Step1_Enhanced_Weaviate.sh:
# - Reduce batch size for memory-constrained systems
# - Increase delays for API stability

# Weaviate performance tuning
# Add to docker run command:
-e GOMEMLIMIT=8GiB \
-e GOGC=50 \
--memory=10g \
--cpus=4
```

### 4. Monitoring and Observability

```bash
# Enable Docker stats monitoring
docker stats weaviate

# Monitor Ollama metrics
curl http://localhost:11434/api/ps

# Check processing progress
tail -f logs/enhanced_weaviate_processor.log
```

---

## Quick Reference

### Essential Commands

```bash
# Infrastructure check
./infrastructure-check.sh

# Full processing pipeline
./Step1_Enhanced_Weaviate.sh production
./Step2_Enhanced_Weaviate.sh production  
./Step3_Enhanced_Weaviate.sh production

# Development environment
./scripts/setup-m3-dev.sh
./start-dev.sh

# Troubleshooting
python3 src/test_ai_providers.py
docker logs weaviate
ollama list
```

### Important URLs

- **Weaviate**: http://localhost:8080
- **Ollama**: http://localhost:11434  
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health

### Support Files

- **Configuration**: `CLAUDE.md`
- **Environment**: `.env`
- **Requirements**: `requirements.txt`
- **Archive**: `archive/README.md` (legacy components)

---

## Conclusion

This Enhanced Weaviate system provides advanced Java JSP application analysis with:

- **Data Structure Discovery**: Automatic entity and DTO identification
- **Architectural Classification**: Layer-based code organization
- **Vector Storage**: Semantic search with Weaviate
- **AI Integration**: Multiple provider support with Ollama optimization
- **Enterprise Ready**: Rate limiting, monitoring, and error handling

For additional help, refer to:
- Issue tracking: The codebase documentation
- Legacy components: `archive/` directory
- Configuration: `CLAUDE.md`

Happy analyzing! 🚀