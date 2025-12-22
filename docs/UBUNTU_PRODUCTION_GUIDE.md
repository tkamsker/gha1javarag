# Ubuntu Production Deployment Guide

Complete guide for running the full codebase analysis pipeline in Ubuntu production environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Service Configuration](#service-configuration)
4. [Pipeline Execution](#pipeline-execution)
5. [Feature 007 Benefits](#feature-007-benefits)
6. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
7. [Production Best Practices](#production-best-practices)

---

## Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04+ (or other Linux distribution)
- **RAM**: 16GB minimum (32GB recommended for large codebases)
- **Disk**: 50GB free space (for Weaviate vector database)
- **CPU**: 4+ cores recommended
- **Network**: Internet access for Ollama model downloads

### Required Software

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker

# Add current user to docker group (logout/login required)
sudo usermod -aG docker $USER

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installations
python3 --version    # Should be 3.8+
docker --version     # Should be 20.10+
ollama --version     # Should be installed
```

---

## Initial Setup

### 1. Clone Repository

```bash
# Clone project
git clone https://github.com/tkamsker/gha1javarag.git
cd gha1javarag

# Checkout main branch (Feature 007 included)
git checkout main
git pull origin main
```

### 2. Python Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Verify installation
codeindex --help
```

### 3. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Required `.env` Configuration**:

```bash
# Source Code Location
JAVA_SOURCE_DIR=/path/to/your/java/source/root

# Ollama Configuration (Feature 007 - US1: Adaptive Timeout)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma2:27b
OLLAMA_CONNECT_TIMEOUT=60     # Connection timeout in seconds
OLLAMA_READ_TIMEOUT=600       # Read timeout (10 minutes for large files)

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080

# Performance Settings
MAX_CONCURRENT_AI_CALLS=5     # Concurrent Ollama requests (adjust based on RAM)
BATCH_SIZE=50                 # Weaviate batch insert size

# Output Directory
OUTPUT_DIR=./output

# Logging
LOG_LEVEL=INFO                # DEBUG for troubleshooting
```

**Important Notes**:
- `OLLAMA_READ_TIMEOUT=600` enables Feature 007's adaptive timeout (base: 300s + dynamic adjustment)
- `MAX_CONCURRENT_AI_CALLS=5` prevents overwhelming system resources
- Set `LOG_LEVEL=DEBUG` for first run to monitor progress

---

## Service Configuration

### 1. Start Ollama Service

```bash
# Start Ollama daemon
ollama serve &

# Pull required model (27B parameter model recommended for production)
ollama pull gemma2:27b

# Verify Ollama is running
curl http://localhost:11434/api/tags

# Expected output: JSON list of installed models
```

**Model Options**:
- `gemma2:27b` - Best accuracy (recommended for production)
- `gemma2:9b` - Faster, less accurate
- `llama3.1:8b` - Alternative model

### 2. Start Weaviate Vector Database

```bash
# Make script executable
chmod +x docker-weaviate.sh

# Start Weaviate (auto-detects Ubuntu)
./docker-weaviate.sh start

# Wait 30 seconds for startup
sleep 30

# Verify Weaviate is running
./docker-weaviate.sh status

# Expected output:
# ✅ Weaviate container is running
# ✅ Weaviate API is accessible
# Container: weaviate-i19 (healthy)
```

**Verify Weaviate API**:

```bash
# Check Weaviate meta endpoint
curl http://localhost:8080/v1/meta

# Expected: JSON with version info
```

### 3. Verify All Services

```bash
# Check Ollama
curl -s http://localhost:11434/api/tags | jq '.models[].name'

# Check Weaviate
curl -s http://localhost:8080/v1/meta | jq '.version'

# If both succeed, services are ready
```

---

## Pipeline Execution

### Full Pipeline Overview

The pipeline consists of 6 stages:

```
JAVA_SOURCE_DIR
       ↓
1. discover  → discovery-inventory.jsonl
       ↓
2. extract   → extraction-results.jsonl
       ↓
3. index     → Weaviate vector database
       ↓
4. search    → Natural language queries
       ↓
5. prd       → Product requirements documents
       ↓
6. diagram   → Architecture diagrams (Mermaid)
```

### Method 1: Quick Start Script (Recommended)

```bash
# Run full pipeline for entire codebase
./run.sh

# Run for specific project in monorepo
./run.sh my-project

# This script runs: discover → extract → index → status
```

**What `run.sh` does**:
1. Discovers all source files
2. Extracts semantic information with Feature 007 improvements
3. Indexes artifacts in Weaviate
4. Shows statistics

### Method 2: Manual Step-by-Step Execution

#### Stage 1: Discover Source Files

```bash
# Basic discovery
codeindex discover \
  --source-dir /path/to/java/source \
  --output ./output/discovery-inventory.jsonl

# With Maven dependency resolution (Feature 004)
codeindex discover \
  --source-dir /path/to/java/source \
  --dependency-depth 1 \
  --output ./output/discovery-inventory.jsonl

# Project-scoped for monorepo
codeindex discover \
  --source-dir /monorepo/root \
  --project backend-api \
  --dependency-depth 1 \
  --output ./output/discovery-inventory.jsonl
```

**Output**: `discovery-inventory.jsonl` containing:
- Java source files (.java)
- JSP templates (.jsp)
- GWT modules (*.gwt.xml)
- UiBinder templates (*.ui.xml)
- Database schemas (.sql)
- iBATIS XML (.xml)
- JavaScript files (.js)

**Monitor Progress**:
```bash
# Watch discovery progress
tail -f ./output/discovery-inventory.jsonl | jq '.file_path'

# Count discovered files
wc -l ./output/discovery-inventory.jsonl
```

#### Stage 2: Extract Semantic Information

```bash
# Full extraction with AI (Feature 007 improvements active)
codeindex extract \
  --inventory ./output/discovery-inventory.jsonl \
  --output ./output/extraction-results.jsonl

# Skip AI for faster extraction (structural analysis only)
codeindex extract \
  --skip-ai \
  --inventory ./output/discovery-inventory.jsonl \
  --output ./output/extraction-results.jsonl
```

**Feature 007 - US1 Active**:
- ✅ Adaptive timeout: 300s + 10s per 1000 lines
- ✅ Retry logic: 3 attempts with exponential backoff
- ✅ Graceful degradation: Falls back to structural analysis if AI fails

**Feature 007 - US2 Active**:
- ✅ Multi-source FK extraction: SQL DDL, iBATIS XML, JPA annotations

**Feature 007 - US3 Active**:
- ✅ GWT navigation graph: Entry point → Module → Presenter → View

**Feature 007 - US4 Active**:
- ✅ Widget hierarchy extraction from UiBinder templates
- ✅ Presenter-View binding with confidence scoring

**Monitor Progress**:
```bash
# Watch extraction progress
tail -f ./output/extraction-results.jsonl | jq '{file: .file_path, type: .type}'

# Monitor for timeout handling
tail -f codeindex.log | grep -i timeout

# Check metrics
tail -f ./output/extraction-results.jsonl | jq 'select(.metrics)'
```

**Expected Output**:
```json
{
  "file_path": "/path/UserService.java",
  "type": "backend_service",
  "entities": ["UserService", "UserDTO"],
  "methods": [...],
  "dependencies": [...],
  "extraction_method": "ollama",  // or "structural_fallback"
  "timeout_applied": 350  // Feature 007: adaptive timeout
}
```

#### Stage 3: Index in Weaviate

```bash
# Index all artifacts
codeindex index \
  --inventory ./output/discovery-inventory.jsonl \
  --extraction ./output/extraction-results.jsonl

# Project-scoped indexing
codeindex index \
  --inventory ./output/discovery-inventory.jsonl \
  --extraction ./output/extraction-results.jsonl \
  --project backend-api
```

**What Gets Indexed**:
- Backend services and DAOs
- Frontend components (Presenters, Views, Activities)
- Database schemas and foreign keys (Feature 007 - US2)
- GWT navigation graph (Feature 007 - US3)
- UiBinder templates with widget hierarchy (Feature 007 - US4)
- DTOs with validation annotations

**Monitor Progress**:
```bash
# Check indexing statistics
./weaviate_stats.py

# Or use CLI
codeindex status
```

#### Stage 4: Search Artifacts

```bash
# Natural language semantic search
codeindex search "user authentication logic"

# Filter by project
codeindex search "database access" --project backend-api

# Limit results
codeindex search "form validation" --limit 10
```

**Example Queries**:
```bash
# Find GWT presenters
codeindex search "GWT presenter user management"

# Find database foreign keys
codeindex search "foreign key relationships customer order"

# Find navigation flows
codeindex search "navigation from login to dashboard"

# Find form fields
codeindex search "form fields with validation email phone"
```

#### Stage 5: Generate PRDs

```bash
# Generate backend PRD
codeindex prd backend \
  --output-dir ./output/prds

# Generate frontend PRD (includes GWT components)
codeindex prd frontend \
  --output-dir ./output/prds

# Generate both
codeindex prd backend --output-dir ./output/prds
codeindex prd frontend --output-dir ./output/prds
```

**Output Files**:
```
output/prds/
├── backend_prd.md         # Services, DAOs, database schemas
├── frontend_prd.md        # GWT Presenters, Views, UiBinder templates
├── backend/
│   ├── services/*.json
│   ├── daos/*.json
│   └── schemas/*.json
└── frontend/
    ├── components/*.json  # Presenters, Views
    └── forms/*.json       # UiBinder forms
```

**Feature 007 Improvements in PRDs**:
- ✅ Complete GWT Presenter-View bindings
- ✅ Navigation flows and entry points
- ✅ Widget hierarchies with field types
- ✅ Database relationships with validated FKs

#### Stage 6: Generate Architecture Diagrams

```bash
# Generate component architecture diagram
codeindex diagram component \
  --output ./output/prds \
  --format mermaid

# Generate GWT MVP diagram
codeindex diagram gwt \
  --extraction-file ./output/extraction-results.jsonl \
  --output ./output/prds \
  --format mermaid

# Generate all diagrams
codeindex diagram all \
  --extraction-file ./output/extraction-results.jsonl \
  --output ./output/prds \
  --format mermaid
```

**Output**:
```
output/prds/diagrams/
├── component/
│   └── architecture.mmd     # Component architecture
├── gwt/
│   └── mvp-overview.mmd     # GWT MVP architecture
└── README.md                # Viewing instructions
```

**View Diagrams**:
```bash
# In GitHub markdown (auto-renders)
cat output/prds/diagrams/component/architecture.mmd

# Convert to PNG/SVG (requires mermaid-cli)
sudo npm install -g @mermaid-js/mermaid-cli
mmdc -i output/prds/diagrams/component/architecture.mmd -o architecture.png
```

---

## Feature 007 Benefits

### US1: Zero Timeout Failures

**Before Feature 007**: 29 timeout failures on large files

**After Feature 007**: 0 timeout failures

**How It Works**:
```python
# Adaptive timeout calculation
timeout = 300 + (file_lines / 1000) * 10

# Example:
# - 1000 lines  → 310s timeout
# - 5000 lines  → 350s timeout
# - 10000 lines → 400s timeout
```

**Retry Logic**:
- Attempt 1: Normal timeout
- Attempt 2: After 2s delay
- Attempt 3: After 4s delay
- Fallback: Structural analysis (no AI)

**Verify in Logs**:
```bash
tail -f codeindex.log | grep "timeout\|retry\|fallback"
```

### US2: 100% Foreign Key Extraction

**Before Feature 007**: 4 validation errors, missed FKs

**After Feature 007**: 100% FK extraction

**Multi-Source Extraction**:
1. SQL DDL files (CREATE TABLE, FOREIGN KEY)
2. iBATIS XML (SQL statements)
3. JPA annotations (@ManyToOne, @OneToMany)

**Verify**:
```bash
# Search for FK relationships
codeindex search "foreign key customer order"

# Check PRD
cat output/prds/backend_prd.md | grep -A5 "Foreign Keys"
```

### US3: 95% GWT Navigation Coverage

**Before Feature 007**: <5% coverage, 1 presenter found

**After Feature 007**: 95% coverage, 40+ presenters, 30+ views

**What's Discovered**:
- Entry points (index.html, index.jsp)
- GWT module inheritance (*.gwt.xml)
- Presenters with event handlers
- Views with UI fields
- Navigation flows
- Activity/Place patterns

**Verify**:
```bash
# Check GWT components
codeindex search "GWT presenter"

# View navigation graph in PRD
cat output/prds/frontend_prd.md | grep -A10 "Navigation"
```

### US4: Complete UI Structure

**Before Feature 007**: No widget hierarchy

**After Feature 007**: Complete nested widget structure

**Extracted Information**:
- Widget types (TextBox, ListBox, Button, Panel)
- Nesting depth and container relationships
- @UiField bindings with types
- Presenter-View confidence scoring

**Verify**:
```bash
# Find form fields
codeindex search "form fields textbox email"

# Check widget hierarchy in PRD
cat output/prds/frontend_prd.md | grep -A20 "Widget Hierarchy"
```

---

## Monitoring & Troubleshooting

### Check Service Health

```bash
# Comprehensive health check
echo "=== Ollama Status ==="
curl -s http://localhost:11434/api/tags | jq '.models[].name'

echo "=== Weaviate Status ==="
./docker-weaviate.sh status

echo "=== Disk Space ==="
df -h | grep -E "Filesystem|/$"

echo "=== Memory Usage ==="
free -h

echo "=== Docker Status ==="
docker ps | grep weaviate
```

### View Pipeline Statistics

```bash
# Comprehensive statistics
./weaviate_stats.py

# Or CLI
codeindex status

# Project-specific
codeindex status --project backend-api
```

**Expected Output**:
```
=== Weaviate Statistics ===

Total artifacts: 1,234

By Type:
  Backend Services: 45
  DAOs: 38
  GWT Presenters: 42
  GWT Views: 35
  UiBinder Templates: 32
  Database Tables: 28
  Foreign Keys: 156

By Project:
  backend-api: 456
  frontend-app: 378
  shared-models: 400
```

### Common Issues

#### Issue 1: Ollama Timeouts

**Symptoms**: "Connection timeout" or "Read timeout" errors

**Solution**:
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Increase timeout in .env
OLLAMA_READ_TIMEOUT=900  # 15 minutes

# Reduce concurrent calls
MAX_CONCURRENT_AI_CALLS=3

# Use faster model
OLLAMA_MODEL_NAME=gemma2:9b
```

#### Issue 2: Weaviate Out of Memory

**Symptoms**: Weaviate container restarts, "OOMKilled"

**Solution**:
```bash
# Check Weaviate logs
./docker-weaviate.sh logs | tail -50

# Increase Docker memory limit
# Edit docker-compose.ubuntu.yml:
nano docker-compose.ubuntu.yml

# Add under weaviate service:
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G

# Restart Weaviate
./docker-weaviate.sh restart
```

#### Issue 3: Disk Space Full

**Symptoms**: "No space left on device"

**Solution**:
```bash
# Check disk usage
du -h --max-depth=1 . | sort -hr | head -20

# Clean old Weaviate data (CAUTION: deletes all indexed data)
./docker-weaviate.sh clean

# Clean Docker cache
docker system prune -af
```

#### Issue 4: Import Errors

**Symptoms**: "ModuleNotFoundError" or "No module named 'codeindex'"

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall package
pip install -e .

# Verify installation
pip show codeindex
```

### View Logs

```bash
# Application logs
tail -f codeindex.log

# Ollama logs (if running as service)
journalctl -u ollama -f

# Weaviate logs
./docker-weaviate.sh logs

# Docker logs
docker logs weaviate-i19 -f
```

---

## Production Best Practices

### 1. Resource Planning

**Small Codebase** (<1000 files):
- RAM: 16GB
- CPU: 4 cores
- Disk: 20GB
- Concurrent calls: 10

**Medium Codebase** (1000-5000 files):
- RAM: 32GB
- CPU: 8 cores
- Disk: 50GB
- Concurrent calls: 5

**Large Codebase** (>5000 files):
- RAM: 64GB
- CPU: 16 cores
- Disk: 100GB
- Concurrent calls: 3

### 2. Performance Optimization

```bash
# Adjust concurrency based on available RAM
# Each Ollama call uses ~2-4GB RAM

# For 32GB RAM system:
MAX_CONCURRENT_AI_CALLS=5

# For 64GB RAM system:
MAX_CONCURRENT_AI_CALLS=10

# Reduce batch size if memory constrained
BATCH_SIZE=25
```

### 3. Incremental Updates

```bash
# For daily updates, only index changed files
# (Note: Full re-indexing recommended monthly)

# Discover only recent changes
find /path/to/source -mtime -1 -name "*.java" > recent_files.txt

# Create filtered inventory (requires custom script)
```

### 4. Backup Strategy

```bash
# Backup Weaviate data directory
tar -czf weaviate-backup-$(date +%Y%m%d).tar.gz weaviate-data/

# Backup extraction results
cp -r output/ backup/output-$(date +%Y%m%d)/

# Backup .env configuration
cp .env backup/.env-$(date +%Y%m%d)
```

### 5. Automation with Cron

```bash
# Edit crontab
crontab -e

# Run pipeline daily at 2 AM
0 2 * * * cd /path/to/gha1javarag && ./run.sh >> /var/log/codeindex.log 2>&1

# Backup weekly on Sunday at 3 AM
0 3 * * 0 cd /path/to/gha1javarag && tar -czf backup/weaviate-$(date +\%Y\%m\%d).tar.gz weaviate-data/
```

### 6. Security Considerations

```bash
# Restrict .env file permissions
chmod 600 .env

# Run services as non-root user
# (Ollama and Weaviate already do this)

# Firewall configuration (if remote access needed)
sudo ufw allow 8080/tcp  # Weaviate (internal only)
sudo ufw allow 11434/tcp # Ollama (internal only)

# Use reverse proxy for external access
# (nginx/traefik recommended)
```

### 7. Monitoring Setup

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor system resources during pipeline
htop

# Monitor disk I/O
sudo iotop

# Monitor network
sudo nethogs

# Create monitoring script
cat > monitor_pipeline.sh << 'EOF'
#!/bin/bash
while true; do
  echo "=== $(date) ==="
  echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')"
  echo "Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
  echo "Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2}')"
  echo "Weaviate: $(docker stats weaviate-i19 --no-stream --format '{{.CPUPerc}} {{.MemUsage}}')"
  echo "---"
  sleep 60
done
EOF

chmod +x monitor_pipeline.sh
```

---

## Quick Reference

### Start Services

```bash
# Start all services
ollama serve &
./docker-weaviate.sh start
sleep 30
```

### Run Full Pipeline

```bash
# Activate environment
source .venv/bin/activate

# Run pipeline
./run.sh

# Or manual:
codeindex discover --source-dir $JAVA_SOURCE_DIR --output output/discovery.jsonl
codeindex extract --inventory output/discovery.jsonl --output output/extraction.jsonl
codeindex index --inventory output/discovery.jsonl --extraction output/extraction.jsonl
codeindex prd frontend --output-dir output/prds
codeindex prd backend --output-dir output/prds
codeindex diagram all --extraction-file output/extraction.jsonl --output output/prds
```

### Check Status

```bash
# Service health
curl http://localhost:11434/api/tags
curl http://localhost:8080/v1/meta

# Pipeline statistics
./weaviate_stats.py
codeindex status
```

### Stop Services

```bash
# Stop Ollama
pkill ollama

# Stop Weaviate
./docker-weaviate.sh stop
```

---

## Support

For issues or questions:

1. Check logs: `tail -f codeindex.log`
2. Review CLAUDE.md: `cat CLAUDE.md | less`
3. Run validation: `bash scripts/validate_feature_007.sh`
4. Check GitHub issues: https://github.com/tkamsker/gha1javarag/issues

---

**Last Updated**: 2025-12-22 (Feature 007 complete)
