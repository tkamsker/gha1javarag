#!/bin/bash
# 2025.06.20 Test of code onlinebookstore with rate limiting
# Exit on error
set -e

# Configuration
MODE=${1:-"test"}  # Default to test mode
echo "Running in $MODE mode"

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY environment variable is not set"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Start time
START_TIME=$(date +%s)

echo "Running Python step 1: main.py (with improved rate limiting)"
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

# Check for quota exceeded error
if [ $? -ne 0 ]; then
    echo "❌ Step 1 failed. This might be due to:"
    echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
    echo "   - Rate limiting issues"
    echo "   - Network connectivity problems"
    echo ""
    echo "💡 Tips:"
    echo "   - Try running in 'emergency' mode: ./lofalassn.sh emergency"
    echo "   - Check your OpenAI billing and plan details"
    echo "   - Wait for quota reset or upgrade your plan"
    exit 1
fi

STEP1_TIME=$(($(date +%s) - START_TIME))
echo "✅ step1 completed in ${STEP1_TIME} seconds"

echo "Running Python step 2: step2.py (with improved rate limiting)"
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

# Check for quota exceeded error
if [ $? -ne 0 ]; then
    echo "❌ Step 2 failed. This might be due to:"
    echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
    echo "   - Rate limiting issues"
    echo "   - Network connectivity problems"
    echo ""
    echo "💡 Tips:"
    echo "   - Try running in 'emergency' mode: ./lofalassn.sh emergency"
    echo "   - Check your OpenAI billing and plan details"
    echo "   - Wait for quota reset or upgrade your plan"
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
echo "Rate limiting applied to prevent API quota exhaustion"
echo ""
echo "📊 Rate Limiting Info:"
echo "   - Environment: $RATE_LIMIT_ENV"
echo "   - Quota exceeded handling: Enabled"
echo "   - Intelligent error detection: Enabled"
echo "   - For more info, see: RATE_LIMITING.md"
