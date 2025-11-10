# Docker Setup Guide

This project includes multiple Docker Compose configurations to handle different operating systems and Ollama connectivity requirements.

## Docker Compose Files

### 1. `docker-compose.yml` (Default - Ubuntu/Linux)
- **Network Mode**: Host networking
- **Ollama URL**: `http://localhost:11434`
- **Use Case**: Ubuntu/Linux where Ollama runs on host localhost

### 2. `docker-compose.macos.yml` (macOS)
- **Network Mode**: Bridge networking with port mapping
- **Ollama URL**: `http://host.docker.internal:11434`
- **Use Case**: macOS where `host.docker.internal` works natively

### 3. `docker-compose.ubuntu.yml` (Ubuntu/Linux)
- **Network Mode**: Host networking
- **Ollama URL**: `http://localhost:11434`
- **Use Case**: Ubuntu/Linux where Ollama runs on host localhost

## Usage

### Automatic OS Detection
The `docker-weaviate.sh` script automatically detects your OS and uses the appropriate Docker Compose file:

```bash
# Start Weaviate (auto-detects OS)
./docker-weaviate.sh start

# Stop Weaviate
./docker-weaviate.sh stop

# Restart Weaviate
./docker-weaviate.sh restart

# Clean data and restart
./docker-weaviate.sh clean

# Check status
./docker-weaviate.sh status

# View logs
./docker-weaviate.sh logs
```

### Manual Usage
You can also use Docker Compose directly:

```bash
# For macOS
docker-compose -f docker-compose.macos.yml up -d

# For Ubuntu/Linux
docker-compose -f docker-compose.ubuntu.yml up -d

# For default (auto-detected)
docker-compose up -d
```

## Prerequisites

### 1. Ollama Installation
Make sure Ollama is installed and running on your host:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull required models
ollama pull gemma3:12b
ollama pull nomic-embed-text
```

### 2. Docker Installation
Make sure Docker and Docker Compose are installed:

```bash
# Check Docker
docker --version
docker-compose --version
```

## Troubleshooting

### Connection Issues
If you get connection refused errors:

1. **Check Ollama is running**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check Weaviate is running**:
   ```bash
   curl http://localhost:8080/v1/meta
   ```

3. **Check container logs**:
   ```bash
   ./docker-weaviate.sh logs
   ```

### Network Issues
- **macOS**: Use `docker-compose.macos.yml` (supports `host.docker.internal`)
- **Ubuntu/Linux**: Use `docker-compose.ubuntu.yml` (uses host networking)
- **Other**: Use `docker-compose.yml` (default configuration)

### Port Conflicts
If ports 8080 or 50051 are already in use:

1. **Stop conflicting services**
2. **Or modify the port mappings in the Docker Compose files**

## Environment Variables

The Docker Compose files use these environment variables:

- `OLLAMA_API_ENDPOINT`: URL to reach Ollama from Weaviate
- `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED`: Enable anonymous access
- `ENABLE_MODULES`: Enable text2vec-ollama module
- `DEFAULT_VECTORIZER_MODULE`: Use Ollama for vectorization

## Data Persistence

Weaviate data is persisted in the `./weaviate-data` directory. This directory is mounted as a volume in the container.

To reset all data:
```bash
./docker-weaviate.sh clean
```

## Health Checks

The containers include health checks that verify:
- Weaviate API is accessible
- Container is running properly

Check health status:
```bash
./docker-weaviate.sh status
```

test 