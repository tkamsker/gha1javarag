#!/bin/bash
################################################################################
# Batch Index and PRD Generation Script
################################################################################
# Automates indexing and PRD generation for multiple Java projects
#
# Usage: ./batch-index-and-prd.sh [--skip-index] [--skip-prd]
#
# Options:
#   --skip-index    Skip indexing phase (use existing Weaviate data)
#   --skip-prd      Skip PRD generation phase
#
# Example: ./batch-index-and-prd.sh
#          ./batch-index-and-prd.sh --skip-index  # Only generate PRDs
################################################################################

set -e

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

################################################################################
# Configuration
################################################################################

# Define projects: name => path
# CUSTOMIZE THIS for your projects
declare -A PROJECTS=(
    ["project-a"]="/path/to/project-a"
    ["project-b"]="/path/to/project-b"
    ["project-c"]="/path/to/project-c"
)

# Alternatively, load from a config file
# Format: name|path (one per line)
# Example config.txt:
#   project-a|/path/to/project-a
#   project-b|/path/to/project-b
CONFIG_FILE="batch-config.txt"
if [ -f "$CONFIG_FILE" ]; then
    info "Loading projects from $CONFIG_FILE"
    while IFS='|' read -r name path; do
        # Skip comments and empty lines
        [[ "$name" =~ ^#.*$ ]] && continue
        [[ -z "$name" ]] && continue
        PROJECTS["$name"]="$path"
    done < "$CONFIG_FILE"
fi

################################################################################
# Parse Arguments
################################################################################

SKIP_INDEX=false
SKIP_PRD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-index)
            SKIP_INDEX=true
            shift
            ;;
        --skip-prd)
            SKIP_PRD=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-index    Skip indexing phase (use existing data)"
            echo "  --skip-prd      Skip PRD generation phase"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            err "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

################################################################################
# Validation
################################################################################

# Check if projects defined
if [ ${#PROJECTS[@]} -eq 0 ]; then
    err "No projects defined!"
    echo ""
    echo "Edit this script and define projects in the PROJECTS array:"
    echo "  declare -A PROJECTS=("
    echo "      [\"project-name\"]=\"/path/to/project\""
    echo "  )"
    echo ""
    echo "Or create a config file: batch-config.txt"
    echo "  Format: name|path (one per line)"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    err "Virtual environment not found!"
    echo "Please run: ./step1.sh"
    exit 1
fi

# Check if services are running
if [ "$SKIP_INDEX" = false ]; then
    info "Checking services..."

    if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
        err "Weaviate is not running!"
        echo "Please start: ./docker-weaviate.sh start"
        exit 1
    fi

    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        err "Ollama is not running!"
        echo "Please start: ollama serve"
        exit 1
    fi

    ok "Services running"
fi

################################################################################
# Summary
################################################################################

echo ""
echo "=============================================="
echo "Batch Index and PRD Generation"
echo "=============================================="
echo "Projects: ${#PROJECTS[@]}"
for name in "${!PROJECTS[@]}"; do
    echo "  - $name: ${PROJECTS[$name]}"
done
echo ""
echo "Mode:"
if [ "$SKIP_INDEX" = true ]; then
    echo "  - Indexing: SKIPPED"
else
    echo "  - Indexing: ENABLED"
fi
if [ "$SKIP_PRD" = true ]; then
    echo "  - PRD Generation: SKIPPED"
else
    echo "  - PRD Generation: ENABLED"
fi
echo "=============================================="
echo ""

# Confirm before starting
read -p "Start batch processing? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    info "Aborted"
    exit 0
fi

################################################################################
# Phase 1: Index All Projects
################################################################################

if [ "$SKIP_INDEX" = false ]; then
    section "PHASE 1: Indexing Projects"
    echo ""

    INDEX_START=$(date +%s)
    INDEXED_COUNT=0
    FAILED_COUNT=0
    declare -a FAILED_PROJECTS

    for name in "${!PROJECTS[@]}"; do
        path="${PROJECTS[$name]}"

        echo ""
        echo "-------------------------------------------"
        info "Indexing: $name"
        info "Path: $path"
        echo "-------------------------------------------"

        # Verify path exists
        if [ ! -d "$path" ]; then
            warn "Directory not found: $path"
            warn "Skipping $name"
            FAILED_COUNT=$((FAILED_COUNT + 1))
            FAILED_PROJECTS+=("$name (directory not found)")
            continue
        fi

        # Run indexing pipeline
        if ./run.sh "$name" "$path"; then
            ok "Indexed: $name"
            INDEXED_COUNT=$((INDEXED_COUNT + 1))
        else
            err "Failed to index: $name"
            FAILED_COUNT=$((FAILED_COUNT + 1))
            FAILED_PROJECTS+=("$name (indexing failed)")
        fi
    done

    INDEX_END=$(date +%s)
    INDEX_DURATION=$((INDEX_END - INDEX_START))
    INDEX_MINUTES=$((INDEX_DURATION / 60))
    INDEX_SECONDS=$((INDEX_DURATION % 60))

    echo ""
    echo "=============================================="
    ok "Indexing Phase Complete!"
    echo "=============================================="
    echo "  Indexed:  $INDEXED_COUNT"
    echo "  Failed:   $FAILED_COUNT"
    echo "  Duration: ${INDEX_MINUTES}m ${INDEX_SECONDS}s"
    if [ ${#FAILED_PROJECTS[@]} -gt 0 ]; then
        echo ""
        echo "Failed projects:"
        for failed in "${FAILED_PROJECTS[@]}"; do
            echo "  - $failed"
        done
    fi
    echo "=============================================="
    echo ""
else
    info "Skipping indexing phase (--skip-index)"
    echo ""
fi

################################################################################
# Phase 2: Generate PRDs
################################################################################

if [ "$SKIP_PRD" = false ]; then
    section "PHASE 2: Generating PRDs"
    echo ""

    # Activate virtual environment
    source .venv/bin/activate

    PRD_START=$(date +%s)
    PRD_COUNT=0
    PRD_FAILED_COUNT=0
    declare -a PRD_FAILED_PROJECTS

    for name in "${!PROJECTS[@]}"; do
        path="${PROJECTS[$name]}"

        echo ""
        echo "-------------------------------------------"
        info "Generating PRD: $name"
        echo "-------------------------------------------"

        # Get project ID from status
        PROJECT_STATUS=$(codeindex status 2>&1 || echo "ERROR")

        if echo "$PROJECT_STATUS" | grep -q "ERROR"; then
            warn "Could not get status for $name"
            warn "Attempting PRD generation with name as project ID..."
            PROJECT_ID="$name"
        else
            # Try to find project ID (this is a heuristic, may need adjustment)
            PROJECT_ID=$(echo "$PROJECT_STATUS" | grep -i "$name" | head -1 | awk '{print $2}' || echo "$name")
        fi

        info "Project ID: $PROJECT_ID"

        # Generate PRD
        OUTPUT_DIR="./output/${name}-prd"

        if codeindex prd full \
            --project "$PROJECT_ID" \
            --source-dir "$path" \
            --output-dir "$OUTPUT_DIR" \
            --quiet; then
            ok "Generated PRD: $name"
            ok "Output: $OUTPUT_DIR"
            PRD_COUNT=$((PRD_COUNT + 1))
        else
            err "Failed to generate PRD: $name"
            PRD_FAILED_COUNT=$((PRD_FAILED_COUNT + 1))
            PRD_FAILED_PROJECTS+=("$name")
        fi
    done

    PRD_END=$(date +%s)
    PRD_DURATION=$((PRD_END - PRD_START))
    PRD_MINUTES=$((PRD_DURATION / 60))
    PRD_SECONDS=$((PRD_DURATION % 60))

    echo ""
    echo "=============================================="
    ok "PRD Generation Phase Complete!"
    echo "=============================================="
    echo "  Generated: $PRD_COUNT"
    echo "  Failed:    $PRD_FAILED_COUNT"
    echo "  Duration:  ${PRD_MINUTES}m ${PRD_SECONDS}s"
    if [ ${#PRD_FAILED_PROJECTS[@]} -gt 0 ]; then
        echo ""
        echo "Failed PRDs:"
        for failed in "${PRD_FAILED_PROJECTS[@]}"; do
            echo "  - $failed"
        done
    fi
    echo "=============================================="
    echo ""
else
    info "Skipping PRD generation phase (--skip-prd)"
    echo ""
fi

################################################################################
# Summary
################################################################################

TOTAL_END=$(date +%s)
TOTAL_START=${INDEX_START:-$PRD_START}
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))
TOTAL_MINUTES=$((TOTAL_DURATION / 60))
TOTAL_SECONDS=$((TOTAL_DURATION % 60))

echo ""
echo "=============================================="
ok "BATCH PROCESSING COMPLETE!"
echo "=============================================="
echo ""
echo "Total Duration: ${TOTAL_MINUTES}m ${TOTAL_SECONDS}s"
echo ""
echo "Output Directory Structure:"
echo "./output/"
for name in "${!PROJECTS[@]}"; do
    if [ -d "./output/${name}-prd" ]; then
        echo "  ├── ${name}-prd/"
        if [ -f "./output/${name}-prd/master_prd.md" ]; then
            SIZE=$(ls -lh "./output/${name}-prd/master_prd.md" | awk '{print $5}')
            echo "  │   └── master_prd.md ($SIZE)"
        fi
    fi
done
echo ""
echo "Next Steps:"
echo "  1. Review generated PRDs:"
echo "     ls -lh ./output/*/master_prd.md"
echo ""
echo "  2. Check indexing status:"
echo "     codeindex status"
echo ""
echo "  3. Search across all projects:"
echo "     codeindex search \"your query\""
echo ""
echo "=============================================="
