# Java Analysis Tool - M3 Max Minimal Development Setup

## Overview

This is the **ultra-minimal** development environment optimized for Apple M3 Max chips. It uses your **local Ollama installation** running directly on macOS, with only essential Docker services to minimize overhead and maximize performance.

## Architecture

### What Runs Locally (No Docker Overhead)
- 🤖 **Ollama with Qwen3-Coder-30B**: Direct macOS execution
- 📁 **File System**: Native file access
- 🔧 **Development Tools**: Native toolchain

### What Runs in Docker (Minimal)
- 🔍 **Weaviate**: Vector database (connects to host Ollama)
- 💾 **Redis**: Lightweight cache (256MB limit)
- 🌐 **Web Interface**: Development UI

## Resource Usage Comparison

| Setup Type | Docker Memory | Total Memory | Containers | Startup Time |
|------------|--------------|--------------|------------|--------------|
| **Full Setup** | ~20GB | ~35GB | 7+ | 5-10 min |
| **Minimal Setup** | ~5GB | ~20GB | 3 | 30-60 sec |

## Prerequisites

### Hardware
- **Minimum**: M3 Max with 32GB unified memory
- **Recommended**: M3 Max with 64GB+ unified memory
- **Storage**: 40GB free (30GB for models + 10GB working)

### Software
```bash
# Required installations
brew install ollama
brew install --cask docker

# Start Ollama service
brew services start ollama
```

## Quick Start

### 1. Automated Setup
```bash
# Run the setup script
./scripts/setup-m3-minimal.sh

# This will:
# - Check prerequisites
# - Install required Ollama models (~30GB download)
# - Create minimal configuration
# - Set up startup scripts
```

### 2. Start Development Environment
```bash
# Start all services
./start-minimal.sh

# Check status
./test-minimal.sh
```

### 3. Access Services
- **Web Interface**: http://localhost:8000
- **Weaviate API**: http://localhost:8080
- **Ollama API**: http://localhost:11434
- **Redis**: localhost:6379

## Required Ollama Models

The setup automatically installs these models:

```bash
# Embedding model (~1GB)
ollama pull nomic-embed-text

# Primary coding model (~20GB) 
ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
```

## Configuration

### Environment Variables (`.env.minimal`)
```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
WEAVIATE_URL=http://localhost:8080
REDIS_URL=redis://localhost:6379/0
```

### Docker Compose (`docker-compose.m3-dev-minimal.yml`)
```yaml
services:
  weaviate:    # 4GB limit
  redis:       # 384MB limit  
  web-interface: # 768MB limit
```

## Development Commands

### Environment Management
```bash
# Start minimal environment
./start-minimal.sh

# Stop Docker services (keeps Ollama running)
./stop-minimal.sh

# Test all services
./test-minimal.sh

# View Docker logs
docker-compose -f docker-compose.m3-dev-minimal.yml logs -f
```

### Ollama Management (Direct)
```bash
# List installed models
ollama list

# Test model
ollama run danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth "Explain this Java code: public class Test {}"

# Monitor Ollama
ps aux | grep ollama
```

### Resource Monitoring
```bash
# Docker resource usage
docker stats

# System resources
top -o mem

# Ollama process
activity monitor  # Look for "ollama" process
```

## Development Workflow

### 1. Code Analysis
```bash
# Place Java/JSP project
mkdir -p test-projects/my-app
cp -r /path/to/java/project/* test-projects/my-app/

# Run analysis (uses local Ollama)
python src/main.py --source test-projects/my-app --output output/my-app
```

### 2. Interactive Development
```bash
# Use Ollama directly for testing
ollama run danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth

# Test API calls
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth","prompt":"Analyze this Java class"}'
```

### 3. Vector Search Testing  
```bash
# Test Weaviate connection
curl http://localhost:8080/v1/.well-known/ready

# Query collections
curl http://localhost:8080/v1/objects
```

## Performance Optimization

### Ollama Settings
```bash
# Set environment variables for optimal M3 Max performance
export OLLAMA_NUM_PARALLEL=8      # Use 8 of 16 CPU cores
export OLLAMA_MAX_LOADED_MODELS=2 # Limit concurrent models
export OLLAMA_ORIGINS="*"         # Allow Docker connections
```

### Memory Management
- **Ollama**: Uses ~15-25GB for Qwen3-Coder-30B
- **Docker**: Uses ~5GB total for all services  
- **Available**: 32GB+ remaining for development tools

### Thermal Management
- **Monitor**: Use Activity Monitor to watch CPU/GPU usage
- **Cooling**: Ensure adequate ventilation for sustained workloads
- **Power**: Use AC adapter for best performance

## Troubleshooting

### Common Issues

**1. Ollama Not Responding**
```bash
# Check if running
brew services list | grep ollama

# Restart if needed
brew services restart ollama

# Manual start
ollama serve
```

**2. Models Not Found**
```bash
# Check installed models
ollama list

# Pull missing models
ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
```

**3. Docker Connection Issues**
```bash
# Check Docker Desktop is running
docker version

# Restart Docker services
./stop-minimal.sh && ./start-minimal.sh
```

**4. Memory Pressure**
```bash
# Check memory usage
memory_pressure

# Free up memory
sudo purge

# Reduce model concurrency
export OLLAMA_MAX_LOADED_MODELS=1
```

### Performance Issues

**Slow Model Response**
- Ensure AC power (not battery)
- Check thermal throttling in Activity Monitor
- Reduce context size if needed
- Use smaller model for testing: `qwen2.5-coder:14b`

**High Memory Usage**  
- Monitor with Activity Monitor
- Adjust Docker memory limits
- Use swap if needed (performance impact)

## Advanced Configuration

### Custom Ollama Models
```bash
# Add additional models
ollama pull qwen2.5-coder:14b  # Smaller backup model
ollama pull codellama:13b      # Alternative coding model

# Update environment
OLLAMA_MODEL_NAME=qwen2.5-coder:14b  # Use smaller model
```

### Docker Resource Limits
Edit `docker-compose.m3-dev-minimal.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 2G      # Reduce if needed
      cpus: '2.0'     # Limit CPU usage
```

## Comparison with Full Setup

| Feature | Minimal Setup | Full Setup |
|---------|---------------|------------|
| **AI Processing** | Local Ollama | Docker Ollama |
| **Memory Usage** | ~20GB total | ~35GB total |
| **Startup Time** | 30-60 seconds | 5-10 minutes |
| **Model Loading** | Instant (pre-loaded) | 2-5 minutes |
| **Development Speed** | Very Fast | Moderate |
| **Resource Efficiency** | Excellent | Good |
| **Monitoring** | Basic | Full Grafana/Prometheus |
| **Database** | None (optional) | PostgreSQL |

## Production Considerations

This minimal setup is **development-only**. For production:
- Use full Docker setup with monitoring
- Add PostgreSQL for persistence  
- Implement proper security
- Add backup strategies
- Use production-grade load balancing

## Next Steps

1. **Start Development**: Use minimal setup for fast iteration
2. **Test Models**: Experiment with different Ollama models
3. **Optimize Performance**: Tune for your specific M3 Max configuration
4. **Scale Up**: Move to full setup when ready for production features

---

**🎯 Perfect for rapid M3 Max development with minimal overhead!**

*Total setup time: 5-10 minutes + model download time*  
*Memory footprint: ~20GB vs 35GB+ for full setup*  
*Performance: Native speed with minimal container overhead*