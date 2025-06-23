#!/bin/bash
# 2025.06.20 Test of code onlinebookstore with rate limiting
# Exit on error
set -e

# Configuration
MODE=${1:-"test"}  # Default to test mode
echo "Running in $MODE mode"

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
    echo "Supported providers: 'openai', 'ollama'"
    exit 1
fi

# Start time
START_TIME=$(date +%s)

echo "Running Python step 1: main.py (with improved rate limiting and $AI_PROVIDER)"
if [ "$MODE" = "test" ]; then
    echo "Using test mode with conservative rate limiting..."
    python src/main_test.py
elif [ "$MODE" = "production" ]; then
    echo "Using production mode with standard rate limiting..."
    export RATE_LIMIT_ENV=production
    python src/main.py
elif [ "$MODE" = "emergency" ]; then
    echo "Using emergency mode with very restrictive rate limiting..."
    export RATE_LIMIT_ENV=emergency
    python src/main.py
else
    echo "Using test mode with conservative rate limiting..."
    python src/main_test.py
fi

# Check for quota exceeded error (only for OpenAI)
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
    fi
    exit 1
fi

STEP1_TIME=$(($(date +%s) - START_TIME))
echo "✅ step1 completed in ${STEP1_TIME} seconds"

echo "Running Python step 2: step2.py (with improved rate limiting and $AI_PROVIDER)"
if [ "$MODE" = "test" ]; then
    echo "Using test mode for step2..."
    export RATE_LIMIT_ENV=test
    python src/step2_test.py
elif [ "$MODE" = "production" ]; then
    echo "Using production mode for step2..."
    export RATE_LIMIT_ENV=production
    python src/step2.py
elif [ "$MODE" = "emergency" ]; then
    echo "Using emergency mode for step2..."
    export RATE_LIMIT_ENV=emergency
    python src/step2.py
else
    echo "Using test mode for step2..."
    export RATE_LIMIT_ENV=test
    python src/step2_test.py
fi

# Check for quota exceeded error (only for OpenAI)
if [ $? -ne 0 ]; then
    if [ "$AI_PROVIDER" = "openai" ]; then
        echo "❌ Step 2 failed. This might be due to:"
        echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./lofalassn.sh emergency"
        echo "   - Check your OpenAI billing and plan details"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to Ollama for local testing: export AI_PROVIDER=ollama"
    else
        echo "❌ Step 2 failed. This might be due to:"
        echo "   - Ollama service issues"
        echo "   - Model loading problems"
        echo "   - Network connectivity problems"
        echo ""
        echo "💡 Tips:"
        echo "   - Check if Ollama is running: ollama serve"
        echo "   - Verify model is available: ollama list"
        echo "   - Check Ollama logs for errors"
    fi
    exit 1
fi

STEP2_TIME=$(($(date +%s) - START_TIME))
echo "✅ step2 completed in $((STEP2_TIME - STEP1_TIME)) seconds (total: ${STEP2_TIME}s)"

echo "Running Python step 3: step3.py"
python src/step3.py
STEP3_TIME=$(($(date +%s) - START_TIME))
echo "✅ step3 completed in $((STEP3_TIME - STEP2_TIME)) seconds (total: ${STEP3_TIME}s)"

echo "🎉 All steps completed successfully in ${STEP3_TIME} seconds"
echo "Mode used: $MODE"
echo "AI Provider: $AI_PROVIDER"
echo "Rate limiting applied to prevent API quota exhaustion"
echo ""
echo "📊 Configuration Info:"
echo "   - AI Provider: $AI_PROVIDER"
if [ "$AI_PROVIDER" = "openai" ]; then
    echo "   - OpenAI Model: ${OPENAI_MODEL_NAME:-'gpt-4-turbo-preview'}"
elif [ "$AI_PROVIDER" = "ollama" ]; then
    echo "   - Ollama Model: ${OLLAMA_MODEL_NAME:-'deepseek-r1:32b'}"
    echo "   - Ollama URL: ${OLLAMA_BASE_URL:-'http://localhost:11434'}"
fi
echo "   - Rate Limit Environment: $RATE_LIMIT_ENV"
echo "   - Quota exceeded handling: Enabled (OpenAI only)"
echo "   - Intelligent error detection: Enabled"
echo "   - For more info, see: RATE_LIMITING.md"
