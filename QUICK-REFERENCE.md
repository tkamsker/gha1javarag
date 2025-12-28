# Quick Reference Guide

**Feature 007: GWT Navigation Analysis and Error Fixes**

---

## 🚀 Quick Start Commands

### First-Time Setup (Ubuntu)
```bash
chmod +x deploy-ubuntu-prod.sh
./deploy-ubuntu-prod.sh
# Select option 1 (Full installation)
```

### Run Analysis Pipeline
```bash
source .venv/bin/activate
./run.sh
```

---

## 📦 Individual Commands

### Discovery
```bash
# Basic discovery
codeindex discover --source-dir /path/to/java/source

# With Maven dependencies
codeindex discover --source-dir /path/to/project --dependency-depth 1

# Project-scoped (monorepo)
codeindex discover --source-dir /monorepo --project backend-api
```

### Extraction
```bash
# Basic extraction (with LLM)
codeindex extract --inventory ./output/discovery-inventory.jsonl

# Skip AI for faster processing (structural only)
codeindex extract --skip-ai --inventory ./output/discovery-inventory.jsonl
```

### Indexing
```bash
codeindex index \
    --inventory ./output/discovery-inventory.jsonl \
    --extraction ./output/extraction-results.jsonl
```

### Status & Search
```bash
# Show pipeline statistics
codeindex status

# Verbose status with detailed metrics
codeindex status --verbose

# Semantic search
codeindex search "user authentication"

# Project-filtered search
codeindex search "database" --project backend-api
```

### PRD Generation
```bash
# Backend PRD
codeindex prd backend --output-dir ./output/prd

# Frontend PRD (includes GWT!)
codeindex prd frontend --output-dir ./output/prd
```

### Architecture Diagrams
```bash
# Component diagram
codeindex diagram component --output ./output

# GWT MVP diagram
codeindex diagram gwt --output ./output

# All diagrams
codeindex diagram all --output ./output
```

---

## 🔧 Service Management

### Ollama
```bash
# Check status
systemctl status ollama
curl http://localhost:11434/api/tags

# Restart
sudo systemctl restart ollama

# Pull model
ollama pull gemma3:12b

# List models
ollama list
```

### Weaviate
```bash
# Start
./docker-weaviate.sh start ubuntu

# Stop
./docker-weaviate.sh stop

# Restart
./docker-weaviate.sh restart

# Check status
./docker-weaviate.sh status
curl http://localhost:8080/v1/meta

# View logs
./docker-weaviate.sh logs

# Clean (delete all data)
./docker-weaviate.sh clean
```

### Python Environment
```bash
# Activate
source .venv/bin/activate

# Deactivate
deactivate

# Reinstall dependencies
pip install -r requirements.txt
pip install -e .
```

---

## 📊 Monitoring

### View Statistics
```bash
# Weaviate statistics
python3 weaviate_stats.py

# Application logs
tail -f logs/codeindex.log

# Service status
./deploy-ubuntu-prod.sh
# Select option 4 (Verify)
```

### Check Metrics
```bash
# After extraction, check for:
codeindex status

# Look for:
# - Timeout Summary: 0 timeouts (should be zero!)
# - Foreign Key Extraction: total extracted, by source
# - GWT Navigation: modules, presenters, views discovered
```

---

## 🐛 Troubleshooting

### Services Not Running
```bash
# Check Ollama
systemctl status ollama
sudo systemctl restart ollama

# Check Weaviate
docker ps | grep weaviate
./docker-weaviate.sh restart ubuntu
```

### Timeout Issues
```bash
# Edit .env file
nano .env

# Increase timeout
OLLAMA_READ_TIMEOUT=900  # 15 minutes

# Restart pipeline
source .venv/bin/activate
./run.sh
```

### Memory Issues
```bash
# Edit .env file
nano .env

# Reduce concurrency
MAX_CONCURRENT_AI_CALLS=5
BATCH_SIZE=25
```

### Clean Start
```bash
# Stop services
./docker-weaviate.sh stop
sudo systemctl stop ollama

# Clean Weaviate data
./docker-weaviate.sh clean

# Restart services
sudo systemctl start ollama
./docker-weaviate.sh start ubuntu

# Verify
./deploy-ubuntu-prod.sh
# Select option 4
```

---

## 📁 File Structure

```
gha1javarag/
├── .env                           # Configuration (gitignored)
├── deploy-ubuntu-prod.sh          # Automated deployment
├── docker-weaviate.sh             # Weaviate management
├── run.sh                         # Pipeline runner
├── weaviate_stats.py              # Statistics viewer
├── requirements.txt               # Python dependencies
├── output/                        # Pipeline outputs (gitignored)
│   ├── discovery-inventory.jsonl
│   ├── extraction-results.jsonl
│   └── prd/                       # Generated PRDs
├── logs/                          # Application logs (gitignored)
├── weaviate-data/                 # Vector database (gitignored)
└── src/codeindex/                 # Source code
    ├── cli/                       # CLI commands
    ├── models/                    # Data models
    ├── parsers/                   # File parsers
    └── services/                  # Business logic
```

---

## 🎯 Common Workflows

### Analyze New Codebase
```bash
# 1. Update .env with source directory
nano .env  # Set JAVA_SOURCE_DIR

# 2. Run pipeline
source .venv/bin/activate
./run.sh

# 3. Check results
codeindex status
codeindex search "main components"
```

### Re-Index After Code Changes
```bash
source .venv/bin/activate

# Run discovery and extraction only
codeindex discover --source-dir $JAVA_SOURCE_DIR
codeindex extract --inventory ./output/discovery-inventory.jsonl

# Re-index (updates existing entries)
codeindex index \
    --inventory ./output/discovery-inventory.jsonl \
    --extraction ./output/extraction-results.jsonl
```

### Generate Documentation
```bash
source .venv/bin/activate

# 1. Generate PRDs
codeindex prd backend --output-dir ./output/docs
codeindex prd frontend --output-dir ./output/docs

# 2. Generate diagrams
codeindex diagram all --output ./output/docs

# 3. View diagrams in browser
codeindex diagram component --output ./output/docs --open
```

### Batch Process Multiple Projects
```bash
source .venv/bin/activate

for project in api frontend shared; do
    echo "Processing $project..."
    codeindex discover \
        --source-dir /monorepo \
        --project $project \
        --output "./output/$project/discovery.jsonl"

    codeindex extract \
        --inventory "./output/$project/discovery.jsonl" \
        --output "./output/$project/extraction.jsonl"

    codeindex index \
        --inventory "./output/$project/discovery.jsonl" \
        --extraction "./output/$project/extraction.jsonl"
done

codeindex status
```

---

## 🔑 Environment Variables Reference

### Required
```bash
JAVA_SOURCE_DIR=/path/to/java/source
```

### Services
```bash
WEAVIATE_URL=http://localhost:8080
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
```

### Timeouts
```bash
OLLAMA_CONNECT_TIMEOUT=10        # Connection timeout (seconds)
OLLAMA_READ_TIMEOUT=600          # Read timeout (seconds)
```

### Performance
```bash
MAX_CONCURRENT_AI_CALLS=10       # Concurrent LLM requests
BATCH_SIZE=50                    # Weaviate batch size
```

### Logging
```bash
LOG_LEVEL=INFO                   # DEBUG|INFO|WARNING|ERROR
OUTPUT_DIR=./output              # Output directory
```

---

## 📈 Expected Results

### Successful Run Indicators
- ✅ Discovery: "Discovered X files"
- ✅ Extraction: "Timeout Summary: 0 timeouts"
- ✅ Extraction: "Foreign Key Extraction Summary: X extracted"
- ✅ Extraction: "GWT Navigation: X modules, Y presenters, Z views"
- ✅ Indexing: "Successfully indexed X artifacts"
- ✅ Status: Shows all metrics without errors

### What to Look For
```
Timeout Summary
───────────────────────────────────────────────────────
Total timeouts: 0               ← Should be ZERO!
Retry successes: 0
Fallback used: 0

Foreign Key Extraction Summary
───────────────────────────────────────────────────────
Total FK extracted: 15          ← Multi-source extraction
FK by source:
  Java: 8                       ← @JoinColumn annotations
  iBATIS: 5                     ← XML associations
  SQL: 2                        ← JOIN statements

GWT Navigation Analysis Metrics
───────────────────────────────────────────────────────
Modules parsed: 5
Presenters discovered: 15
Views discovered: 15            ← >90% discovery rate
Navigation edges: 24
```

---

## 🆘 Quick Help

```bash
# Get help for any command
codeindex --help
codeindex discover --help
codeindex extract --help

# Check version
codeindex --version

# Validate installation
./deploy-ubuntu-prod.sh
# Select option 4
```

---

**Quick Reference Version**: 1.0
**Feature**: 007 (MVP Complete)
**Last Updated**: 2025-12-28
