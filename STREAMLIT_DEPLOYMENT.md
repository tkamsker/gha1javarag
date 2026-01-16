# Streamlit Deployment Guide

This guide explains how to deploy and manage the Streamlit web application for Feature 009.

## Quick Start

```bash
# Start Streamlit (foreground - recommended for testing)
./start_streamlit.sh

# Start Streamlit (background - recommended for production)
./start_streamlit_background.sh

# Check status
./status_streamlit.sh

# Stop Streamlit
./stop_streamlit.sh
```

## Available Scripts

### 1. `start_streamlit.sh` - Foreground Mode

Starts Streamlit in the foreground (attached to your terminal).

**Use when:**
- Testing the application
- Debugging issues
- You want to see logs in real-time

**How to use:**
```bash
./start_streamlit.sh
```

**To stop:** Press `Ctrl+C`

### 2. `start_streamlit_background.sh` - Background Mode

Starts Streamlit as a background process with logging to `streamlit.log`.

**Use when:**
- Running in production
- You want it to keep running after logout
- You need to free up your terminal

**How to use:**
```bash
./start_streamlit_background.sh

# View logs
tail -f streamlit.log
```

**To stop:** Run `./stop_streamlit.sh`

### 3. `stop_streamlit.sh` - Stop Application

Safely stops the Streamlit application.

```bash
./stop_streamlit.sh
```

### 4. `status_streamlit.sh` - Check Status

Displays comprehensive status of:
- Streamlit process
- Port availability (8501)
- Ollama service
- Weaviate service
- Log files
- Application URLs

```bash
./status_streamlit.sh
```

## Configuration

### Environment Variables

The scripts use these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL_NAME` | `qwen2.5-coder:32b` | Ollama model to use |
| `STREAMLIT_PORT` | `8501` | Port for Streamlit |

### Override Configuration

```bash
# Use different model
export OLLAMA_MODEL_NAME="gemma3:12b"
./start_streamlit.sh

# Use different port
export STREAMLIT_PORT=8502
./start_streamlit.sh
```

### `.env` File

The scripts automatically load settings from `.env` if it exists:

```bash
# .env example
OLLAMA_MODEL_NAME=qwen2.5-coder:32b
STREAMLIT_PORT=8501
JAVA_SOURCE_DIR=/path/to/java/source
```

## Production Deployment

### Step 1: Copy Updated Files

Copy these files to your production server:

```bash
# On production machine
cd /home/tkamsker/development/Iteration20/gha1javarag

# Backup old ollama_client.py
cp src/codeindex/services/ollama_client.py src/codeindex/services/ollama_client.py.backup

# Copy the new ollama_client.py (provided separately)
# nano src/codeindex/services/ollama_client.py
# (paste content and save)
```

### Step 2: Copy Scripts

```bash
# Copy all startup scripts
# (These are already in the repository)
ls -la *.sh
# You should see:
# - start_streamlit.sh
# - start_streamlit_background.sh
# - stop_streamlit.sh
# - status_streamlit.sh
```

### Step 3: Verify Setup

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check your model exists
ollama list | grep qwen2.5-coder:32b

# Check Python virtual environment
ls -la venv/

# Check .env file
cat .env | grep OLLAMA_MODEL_NAME
```

### Step 4: Start Application

```bash
# Production start (background mode)
./start_streamlit_background.sh

# Check it's running
./status_streamlit.sh

# View logs
tail -f streamlit.log
```

## Troubleshooting

### Streamlit Won't Start

```bash
# Check what's blocking port 8501
netstat -tuln | grep 8501
# OR
ss -tuln | grep 8501

# Kill process on that port
lsof -ti:8501 | xargs kill -9
```

### Ollama Connection Issues

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Verify model is loaded
ollama list
```

### Model Not Found Error

```bash
# Check available models
ollama list

# Pull the model if missing
ollama pull qwen2.5-coder:32b

# Test the model works
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5-coder:32b","prompt":"test","stream":false}'
```

### Permission Denied on Scripts

```bash
# Make scripts executable
chmod +x *.sh
```

### Python Module Not Found

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### View Recent Errors

```bash
# Last 50 lines of log
tail -50 streamlit.log

# Search for errors
grep -i error streamlit.log | tail -20
```

## Monitoring

### Check Application Health

```bash
# Full status check
./status_streamlit.sh

# Just check if running
pgrep -f streamlit
```

### Watch Logs in Real-Time

```bash
# Follow log file
tail -f streamlit.log

# Follow with filtering
tail -f streamlit.log | grep -i "error\|warning"
```

### Resource Usage

```bash
# Check Streamlit memory/CPU
ps aux | grep streamlit

# Detailed process info
top -p $(pgrep -f streamlit)
```

## Automatic Restart on Reboot

To start Streamlit automatically on server reboot, add to crontab:

```bash
# Edit crontab
crontab -e

# Add this line:
@reboot cd /home/tkamsker/development/Iteration20/gha1javarag && ./start_streamlit_background.sh
```

Or create a systemd service (more robust):

```bash
# Create service file
sudo nano /etc/systemd/system/streamlit.service

# Add content:
[Unit]
Description=Streamlit Web Application
After=network.target

[Service]
Type=simple
User=tkamsker
WorkingDirectory=/home/tkamsker/development/Iteration20/gha1javarag
ExecStart=/home/tkamsker/development/Iteration20/gha1javarag/venv/bin/streamlit run src/codeindex/web/app.py
Restart=always
Environment="OLLAMA_MODEL_NAME=qwen2.5-coder:32b"

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable streamlit
sudo systemctl start streamlit

# Check status
sudo systemctl status streamlit
```

## Access URLs

Once Streamlit is running, access it at:

- **Local:** http://localhost:8501
- **Network:** http://YOUR_SERVER_IP:8501
- **External:** http://YOUR_EXTERNAL_IP:8501 (if firewall allows)

## Support

For issues or questions:
1. Check `streamlit.log` for error messages
2. Run `./status_streamlit.sh` for diagnostics
3. Verify Ollama and Weaviate are running
4. Check the troubleshooting section above
