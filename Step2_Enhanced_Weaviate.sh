#!/bin/bash
# Enhanced Step 2 Script - Traditional Requirements with Weaviate, Data Structure Analysis, and UI Requirements (Iteration 14)
# Exit on error
set -e

# Configuration
MODE=${1:-"production"}  # Default to production mode
echo "🚀 Running Enhanced Step 2 (Traditional Requirements + UI Requirements) in $MODE mode"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

export TOKENIZERS_PARALLELISM=false

# Check AI provider configuration
AI_PROVIDER=${AI_PROVIDER:-"ollama"}
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
elif [ "$AI_PROVIDER" = "ollama" ]; then
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ ERROR: Ollama is not running or not accessible at http://localhost:11434"
        echo "Please start Ollama:"
        echo "ollama serve"
        echo "And ensure the model is available:"
        echo "ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        exit 1
    fi
    echo "✅ Ollama is running and accessible"
    
    # Check if the model is available (case-insensitive)
    MODEL_NAME=${OLLAMA_MODEL_NAME:-"danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"}
    if ! curl -s http://localhost:11434/api/tags | grep -qi "qwen.*coder.*30b"; then
        echo "⚠️  WARNING: Required Qwen3-Coder-30B model not found in Ollama"
        echo "Available models:"
        curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "Could not retrieve model list"
        echo ""
        echo "To pull the model:"
        echo "ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        echo ""
        echo "Continue anyway? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✅ Qwen3-Coder-30B model is available"
    fi
else
    echo "❌ ERROR: Invalid AI_PROVIDER: $AI_PROVIDER"
    echo "Supported providers: 'openai', 'anthropic', 'ollama'"
    exit 1
fi

# Check if Weaviate is running
if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    echo "❌ ERROR: Weaviate is not running or not accessible at http://localhost:8080"
    echo "Please start Weaviate using Docker:"
    echo "docker run -d --name weaviate -p 8080:8080 -p 50051:50051 semitechnologies/weaviate:latest"
    exit 1
fi
echo "✅ Weaviate is running and accessible"

# Check if Weaviate metadata exists
WEAVIATE_METADATA_FILE="./output/weaviate_metadata.json"
if [ ! -f "$WEAVIATE_METADATA_FILE" ]; then
    echo "❌ ERROR: Weaviate metadata file not found: $WEAVIATE_METADATA_FILE"
    echo "Please run Step1_Enhanced_Weaviate.sh first to generate Weaviate metadata"
    exit 1
fi

DATA_STRUCTURES_FILE="./output/data_structures_analysis.json"
if [ ! -f "$DATA_STRUCTURES_FILE" ]; then
    echo "⚠️  WARNING: Data structures analysis not found: $DATA_STRUCTURES_FILE"
    echo "Continuing with basic Weaviate metadata..."
fi

ARCHITECTURE_REPORT_FILE="./output/enhanced_architecture_report.json"
if [ ! -f "$ARCHITECTURE_REPORT_FILE" ]; then
    echo "⚠️  WARNING: Enhanced architecture report not found: $ARCHITECTURE_REPORT_FILE"
    echo "Continuing with basic analysis..."
fi

echo "✅ Weaviate metadata files found"

# Start time for step 2
STEP2_START_TIME=$(date +%s)

# Check for debug mode
DEBUGFILE=${DEBUGFILE:-""}
if [ -n "$DEBUGFILE" ] && [ -f "$DEBUGFILE" ]; then
    echo "🔍 DEBUG MODE ENABLED for Enhanced Step 2 Traditional Requirements"
    echo "Debug file: $DEBUGFILE"
    echo "Processing traditional requirements with debug enhancements..."
    
    export RATE_LIMIT_ENV=$MODE
    python3 -c "
import sys
sys.path.append('src')
from traditional_requirements_processor import TraditionalRequirementsProcessor
import asyncio

async def main():
    try:
        processor = TraditionalRequirementsProcessor(
            weaviate_metadata_file='$WEAVIATE_METADATA_FILE',
            data_structures_file='$DATA_STRUCTURES_FILE',
            architecture_file='$ARCHITECTURE_REPORT_FILE',
            debug_file='$DEBUGFILE',
            mode='$MODE'
        )
        
        results = await processor.process_traditional_requirements()
        
        if results.get('success', False):
            print('✅ Traditional requirements processing completed successfully!')
            print(f'📊 Generated {results.get(\"requirements_count\", 0)} traditional requirements')
            print(f'🏗️ Processed {results.get(\"data_structures_analyzed\", 0)} data structures')
            return True
        else:
            print('❌ Traditional requirements processing failed')
            return False
            
    except Exception as e:
        print(f'❌ Traditional requirements processing failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"
else
    echo "🔧 Running Traditional Requirements Generation with Weaviate and Data Structures"
    echo "📊 Features enabled:"
    echo "   - Weaviate vector database integration"
    echo "   - Data structure-driven requirements"
    echo "   - Traditional requirements documentation"
    echo "   - Layer-aware requirements analysis"
    echo "   - Entity relationship analysis"
    echo "   - Business domain organization"
    echo "   - AI-powered requirements with $AI_PROVIDER"
    
    export RATE_LIMIT_ENV=$MODE
    python3 -c "
import sys
sys.path.append('src')
from traditional_requirements_processor import TraditionalRequirementsProcessor
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        processor = TraditionalRequirementsProcessor(
            weaviate_metadata_file='$WEAVIATE_METADATA_FILE',
            data_structures_file='$DATA_STRUCTURES_FILE',
            architecture_file='$ARCHITECTURE_REPORT_FILE',
            mode='$MODE'
        )
        
        results = await processor.process_traditional_requirements()
        
        if results.get('success', False):
            print('✅ Traditional requirements processing completed successfully!')
            print(f'📊 Generated {results.get(\"requirements_count\", 0)} traditional requirements')
            print(f'🏗️ Processed {results.get(\"data_structures_analyzed\", 0)} data structures')
            print(f'📋 Created {results.get(\"documents_generated\", 0)} requirement documents')
            return True
        else:
            print('❌ Traditional requirements processing failed')
            return False
            
    except Exception as e:
        print(f'❌ Traditional requirements processing failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"
fi

# Check for quota exceeded error (for OpenAI and Anthropic)
if [ $? -ne 0 ]; then
    if [ "$AI_PROVIDER" = "openai" ]; then
        echo "❌ Enhanced Step 2 failed. This might be due to:"
        echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo "   - Weaviate connectivity issues"
        echo "   - Data structure analysis compatibility issues"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./Step2_Enhanced_Weaviate.sh emergency"
        echo "   - Check your OpenAI billing and plan details"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to Anthropic: export AI_PROVIDER=anthropic"
        echo "   - Switch to Ollama for local processing: export AI_PROVIDER=ollama"
        echo "   - Verify Weaviate is running: docker ps | grep weaviate"
        echo "   - Check Weaviate metadata files are valid JSON"
    elif [ "$AI_PROVIDER" = "anthropic" ]; then
        echo "❌ Enhanced Step 2 failed. This might be due to:"
        echo "   - Anthropic API quota exceeded (check billing at https://console.anthropic.com/)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo "   - Invalid API key"
        echo "   - Weaviate connectivity issues"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./Step2_Enhanced_Weaviate.sh emergency"
        echo "   - Check your Anthropic billing and plan details"
        echo "   - Verify your API key format (should start with 'sk-ant-')"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to OpenAI: export AI_PROVIDER=openai"
        echo "   - Switch to Ollama for local processing: export AI_PROVIDER=ollama"
        echo "   - Verify Weaviate is running and accessible"
    else
        echo "❌ Enhanced Step 2 failed. This might be due to:"
        echo "   - Ollama service issues"
        echo "   - Qwen3-Coder-30B model loading problems"
        echo "   - Network connectivity problems"
        echo "   - Weaviate connectivity issues"
        echo "   - Data structure analysis issues"
        echo ""
        echo "💡 Tips:"
        echo "   - Check if Ollama is running: ollama serve"
        echo "   - Verify Qwen3-Coder-30B model: ollama list"
        echo "   - Check Ollama logs for errors"
        echo "   - Verify Weaviate is running: docker ps | grep weaviate"
        echo "   - Switch to OpenAI: export AI_PROVIDER=openai"
        echo "   - Switch to Anthropic: export AI_PROVIDER=anthropic"
        echo "   - Check data structure files are valid JSON"
    fi
    exit 1
fi

STEP2_TIME=$(($(date +%s) - STEP2_START_TIME))
echo "✅ Enhanced Step 2 (Traditional Requirements) completed successfully in ${STEP2_TIME} seconds"
echo "Mode used: $MODE"
echo "AI Provider: $AI_PROVIDER"
echo "Enhanced features: Weaviate integration, data structure analysis, traditional requirements"
echo ""
echo "📊 Configuration Info:"
echo "   - AI Provider: $AI_PROVIDER"
if [ "$AI_PROVIDER" = "openai" ]; then
    echo "   - OpenAI Model: ${OPENAI_MODEL_NAME:-'gpt-4-turbo-preview'}"
elif [ "$AI_PROVIDER" = "anthropic" ]; then
    echo "   - Anthropic Model: ${ANTHROPIC_MODEL_NAME:-'claude-3-5-sonnet-20241022'}"
elif [ "$AI_PROVIDER" = "ollama" ]; then
    echo "   - Ollama Model: ${OLLAMA_MODEL_NAME:-'danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth'}"
    echo "   - Ollama URL: ${OLLAMA_BASE_URL:-'http://localhost:11434'}"
fi
echo "   - Rate Limit Environment: $RATE_LIMIT_ENV"
echo "   - Weaviate Integration: Enabled"
echo "   - Data Structure Analysis: Enabled"
echo "   - Traditional Requirements Generation: Enabled"
echo "   - Entity Relationship Analysis: Enabled"
echo "   - Business Domain Organization: Enabled"
echo "   - Quota exceeded handling: Enabled (OpenAI and Anthropic)"
echo "   - Intelligent error detection: Enabled"
echo ""
echo "📁 Traditional Requirements Output Files:"
echo "   - Traditional requirements: ./output/requirements_traditional/"
echo "   - Entity requirements: ./output/requirements_traditional/entities/"
echo "   - Functional requirements: ./output/requirements_traditional/functional/"
echo "   - Non-functional requirements: ./output/requirements_traditional/non_functional/"
echo "   - Data requirements: ./output/requirements_traditional/data/"
echo "   - Integration requirements: ./output/requirements_traditional/integration/"
echo "   - Security requirements: ./output/requirements_traditional/security/"
echo "   - Master requirements document: ./output/requirements_traditional/master_requirements.md"
echo ""
echo "🔍 Data Structure Analysis Results:"
if [ -f "$DATA_STRUCTURES_FILE" ]; then
    python3 -c "
import json
try:
    with open('$DATA_STRUCTURES_FILE', 'r') as f:
        data = json.load(f)
    
    entities = data.get('entities', [])
    dtos = data.get('dtos', [])
    relationships = data.get('relationships', [])
    
    print(f'   • Entities: {len(entities)} analyzed')
    print(f'   • DTOs: {len(dtos)} analyzed') 
    print(f'   • Relationships: {len(relationships)} identified')
    
    if entities:
        print('   • Key Entities:')
        for entity in entities[:5]:
            print(f'     - {entity.get(\"name\", \"Unknown\")}: {len(entity.get(\"fields\", []))} fields')
    
except Exception as e:
    print('   • Data structure summary not available')
"
fi

echo ""
echo "🖥️ Generating UI Requirements from Enhanced Weaviate Analysis..."

# Check for enhanced UI analysis file
UI_ANALYSIS_FILE="./output/enhanced_ui_analysis_${MODE}.json"
if [ -f "$UI_ANALYSIS_FILE" ]; then
    echo "✅ Enhanced UI analysis file found: $UI_ANALYSIS_FILE"
    
    python3 -c "
import sys
sys.path.append('src')
from ui_requirements_processor import UIRequirementsProcessor
import json

try:
    # Load UI analysis results
    with open('$UI_ANALYSIS_FILE', 'r') as f:
        ui_analysis_results = json.load(f)
    
    # Extract UI analysis data
    ui_analysis = ui_analysis_results.get('ui_analysis', {})
    
    if ui_analysis:
        # Generate UI requirements
        processor = UIRequirementsProcessor('./output')
        generated_files = processor.save_ui_requirements(ui_analysis, '$MODE')
        
        print('✅ UI requirements generation completed successfully!')
        print(f'📋 Generated {len(generated_files)} UI requirement documents:')
        for doc_type, file_path in generated_files.items():
            print(f'   - {doc_type.title()}: {file_path}')
        
        # Display UI analysis summary
        ui_stats = ui_analysis.get('ui_statistics', {})
        ui_arch = ui_analysis.get('ui_architecture', {})
        ui_modern = ui_analysis.get('modernization_analysis', {})
        
        print('')
        print('🎯 UI Analysis Summary:')
        print(f'   • UI Components: {ui_arch.get(\"total_components\", 0)}')
        print(f'   • Navigation Flows: {ui_arch.get(\"total_navigation_flows\", 0)}')
        print(f'   • Business Domains: {len(ui_arch.get(\"business_domains\", []))}')
        print(f'   • High Priority Components: {ui_modern.get(\"high_priority_count\", 0)}')
        print(f'   • Average Complexity Score: {ui_modern.get(\"average_complexity_score\", 0):.1f}')
        
    else:
        print('⚠️  No UI analysis data found in results file')
        
except Exception as e:
    print(f'❌ UI requirements generation failed: {e}')
    import traceback
    traceback.print_exc()
"

else
    echo "⚠️  Enhanced UI analysis file not found: $UI_ANALYSIS_FILE"
    echo "UI requirements generation skipped. Run Step1_Enhanced_Weaviate.sh first."
fi

echo ""
echo "🚀 Next Steps:"
echo "1. Review traditional requirements: ./output/requirements_traditional/"
echo "2. Review UI requirements: ./output/requirements_ui/"
echo "3. Validate entity-specific requirements with business stakeholders"
echo "4. Run Step3_Enhanced_Weaviate.sh for modern requirements"
echo "5. Use web interface to query requirements: ./start_web_weaviate.sh"