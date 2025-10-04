#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running Step 3-CrewAI: Agent-Based Backend/Frontend Analysis"

# Parse command line arguments
VERBOSE="--verbose"

while [[ $# -gt 0 ]]; do
  case $1 in
    --no-verbose)
      VERBOSE=""
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Step 3-CrewAI: Agent-Based Backend/Frontend Requirements Analysis"
      echo ""
      echo "🤖 Agent Architecture:"
      echo "  - Backend Architecture Analyst: DAO/DTO/Service analysis"
      echo "  - Frontend Architecture Analyst: UI/Workflow analysis"
      echo "  - Semantic Enrichment Specialist: Weaviate-based enrichment"
      echo "  - Integration Architecture Specialist: Cross-layer synthesis"
      echo ""
      echo "Features:"
      echo "  - Autonomous agent decision-making"
      echo "  - Dynamic Weaviate semantic enrichment"
      echo "  - Cross-agent collaboration and memory"
      echo "  - Intelligent source code revisiting"
      echo "  - Hierarchical task processing"
      echo ""
      echo "Options:"
      echo "  --no-verbose      Disable verbose logging"
      echo "  -h, --help        Show this help message"
      echo ""
      echo "Output Structure:"
      echo "  \$OUTPUT_DIR/requirements/crewai/"
      echo "  ├── _crewai_summary.md              # Agent analysis summary"
      echo "  └── projects/"
      echo "      └── {project_name}/"
      echo "          ├── requirements.md         # Synthesized requirements"
      echo "          ├── backend_analysis.json   # Backend agent results"
      echo "          ├── frontend_analysis.json  # Frontend agent results"
      echo "          ├── enrichment_data.json    # Weaviate enrichment"
      echo "          ├── agent_execution_log.json# Agent interactions"
      echo "          └── summary.md              # Project summary"
      echo ""
      echo "Prerequisites:"
      echo "  - CrewAI framework installed (crewai>=0.28.0)"
      echo "  - Valid LLM provider configuration"
      echo "  - Weaviate database running and accessible"
      echo "  - Intermediate data from step 2 (analyze)"
      echo ""
      echo "Environment Variables (.env):"
      echo "  JAVA_SOURCE_DIR     - Full path to Java source code directory"
      echo "  OUTPUT_DIR          - Output directory for results"
      echo "  WEAVIATE_URL        - Weaviate database URL"
      echo "  AI_PROVIDER         - LLM provider (openai/anthropic/ollama)"
      echo ""
      echo "Example .env configuration:"
      echo "  JAVA_SOURCE_DIR=/path/to/your/java/projects"
      echo "  OUTPUT_DIR=./output"
      echo "  WEAVIATE_URL=http://localhost:8080"
      echo "  AI_PROVIDER=openai"
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Environment setup
if [ ! -d "venv" ]; then
  echo "[INFO] Creating Python virtual environment..."
  python3 -m venv venv
fi

echo "[INFO] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1

# Check for CrewAI dependencies
echo "[INFO] Checking CrewAI dependencies..."
if ! pip show crewai >/dev/null 2>&1; then
  echo "[INFO] Installing CrewAI dependencies..."
  pip install crewai>=0.28.0 crewai-tools>=0.1.0 >/dev/null 2>&1
fi

pip install -r requirements.txt >/dev/null 2>&1

# Configuration validation
if [ ! -f ".env" ]; then
  echo "[ERROR] .env configuration file not found"
  echo "[ERROR] Please create .env with required variables:"
  echo "        WEAVIATE_URL, OUTPUT_DIR, AI_PROVIDER"
  echo "        JAVA_SOURCE_DIR (recommended for source code analysis)"
  exit 1
fi

# Validate JAVA_SOURCE_DIR if provided
JAVA_SOURCE_DIR=$(grep -E '^JAVA_SOURCE_DIR=' .env | cut -d'=' -f2 | tr -d '"' || echo "")
if [ -n "$JAVA_SOURCE_DIR" ]; then
  if [ ! -d "$JAVA_SOURCE_DIR" ]; then
    echo "[WARNING] JAVA_SOURCE_DIR does not exist: $JAVA_SOURCE_DIR"
    echo "[WARNING] Agent source code analysis may not work properly"
  else
    echo "[INFO] Using JAVA_SOURCE_DIR for agent analysis: $JAVA_SOURCE_DIR"
  fi
else
  echo "[WARNING] JAVA_SOURCE_DIR not configured"
  echo "[WARNING] Agents will use limited source code analysis"
  echo "[WARNING] Consider adding JAVA_SOURCE_DIR=/path/to/your/java/projects to .env"
fi

# Validate LLM provider configuration
echo "[INFO] Validating LLM provider configuration..."
AI_PROVIDER=$(grep -E '^AI_PROVIDER=' .env | cut -d'=' -f2 | tr -d '"' || echo "")
if [ -z "$AI_PROVIDER" ]; then
  echo "[ERROR] AI_PROVIDER not configured in .env"
  echo "[ERROR] CrewAI requires valid LLM provider (openai, anthropic, ollama)"
  exit 1
fi

# Validate Weaviate configuration  
WEAVIATE_URL=$(grep -E '^WEAVIATE_URL=' .env | cut -d'=' -f2 | tr -d '"' || echo "")
if [ -z "$WEAVIATE_URL" ]; then
  echo "[ERROR] WEAVIATE_URL not configured in .env"
  echo "[ERROR] CrewAI agents require Weaviate for semantic enrichment"
  exit 1
fi

# Check for required intermediate data
OUTPUT_DIR=$(grep -E '^OUTPUT_DIR=' .env | cut -d'=' -f2 | tr -d '"' || echo "output")
if [ ! -f "$OUTPUT_DIR/intermediate_step2.json" ] && [ ! -f "$OUTPUT_DIR/consolidated_metadata.json" ]; then
  echo "[ERROR] No intermediate data found"
  echo "[ERROR] Expected: $OUTPUT_DIR/intermediate_step2.json or $OUTPUT_DIR/consolidated_metadata.json"
  echo "[ERROR] Run step 2 (analyze) first to generate required metadata"
  exit 1
fi

# Test Weaviate connectivity
echo "[INFO] Testing Weaviate connectivity..."
python -c "
import os
import sys
sys.path.append('src')
try:
    from weaviate_client import WeaviateClient
    from env_loader import load_config
    config = load_config()
    client = WeaviateClient(config)
    stats = client.get_all_collection_stats()
    print(f'[INFO] Weaviate connected: {stats.get(\"total_count\", 0)} objects available')
    client.close()
except Exception as e:
    print(f'[ERROR] Weaviate connectivity test failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
  echo "[ERROR] Weaviate connectivity test failed"
  echo "[ERROR] Ensure Weaviate is running and accessible at $WEAVIATE_URL"
  exit 1
fi

# Build command
CMD="python -m src.cli"
if [ -n "$VERBOSE" ]; then
  CMD="$CMD $VERBOSE"
fi

CMD="$CMD step3-crewai"

echo ""
echo "🚀 Starting CrewAI Agent-Based Analysis..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 Agent Configuration:"
echo "   ├── Backend Architecture Analyst"
echo "   ├── Frontend Architecture Analyst" 
echo "   ├── Semantic Enrichment Specialist"
echo "   └── Integration Architecture Specialist"
echo ""
echo "🔧 Execution Command: $CMD"
echo "🔍 Analysis Type: Multi-Agent Collaborative Processing"
echo "🌐 LLM Provider: $AI_PROVIDER"
echo "🗄️  Vector Database: $WEAVIATE_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Execute step3-crewai processing
eval $CMD

echo ""
echo "🎉 Step 3-CrewAI completed successfully!"
echo ""
echo "📊 Output Structure Created:"
echo "   📁 $OUTPUT_DIR/requirements/crewai/"
echo "   ├── 📄 _crewai_summary.md              # Multi-project agent analysis"
echo "   └── 📁 projects/"
echo "       └── 📁 {project_name}/"
echo "           ├── 📄 requirements.md         # Agent-synthesized requirements"
echo "           ├── 📊 backend_analysis.json   # Backend agent findings"
echo "           ├── 🎯 frontend_analysis.json  # Frontend agent findings" 
echo "           ├── 🔍 enrichment_data.json    # Weaviate semantic data"
echo "           ├── 🤖 agent_execution_log.json # Agent collaboration log"
echo "           └── 📋 summary.md              # Project analysis summary"
echo ""
echo "🔬 Agent-Based Analysis Features:"
echo "   ✅ Autonomous decision-making agents"
echo "   ✅ Dynamic Weaviate semantic enrichment" 
echo "   ✅ Cross-agent collaboration and memory"
echo "   ✅ Intelligent source code revisiting"
echo "   ✅ Hierarchical task processing"
echo "   ✅ Backend/Frontend specialized analysis"
echo "   ✅ Integration synthesis across layers"
echo "   ✅ Full agent interaction traceability"
echo ""
echo "📈 Analysis Insights:"
echo "   🔍 Review _crewai_summary.md for agent collaboration insights"
echo "   📊 Compare with step3-pgm results for comprehensive understanding"
echo "   🤖 Examine agent_execution_log.json for interaction patterns"
echo "   🎯 Use backend/frontend analysis for specialized requirements"
echo ""
echo "🔄 Next Steps:"
echo "   1. Review multi-agent analysis summary"
echo "   2. Compare agent-based vs programmatic results" 
echo "   3. Validate agent classifications and enrichment"
echo "   4. Use collaboration insights for process improvement"