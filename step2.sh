#!/bin/bash
# ==============================================================================
# Step 2: PRD Generation from Indexed Codebase
# ==============================================================================
# Usage: ./step2.sh [project-name] [source-dir] [output-dir]
#
# Project name determination (in priority order):
#   1. If provided as first argument, use it
#   2. If source-dir contains pom.xml, use directory name
#   3. Otherwise use timestamp: YYYY_MMM_DD_HHMM
#
# Source directory determination:
#   1. If provided as second argument, use it
#   2. Otherwise use JAVA_SOURCE_DIR from .env
#
# Examples:
#   ./step2.sh myapp                    # Uses JAVA_SOURCE_DIR from .env
#   ./step2.sh myapp /path/to/source    # Explicit source dir
#   ./step2.sh                          # Auto-detect project name from source dir
#
# Prerequisites:
#   - Run ./step1.sh first (setup virtual environment)
#   - Run ./run.sh [project-name] first (index the codebase)
#   - Ollama and Weaviate services must be running

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }
section() { echo -e "${CYAN}[SECTION]${NC} $1"; }

# ==============================================================================
# Environment Setup
# ==============================================================================

# Check if virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found. Run ./step1.sh first."
    exit 1
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Load .env for JAVA_SOURCE_DIR
if [ ! -f ".env" ]; then
    warn ".env file not found. JAVA_SOURCE_DIR must be provided as argument."
else
    # Load .env
    export $(grep -v '^#' .env | xargs)
fi

# ==============================================================================
# Parse Arguments and Determine Project Name
# ==============================================================================

# Get source directory (argument or from .env)
if [ -n "$2" ]; then
    SOURCE_DIR="$2"
elif [ -n "$JAVA_SOURCE_DIR" ]; then
    SOURCE_DIR="$JAVA_SOURCE_DIR"
else
    err "Source directory not specified!"
    echo "Either provide it as second argument or set JAVA_SOURCE_DIR in .env"
    echo "Usage: ./step2.sh [project-name] [source-dir] [output-dir]"
    exit 1
fi

# Verify source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Determine project name
if [ -n "$1" ]; then
    # Project name provided as argument
    PROJECT_NAME="$1"
    info "Using provided project name: $PROJECT_NAME"
else
    # Auto-detect project name
    info "No project name provided, auto-detecting..."

    # Check if source directory contains pom.xml
    if [ -f "$SOURCE_DIR/pom.xml" ]; then
        # Use directory name as project name
        PROJECT_NAME=$(basename "$SOURCE_DIR")
        ok "Found pom.xml, using directory name: $PROJECT_NAME"
    else
        # Use timestamp as project name
        PROJECT_NAME=$(date +"%Y_%b_%d_%H%M" | tr '[:upper:]' '[:lower:]')
        warn "No pom.xml found, using timestamp: $PROJECT_NAME"
    fi
fi

# Determine output directory
OUTPUT_DIR="${3:-./output/${PROJECT_NAME}-prd}"

# ==============================================================================
# Summary of Configuration
# ==============================================================================

echo ""
echo "=============================================="
echo "PRD Generation Pipeline (Step 2)"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "Output:     $OUTPUT_DIR"
echo "=============================================="
echo ""

# ==============================================================================
# Service Health Check
# ==============================================================================

section "Checking service health..."

# Check Ollama
info "Checking Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is running"
else
    err "Ollama is not running!"
    echo "Start Ollama with: ollama serve"
    exit 1
fi

# Check Weaviate
info "Checking Weaviate service..."
if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate is running"
else
    err "Weaviate is not running!"
    echo "Start Weaviate with: ./docker-weaviate.sh start"
    exit 1
fi

# Check if project is indexed
info "Checking if project is indexed..."
STATUS_OUTPUT=$(codeindex status --project "$PROJECT_NAME" 2>&1 || echo "ERROR")
if echo "$STATUS_OUTPUT" | grep -q "Artifacts: 0" || echo "$STATUS_OUTPUT" | grep -q "ERROR"; then
    err "Project '$PROJECT_NAME' has no indexed artifacts!"
    echo ""
    echo "Run the indexing pipeline first:"
    echo "  ./run.sh $PROJECT_NAME \"$SOURCE_DIR\""
    echo ""
    exit 1
fi

ok "Project is indexed and ready"
echo ""

# ==============================================================================
# PRD Generation
# ==============================================================================

section "Generating PRD Documentation..."
echo ""

# Database Layer
info "Analyzing database layer..."
echo "Command: codeindex prd database --project \"$PROJECT_NAME\" --source-dir \"$SOURCE_DIR\" --output-dir \"$OUTPUT_DIR\" --quiet"
codeindex prd database --project "$PROJECT_NAME" --source-dir "$SOURCE_DIR" --output-dir "$OUTPUT_DIR" --quiet
ok "Database PRD generated"
echo ""

# Service Layer
info "Analyzing service layer..."
echo "Command: codeindex prd services --project \"$PROJECT_NAME\" --source-dir \"$SOURCE_DIR\" --output-dir \"$OUTPUT_DIR\" --quiet"
codeindex prd services --project "$PROJECT_NAME" --source-dir "$SOURCE_DIR" --output-dir "$OUTPUT_DIR" --quiet
ok "Service PRD generated"
echo ""

# Frontend Layer
info "Analyzing frontend layer..."
echo "Command: codeindex prd frontend --project \"$PROJECT_NAME\" --source-dir \"$SOURCE_DIR\" --output-dir \"$OUTPUT_DIR\" --quiet"
codeindex prd frontend --project "$PROJECT_NAME" --source-dir "$SOURCE_DIR" --output-dir "$OUTPUT_DIR" --quiet
ok "Frontend PRD generated"
echo ""

# Master PRD (Full with all layers)
info "Generating master PRD (synthesizing all layers)..."
echo "Command: codeindex prd full --project \"$PROJECT_NAME\" --source-dir \"$SOURCE_DIR\" --output-dir \"$OUTPUT_DIR\" --quiet"
codeindex prd full --project "$PROJECT_NAME" --source-dir "$SOURCE_DIR" --output-dir "$OUTPUT_DIR" --quiet
ok "Master PRD generated"
echo ""

# ==============================================================================
# Verify Output
# ==============================================================================

section "Verifying generated documentation..."
echo ""

# Check if files were created
PRD_DIR="$OUTPUT_DIR/prd"
MASTER_PRD="$OUTPUT_DIR/master_prd.md"

if [ -f "$PRD_DIR/database_prd.md" ]; then
    SIZE=$(ls -lh "$PRD_DIR/database_prd.md" | awk '{print $5}')
    ok "Database PRD: $PRD_DIR/database_prd.md ($SIZE)"
else
    warn "Database PRD not generated"
fi

if [ -f "$PRD_DIR/service_prd.md" ]; then
    SIZE=$(ls -lh "$PRD_DIR/service_prd.md" | awk '{print $5}')
    ok "Service PRD: $PRD_DIR/service_prd.md ($SIZE)"
else
    warn "Service PRD not generated"
fi

if [ -f "$PRD_DIR/frontend_prd.md" ]; then
    SIZE=$(ls -lh "$PRD_DIR/frontend_prd.md" | awk '{print $5}')
    ok "Frontend PRD: $PRD_DIR/frontend_prd.md ($SIZE)"
else
    warn "Frontend PRD not generated"
fi

if [ -f "$MASTER_PRD" ]; then
    SIZE=$(ls -lh "$MASTER_PRD" | awk '{print $5}')
    ok "Master PRD: $MASTER_PRD ($SIZE)"
else
    err "Master PRD not generated!"
fi

echo ""

# ==============================================================================
# Summary and Statistics
# ==============================================================================

section "PRD Generation Summary"
echo ""

# Count entities, services, forms
DB_ENTITIES=$(find "$OUTPUT_DIR/database/entities" -name "*.json" 2>/dev/null | wc -l || echo 0)
SERVICES=$(find "$OUTPUT_DIR/services/definitions" -name "*.json" 2>/dev/null | wc -l || echo 0)
ENDPOINTS=$(find "$OUTPUT_DIR/services/endpoints" -name "*.json" 2>/dev/null | wc -l || echo 0)
FORMS=$(find "$OUTPUT_DIR/frontend/forms" -name "*.json" 2>/dev/null | wc -l || echo 0)
COMPONENTS=$(find "$OUTPUT_DIR/frontend/components" -name "*.json" 2>/dev/null | wc -l || echo 0)

echo "Documented Artifacts:"
echo "  Database Entities: $DB_ENTITIES"
echo "  Services:          $SERVICES"
echo "  API Endpoints:     $ENDPOINTS"
echo "  Forms:             $FORMS"
echo "  UI Components:     $COMPONENTS"
echo ""

# ==============================================================================
# Next Steps
# ==============================================================================

echo "=============================================="
ok "PRD Generation Complete!"
echo "=============================================="
echo ""
echo "Generated Documentation:"
echo "  Master PRD:    $MASTER_PRD"
echo "  Database PRD:  $PRD_DIR/database_prd.md"
echo "  Service PRD:   $PRD_DIR/service_prd.md"
echo "  Frontend PRD:  $PRD_DIR/frontend_prd.md"
echo ""
echo "Output Directory: $OUTPUT_DIR"
echo "  ├── master_prd.md           # Comprehensive master document"
echo "  ├── prd/                    # Layer-specific PRDs"
echo "  ├── database/               # Entity definitions"
echo "  ├── services/               # Service definitions"
echo "  ├── frontend/               # Form and component definitions"
echo "  └── business_rules/         # Business rules catalog"
echo ""
echo "Next steps:"
echo "  1. Review the generated documentation:"
echo "     open $MASTER_PRD"
echo "     # or"
echo "     cat $MASTER_PRD"
echo ""
echo "  2. Use with GitHub Spec Kit:"
echo "     cp $MASTER_PRD specs/myfeature/prd.md"
echo "     /speckit.specify"
echo ""
echo "  3. Search your codebase:"
echo "     codeindex search \"your query\" --project $PROJECT_NAME"
echo ""
echo "=============================================="
