# Ubuntu Deployment Guide

This guide helps you deploy the Java analysis pipeline to a remote Ubuntu server.

## Prerequisites

### 1. Install Docker and Docker Compose
```bash
# Update package index
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose (if not included with Docker)
sudo apt install docker-compose-plugin
```

### 2. Install Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models
ollama pull gemma3:12b
ollama pull nomic-embed-text
```

### 3. Install Python Dependencies
```bash
# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Deployment Steps

### 1. Upload Project Files
Upload your project to the Ubuntu server:
```bash
# Using scp
scp -r /path/to/local/project user@ubuntu-server:/home/user/

# Or using git
git clone <your-repo> /home/user/a1javarag
cd /home/user/a1javarag
```

### 2. Configure Environment
```bash
# Create .env file for Ubuntu
cat > .env << 'EOF'
# Ollama Configuration - Ubuntu with host networking
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=

# Java Source Directory (update this to your actual source path)
JAVA_SOURCE_DIR=/path/to/your/java/source

# Default Project
DEFAULT_PROJECT_NAME=default-project
EOF
```

### 3. Start Services

#### Option A: Using the Management Script (Recommended)
```bash
# Start Weaviate with Ubuntu configuration
./docker-weaviate.sh start ubuntu

# Check status
./docker-weaviate.sh status

# View logs if needed
./docker-weaviate.sh logs
```

#### Option B: Manual Docker Compose
```bash
# Start Weaviate with Ubuntu configuration
docker compose -f docker-compose.ubuntu.yml up -d

# Check status
docker ps | grep weaviate
```

### 4. Test the Setup
```bash
# Test Weaviate connection
curl http://localhost:8080/v1/meta

# Test Ollama connection
curl http://localhost:11434/api/tags

# Test Python connection
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
client = WeaviateClient(ensure_schema=False)
print('✅ Weaviate connection successful')
"
```

### 5. Run the Pipeline
```bash
# Run the complete pipeline
./new_run.sh

# Or run individual steps
python main.py discover --project test --include-frontend
python main.py extract --project test --include-frontend
python main.py index --project test
python main.py prd --project test --frontend
```

## Troubleshooting

### Common Issues

#### 1. Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker compose -f docker-compose.ubuntu.yml up -d
```

#### 2. Ollama Not Accessible
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama if not running
ollama serve

# Check if port is open
netstat -tlnp | grep 11434
```

#### 3. Weaviate Connection Issues
```bash
# Check Weaviate container
docker ps | grep weaviate

# Check Weaviate logs
docker logs weaviate-java-analysis

# Restart Weaviate
./docker-weaviate.sh restart ubuntu
```

#### 4. Port Conflicts
```bash
# Check what's using port 8080
sudo netstat -tlnp | grep 8080

# Kill process if needed
sudo kill -9 <PID>

# Or change ports in docker-compose.ubuntu.yml
```

### 5. Firewall Issues
```bash
# Open required ports
sudo ufw allow 8080
sudo ufw allow 11434

# Check firewall status
sudo ufw status
```

## Service Management

### Start Services on Boot
```bash
# Create systemd service for Ollama
sudo tee /etc/systemd/system/ollama.service > /dev/null << 'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=ollama
Group=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Monitor Services
```bash
# Check service status
./docker-weaviate.sh status

# Monitor logs
./docker-weaviate.sh logs

# Check system resources
htop
df -h
```

## Production Considerations

### 1. Security
- Use proper authentication for Weaviate
- Set up firewall rules
- Use HTTPS if exposing services

### 2. Performance
- Allocate sufficient memory for Ollama models
- Monitor disk space for Weaviate data
- Consider using SSD storage

### 3. Backup
- Regular backups of Weaviate data
- Backup of configuration files
- Version control for code changes

## Quick Commands Reference

```bash
# Start everything
./docker-weaviate.sh start ubuntu

# Stop everything
./docker-weaviate.sh stop ubuntu

# Restart everything
./docker-weaviate.sh restart ubuntu

# Clean and restart
./docker-weaviate.sh clean

# Check status
./docker-weaviate.sh status

# View logs
./docker-weaviate.sh logs

# Run full pipeline
./new_run.sh

# Search Weaviate
./search_weaviate.sh
```
