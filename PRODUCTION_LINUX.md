# Production Deployment Guide - Linux

Complete guide for running a full iteration on Linux production servers.

## Prerequisites

### 1. System Requirements
- Ubuntu 20.04+ or similar Linux distribution
- Docker and Docker Compose installed
- Python 3.11+ with venv support
- Ollama installed and running
- At least 16GB RAM (32GB recommended for large codebases)
- Sufficient disk space for Weaviate data and extracted artifacts

### 2. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker  # or logout/login

# Install Docker Compose plugin
sudo apt install docker-compose-plugin

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv curl jq

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

## Initial Setup

### 1. Clone/Upload Project

```bash
# Option A: Git clone
git clone <your-repo-url> /opt/gha1javarag
cd /opt/gha1javarag

# Option B: Upload via scp
# From your local machine:
# scp -r /path/to/project user@production-server:/opt/gha1javarag
```

### 2. Create Virtual Environment

```bash
cd /opt/gha1javarag
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```bash
cat > .env << 'EOF'
# Source Discovery
JAVA_SOURCE_DIR=/path/to/your/java/project
JAVA_INCLUDE_GLOBS=**/*.java
JSP_INCLUDE_GLOBS=**/*.jsp,**/*.jspf
GWT_INCLUDE_GLOBS=**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java
JS_INCLUDE_GLOBS=**/*.js

# Ollama Configuration - Linux uses 127.0.0.1 with host networking
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_GRPC_URL=localhost:50051
WEAVIATE_API_KEY=

# Output Configuration
OUTPUT_DIR=./data/output
BUILD_DIR=./data/build
LOG_LEVEL=INFO

# Project Configuration
DEFAULT_PROJECT_NAME=production-project
EOF
```

**Important:** Update `JAVA_SOURCE_DIR` to your actual Java project path.

### 4. Start Services

```bash
# Make scripts executable
chmod +x docker-weaviate.sh

# Start Ollama (if not running as service)
ollama serve &
# Or set up as systemd service (see below)

# Start Weaviate with Ubuntu configuration
./docker-weaviate.sh start ubuntu

# Verify services are running
./docker-weaviate.sh status
```

Expected output:
```
[SUCCESS] Weaviate container is running
[SUCCESS] Weaviate API is accessible
[SUCCESS] Ollama is accessible
```

## Running a Full Iteration

### Option 1: Using the Run Script (Recommended)

The `run_production_linux.sh` script handles all path setup automatically:

```bash
# Run complete pipeline with frontend
./run_production_linux.sh production-project true

# Or without frontend
./run_production_linux.sh production-project false
```

The script will:
- Verify virtual environment
- Set up Python path correctly
- Check services (Ollama, Weaviate)
- Run the complete pipeline
- Report success/failure

### Option 2: Manual Command

```bash
# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH (important!)
export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

# Run complete pipeline with frontend
python main.py all --project production-project --include-frontend
```

This runs:
1. **Discover** - Find all relevant files
2. **Extract** - Extract artifacts (Java, JSP, GWT, JS, etc.)
3. **Index** - Index artifacts in Weaviate
4. **PRD** - Generate Product Requirements Document

### Option 3: Step-by-Step

```bash
source venv/bin/activate

# Set PYTHONPATH (important!)
export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

# Step 1: Discover files
python main.py discover --project production-project --include-frontend

# Step 2: Extract artifacts
python main.py extract --project production-project --include-frontend

# Step 3: Index in Weaviate
python main.py index --project production-project

# Step 4: Generate PRD
python main.py prd --project production-project --frontend
```

### Option 4: Generate Detailed Requirements (Optional)

```bash
# Generate extreme-detailed requirements per artifact
python main.py requirements --project production-project

# Or use CrewAI multi-agent approach (if installed)
python main.py requirements --project production-project --use-crewai
```

## Production Service Setup

### 1. Ollama as Systemd Service

```bash
sudo tee /etc/systemd/system/ollama.service > /dev/null << 'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=0.0.0.0"

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### 2. Weaviate Auto-Start

Weaviate is already configured with `restart: unless-stopped` in `docker-compose.ubuntu.yml`, so it will auto-start on system boot if Docker is running.

### 3. Run Pipeline as Cron Job (Optional)

```bash
# Edit crontab
crontab -e

# Add daily run at 2 AM
0 2 * * * cd /opt/gha1javarag && /opt/gha1javarag/venv/bin/python main.py all --project production-project --include-frontend >> /var/log/gha1javarag.log 2>&1
```

## Verification and Monitoring

### Check Service Status

```bash
# Check all services
./docker-weaviate.sh status

# Check Weaviate logs
./docker-weaviate.sh logs

# Check Ollama
curl http://localhost:11434/api/tags

# Check Weaviate
curl http://localhost:8080/v1/meta | jq .
```

### Verify Indexing

```bash
# Check indexed artifacts
curl -s "http://localhost:8080/v1/objects?class=BackendDoc&limit=5" | jq .

# Or use the search script
./search_weaviate.sh
```

### View Generated Output

```bash
# PRD document
cat data/output/production-project_prd.md

# Extracted artifacts
ls -lh data/build/
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'store.weaviate_client'

**Symptoms:**
```
ModuleNotFoundError: No module named 'store.weaviate_client'
```

**Solution:**

1. **Ensure you're in the project directory:**
   ```bash
   cd /opt/gha1javarag  # or your project path
   ```

2. **Verify file structure:**
   ```bash
   ls -la src/store/weaviate_client.py
   # Should show the file exists
   ```

3. **Set PYTHONPATH explicitly:**
   ```bash
   export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"
   ```

4. **Use the run script (recommended):**
   ```bash
   ./run_production_linux.sh production-project true
   ```
   The script automatically sets up the Python path correctly.

5. **Or run manually with explicit path:**
   ```bash
   source venv/bin/activate
   export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"
   python main.py all --project production-project --include-frontend
   ```

6. **Verify virtual environment is activated:**
   ```bash
   which python
   # Should show: /opt/gha1javarag/venv/bin/python
   ```

### Issue: Ollama Connection Refused

```bash
# Check if Ollama is running
ps aux | grep ollama

# Check if port is accessible
netstat -tlnp | grep 11434

# Restart Ollama
sudo systemctl restart ollama
# Or manually: ollama serve
```

### Issue: Weaviate Can't Connect to Ollama

```bash
# Verify environment variables in container
docker exec -it weaviate-i17 env | grep OLLAMA

# Should show:
# OLLAMA_API_ENDPOINT=http://127.0.0.1:11434
# TEXT2VEC_OLLAMA_API_ENDPOINT=http://127.0.0.1:11434

# Test connectivity from container
docker exec -it weaviate-i17 curl -s http://127.0.0.1:11434/api/tags

# If fails, check host networking mode in docker-compose.ubuntu.yml
```

### Issue: Schema Not Using Correct Endpoint

```bash
# Delete existing classes to recreate with correct endpoint
curl -s -X DELETE http://localhost:8080/v1/schema/GwtModule
curl -s -X DELETE http://localhost:8080/v1/schema/GwtUiBinder
curl -s -X DELETE http://localhost:8080/v1/schema/BackendDoc

# Restart Weaviate
./docker-weaviate.sh restart ubuntu

# Re-run indexing
python main.py index --project production-project
```

### Issue: Out of Memory

```bash
# Check memory usage
free -h

# Reduce Ollama model size or increase system RAM
# Edit .env:
# OLLAMA_MODEL_NAME=llama3.1:8b  # Use smaller model if needed

# Monitor during indexing
watch -n 1 'free -h && docker stats --no-stream weaviate-i17'
```

### Issue: Disk Space

```bash
# Check disk usage
df -h

# Clean old Weaviate data (WARNING: deletes all indexed data)
./docker-weaviate.sh clean

# Clean build artifacts (keeps Weaviate data)
rm -rf data/build/*
```

## Performance Optimization

### 1. Increase Weaviate Resources

Edit `docker-compose.ubuntu.yml`:

```yaml
services:
  weaviate:
    # ... existing config ...
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

### 2. Optimize Ollama

```bash
# Set number of threads (adjust based on CPU cores)
export OLLAMA_NUM_THREAD=8

# Or in systemd service:
Environment="OLLAMA_NUM_THREAD=8"
```

### 3. Batch Processing

For very large codebases, consider running extraction in batches:

```bash
# Extract only backend first
python main.py extract --project production-project

# Then frontend separately
python main.py extract --project production-project --include-frontend
```

## Security Considerations

### 1. Firewall Configuration

```bash
# Allow only localhost access (if services should not be exposed)
sudo ufw deny 8080
sudo ufw deny 11434

# Or allow specific IPs
sudo ufw allow from <your-ip> to any port 8080
sudo ufw allow from <your-ip> to any port 11434
```

### 2. Weaviate Authentication

For production, enable authentication in `docker-compose.ubuntu.yml`:

```yaml
environment:
  AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "false"
  AUTHENTICATION_APIKEY_ENABLED: "true"
  AUTHENTICATION_APIKEY_ALLOWED_KEYS: "your-secret-key"
  AUTHENTICATION_APIKEY_USERS: "admin"
```

Then update `.env`:
```
WEAVIATE_API_KEY=your-secret-key
```

### 3. File Permissions

```bash
# Restrict access to sensitive files
chmod 600 .env
chmod 700 venv
```

## Backup and Recovery

### Backup Weaviate Data

```bash
# Stop Weaviate
./docker-weaviate.sh stop ubuntu

# Backup data directory
tar -czf weaviate-backup-$(date +%Y%m%d).tar.gz weaviate-data/

# Restart Weaviate
./docker-weaviate.sh start ubuntu
```

### Backup Extracted Artifacts

```bash
# Backup build directory
tar -czf artifacts-backup-$(date +%Y%m%d).tar.gz data/build/

# Backup output (PRD documents)
tar -czf output-backup-$(date +%Y%m%d).tar.gz data/output/
```

## Quick Reference

```bash
# Start services
./docker-weaviate.sh start ubuntu

# Run full iteration
source venv/bin/activate
python main.py all --project production-project --include-frontend

# Check status
./docker-weaviate.sh status

# View logs
./docker-weaviate.sh logs

# Restart services
./docker-weaviate.sh restart ubuntu

# Stop services
./docker-weaviate.sh stop ubuntu

# Clean everything (WARNING: deletes data)
./docker-weaviate.sh clean
```

## Next Steps

1. **Monitor first run** - Watch logs and resource usage
2. **Verify output** - Check generated PRD and indexed artifacts
3. **Optimize** - Adjust resources based on codebase size
4. **Automate** - Set up cron jobs or CI/CD pipelines
5. **Document** - Keep notes on project-specific configurations

