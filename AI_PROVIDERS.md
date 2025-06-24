# AI Provider System

## Overview

The application now supports multiple AI providers through a unified interface, allowing you to easily switch between OpenAI and Ollama (local) for code analysis. This addresses rate limiting issues by providing a local alternative.

## Supported Providers

### 1. OpenAI
- **Use Case**: Production, high-quality analysis
- **Requirements**: OpenAI API key
- **Rate Limiting**: Full rate limiting and quota management
- **Cost**: Per-token pricing

### 2. Ollama (Local)
- **Use Case**: Testing, development, offline work
- **Requirements**: Ollama installed and running
- **Rate Limiting**: Minimal (local processing)
- **Cost**: Free (local processing)

## Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```bash
# AI Provider Selection
AI_PROVIDER=openai  # or 'ollama'

# OpenAI Configuration (when AI_PROVIDER=openai)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4-turbo-preview

# Ollama Configuration (when AI_PROVIDER=ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=deepseek-r1:32b
OLLAMA_TIMEOUT=120

# Rate Limiting
RATE_LIMIT_ENV=test  # production, test, development, emergency
```

### Quick Setup

#### For OpenAI:
```bash
export AI_PROVIDER=openai
export OPENAI_API_KEY="your-api-key"
```

#### For Ollama:
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the model
ollama pull deepseek-r1:32b

# Set environment
export AI_PROVIDER=ollama
```

## Usage

### Switching Providers

#### Method 1: Environment Variable
```bash
# Use OpenAI
export AI_PROVIDER=openai
./lofalassn.sh test

# Use Ollama
export AI_PROVIDER=ollama
./lofalassn.sh test
```

#### Method 2: .env File
```bash
# Edit .env file
echo "AI_PROVIDER=ollama" > .env
./lofalassn.sh test
```

#### Method 3: Inline
```bash
AI_PROVIDER=ollama ./lofalassn.sh test
```

### Running the Application

```bash
# Test mode with current provider
./lofalassn.sh test

# Production mode with current provider
./lofalassn.sh production

# Emergency mode with current provider
./lofalassn.sh emergency
```

## Provider-Specific Features

### OpenAI Provider
- ✅ Full rate limiting and quota management
- ✅ Intelligent error handling (quota exceeded, rate limits)
- ✅ Exponential backoff for retries
- ✅ Detailed error messages with billing links
- ❌ Requires API key and internet connection
- ❌ Subject to rate limits and quotas

### Ollama Provider
- ✅ No API costs or quotas
- ✅ Works offline
- ✅ Faster response times (local processing)
- ✅ No rate limiting issues
- ✅ Privacy (data stays local)
- ❌ Requires local computational resources
- ❌ Model quality may vary
- ❌ Requires model download

## Rate Limiting Behavior

### OpenAI
- **Conservative Limits**: 15 req/min, 800 req/hour
- **Quota Management**: Automatic detection and handling
- **Error Recovery**: Exponential backoff and retry logic
- **Wait Times**: Configurable wait periods for quota exceeded

### Ollama
- **Relaxed Limits**: 60 req/min, 1000 req/hour
- **No Quota**: Local processing, no external limits
- **Fast Recovery**: Minimal delays between requests
- **No Wait Times**: Immediate retry on failure

## Testing

### Test Provider Setup
```bash
# Test both providers
python src/test_ai_providers.py

# Test rate limiting
python src/test_rate_limiter.py
```

### Manual Testing
```bash
# Test OpenAI
AI_PROVIDER=openai python src/main_test.py

# Test Ollama
AI_PROVIDER=ollama python src/main_test.py
```

## Troubleshooting

### OpenAI Issues
```bash
# Check API key
echo $OPENAI_API_KEY

# Test connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models

# Check billing
# Visit: https://platform.openai.com/account/billing
```

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check available models
ollama list

# Pull model if missing
ollama pull deepseek-r1:32b

# Check Ollama logs
ollama serve --verbose
```

### Common Issues

#### "Ollama is not running"
```bash
# Start Ollama service
ollama serve

# Check if it's accessible
curl http://localhost:11434/api/tags
```

#### "Model not found"
```bash
# List available models
ollama list

# Pull the required model
ollama pull deepseek-r1:32b
```

#### "OpenAI API key not set"
```bash
# Set the API key
export OPENAI_API_KEY="your-api-key"

# Or add to .env file
echo "OPENAI_API_KEY=your-api-key" >> .env
```

## Performance Comparison

| Aspect | OpenAI | Ollama |
|--------|--------|--------|
| **Speed** | Network dependent | Local (faster) |
| **Quality** | High (GPT-4) | Variable (model dependent) |
| **Cost** | Per token | Free |
| **Reliability** | High (with rate limits) | High (local) |
| **Privacy** | Data sent to OpenAI | Local only |
| **Setup** | API key only | Install + model download |

## Best Practices

### Development Workflow
1. **Start with Ollama**: Use for development and testing
2. **Switch to OpenAI**: Use for production and final analysis
3. **Monitor Usage**: Check rate limiting stats and quotas

### Environment Management
```bash
# Development environment
export AI_PROVIDER=ollama
export RATE_LIMIT_ENV=development

# Production environment
export AI_PROVIDER=openai
export RATE_LIMIT_ENV=production

# Emergency environment
export AI_PROVIDER=ollama
export RATE_LIMIT_ENV=emergency
```

### Model Selection
- **OpenAI**: Use `gpt-4-turbo-preview` for best quality
- **Ollama**: Use `deepseek-r1:32b` for good balance of quality and speed

## Migration Guide

### From OpenAI-only to Multi-Provider

1. **Install Ollama** (if not already installed)
2. **Pull the model**: `ollama pull deepseek-r1:32b`
3. **Set environment**: `export AI_PROVIDER=ollama`
4. **Test**: `python src/test_ai_providers.py`
5. **Run**: `./lofalassn.sh test`

### Switching Between Providers

```bash
# Quick switch to Ollama for testing
AI_PROVIDER=ollama ./lofalassn.sh test

# Switch back to OpenAI for production
AI_PROVIDER=openai ./lofalassn.sh production
```

## Architecture

The provider system uses a factory pattern:

```
AIProvider (Abstract Base Class)
├── OpenAIProvider
│   ├── AsyncOpenAI client
│   ├── Rate limiting
│   └── Quota management
└── OllamaProvider
    ├── HTTP client
    ├── Local processing
    └── Minimal rate limiting
```

This design allows for:
- Easy addition of new providers
- Consistent interface across providers
- Provider-specific optimizations
- Graceful fallback mechanisms 