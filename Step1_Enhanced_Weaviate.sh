#!/bin/bash

# Enhanced Step 1: Process and analyze files with Weaviate, Data Structure Discovery, and UI Analysis (Iteration 14)
# This script runs the enhanced analysis pipeline with architectural classification, data structure analysis, and comprehensive GWT UI component analysis

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

echo "🚀 Starting Enhanced AI-Powered Java Analysis with Weaviate, Data Structure Discovery, and UI Analysis"
echo "====================================================================================================="
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
echo "📊 Starting enhanced analysis pipeline with data structure discovery and UI analysis..."

# Run enhanced analysis with Weaviate, data structure discovery, and comprehensive UI analysis
echo "Phase 1: Enhanced file analysis with Weaviate storage, data structure extraction, and UI component analysis..."

python3 -c "
import sys
sys.path.append('src')
from enhanced_weaviate_ui_processor import EnhancedWeaviateUIProcessor
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        # Initialize processor with UI analysis capabilities
        processor = EnhancedWeaviateUIProcessor()
        
        # Run comprehensive analysis with UI processing
        results = await processor.process_with_ui_analysis('$RATE_LIMIT_ENV')
        
        # Extract results for reporting
        processing_metadata = results.get('processing_metadata', {})
        ui_analysis = results.get('ui_analysis', {})
        ui_stats = ui_analysis.get('ui_statistics', {})
        ui_arch = ui_analysis.get('ui_architecture', {})
        
        print('✅ Enhanced Weaviate UI analysis completed successfully!')
        print(f'📊 Files Processed: {ui_stats.get(\"total_files\", 0)} (including UI files)')
        print(f'🖥️ UI Components Discovered: {ui_arch.get(\"total_components\", 0)} portlets, dialogs, widgets')
        print(f'🔄 Navigation Flows Mapped: {ui_arch.get(\"total_navigation_flows\", 0)} user workflows')
        print(f'⚙️ GWT Widgets Cataloged: {len(ui_arch.get(\"gwt_widgets_used\", []))} unique widgets')
        print(f'🏗️ Data Structures Found: {processing_metadata.get(\"data_structures_found\", 0)}')
        print(f'⏱️ Processing Time: {processing_metadata.get(\"processing_time\", 0):.2f} seconds')
        
        return True
        
    except Exception as e:
        print(f'❌ Enhanced UI analysis failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Enhanced Weaviate UI analysis completed successfully!"
    echo ""
    echo "📁 Generated files:"
    echo "- $OUTPUT_DIR/enhanced_ui_analysis_$RATE_LIMIT_ENV.json"
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
import asyncio
sys.path.insert(0, 'src')
from weaviate_requirements_generator import WeaviateRequirementsGenerator

async def generate_requirements():
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
        generator = WeaviateRequirementsGenerator('$OUTPUT_DIR')
        await generator.generate_comprehensive_requirements(metadata, data_structures)
        
        print('✅ Enhanced requirements generation with data structures completed!')
        return True
        
    except Exception as e:
        print(f'❌ Requirements generation failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(generate_requirements())
    sys.exit(0 if success else 1)
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Enhanced Weaviate UI Analysis Pipeline Completed Successfully!"
        echo ""
        echo "📋 Summary:"
        echo "- Enhanced metadata with Weaviate vector storage"
        echo "- Data structure discovery and analysis"
        echo "- Comprehensive GWT UI component analysis"
        echo "- Navigation flow mapping and user workflow documentation"
        echo "- UI modernization assessment and recommendations"
        echo "- Architectural classification and layer analysis"
        echo "- Comprehensive requirements documentation"
        echo "- Semantic search capabilities for UI and data components"
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
        
        # Show data structure summary if available
        if [ -f "$OUTPUT_DIR/data_structures_analysis.json" ]; then
            python3 -c "
import json
try:
    with open('$OUTPUT_DIR/data_structures_analysis.json', 'r') as f:
        data = json.load(f)
    
    entities = data.get('entities', [])
    dtos = data.get('dtos', [])
    relationships = data.get('relationships', [])
    
    print(f'   • Entities: {len(entities)} found')
    print(f'   • DTOs: {len(dtos)} found') 
    print(f'   • Relationships: {len(relationships)} found')
    
    if entities:
        print('   • Top Entities:')
        for entity in entities[:5]:
            print(f'     - {entity.get(\"name\", \"Unknown\")}: {entity.get(\"fields_count\", 0)} fields')
    
except Exception as e:
    print('   • Data structure summary not available')
"
        fi
        
        # Run enhanced output processing
        echo ""
        echo "🔧 Running enhanced output processing..."
        python3 -c "
import sys
sys.path.append('src')
from enhanced_output_processor import EnhancedOutputProcessor

try:
    processor = EnhancedOutputProcessor('./output')
    results = processor.process_all_outputs()
    print(f'✅ Enhanced processing complete: {results[\"files_fixed\"]} files fixed, {results[\"ui_components_extracted\"]} UI components extracted')
except Exception as e:
    print(f'⚠️  Enhanced processing failed: {e}')
    print('📊 Continuing with standard output...')
"
        
    else
        echo "❌ Requirements generation failed"
        exit 1
    fi
    
else
    echo "❌ Enhanced Weaviate analysis failed"
    exit 1
fi