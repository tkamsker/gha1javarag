# Streamlit Web UI Deployment Guide

**Last Updated**: 2026-01-15
**Feature**: 009-streamlit-crewai-web-client
**Status**: Production Ready

---

## Overview

This guide provides instructions for deploying the Streamlit Web UI to production environments with proper configuration, monitoring, and security.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Production Deployment Architecture                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Streamlit  │─────→│   Weaviate   │      │  Ollama  │  │
│  │   Web UI     │      │   Vector DB  │      │   LLM    │  │
│  │  (Port 8501) │      │  (Port 8080) │      │ (11434)  │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                      │                     │       │
│         └──────────────────────┴─────────────────────┘       │
│                            │                                 │
│                    ┌───────────────┐                         │
│                    │   SQLite DB   │                         │
│                    │  (Workspace)  │                         │
│                    └───────────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Options

### Option 1: Local Production Setup (Recommended for Testing)

**Use Case**: Internal team deployment, development, testing

**Requirements**:
- Linux/macOS server
- Python 3.8+
- Docker (for Weaviate)
- 8GB+ RAM
- 20GB+ disk space

**Pros**:
- Simple setup
- Full control
- Easy debugging

**Cons**:
- Manual service management
- Not auto-scaling

---

### Option 2: Docker Compose (Recommended for Production)

**Use Case**: Production deployment, containerized environments

**Requirements**:
- Docker 20+
- Docker Compose 2+
- 16GB+ RAM
- 50GB+ disk space

**Pros**:
- All services containerized
- Easy scaling
- Consistent environment
- Simple updates

**Cons**:
- Docker overhead
- Requires Docker knowledge

---

### Option 3: Kubernetes (Enterprise)

**Use Case**: Large-scale deployment, high availability

**Requirements**:
- Kubernetes cluster
- Helm (optional)
- Load balancer
- Persistent volume storage

**Pros**:
- Auto-scaling
- High availability
- Load balancing
- Health checks

**Cons**:
- Complex setup
- Requires K8s expertise
- Higher resource requirements

---

## Option 1: Local Production Setup

### Step 1: System Prerequisites

```bash
# Update system
sudo apt-get update  # Ubuntu/Debian
brew update          # macOS

# Install Python 3.8+
python3 --version  # Verify ≥3.8

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose  # Ubuntu
brew install docker-compose          # macOS
```

### Step 2: Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd gha1javarag

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
vim .env
```

**Production `.env` configuration:**
```bash
# Source Code Location
JAVA_SOURCE_DIR=/data/source/codebase

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_SCHEME=http
WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_CONNECT_TIMEOUT=10
OLLAMA_READ_TIMEOUT=300
MAX_CONCURRENT_AI_CALLS=5

# Streamlit Configuration
STREAMLIT_PORT=8501
STREAMLIT_HOST=0.0.0.0  # Allow external connections
WORKSPACE_DB_PATH=/data/workspaces/workspaces.db
EXPORT_DIR=/data/exports

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/streamlit/app.log

# Security
AUTH_ENABLED=true  # Enable if authentication needed
```

### Step 4: Initialize Services

```bash
# Start Weaviate
./docker-weaviate.sh start

# Verify Weaviate is running
curl http://localhost:8080/v1/meta

# Start Ollama
ollama serve > /var/log/ollama/ollama.log 2>&1 &

# Pull required model
ollama pull gemma3:12b

# Initialize database
./init-database.sh

# Verify all services
./check-services.sh
```

### Step 5: Index Production Data

```bash
# Run production pipeline
./production-requirements-generation.sh <project-name> /data/source/codebase

# Verify data is indexed
./weaviate_stats.py
```

### Step 6: Launch Streamlit

```bash
# Launch in production mode
streamlit run src/codeindex/web/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false \
  --logger.level info

# Access at: http://your-server-ip:8501
```

### Step 7: Setup Process Manager (systemd)

Create systemd service file:

```bash
sudo vim /etc/systemd/system/streamlit-web.service
```

**Service file content:**
```ini
[Unit]
Description=Streamlit Web UI for Code Intelligence
After=network.target docker.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/gha1javarag
Environment="PATH=/home/ubuntu/gha1javarag/.venv/bin"
ExecStart=/home/ubuntu/gha1javarag/.venv/bin/streamlit run src/codeindex/web/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit-web
sudo systemctl start streamlit-web

# Check status
sudo systemctl status streamlit-web

# View logs
sudo journalctl -u streamlit-web -f
```

---

## Option 2: Docker Compose Deployment

### Step 1: Create Docker Compose File

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      CLUSTER_HOSTNAME: 'node1'
    volumes:
      - weaviate-data:/var/lib/weaviate
    restart: always
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8080/v1/.well-known/ready"]
      interval: 30s
      timeout: 10s
      retries: 3

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-models:/root/.ollama
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/"]
      interval: 30s
      timeout: 10s
      retries: 3

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      WEAVIATE_URL: http://weaviate:8080
      OLLAMA_BASE_URL: http://ollama:11434
      OLLAMA_MODEL_NAME: gemma3:12b
      JAVA_SOURCE_DIR: /data/source
      WORKSPACE_DB_PATH: /data/workspaces/workspaces.db
      LOG_LEVEL: INFO
    volumes:
      - ./data:/data
      - ./output:/output
      - source-code:/data/source:ro
    depends_on:
      weaviate:
        condition: service_healthy
      ollama:
        condition: service_healthy
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  weaviate-data:
  ollama-models:
  source-code:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/your/source/code
```

### Step 2: Create Streamlit Dockerfile

Create `Dockerfile.streamlit`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY setup.py .
RUN pip install -e .

# Create data directories
RUN mkdir -p /data/workspaces /data/exports

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "src/codeindex/web/app.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--server.headless", "true", \
     "--browser.gatherUsageStats", "false"]
```

### Step 3: Deploy with Docker Compose

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f streamlit

# Check status
docker-compose -f docker-compose.prod.yml ps

# Stop services
docker-compose -f docker-compose.prod.yml down

# Update and restart
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build
```

### Step 4: Load Ollama Model

```bash
# Execute in ollama container
docker-compose -f docker-compose.prod.yml exec ollama ollama pull gemma3:12b

# Verify model is loaded
docker-compose -f docker-compose.prod.yml exec ollama ollama list
```

---

## Reverse Proxy Setup (nginx)

### Install nginx

```bash
sudo apt-get install nginx
```

### Configure nginx

Create `/etc/nginx/sites-available/streamlit`:

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Proxy settings
    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_read_timeout 86400;
    }

    # Health check endpoint
    location /_stcore/health {
        proxy_pass http://streamlit/_stcore/health;
        access_log off;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

---

## Monitoring and Logging

### Application Logging

**Configure in `src/codeindex/utils/logging_config.py`:**

```python
import logging
import logging.handlers
import os

def setup_production_logging():
    """Setup production-grade logging."""
    log_dir = "/var/log/streamlit"
    os.makedirs(log_dir, exist_ok=True)

    # Root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # Rotating file handler
            logging.handlers.RotatingFileHandler(
                f"{log_dir}/app.log",
                maxBytes=10485760,  # 10MB
                backupCount=10
            )
        ]
    )

    # Set levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
```

### System Monitoring

**Install monitoring tools:**

```bash
# Install Prometheus node exporter
sudo apt-get install prometheus-node-exporter

# Install Grafana (optional)
sudo apt-get install grafana
```

### Health Check Endpoint

Streamlit provides built-in health check:

```bash
curl http://localhost:8501/_stcore/health

# Response: {"status": "ok"}
```

**Monitor script:**

```bash
#!/bin/bash
# /usr/local/bin/check-streamlit-health.sh

if curl -sf http://localhost:8501/_stcore/health > /dev/null; then
    echo "Streamlit is healthy"
    exit 0
else
    echo "Streamlit is unhealthy"
    # Restart service
    systemctl restart streamlit-web
    exit 1
fi
```

**Add to crontab:**
```bash
*/5 * * * * /usr/local/bin/check-streamlit-health.sh >> /var/log/streamlit/health-check.log 2>&1
```

---

## Security Considerations

### 1. Authentication

**Enable authentication in Streamlit:**

Create `.streamlit/config.toml`:

```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
```

**Add basic auth with nginx:**

```nginx
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;

    proxy_pass http://streamlit;
    # ... other proxy settings
}
```

Create password file:
```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
```

### 2. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Block direct access to services
sudo ufw deny 8501/tcp   # Streamlit (use nginx)
sudo ufw deny 8080/tcp   # Weaviate
sudo ufw deny 11434/tcp  # Ollama
```

### 3. Data Protection

```bash
# Restrict file permissions
chmod 700 /data/workspaces
chmod 600 /data/workspaces/workspaces.db

# Encrypt sensitive data at rest
sudo apt-get install ecryptfs-utils
```

### 4. Rate Limiting

**Configure in nginx:**

```nginx
http {
    limit_req_zone $binary_remote_addr zone=streamlit_limit:10m rate=10r/s;

    server {
        location / {
            limit_req zone=streamlit_limit burst=20 nodelay;
            # ... other settings
        }
    }
}
```

---

## Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# /usr/local/bin/backup-streamlit.sh

BACKUP_DIR="/backup/streamlit"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup SQLite database
mkdir -p $BACKUP_DIR
cp /data/workspaces/workspaces.db $BACKUP_DIR/workspaces_$DATE.db

# Backup Weaviate data
docker exec weaviate weaviate-backup create backup-$DATE

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
```

**Add to crontab:**
```bash
0 2 * * * /usr/local/bin/backup-streamlit.sh >> /var/log/streamlit/backup.log 2>&1
```

### Disaster Recovery

```bash
# Restore SQLite database
cp /backup/streamlit/workspaces_YYYYMMDD_HHMMSS.db /data/workspaces/workspaces.db

# Restore Weaviate
docker exec weaviate weaviate-backup restore backup-YYYYMMDD_HHMMSS

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

---

## Scaling Recommendations

### Horizontal Scaling

**Option 1: Multiple Streamlit Instances + Load Balancer**

```nginx
upstream streamlit_cluster {
    least_conn;
    server streamlit1:8501;
    server streamlit2:8501;
    server streamlit3:8501;
}

server {
    location / {
        proxy_pass http://streamlit_cluster;
        # ... other settings
    }
}
```

**Option 2: Kubernetes Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streamlit-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: streamlit
  template:
    metadata:
      labels:
        app: streamlit
    spec:
      containers:
      - name: streamlit
        image: your-registry/streamlit:latest
        ports:
        - containerPort: 8501
---
apiVersion: v1
kind: Service
metadata:
  name: streamlit-service
spec:
  selector:
    app: streamlit
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

### Vertical Scaling

**Resource Requirements:**

| Component | Minimum | Recommended | High Load |
|-----------|---------|-------------|-----------|
| CPU | 2 cores | 4 cores | 8+ cores |
| RAM | 8 GB | 16 GB | 32+ GB |
| Disk | 20 GB | 50 GB | 100+ GB |
| Network | 100 Mbps | 1 Gbps | 10 Gbps |

**Docker resource limits:**

```yaml
services:
  streamlit:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

---

## Performance Optimization

### 1. Caching Strategy

Add caching to search and agent services:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_search(query_hash: str, filters_hash: str):
    """Cache search results for frequent queries."""
    # Implementation
    pass

def search_with_cache(query: str, filters: dict):
    query_hash = hashlib.md5(query.encode()).hexdigest()
    filters_hash = hashlib.md5(str(filters).encode()).hexdigest()
    return cached_search(query_hash, filters_hash)
```

### 2. Connection Pooling

Configure in `weaviate_store.py`:

```python
import weaviate

client = weaviate.Client(
    url="http://localhost:8080",
    additional_config=weaviate.AdditionalConfig(
        connection_config=weaviate.ConnectionConfig(
            session_pool_connections=20,
            session_pool_maxsize=100
        )
    )
)
```

### 3. Ollama Optimization

```bash
# Use GPU acceleration (if available)
docker run --gpus all ollama/ollama

# Adjust worker threads
export OLLAMA_NUM_PARALLEL=4
```

---

## Maintenance Tasks

### Daily
- ✅ Check service health
- ✅ Monitor disk space
- ✅ Review error logs

### Weekly
- ✅ Backup database
- ✅ Update dependencies
- ✅ Review performance metrics

### Monthly
- ✅ Security updates
- ✅ Log rotation
- ✅ Capacity planning review

---

## Troubleshooting Production Issues

### High Memory Usage

```bash
# Check memory usage
docker stats

# Restart services to free memory
docker-compose -f docker-compose.prod.yml restart

# Increase Docker memory limit
# Edit /etc/docker/daemon.json
{
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

### Slow Response Times

```bash
# Check Ollama performance
docker logs ollama

# Check Weaviate performance
curl http://localhost:8080/v1/meta

# Monitor network latency
ping -c 10 localhost
```

### Service Crashes

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs streamlit

# Check disk space
df -h

# Check memory
free -h

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] SSL certificates obtained
- [ ] Firewall rules configured
- [ ] Backup strategy in place
- [ ] Monitoring tools installed

### Deployment
- [ ] Services started successfully
- [ ] Health checks passing
- [ ] Data indexed in Weaviate
- [ ] Ollama model loaded
- [ ] Streamlit accessible via HTTPS

### Post-Deployment
- [ ] Smoke tests passed
- [ ] Performance acceptable
- [ ] Logs being captured
- [ ] Backups running
- [ ] Documentation updated

---

## Support and Maintenance

### Contact Information
- **Technical Lead**: [Name]
- **DevOps Team**: [Email]
- **On-Call**: [Phone]

### Escalation Path
1. Check logs and troubleshooting guide
2. Contact technical lead
3. Escalate to DevOps team
4. Emergency on-call if production down

---

## Appendix

### A. Environment Variables Reference

See `.env.example` for complete list

### B. Port Reference

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Streamlit | 8501 | HTTP | Web UI |
| Weaviate | 8080 | HTTP | Vector DB |
| Ollama | 11434 | HTTP | LLM API |
| nginx | 80/443 | HTTP/HTTPS | Reverse proxy |

### C. Useful Commands

```bash
# View all service logs
docker-compose logs -f --tail=100

# Restart specific service
docker-compose restart streamlit

# Check resource usage
docker stats

# Clean up unused resources
docker system prune -a
```
