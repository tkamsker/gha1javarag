# Ollama Debugging Guide

## Overview

Enhanced debugging has been added to the Ollama provider to help troubleshoot issues like timeouts, connection problems, and model availability. This guide shows you how to use these debugging features effectively.

## Enhanced Logging Features

### 1. Request Details Logging
Every Ollama request now logs detailed information:

```
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO - Ollama request details:
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   URL: http://localhost:11434/api/chat
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   Model: deepseek-r1:32b
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   Temperature: 0.1
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   Max tokens: 50
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   Timeout: 30 seconds
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   Message count: 1
2025-06-23 14:03:15,772 - java_analysis.ai_providers - INFO -   First message preview: You are a helpful assistant...
```

### 2. Response Details Logging
Response information is logged for debugging:

```
2025-06-23 14:03:20,881 - java_analysis.ai_providers - INFO - Ollama response received in 5.11 seconds
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO -   Status code: 200
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO -   Content-Type: application/json; charset=utf-8
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO - Ollama response parsed successfully
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO -   Response keys: ['model', 'created_at', 'message', ...]
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO -   Response preview: <think>Okay, so I need to figure out...
2025-06-23 14:03:20,882 - java_analysis.ai_providers - INFO -   Response length: 202 characters
```

### 3. Health Check Logging
Service health is checked before each request:

```
2025-06-23 14:03:15,737 - java_analysis.ai_providers - INFO - Checking Ollama service health...
2025-06-23 14:03:15,760 - java_analysis.ai_providers - INFO - Available Ollama models: ['deepseek-r1:32b']
```

### 4. Enhanced Error Logging
Detailed error information is logged:

```
2025-06-23 14:03:51,583 - java_analysis.ai_providers - ERROR - Ollama request timed out after 30 seconds
2025-06-23 14:03:51,583 - java_analysis.ai_providers - ERROR - Request details:
2025-06-23 14:03:51,583 - java_analysis.ai_providers - ERROR -   URL: http://localhost:11434/api/chat
2025-06-23 14:03:51,583 - java_analysis.ai_providers - ERROR -   Model: deepseek-r1:32b
2025-06-23 14:03:51,583 - java_analysis.ai_providers - ERROR -   Timeout: 30 seconds
```

## Configurable Timeouts

### Environment-Based Timeout Configuration
Timeouts are now configurable based on the rate limiting environment:

| Environment | Timeout | Use Case |
|-------------|---------|----------|
| `production` | 120s | Normal production use |
| `test` | 60s | Testing with faster feedback |
| `development` | 90s | Development with moderate speed |
| `emergency` | 30s | Fast debugging and troubleshooting |

### Configuration File
Timeouts are defined in `config/rate_limiting.yaml`:

```yaml
production:
  ollama_timeout: 120  # 2 minutes for Ollama requests

test:
  ollama_timeout: 60  # 1 minute for Ollama requests (faster debugging)

emergency:
  ollama_timeout: 30  # 30 seconds for Ollama requests (very fast debugging)
```

## Debugging Tools

### 1. Health Check Test
Test Ollama service health:

```bash
python src/test_ollama_debug.py
```

This will:
- Check if Ollama is running
- Verify model availability
- Test basic completion
- Demonstrate timeout handling

### 2. Environment-Specific Testing
Test with different timeout configurations:

```bash
# Fast debugging (30s timeout)
export RATE_LIMIT_ENV=emergency
python src/test_ollama_debug.py

# Normal testing (60s timeout)
export RATE_LIMIT_ENV=test
python src/test_ollama_debug.py

# Production testing (120s timeout)
export RATE_LIMIT_ENV=production
python src/test_ollama_debug.py
```

### 3. Manual Health Check
You can also check Ollama health manually:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List available models
ollama list

# Check Ollama logs
ollama serve --verbose
```

## Common Issues and Solutions

### 1. Timeout Issues

**Problem**: `Ollama request timed out after X seconds`

**Solutions**:
- Increase timeout in config: `config/rate_limiting.yaml`
- Use emergency mode for faster debugging: `export RATE_LIMIT_ENV=emergency`
- Check if Ollama is overloaded: `ollama list`
- Restart Ollama service: `ollama serve`

### 2. Model Not Found

**Problem**: `Model deepseek-r1:32b not found`

**Solutions**:
- Pull the model: `ollama pull deepseek-r1:32b`
- Check available models: `ollama list`
- Use a different model: `export OLLAMA_MODEL_NAME=llama3.2:3b`

### 3. Service Not Responding

**Problem**: `Ollama service not responding`

**Solutions**:
- Start Ollama: `ollama serve`
- Check if port is available: `lsof -i :11434`
- Check Ollama logs: `ollama serve --verbose`

### 4. Network Errors

**Problem**: `Ollama network error`

**Solutions**:
- Check Ollama URL: `export OLLAMA_BASE_URL=http://localhost:11434`
- Verify firewall settings
- Check if Ollama is accessible: `curl http://localhost:11434/api/tags`

## Debugging Workflow

### Step 1: Quick Health Check
```bash
python src/test_ollama_debug.py
```

### Step 2: Check Logs
Look for these key log entries:
- ✅ `Health status: healthy`
- ✅ `Model deepseek-r1:32b is available`
- ✅ `Ollama response received in X seconds`

### Step 3: Adjust Timeout if Needed
```bash
# For faster debugging
export RATE_LIMIT_ENV=emergency

# For normal operation
export RATE_LIMIT_ENV=production
```

### Step 4: Test with Your Application
```bash
export AI_PROVIDER=ollama
export RATE_LIMIT_ENV=test
./lofalassn.sh test
```

## Performance Monitoring

### Response Time Tracking
The system logs response times for performance monitoring:

```
Ollama response received in 5.11 seconds
```

### Model Performance
Track model performance with different configurations:

- **Temperature**: Lower = more deterministic
- **Max tokens**: Higher = longer responses
- **Timeout**: Lower = faster failure detection

### Optimization Tips

1. **For Development**: Use `RATE_LIMIT_ENV=emergency` (30s timeout)
2. **For Testing**: Use `RATE_LIMIT_ENV=test` (60s timeout)
3. **For Production**: Use `RATE_LIMIT_ENV=production` (120s timeout)
4. **For Complex Analysis**: Increase `max_tokens` in the request
5. **For Faster Responses**: Lower `temperature` for more deterministic output

## Integration with Main Application

The enhanced debugging is automatically available when using Ollama:

```bash
# Normal operation with debugging
export AI_PROVIDER=ollama
export RATE_LIMIT_ENV=test
./lofalassn.sh test
```

All Ollama requests will now include detailed logging for better troubleshooting and performance monitoring. 