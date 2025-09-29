#!/bin/bash

# Enhanced Step 1: Process and analyze files with Weaviate and Data Structure Discovery
# This script runs the enhanced analysis pipeline with architectural classification and data structure analysis

set -e  # Exit on any error

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Set default values if not provided
AI_PROVIDER=${AI_PROVIDER:-"ollama"}
OUTPUT_DIR=${OUTPUT_DIR:-"./output"}
WEAVIATE_DIR=${WEAVIATE_DIR:-"./data/weaviate"}

# Rate limiting mode based on argument
RATE_LIMIT_ENV=${1:-"production"}

echo "🚀 Starting Enhanced AI-Powered Java Analysis with Weaviate and Data Structure Discovery"
echo "===================================================================================="
echo "AI Provider: $AI_PROVIDER"
echo "Output Directory: $OUTPUT_DIR"
echo "Weaviate Directory: $WEAVIATE_DIR"
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
        OLLAMA_MODEL_NAME=${OLLAMA_MODEL_NAME:-"danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"}
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
mkdir -p "$WEAVIATE_DIR"

echo ""
echo "🧪 Running system validation tests..."

# Check if Weaviate is running
if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    echo "❌ Error: Weaviate is not running on localhost:8080"
    echo "Please start Weaviate using Docker:"
    echo "docker run -d --name weaviate -p 8080:8080 -p 50051:50051 semitechnologies/weaviate:latest"
    exit 1
fi
echo "✅ Weaviate is running and accessible"

# Check Ollama if using it
if [ "$AI_PROVIDER" = "ollama" ]; then
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ Error: Ollama is not running on localhost:11434"
        echo "Please start Ollama and pull the required model"
        exit 1
    fi
    echo "✅ Ollama is running and accessible"
fi

echo ""
echo "📊 Starting enhanced analysis pipeline with data structure discovery..."

# Run enhanced analysis with Weaviate and data structure discovery
echo "Phase 1: Enhanced file analysis with Weaviate storage and data structure extraction..."

python3 -c "
import sys
sys.path.append('src')
from enhanced_weaviate_processor import EnhancedWeaviateProcessor
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        # Initialize processor with data structure discovery
        processor = EnhancedWeaviateProcessor(
            java_root_path='/Users/thomaskamsker/Documents/Atom/vron.one/playground/java',
            output_dir='$OUTPUT_DIR',
            enable_data_structure_discovery=True
        )
        
        # Run comprehensive analysis
        results = await processor.run_comprehensive_analysis()
        
        print('✅ Enhanced Weaviate analysis completed successfully!')
        print(f'📊 Processed {results.get(\"files_processed\", 0)} files')
        print(f'🏗️ Identified {results.get(\"data_structures_found\", 0)} data structures')
        print(f'📋 Generated {results.get(\"requirements_generated\", 0)} requirements')
        
        return True
        
    except Exception as e:
        print(f'❌ Enhanced analysis failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Enhanced Weaviate analysis completed successfully!"
    echo ""
    echo "📁 Generated files:"
    echo "- $OUTPUT_DIR/weaviate_metadata.json"
    echo "- $OUTPUT_DIR/data_structures_analysis.json"
    echo "- $OUTPUT_DIR/enhanced_architecture_report.json"
    echo "- $OUTPUT_DIR/module_analysis_*.json"
    echo "- $OUTPUT_DIR/analysis_summary.json"
    echo ""
    
    # Generate enhanced requirements with data structure insights
    echo "Phase 2: Generating enhanced requirements with data structure insights..."
    python3 -c "
import json
import sys
sys.path.insert(0, 'src')
from weaviate_requirements_generator import WeaviateRequirementsGenerator

try:
    # Load analyzed metadata
    with open('$OUTPUT_DIR/weaviate_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Load data structures analysis
    try:
        with open('$OUTPUT_DIR/data_structures_analysis.json', 'r') as f:
            data_structures = json.load(f)
    except FileNotFoundError:
        data_structures = {}
    
    # Generate requirements with data structure insights
    import asyncio
    generator = WeaviateRequirementsGenerator('$OUTPUT_DIR')
    asyncio.run(generator.generate_comprehensive_requirements(metadata, data_structures))
    
    print('✅ Enhanced requirements generation with data structures completed!')
    
except Exception as e:
    print(f'❌ Requirements generation failed: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Enhanced Weaviate Analysis Pipeline Completed Successfully!"
        echo ""
        echo "📋 Summary:"
        echo "- Enhanced metadata with Weaviate vector storage"
        echo "- Data structure discovery and analysis"
        echo "- Architectural classification and layer analysis"
        echo "- Comprehensive requirements documentation"
        echo "- Semantic search capabilities"
        echo ""
        echo "📁 Check the following directories:"
        echo "- $OUTPUT_DIR/requirements_weaviate/by_layer/"
        echo "- $OUTPUT_DIR/requirements_weaviate/by_data_structure/"
        echo "- $OUTPUT_DIR/requirements_weaviate/analysis/"
        echo "- $OUTPUT_DIR/data_structures/"
        echo ""
        echo "🔍 Next steps:"
        echo "1. Review data structures: $OUTPUT_DIR/data_structures_analysis.json"
        echo "2. Explore requirements by layer: $OUTPUT_DIR/requirements_weaviate/by_layer/"
        echo "3. Check data-driven requirements: $OUTPUT_DIR/requirements_weaviate/by_data_structure/"
        echo "4. Use the web interface to query Weaviate: ./start_web_weaviate.sh"
        echo ""
        echo "🗃️ Data Structure Discovery Results:"
        
        # Show quick data structure summary using file info
        if [ -f "$OUTPUT_DIR/data_structures_analysis.json" ]; then
            echo "   • Data structure analysis file generated"
            file_size=$(wc -c < "$OUTPUT_DIR/data_structures_analysis.json" 2>/dev/null || echo "0")
            echo "   • Analysis file size: $((file_size / 1024))KB"
            
            # Quick count using simple grep instead of loading large JSON
            entity_count=$(grep -c '"type": "entity"' "$OUTPUT_DIR/data_structures_analysis.json" 2>/dev/null || echo "0")
            dto_count=$(grep -c '"type": "dto"' "$OUTPUT_DIR/data_structures_analysis.json" 2>/dev/null || echo "0")
            
            echo "   • Entities: $entity_count found"
            echo "   • DTOs: $dto_count found"
            echo "   • Use web interface to explore detailed analysis"
        else
            echo "   • Data structure summary file not found"
        fi
        
    else
        echo "❌ Requirements generation failed"
        exit 1
    fi
    
else
    echo "❌ Enhanced Weaviate analysis failed"
    exit 1
fi