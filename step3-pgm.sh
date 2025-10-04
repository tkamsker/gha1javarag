#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running Step 3-PGM: Programmatic Backend/Frontend Analysis"

# Parse command line arguments
PARALLEL="--parallel"
MAX_WORKERS="3"
VERBOSE="--verbose"

while [[ $# -gt 0 ]]; do
  case $1 in
    --sequential)
      PARALLEL="--sequential"
      shift
      ;;
    --parallel)
      PARALLEL="--parallel"
      shift
      ;;
    --max-workers)
      MAX_WORKERS="$2"
      shift 2
      ;;
    --no-verbose)
      VERBOSE=""
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Step 3-PGM: Programmatic Backend/Frontend Requirements Analysis"
      echo ""
      echo "Features:"
      echo "  - Distinguishes backend (DAO/DTO/Service) and frontend components"
      echo "  - Revisits source code for detailed analysis"
      echo "  - Enriches requirements with Weaviate semantic data"
      echo "  - Generates layered documentation with traceability"
      echo ""
      echo "Options:"
      echo "  --sequential      Disable parallel processing"
      echo "  --parallel        Enable parallel processing (default)"
      echo "  --max-workers N   Set maximum number of workers (default: 3)"
      echo "  --no-verbose      Disable verbose logging"
      echo "  -h, --help        Show this help message"
      echo ""
      echo "Output Structure:"
      echo "  \$OUTPUT_DIR/requirements/pgm/"
      echo "  ├── _pgm_summary.md                    # Cross-project summary"
      echo "  └── projects/"
      echo "      └── {project_name}/"
      echo "          ├── requirements.md            # Main requirements"
      echo "          ├── backend_details.md         # Backend-specific docs"
      echo "          ├── frontend_details.md        # Frontend-specific docs"
      echo "          └── traceability.json          # Source mapping"
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
    echo "[WARNING] Source code revisiting may not work properly"
  else
    echo "[INFO] Using JAVA_SOURCE_DIR: $JAVA_SOURCE_DIR"
  fi
else
  echo "[WARNING] JAVA_SOURCE_DIR not configured"
  echo "[WARNING] Source code revisiting will use relative paths only"
  echo "[WARNING] Consider adding JAVA_SOURCE_DIR=/path/to/your/java/projects to .env"
fi

# Check for required intermediate data
OUTPUT_DIR=$(grep -E '^OUTPUT_DIR=' .env | cut -d'=' -f2 | tr -d '"' || echo "output")
if [ ! -f "$OUTPUT_DIR/intermediate_step2.json" ] && [ ! -f "$OUTPUT_DIR/consolidated_metadata.json" ]; then
  echo "[ERROR] No intermediate data found"
  echo "[ERROR] Expected: $OUTPUT_DIR/intermediate_step2.json or $OUTPUT_DIR/consolidated_metadata.json"
  echo "[ERROR] Run step 2 (analyze) first to generate required metadata"
  exit 1
fi

# Build command
CMD="python -m src.cli"
if [ -n "$VERBOSE" ]; then
  CMD="$CMD $VERBOSE"
fi

CMD="$CMD step3-pgm $PARALLEL --max-workers $MAX_WORKERS"

echo "[INFO] Executing: $CMD"
echo "[INFO] Processing mode: $([ "$PARALLEL" = "--parallel" ] && echo "Parallel ($MAX_WORKERS workers)" || echo "Sequential")"
echo "[INFO] Analysis type: Backend/Frontend Component Analysis with Weaviate Enrichment"

# Execute step3-pgm processing
eval $CMD

echo ""
echo "[SUCCESS] Step 3-PGM completed successfully!"
echo ""
echo "📊 Output Structure:"
echo "   📁 $OUTPUT_DIR/requirements/pgm/"
echo "   ├── 📄 _pgm_summary.md                 # Cross-project analysis summary"
echo "   └── 📁 projects/"
echo "       └── 📁 {project_name}/"
echo "           ├── 📄 requirements.md         # Enhanced layered requirements"
echo "           ├── 📄 backend_details.md      # DAO/DTO/Service documentation"
echo "           ├── 📄 frontend_details.md     # UI/Workflow documentation"
echo "           └── 📄 traceability.json       # Source code traceability"
echo ""
echo "🔍 Key Features Delivered:"
echo "   ✅ Backend/Frontend component separation"
echo "   ✅ Source code revisiting and analysis"
echo "   ✅ Weaviate semantic data enrichment"
echo "   ✅ Component relationship mapping"
echo "   ✅ API endpoint documentation"
echo "   ✅ Data flow analysis"
echo "   ✅ Business process identification"
echo "   ✅ Full traceability reporting"
echo ""
echo "📝 Next Steps:"
echo "   1. Review _pgm_summary.md for cross-project insights"
echo "   2. Examine individual project requirements for detailed analysis"
echo "   3. Validate component classifications and relationships"
echo "   4. Use traceability.json for source code mapping"