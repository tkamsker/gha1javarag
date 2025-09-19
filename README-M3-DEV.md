# Java Analysis Tool - M3 Max Development Setup

## Overview

This development environment is optimized for Apple M3 Max chips and provides a complete local setup for Iteration 13 of the Java JSP Application Reverse Engineering Tool.

## Features

- 🚀 **Ollama with Qwen3-Coder-30B**: Local AI processing with 1M token context
- 🔍 **Weaviate Vector Database**: Scalable semantic search with local embeddings
- 🐳 **Docker Compose**: Fully containerized development environment
- 📊 **Monitoring Stack**: Prometheus + Grafana for performance monitoring
- 💾 **Redis Caching**: Fast caching layer for improved performance
- 🗄️ **PostgreSQL**: Metadata and session storage
- 🌐 **Web Interface**: Development-friendly web UI

## Prerequisites

### Hardware Requirements (M3 Max Optimized)
- **Minimum**: M3 Max with 32GB unified memory
- **Recommended**: M3 Max with 64GB+ unified memory
- **Storage**: 50GB free space (for models and data)

### Software Requirements
- macOS 14.0+ (Sonoma)
- Docker Desktop for Mac 4.25+
- Git

## Quick Start

1. **Clone and setup the environment:**
   ```bash
   cd /path/to/project
   ./scripts/setup-m3-dev.sh
   ```

2. **Start the development environment:**
   ```bash
   ./start-dev.sh
   ```

3. **Monitor the initialization:**
   ```bash
   docker-compose -f docker-compose.m3-dev.yml logs -f ollama-init
   ```

4. **Access the web interface:**
   Open http://localhost:8000

## First Run Notes

⏱️ **Initial Setup Time**: 20-30 minutes for model download  
📦 **Models Downloaded**: 
- `danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth` (~20GB)
- `nomic-embed-text` (~1GB)  
- `qwen2.5-coder:14b` (~8GB backup model)

## Service URLs

| Service | URL | Credentials |
|---------|-----|------------|
| Web Interface | http://localhost:8000 | - |
| Weaviate | http://localhost:8080 | - |
| Ollama | http://localhost:11434 | - |
| Grafana | http://localhost:3000 | admin/dev123 |
| Prometheus | http://localhost:9090 | - |
| PostgreSQL | localhost:5432 | dev_user/dev_password |
| Redis | localhost:6379 | - |

## Development Commands

### Environment Management
```bash
# Start all services
./start-dev.sh

# Stop all services  
./stop-dev.sh

# View logs for all services
docker-compose -f docker-compose.m3-dev.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.m3-dev.yml logs -f ollama
```

### Ollama Model Management
```bash
# List available models
docker exec -it $(docker-compose -f docker-compose.m3-dev.yml ps -q ollama) ollama list

# Pull additional models
docker exec -it $(docker-compose -f docker-compose.m3-dev.yml ps -q ollama) ollama pull model-name

# Test model inference
docker exec -it $(docker-compose -f docker-compose.m3-dev.yml ps -q ollama) ollama run danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
```

### Database Management
```bash
# Connect to PostgreSQL
docker exec -it $(docker-compose -f docker-compose.m3-dev.yml ps -q postgres) psql -U dev_user -d java_analysis_dev

# Connect to Redis
docker exec -it $(docker-compose -f docker-compose.m3-dev.yml ps -q redis) redis-cli
```

### Monitoring and Debugging
```bash
# Check system health
curl http://localhost:8000/api/health

# Monitor resource usage
docker stats

# Check Weaviate status
curl http://localhost:8080/v1/.well-known/ready

# Check Ollama models
curl http://localhost:11434/api/tags
```

## Development Workflow

### 1. Code Analysis Workflow
```bash
# 1. Place your Java/JSP project in test-projects/
mkdir -p test-projects/my-project
cp -r /path/to/java/project test-projects/my-project/

# 2. Run analysis via Python scripts
python src/main.py --source test-projects/my-project --output output/my-project

# 3. View results in web interface
open http://localhost:8000
```

### 2. Model Testing and Optimization
```bash
# Test different context sizes
python src/test_context_optimization.py --context-size 100000
python src/test_context_optimization.py --context-size 500000
python src/test_context_optimization.py --context-size 1000000
```

### 3. Performance Monitoring
- **Grafana Dashboard**: http://localhost:3000
- **Prometheus Metrics**: http://localhost:9090
- **System Resources**: Activity Monitor

## Configuration Files

### Environment Variables (`.env.dev`)
- AI provider settings
- Database connections  
- Service URLs
- Debug flags

### Docker Compose (`docker-compose.m3-dev.yml`)
- Service definitions optimized for M3 Max
- Resource limits and reservations
- Network configuration
- Volume mappings

### Monitoring (`monitoring/prometheus-dev.yml`)
- Scrape configurations
- Alert rules for development
- Storage retention settings

## Troubleshooting

### Common Issues

**1. Model Download Fails**
```bash
# Check internet connection and retry
docker-compose -f docker-compose.m3-dev.yml restart ollama-init
```

**2. Out of Memory Errors**  
```bash
# Check available memory
system_profiler SPHardwareDataType | grep Memory
# Reduce concurrent processes or use smaller models
```

**3. Slow Performance**
```bash
# Check if running on battery power (use AC adapter)
# Monitor CPU/GPU usage in Activity Monitor
# Consider reducing batch sizes in configuration
```

**4. Port Conflicts**
```bash
# Check what's using the ports
lsof -i :8080
lsof -i :11434
# Modify port mappings in docker-compose file if needed
```

### Resource Monitoring

Monitor these metrics during development:
- **Memory Usage**: Should stay under 80% of available unified memory
- **CPU Usage**: Expect high usage during model inference
- **GPU Usage**: Monitor via Activity Monitor -> GPU tab
- **Storage**: Models require ~30GB space

### Performance Tips

1. **Use AC Power**: Ensure MacBook is plugged in for optimal performance
2. **Close Unused Apps**: Free up memory for AI models
3. **Monitor Thermal**: Use fan control if system gets too hot
4. **Batch Processing**: Process files in smaller batches if memory constrained

## Advanced Configuration

### Custom Model Selection

Edit `docker-compose.m3-dev.yml` to use different models:
```yaml
environment:
  GENERATIVE_OLLAMA_DEFAULT_MODEL: 'your-preferred-model'
```

### Resource Limits

Adjust memory limits based on your M3 Max configuration:
```yaml
deploy:
  resources:
    limits:
      memory: 32G  # Adjust based on available memory
```

### Development vs Production

This setup is optimized for development:
- Relaxed security settings
- Verbose logging
- Hot reloading enabled
- Smaller retention periods

For production deployment, see `docker-compose.yml` and related production configurations.

## Support

For issues specific to M3 Max development:
1. Check Activity Monitor for resource usage
2. Review Docker logs for error messages  
3. Ensure sufficient free storage space
4. Verify Docker Desktop is using Apple Silicon optimization

## Next Steps

1. **Run Sample Analysis**: Test with provided sample projects
2. **Customize Models**: Experiment with different Ollama models
3. **Monitor Performance**: Use Grafana dashboards to optimize
4. **Develop Features**: Begin implementing Iteration 13 improvements

---

**🎯 Ready to develop enterprise-scale Java code analysis with local AI on Apple Silicon!**