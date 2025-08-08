#!/bin/bash

# Enhanced Step 1: Process and analyze files with AI-Enhanced Metadata Classification
# This script runs the enhanced analysis pipeline with architectural classification

set -e  # Exit on any error

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Set default values if not provided
AI_PROVIDER=${AI_PROVIDER:-"ollama"}
OUTPUT_DIR=${OUTPUT_DIR:-"./output"}
CHROMADB_DIR=${CHROMADB_DIR:-"./data/chromadb"}

# Rate limiting mode based on argument
RATE_LIMIT_ENV=${1:-"production"}

echo "🚀 Starting Enhanced AI-Powered Java Analysis with Architectural Classification"
echo "=============================================================================="
echo "AI Provider: $AI_PROVIDER"
echo "Output Directory: $OUTPUT_DIR"
echo "ChromaDB Directory: $CHROMADB_DIR"
echo "Rate Limiting Mode: $RATE_LIMIT_ENV"
echo ""

# Validate AI provider configuration
case $AI_PROVIDER in
    "openai")
        if [ -z "$OPENAI_API_KEY" ]; then
            echo "❌ Error: OPENAI_API_KEY environment variable is required for OpenAI provider"
            exit 1
        fi
        echo "✅ OpenAI configuration validated"
        ;;
    "anthropic")
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "❌ Error: ANTHROPIC_API_KEY environment variable is required for Anthropic provider"
            exit 1
        fi
        echo "✅ Anthropic configuration validated"
        ;;
    "ollama")
        OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-"http://localhost:11434"}
        OLLAMA_MODEL_NAME=${OLLAMA_MODEL_NAME:-"deepseek-r1:32b"}
        echo "✅ Ollama configuration: $OLLAMA_BASE_URL using model $OLLAMA_MODEL_NAME"
        ;;
    *)
        echo "❌ Error: Unsupported AI provider: $AI_PROVIDER"
        echo "Supported providers: openai, anthropic, ollama"
        exit 1
        ;;
esac

# Export rate limiting environment
export RATE_LIMIT_ENV

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$CHROMADB_DIR"

echo ""
echo "🧪 Running system validation tests..."
python3 test_enhanced_classification.py
if [ $? -ne 0 ]; then
    echo "❌ System validation failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "📊 Starting enhanced analysis pipeline..."

# Run enhanced analysis
echo "Phase 1: Enhanced file analysis with architectural classification..."
python3 src/enhanced_main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Enhanced analysis completed successfully!"
    echo ""
    echo "📁 Generated files:"
    echo "- $OUTPUT_DIR/enhanced_metadata.json"
    echo "- $OUTPUT_DIR/enhanced_architecture_report.json"
    echo "- $OUTPUT_DIR/layer_summary_*.json"
    echo "- $OUTPUT_DIR/analysis_summary.json"
    echo ""
    
    # Generate enhanced requirements
    echo "Phase 2: Generating enhanced requirements documentation..."
    python3 -c "
import json
import sys
sys.path.insert(0, 'src')
from enhanced_requirements_generator import EnhancedRequirementsGenerator

try:
    # Load analyzed metadata
    with open('$OUTPUT_DIR/enhanced_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Generate requirements
    generator = EnhancedRequirementsGenerator('$OUTPUT_DIR')
    generator.generate_grouped_requirements(metadata)
    
    print('✅ Enhanced requirements generation completed!')
    
except Exception as e:
    print(f'❌ Requirements generation failed: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Enhanced Analysis Pipeline Completed Successfully!"
        echo ""
        echo "📋 Summary:"
        echo "- Enhanced metadata with architectural classification"
        echo "- Intelligent ChromaDB storage with semantic search"
        echo "- Grouped requirements documentation"
        echo "- Architecture analysis reports"
        echo ""
        echo "📁 Check the following directories:"
        echo "- $OUTPUT_DIR/requirements_enhanced/by_layer/"
        echo "- $OUTPUT_DIR/requirements_enhanced/by_component/"
        echo "- $OUTPUT_DIR/requirements_enhanced/analysis/"
        echo ""
        echo "🔍 Next steps:"
        echo "1. Review the enhanced architecture report: $OUTPUT_DIR/enhanced_architecture_report.json"
        echo "2. Explore requirements by layer: $OUTPUT_DIR/requirements_enhanced/by_layer/"
        echo "3. Check component-specific docs: $OUTPUT_DIR/requirements_enhanced/by_component/"
        echo "4. Use the web interface to query the enhanced ChromaDB: ./start_web.sh"
        echo ""
    else
        echo "❌ Requirements generation failed"
        exit 1
    fi
    
else
    echo "❌ Enhanced analysis failed"
    exit 1
fi