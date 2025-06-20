#!/bin/bash
# 2025.06.20 Test of code onlinebookstore with rate limiting
# Exit on error
set -e

# Configuration
MODE=${1:-"test"}  # Default to test mode
echo "Running in $MODE mode"

# Start time
START_TIME=$(date +%s)

echo "Running Python step 1: main.py (with rate limiting)"
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

STEP1_TIME=$(($(date +%s) - START_TIME))
echo "✅ step1 completed in ${STEP1_TIME} seconds"

echo "Running Python step 2: step2.py (with rate limiting)"
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

STEP2_TIME=$(($(date +%s) - START_TIME))
echo "✅ step2 completed in $((STEP2_TIME - STEP1_TIME)) seconds (total: ${STEP2_TIME}s)"

echo "Running Python step 3: step3.py"
python src/step3.py
STEP3_TIME=$(($(date +%s) - START_TIME))
echo "✅ step3 completed in $((STEP3_TIME - STEP2_TIME)) seconds (total: ${STEP3_TIME}s)"

echo "🎉 All steps completed successfully in ${STEP3_TIME} seconds"
echo "Mode used: $MODE"
echo "Rate limiting applied to prevent API quota exhaustion"
