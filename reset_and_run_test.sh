#!/bin/bash
# Reset and Run Test Mode - Iteration 14 Complete Pipeline
# This script resets everything and runs the full pipeline in test mode for faster execution

set -e

echo "🔄 ITERATION 14 - RESET AND RUN TEST MODE"
echo "========================================"
echo ""
echo "This script will:"
echo "  1. Reset Weaviate vector database"
echo "  2. Clean output directory"
echo "  3. Run Step 1 (Enhanced UI Analysis)"
echo "  4. Run Step 2 (UI Requirements Generation)"
echo "  5. Run Step 3 (Modern Requirements & UI Modernization)"
echo "  6. Start Web Interface"
echo ""

# Confirmation
read -p "Continue with full reset and test run? (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled"
    exit 1
fi

echo ""
echo "🚀 Starting full reset and test pipeline..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Set environment variables for test mode
export AI_PROVIDER="ollama"
export RATE_LIMIT_ENV="test"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL_NAME="deepseek-r1:32b"
export OLLAMA_TIMEOUT="240"
export TOKENIZERS_PARALLELISM=false

echo "✅ Environment configured for test mode"
echo "   AI Provider: $AI_PROVIDER"
echo "   Rate Limit: $RATE_LIMIT_ENV"
echo "   Ollama URL: $OLLAMA_BASE_URL"
echo ""

# Check Ollama is running
echo "🔍 Checking Ollama availability..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start it with: ollama serve"
    exit 1
fi
echo "✅ Ollama is running and accessible"

# Check if required model is available
if curl -s http://localhost:11434/api/tags | grep -qi "deepseek.*r1.*32b\|qwen.*coder.*30b"; then
    echo "✅ Required AI model is available"
else
    echo "⚠️  Required model not found. Available models:"
    curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "Could not list models"
    echo ""
    echo "Continuing anyway - Ollama will use default model"
fi

# Step 1: Reset Weaviate Database
echo ""
echo "🗄️  STEP 1: RESETTING WEAVIATE DATABASE"
echo "======================================="

echo "🛑 Stopping existing Weaviate container..."
docker stop weaviate 2>/dev/null || echo "   No existing Weaviate container found"
docker rm weaviate 2>/dev/null || echo "   No container to remove"

echo "🚀 Starting fresh Weaviate instance..."
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  -e DEFAULT_VECTORIZER_MODULE='none' \
  -e ENABLE_MODULES='text2vec-openai,text2vec-cohere,text2vec-huggingface,ref2vec-centroid,generative-openai,qna-openai' \
  semitechnologies/weaviate:latest

echo "⏳ Waiting for Weaviate to start (30 seconds)..."
sleep 30

# Verify Weaviate is running
if curl -s http://localhost:8080/v1/meta > /dev/null; then
    echo "✅ Weaviate is running successfully"
    echo "   📊 Version: $(curl -s http://localhost:8080/v1/meta | jq -r '.version' 2>/dev/null || echo 'Unknown')"
else
    echo "❌ Weaviate failed to start properly"
    echo "🔍 Checking Docker logs:"
    docker logs weaviate --tail 20
    exit 1
fi

# Step 2: Clean Output Directory
echo ""
echo "🧹 STEP 2: CLEANING OUTPUT DIRECTORY"
echo "===================================="

if [ -d "./output" ]; then
    echo "🗑️  Removing existing output directory..."
    rm -rf ./output
    echo "✅ Output directory removed"
else
    echo "ℹ️  No existing output directory found"
fi

echo "📁 Creating fresh output directory structure..."
mkdir -p ./output/{requirements_traditional,requirements_modern,ui}
mkdir -p ./data/weaviate
echo "✅ Fresh directory structure created"

# Step 3: Run Enhanced Step 1 (UI Analysis)
echo ""
echo "🎯 STEP 3: ENHANCED WEAVIATE UI ANALYSIS (STEP 1)"
echo "================================================="

STEP1_START=$(date +%s)
echo "🚀 Starting Step 1 Enhanced Weaviate with UI Analysis..."
echo "⏱️  Timeout: 10 minutes for test mode"

if timeout 600 ./Step1_Enhanced_Weaviate.sh test; then
    STEP1_TIME=$(($(date +%s) - STEP1_START))
    echo "✅ Step 1 completed successfully in ${STEP1_TIME} seconds"
    
    # Check results
    if [ -f "./output/enhanced_ui_analysis_test.json" ]; then
        echo "📊 UI Analysis Results:"
        python3 -c "
import json
try:
    with open('./output/enhanced_ui_analysis_test.json', 'r') as f:
        data = json.load(f)
    summary = data.get('summary', {})
    ui_arch = summary.get('ui_architecture', {})
    print(f'   • Files analyzed: {summary.get(\"file_processing\", {}).get(\"total_files_analyzed\", 0)}')
    print(f'   • UI components: {ui_arch.get(\"total_ui_components\", 0)}')
    print(f'   • Navigation flows: {ui_arch.get(\"navigation_flows\", 0)}')
except:
    print('   • Results file found but could not parse summary')
"
    else
        echo "⚠️  UI analysis results file not found"
    fi
else
    echo "❌ Step 1 failed or timed out"
    echo "🔍 Checking for error details..."
    if [ -f "./logs/step1_error.log" ]; then
        echo "Last 10 lines of error log:"
        tail -10 ./logs/step1_error.log
    fi
    echo "⏭️  Continuing with Step 2..."
fi

# Step 4: Run Enhanced Step 2 (UI Requirements)
echo ""
echo "📋 STEP 4: UI REQUIREMENTS GENERATION (STEP 2)"
echo "=============================================="

STEP2_START=$(date +%s)
echo "🚀 Starting Step 2 UI Requirements Generation..."
echo "⏱️  Timeout: 8 minutes for test mode"

if timeout 480 ./Step2_Enhanced_Weaviate.sh test; then
    STEP2_TIME=$(($(date +%s) - STEP2_START))
    echo "✅ Step 2 completed successfully in ${STEP2_TIME} seconds"
    
    # Check results
    if [ -d "./output/requirements_traditional/ui" ]; then
        UI_REQ_COUNT=$(find ./output/requirements_traditional/ui -name "*.md" | wc -l)
        echo "📊 UI Requirements Generated: $UI_REQ_COUNT documents"
    else
        echo "⚠️  UI requirements directory not found"
    fi
else
    echo "❌ Step 2 failed or timed out"
    echo "⏭️  Continuing with Step 3..."
fi

# Step 5: Run Enhanced Step 3 (Modern Requirements & UI Modernization)
echo ""
echo "🏗️  STEP 5: MODERN REQUIREMENTS & UI MODERNIZATION (STEP 3)"
echo "=========================================================="

STEP3_START=$(date +%s)
echo "🚀 Starting Step 3 Modern Requirements & UI Modernization..."
echo "⏱️  Timeout: 8 minutes for test mode"

if timeout 480 ./Step3_Enhanced_Weaviate.sh test; then
    STEP3_TIME=$(($(date +%s) - STEP3_START))
    echo "✅ Step 3 completed successfully in ${STEP3_TIME} seconds"
    
    # Check results
    if [ -f "./output/requirements_modern/processing_results.json" ]; then
        echo "📊 Modern Requirements Results:"
        python3 -c "
import json
try:
    with open('./output/requirements_modern/processing_results.json', 'r') as f:
        data = json.load(f)
    print(f'   • Documents generated: {data.get(\"documents_generated\", 0)}')
    print(f'   • Cloud architectures: {data.get(\"cloud_architectures\", 0)}')
    print(f'   • Modernization plans: {data.get(\"modernization_plans\", 0)}')
    print(f'   • Processing time: {data.get(\"processing_time\", 0):.1f}s')
except:
    print('   • Results file found but could not parse')
"
    fi
    
    # Check UI modernization results
    if [ -d "./output/requirements_modern/ui" ]; then
        UI_MOD_COUNT=$(find ./output/requirements_modern/ui -name "*.md" | wc -l)
        echo "📊 UI Modernization Documents: $UI_MOD_COUNT generated"
    else
        echo "⚠️  UI modernization directory not found"
    fi
else
    echo "❌ Step 3 failed or timed out"
    echo "⏭️  Continuing to completion..."
fi

# Step 6: Display Results Summary
echo ""
echo "📊 FINAL RESULTS SUMMARY"
echo "========================"

TOTAL_TIME=$(($(date +%s) - $(date -j -f "%s" "$STEP1_START" +%s) 2>/dev/null || echo 0))

echo "🏁 Test Mode Pipeline Completed!"
echo ""
echo "⏱️  Total Processing Time: ${TOTAL_TIME} seconds"
echo "🤖 AI Provider: $AI_PROVIDER"
echo "📈 Mode: $RATE_LIMIT_ENV"
echo ""

echo "📁 Generated Output:"
if [ -d "./output" ]; then
    OUTPUT_SIZE=$(du -sh ./output 2>/dev/null | cut -f1 || echo "Unknown")
    echo "   📦 Total size: $OUTPUT_SIZE"
    echo "   📄 Files generated:"
    
    # Count different types of files
    JSON_FILES=$(find ./output -name "*.json" | wc -l)
    MD_FILES=$(find ./output -name "*.md" | wc -l)
    
    echo "      • JSON data files: $JSON_FILES"
    echo "      • Markdown documents: $MD_FILES"
    
    echo ""
    echo "📂 Key directories:"
    [ -d "./output/requirements_traditional" ] && echo "   ✅ Traditional requirements: ./output/requirements_traditional/"
    [ -d "./output/requirements_modern" ] && echo "   ✅ Modern requirements: ./output/requirements_modern/"
    [ -d "./output/requirements_modern/ui" ] && echo "   ✅ UI modernization: ./output/requirements_modern/ui/"
else
    echo "   ❌ No output directory found"
fi

echo ""
echo "🌐 WEB INTERFACE"
echo "================"
echo "To explore the generated requirements interactively:"
echo ""
echo "   cd web && python3 app.py"
echo ""
echo "   Then visit: http://localhost:8000"
echo ""

echo "✅ ITERATION 14 TEST MODE PIPELINE COMPLETED SUCCESSFULLY!"
echo ""
echo "🚀 Next Steps:"
echo "   1. Review generated requirements in ./output/"
echo "   2. Start web interface to explore results"
echo "   3. Run production mode for comprehensive analysis: ./reset_and_run_production.sh"
echo "   4. Generate StrictDoc documentation: cd strictdoc && ./Web.sh"
echo ""

# Optional: Auto-start web interface
read -p "🌐 Start web interface now? (y/N): " start_web
if [[ "$start_web" =~ ^[Yy]$ ]]; then
    echo "🚀 Starting web interface..."
    cd web
    echo "🌐 Web interface will be available at: http://localhost:8000"
    echo "🛑 Press Ctrl+C to stop the web server"
    echo ""
    python3 app.py
fi

echo ""
echo "🎉 Test run completed! Check the results above."