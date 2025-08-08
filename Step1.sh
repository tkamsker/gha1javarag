#!/bin/bash
# 2025.06.20 Test of code onlinebookstore with rate limiting
# 2025.06.26 copy von Lofalassn.sh
# Exit on error
set -e

# Configuration
MODE=${1:-"test"}  # Default to test mode
echo "Running in $MODE mode"

export TOKENIZERS_PARALLELISM=false

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check AI provider configuration
AI_PROVIDER=${AI_PROVIDER:-"openai"}
echo "Using AI Provider: $AI_PROVIDER"

if [ "$AI_PROVIDER" = "openai" ]; then
    # Check OpenAI API key
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "❌ ERROR: OPENAI_API_KEY environment variable is not set"
        echo "Please set your OpenAI API key:"
        echo "export OPENAI_API_KEY='your-api-key-here'"
        echo "Or add it to your .env file"
        exit 1
    fi
    echo "✅ OpenAI API key configured"
elif [ "$AI_PROVIDER" = "anthropic" ]; then
    # Check Anthropic API key
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ ERROR: ANTHROPIC_API_KEY environment variable is not set"
        echo "Please set your Anthropic API key:"
        echo "export ANTHROPIC_API_KEY='your-api-key-here'"
        echo "Or add it to your .env file"
        exit 1
    fi
    echo "✅ Anthropic API key configured"
    
    # Validate API key format (should start with 'sk-ant-')
    if [[ ! "$ANTHROPIC_API_KEY" =~ ^sk-ant- ]]; then
        echo "⚠️  WARNING: Anthropic API key format appears incorrect"
        echo "Expected format: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        echo "Current format: ${ANTHROPIC_API_KEY:0:10}..."
        echo ""
        echo "Continue anyway? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
elif [ "$AI_PROVIDER" = "ollama" ]; then
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ ERROR: Ollama is not running or not accessible at http://localhost:11434"
        echo "Please start Ollama:"
        echo "ollama serve"
        echo "And ensure the model is available:"
        echo "ollama pull deepseek-r1:32b"
        exit 1
    fi
    echo "✅ Ollama is running and accessible"
    
    # Check if the model is available
    MODEL_NAME=${OLLAMA_MODEL_NAME:-"deepseek-r1:32b"}
    if ! curl -s http://localhost:11434/api/tags | grep -q "$MODEL_NAME"; then
        echo "⚠️  WARNING: Model $MODEL_NAME not found in Ollama"
        echo "Available models:"
        curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "Could not retrieve model list"
        echo ""
        echo "To pull the model:"
        echo "ollama pull $MODEL_NAME"
        echo ""
        echo "Continue anyway? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✅ Model $MODEL_NAME is available"
    fi
else
    echo "❌ ERROR: Invalid AI_PROVIDER: $AI_PROVIDER"
    echo "Supported providers: 'openai', 'anthropic', 'ollama'"
    exit 1
fi

# Start time
START_TIME=$(date +%s)

# Check for debug mode
DEBUGFILE=${DEBUGFILE:-""}
if [ -n "$DEBUGFILE" ] && [ -f "$DEBUGFILE" ]; then
    echo "🔍 DEBUG MODE ENABLED"
    echo "Debug file: $DEBUGFILE"
    echo "Processing specific files listed in debug file..."
    
    if [ "$MODE" = "test" ]; then
        echo "Using debug mode with test settings..."
        python3 src/main_debug.py
    elif [ "$MODE" = "production" ]; then
        echo "Using debug mode with production settings..."
        export RATE_LIMIT_ENV=production
        python3 src/main_debug.py
    elif [ "$MODE" = "emergency" ]; then
        echo "Using debug mode with emergency settings..."
        export RATE_LIMIT_ENV=emergency
        python3 src/main_debug.py
    else
        echo "Using debug mode with test settings..."
        python3 src/main_debug.py
    fi
else
    echo "Running Python step 1: main.py (with improved rate limiting and $AI_PROVIDER)"
    if [ "$MODE" = "test" ]; then
        echo "Using test mode with conservative rate limiting..."
        python3 src/main_test.py
    elif [ "$MODE" = "production" ]; then
        echo "Using production mode with standard rate limiting..."
        export RATE_LIMIT_ENV=production
        python3 src/main.py
    elif [ "$MODE" = "emergency" ]; then
        echo "Using emergency mode with very restrictive rate limiting..."
        export RATE_LIMIT_ENV=emergency
        python3 src/main.py
    else
        echo "Using test mode with conservative rate limiting..."
        python3 src/main_test.py
    fi
fi

# Check for quota exceeded error (for OpenAI and Anthropic)
if [ $? -ne 0 ]; then
    if [ "$AI_PROVIDER" = "openai" ]; then
        echo "❌ Step 1 failed. This might be due to:"
        echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./lofalassn.sh emergency"
        echo "   - Check your OpenAI billing and plan details"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to Anthropic: export AI_PROVIDER=anthropic"
        echo "   - Switch to Ollama for local testing: export AI_PROVIDER=ollama"
    elif [ "$AI_PROVIDER" = "anthropic" ]; then
        echo "❌ Step 1 failed. This might be due to:"
        echo "   - Anthropic API quota exceeded (check billing at https://console.anthropic.com/)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo "   - Invalid API key"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./lofalassn.sh emergency"
        echo "   - Check your Anthropic billing and plan details"
        echo "   - Verify your API key format (should start with 'sk-ant-')"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to OpenAI: export AI_PROVIDER=openai"
        echo "   - Switch to Ollama for local testing: export AI_PROVIDER=ollama"
    else
        echo "❌ Step 1 failed. This might be due to:"
        echo "   - Ollama service issues"
        echo "   - Model loading problems"
        echo "   - Network connectivity problems"
        echo ""
        echo "💡 Tips:"
        echo "   - Check if Ollama is running: ollama serve"
        echo "   - Verify model is available: ollama list"
        echo "   - Check Ollama logs for errors"
        echo "   - Switch to OpenAI: export AI_PROVIDER=openai"
        echo "   - Switch to Anthropic: export AI_PROVIDER=anthropic"
    fi
    exit 1
fi

STEP1_TIME=$(($(date +%s) - START_TIME))
echo "✅ step1 completed in ${STEP1_TIME} seconds"

