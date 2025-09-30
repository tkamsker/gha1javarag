#!/bin/bash
# Enhanced Step 3 Script - Modern Requirements with Weaviate and Data Structure Analysis
# Exit on error
set -e

# Configuration
MODE=${1:-"production"}  # Default to production mode
echo "🚀 Running Enhanced Step 3 (Modern Requirements) in $MODE mode"

# Load environment variables (safe: supports comments and spaces)
if [ -f .env ]; then
    set -a
    # shellcheck disable=SC1091
    . ./.env
    set +a
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

# Check if traditional requirements exist
TRADITIONAL_REQUIREMENTS_DIR="./output/requirements_traditional"
if [ ! -d "$TRADITIONAL_REQUIREMENTS_DIR" ]; then
    echo "⚠️  WARNING: Traditional requirements directory not found: $TRADITIONAL_REQUIREMENTS_DIR"
    echo "Consider running Step2_Enhanced_Weaviate.sh first for optimal results"
    echo "Continuing with Weaviate metadata only..."
fi

echo "✅ Weaviate metadata files found"

# Start time for step 3
STEP3_START_TIME=$(date +%s)

# Check for debug mode
DEBUGFILE=${DEBUGFILE:-""}
if [ -n "$DEBUGFILE" ] && [ -f "$DEBUGFILE" ]; then
    echo "🔍 DEBUG MODE ENABLED for Enhanced Step 3 Modern Requirements"
    echo "Debug file: $DEBUGFILE"
    echo "Processing modern requirements with debug enhancements..."
    
    export RATE_LIMIT_ENV=$MODE
    python3 -c "
import sys
sys.path.append('src')
from modern_requirements_processor import ModernRequirementsProcessor
import asyncio

async def main():
    try:
        processor = ModernRequirementsProcessor(
            weaviate_metadata_file='$WEAVIATE_METADATA_FILE',
            data_structures_file='$DATA_STRUCTURES_FILE',
            architecture_file='$ARCHITECTURE_REPORT_FILE',
            traditional_requirements_dir='$TRADITIONAL_REQUIREMENTS_DIR',
            debug_file='$DEBUGFILE',
            mode='$MODE'
        )
        
        results = await processor.process_modern_requirements()
        
        if results.get('success', False):
            print('✅ Modern requirements processing completed successfully!')
            print(f'📊 Generated {results.get(\"requirements_count\", 0)} modern requirements')
            print(f'🏗️ Processed {results.get(\"data_structures_analyzed\", 0)} data structures')
            print(f'☁️ Created {results.get(\"cloud_architectures\", 0)} cloud architecture blueprints')
            return True
        else:
            print('❌ Modern requirements processing failed')
            return False
            
    except Exception as e:
        print(f'❌ Modern requirements processing failed: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
"
else
    echo "🔧 Running Modern Requirements Generation with Weaviate and Data Structures"
    echo "📊 Features enabled:"
    echo "   - Weaviate vector database integration"
    echo "   - Data structure-driven modern requirements"
    echo "   - Cloud-native architecture requirements"
    echo "   - Microservices architecture specifications"
    echo "   - DevOps and CI/CD requirements"
    echo "   - Modern technology stack recommendations"
    echo "   - Container and Kubernetes requirements"
    echo "   - AI-powered requirements with $AI_PROVIDER"
    
    export RATE_LIMIT_ENV=$MODE
    python3 -c "
import sys
sys.path.append('src')
from modern_requirements_processor import ModernRequirementsProcessor
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        processor = ModernRequirementsProcessor(
            weaviate_metadata_file='$WEAVIATE_METADATA_FILE',
            data_structures_file='$DATA_STRUCTURES_FILE',
            architecture_file='$ARCHITECTURE_REPORT_FILE',
            traditional_requirements_dir='$TRADITIONAL_REQUIREMENTS_DIR',
            mode='$MODE'
        )
        
        results = await processor.process_modern_requirements()
        
        if results.get('success', False):
            print('✅ Modern requirements processing completed successfully!')
            print(f'📊 Generated {results.get(\"requirements_count\", 0)} modern requirements')
            print(f'🏗️ Processed {results.get(\"data_structures_analyzed\", 0)} data structures')
            print(f'☁️ Created {results.get(\"cloud_architectures\", 0)} cloud architecture blueprints')
            print(f'📋 Generated {results.get(\"documents_generated\", 0)} modern requirement documents')
            print(f'🔄 Created {results.get(\"modernization_plans\", 0)} modernization plans')
            return True
        else:
            print('❌ Modern requirements processing failed')
            return False
            
    except Exception as e:
        print(f'❌ Modern requirements processing failed: {e}')
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
        echo "❌ Enhanced Step 3 failed. This might be due to:"
        echo "   - OpenAI API quota exceeded (check billing at https://platform.openai.com/account/billing)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo "   - Weaviate connectivity issues"
        echo "   - Data structure analysis compatibility issues"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./Step3_Enhanced_Weaviate.sh emergency"
        echo "   - Check your OpenAI billing and plan details"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to Anthropic: export AI_PROVIDER=anthropic"
        echo "   - Switch to Ollama for local processing: export AI_PROVIDER=ollama"
        echo "   - Verify Weaviate is running: docker ps | grep weaviate"
        echo "   - Check Weaviate metadata files are valid JSON"
        echo "   - Verify Step2_Enhanced_Weaviate.sh completed successfully"
    elif [ "$AI_PROVIDER" = "anthropic" ]; then
        echo "❌ Enhanced Step 3 failed. This might be due to:"
        echo "   - Anthropic API quota exceeded (check billing at https://console.anthropic.com/)"
        echo "   - Rate limiting issues"
        echo "   - Network connectivity problems"
        echo "   - Invalid API key"
        echo "   - Weaviate connectivity issues"
        echo ""
        echo "💡 Tips:"
        echo "   - Try running in 'emergency' mode: ./Step3_Enhanced_Weaviate.sh emergency"
        echo "   - Check your Anthropic billing and plan details"
        echo "   - Verify your API key format (should start with 'sk-ant-')"
        echo "   - Wait for quota reset or upgrade your plan"
        echo "   - Switch to OpenAI: export AI_PROVIDER=openai"
        echo "   - Switch to Ollama for local processing: export AI_PROVIDER=ollama"
        echo "   - Verify Weaviate is running and accessible"
        echo "   - Check if Step2_Enhanced_Weaviate.sh completed successfully"
    else
        echo "❌ Enhanced Step 3 failed. This might be due to:"
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
        echo "   - Verify Step2_Enhanced_Weaviate.sh completed successfully"
    fi
    exit 1
fi

STEP3_TIME=$(($(date +%s) - STEP3_START_TIME))
echo "✅ Enhanced Step 3 (Modern Requirements) completed successfully in ${STEP3_TIME} seconds"
echo "Mode used: $MODE"
echo "AI Provider: $AI_PROVIDER"
echo "Enhanced features: Weaviate integration, data structure analysis, modern requirements"
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
echo "   - Modern Requirements Generation: Enabled"
echo "   - Cloud Architecture Blueprints: Enabled"
echo "   - Microservices Architecture Design: Enabled"
echo "   - DevOps and CI/CD Requirements: Enabled"
echo "   - Container and Kubernetes Specifications: Enabled"
echo "   - Quota exceeded handling: Enabled (OpenAI and Anthropic)"
echo "   - Intelligent error detection: Enabled"
echo ""
echo "📁 Modern Requirements Output Files:"
echo "   - Modern requirements: ./output/requirements_modern/"
echo "   - Cloud architecture: ./output/requirements_modern/cloud_architecture/"
echo "   - Microservices design: ./output/requirements_modern/microservices/"
echo "   - DevOps requirements: ./output/requirements_modern/devops/"
echo "   - Technology stack: ./output/requirements_modern/technology/"
echo "   - Migration strategy: ./output/requirements_modern/migration/"
echo "   - Container requirements: ./output/requirements_modern/containers/"
echo "   - API specifications: ./output/requirements_modern/apis/"
echo "   - Modernization roadmap: ./output/requirements_modern/modernization_roadmap.md"
echo "   - Master modern requirements: ./output/requirements_modern/master_modern_requirements.md"
echo ""
echo "🔍 Modern Architecture Results:"
if [ -f "./output/requirements_modern/processing_results.json" ]; then
    python3 -c "
import json
try:
    with open('./output/requirements_modern/processing_results.json', 'r') as f:
        data = json.load(f)
    
    print(f'   • Modern Requirements: {data.get(\"requirements_count\", 0)} generated')
    print(f'   • Cloud Architectures: {data.get(\"cloud_architectures\", 0)} designed')
    print(f'   • Microservices: {data.get(\"microservices_count\", 0)} identified')
    print(f'   • DevOps Pipelines: {data.get(\"devops_pipelines\", 0)} specified')
    print(f'   • Technology Recommendations: {data.get(\"tech_recommendations\", 0)} provided')
    
except Exception as e:
    print('   • Modern requirements summary not yet available')
"
fi
echo ""
echo "🚀 Next Steps:"
echo "1. Review modern requirements: ./output/requirements_modern/"
echo "2. Validate cloud architecture designs with infrastructure teams"
echo "3. Review microservices architecture with development teams"
echo "4. Plan DevOps implementation based on generated pipelines"
echo "5. Use web interface to explore modern requirements: ./start_web_weaviate.sh"
echo "6. Compare traditional vs modern requirements for migration planning"