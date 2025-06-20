#!/bin/bash
# 2025.06.20 Tets of code onlinebookstore 
# Exit on error
set -e

# Start time
START_TIME=$(date +%s)

echo "Running Python step 1: main.py"
python src/main.py
STEP1_TIME=$(($(date +%s) - START_TIME))
echo "✅ step1 completed in ${STEP1_TIME} seconds"

echo "Running Python step 2: step2.py"
python src/step2.py
STEP2_TIME=$(($(date +%s) - START_TIME))
echo "✅ step2 completed in $((STEP2_TIME - STEP1_TIME)) seconds (total: ${STEP2_TIME}s)"

echo "Running Python step 3: step3.py"
python src/step3.py
STEP3_TIME=$(($(date +%s) - START_TIME))
echo "✅ step3 completed in $((STEP3_TIME - STEP2_TIME)) seconds (total: ${STEP3_TIME}s)"

echo "🎉 All steps completed successfully in ${STEP3_TIME} seconds"
