# Weaviate Docker Setup for Java Codebase Analysis

This document explains how to set up Weaviate with the required modules for the Java codebase analysis tool.

## Quick Start

### Option 1: Using the Shell Script (Recommended)
```bash
# Start Weaviate with all required modules
./docker-weaviate.sh

# Check status
./docker-weaviate.sh status

# View logs
./docker-weaviate.sh logs

# Stop Weaviate
./docker-weaviate.sh stop

# Restart Weaviate
./docker-weaviate.sh restart

# Clean up everything
./docker-weaviate.sh clean
```

### Option 2: Using Docker Compose
```bash
# Start Weaviate
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f weaviate

# Stop Weaviate
docker-compose down

# Stop and remove data
docker-compose down -v
```

## What This Setup Provides

### Required Modules
- **text2vec-ollama**: For vectorizing text using Ollama models
- **generative-ollama**: For generating text using Ollama models

### Configuration
- **Ports**: 
  - HTTP API: `http://localhost:8080`
  - gRPC: `localhost:50051`
- **Authentication**: Anonymous access enabled
- **CORS**: Enabled for all origins
- **Persistence**: Data stored in `./weaviate-data/`
- **Ollama Integration**: Connected to `http://host.docker.internal:11434`

## Prerequisites

1. **Docker**: Must be installed and running
2. **Ollama**: Must be running on `localhost:11434`
3. **Ports**: 8080 and 50051 must be available

## Verification

After starting Weaviate, verify it's working:

```bash
# Check if Weaviate is responding
curl http://localhost:8080/v1/meta

# Check available modules
curl http://localhost:8080/v1/modules

# Check if text2vec-ollama is available
curl http://localhost:8080/v1/modules/text2vec-ollama
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8080
   lsof -i :8080
   
   # Kill the process or change the port in the script
   ```

2. **Ollama Not Accessible**
   ```bash
   # Make sure Ollama is running
   ollama serve
   
   # Check if it's accessible
   curl http://localhost:11434/api/tags
   ```

3. **Permission Issues**
   ```bash
   # Make sure the script is executable
   chmod +x docker-weaviate.sh
   
   # Check Docker permissions
   docker ps
   ```

4. **Module Not Found**
   ```bash
   # Check Weaviate logs
   docker logs weaviate-java-analysis
   
   # Restart with clean data
   ./docker-weaviate.sh clean
   ./docker-weaviate.sh
   ```

### Data Persistence

- **Data Location**: `./weaviate-data/`
- **Backup**: Copy the `weaviate-data` directory
- **Reset**: Delete the `weaviate-data` directory and restart

### Performance Tuning

For large codebases, you may want to adjust:

```bash
# Increase memory limit
docker run --memory=4g ...

# Increase CPU limit
docker run --cpus=2 ...

# Adjust batch sizes in .env
WEAVIATE_BATCH_SIZE=100
```

## Integration with Java Analysis Tool

Once Weaviate is running with the required modules:

1. **Update .env**: Ensure `WEAVIATE_URL=http://localhost:8080`
2. **Two-step workflow (recommended)**
   - Step 1 (analyze/export JSON only): `python -m src.cli analyze --no-upsert`
   - Step 1 (analyze + upsert to Weaviate): `python -m src.cli analyze`
   - Step 2 (generate requirements from JSON): `python -m src.cli requirements`
3. **Single-step legacy**: `python -m src.cli index`
4. **Check Results**: View output in `output_YYYYMMDD_HHMMSS/`

## Monitoring

### Health Checks
```bash
# Check container health
docker ps --filter "name=weaviate-java-analysis"

# Check Weaviate health
curl http://localhost:8080/v1/meta
```

### Logs
```bash
# View real-time logs
docker logs -f weaviate-java-analysis

# View last 100 lines
docker logs --tail 100 weaviate-java-analysis
```

### Resource Usage
```bash
# Check resource usage
docker stats weaviate-java-analysis

# Check disk usage
du -sh ./weaviate-data/
```

## Security Notes

- **Anonymous Access**: Enabled for development
- **CORS**: Open to all origins
- **Data**: Stored locally in `./weaviate-data/`

For production use, consider:
- Enabling authentication
- Restricting CORS origins
- Using HTTPS
- Setting up proper backup strategies
