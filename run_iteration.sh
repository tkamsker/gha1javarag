#!/bin/bash

# Java Codebase Analysis Tool - Iteration Runner
# This script runs a complete iteration and saves output with timestamp

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Function to check if .env file exists
check_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warning "Please edit .env file with your configuration before running again"
            exit 1
        else
            print_error ".env.example file not found. Cannot create .env file"
            exit 1
        fi
    fi
}

# Function to check source directory and Java files
check_source_directory() {
    print_status "Checking source directory..."
    
    # Get source directory from .env
    JAVA_SOURCE_DIR=$(grep "^JAVA_SOURCE_DIR=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$JAVA_SOURCE_DIR" ]; then
        print_error "JAVA_SOURCE_DIR not configured in .env file"
        print_error "Please set JAVA_SOURCE_DIR in your .env file"
        exit 1
    fi
    
    # Check if source directory exists
    if [ ! -d "$JAVA_SOURCE_DIR" ]; then
        print_error "Source directory does not exist: $JAVA_SOURCE_DIR"
        print_error "Please check the JAVA_SOURCE_DIR path in your .env file"
        exit 1
    fi
    
    print_success "Source directory exists: $JAVA_SOURCE_DIR"
    
    # Check if directory contains Java files
    print_status "Checking for Java files in source directory..."
    JAVA_FILE_COUNT=$(find "$JAVA_SOURCE_DIR" -name "*.java" -type f 2>/dev/null | wc -l)
    JSP_FILE_COUNT=$(find "$JAVA_SOURCE_DIR" -name "*.jsp" -type f 2>/dev/null | wc -l)
    XML_FILE_COUNT=$(find "$JAVA_SOURCE_DIR" -name "*.xml" -type f 2>/dev/null | wc -l)
    
    TOTAL_FILES=$((JAVA_FILE_COUNT + JSP_FILE_COUNT + XML_FILE_COUNT))
    
    if [ $TOTAL_FILES -eq 0 ]; then
        print_warning "No Java/JSP/XML files found in source directory"
        print_warning "This may indicate an incorrect path or empty directory"
        print_status "Found files:"
        echo "  Java files: $JAVA_FILE_COUNT"
        echo "  JSP files: $JSP_FILE_COUNT"
        echo "  XML files: $XML_FILE_COUNT"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Found $TOTAL_FILES relevant files:"
        echo "  Java files: $JAVA_FILE_COUNT"
        echo "  JSP files: $JSP_FILE_COUNT"
        echo "  XML files: $XML_FILE_COUNT"
    fi
}

# Function to check LLM services based on configuration
check_llm_services() {
    print_status "Checking LLM services..."
    
    # Get AI provider from .env
    AI_PROVIDER=$(grep "^AI_PROVIDER=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$AI_PROVIDER" ]; then
        AI_PROVIDER="ollama"
    fi
    
    print_status "Configured AI Provider: $AI_PROVIDER"
    
    case "$AI_PROVIDER" in
        "openai")
            check_openai
            ;;
        "ollama")
            check_ollama
            ;;
        "anthropic")
            check_anthropic
            ;;
        *)
            print_error "Unknown AI provider: $AI_PROVIDER"
            print_error "Supported providers: openai, ollama, anthropic"
            exit 1
            ;;
    esac
}

# Function to check OpenAI configuration
check_openai() {
    print_status "Checking OpenAI configuration..."
    
    # Check API key
    OPENAI_API_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-your-openai-api-key-here" ]; then
        print_error "OpenAI API key not configured in .env file"
        print_error "Please set OPENAI_API_KEY in your .env file"
        exit 1
    fi
    
    # Check API base URL
    OPENAI_API_BASE=$(grep "^OPENAI_API_BASE=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$OPENAI_API_BASE" ]; then
        OPENAI_API_BASE="https://api.openai.com/v1"
    fi
    
    # Test OpenAI API connection
    print_status "Testing OpenAI API connection..."
    if curl -s --connect-timeout 10 \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        "$OPENAI_API_BASE/models" >/dev/null 2>&1; then
        print_success "OpenAI API is accessible"
    else
        print_error "Cannot connect to OpenAI API at $OPENAI_API_BASE"
        print_error "Please check your API key and network connection"
        exit 1
    fi
}

# Function to check Ollama configuration
check_ollama() {
    print_status "Checking Ollama configuration..."
    
    # Get Ollama base URL
    OLLAMA_BASE_URL=$(grep "^OLLAMA_BASE_URL=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$OLLAMA_BASE_URL" ]; then
        OLLAMA_BASE_URL="http://localhost:11434"
    fi
    
    # Check if Ollama is running
    if curl -s --connect-timeout 10 "$OLLAMA_BASE_URL/api/tags" >/dev/null 2>&1; then
        print_success "Ollama is running at $OLLAMA_BASE_URL"
        
        # Check if the configured model is available
        OLLAMA_MODEL=$(grep "^OLLAMA_MODEL_NAME=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ -n "$OLLAMA_MODEL" ]; then
            print_status "Checking if model '$OLLAMA_MODEL' is available..."
            MODELS_RESPONSE=$(curl -s --connect-timeout 10 "$OLLAMA_BASE_URL/api/tags" 2>/dev/null)
            if echo "$MODELS_RESPONSE" | grep -q "\"name\":\"$OLLAMA_MODEL\""; then
                print_success "Model '$OLLAMA_MODEL' is available"
            else
                print_warning "Model '$OLLAMA_MODEL' not found in Ollama"
                print_status "Available models:"
                echo "$MODELS_RESPONSE" | grep -o '"name":"[^"]*"' | sed 's/"name":"//g' | sed 's/"//g' | head -10
                print_status "You may need to pull the model: ollama pull $OLLAMA_MODEL"
            fi
        fi
        
        # Check embedding model if using client-side embeddings
        EMBEDDING_PROVIDER=$(grep "^EMBEDDING_PROVIDER=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ "$EMBEDDING_PROVIDER" = "client" ]; then
            LOCAL_EMBED_URL=$(grep "^LOCAL_EMBED_URL=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
            if [ -n "$LOCAL_EMBED_URL" ]; then
                print_status "Checking embedding service at $LOCAL_EMBED_URL..."
                if curl -s --connect-timeout 10 "$LOCAL_EMBED_URL" >/dev/null 2>&1; then
                    print_success "Embedding service is accessible"
                else
                    print_warning "Embedding service not accessible at $LOCAL_EMBED_URL"
                    print_status "You may need to start an embedding service"
                fi
            fi
        fi
    else
        print_error "Ollama is not running at $OLLAMA_BASE_URL"
        print_error "Please start Ollama first:"
        echo "  1. Install Ollama: https://ollama.ai"
        echo "  2. Start Ollama service"
        echo "  3. Pull your model: ollama pull $OLLAMA_MODEL"
        exit 1
    fi
}

# Function to check Anthropic configuration
check_anthropic() {
    print_status "Checking Anthropic configuration..."
    
    # Check API key
    ANTHROPIC_API_KEY=$(grep "^ANTHROPIC_API_KEY=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-your-anthropic-api-key-here" ]; then
        print_error "Anthropic API key not configured in .env file"
        print_error "Please set ANTHROPIC_API_KEY in your .env file"
        exit 1
    fi
    
    # Check API base URL
    ANTHROPIC_API_BASE=$(grep "^ANTHROPIC_API_BASE=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$ANTHROPIC_API_BASE" ]; then
        ANTHROPIC_API_BASE="https://api.anthropic.com"
    fi
    
    # Test Anthropic API connection (simplified check)
    print_status "Testing Anthropic API configuration..."
    if [ ${#ANTHROPIC_API_KEY} -gt 20 ]; then
        print_success "Anthropic API key appears to be configured"
        print_status "Note: Full API connectivity test requires a valid request"
    else
        print_error "Anthropic API key appears to be invalid or placeholder"
        exit 1
    fi
}

# Function to check if Weaviate is running
check_weaviate() {
    print_status "Checking Weaviate connection..."
    
    # Try to get Weaviate URL from .env file
    WEAVIATE_URL=$(grep "^WEAVIATE_URL=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$WEAVIATE_URL" ]; then
        WEAVIATE_URL="http://localhost:8080"
    fi
    
    # Check if Weaviate is responding
    if curl -s --connect-timeout 10 "$WEAVIATE_URL/v1/meta" >/dev/null 2>&1; then
        print_success "Weaviate is running at $WEAVIATE_URL"
        
        # Check if Weaviate has the required modules
        print_status "Checking Weaviate modules..."
        MODULES_RESPONSE=$(curl -s --connect-timeout 10 "$WEAVIATE_URL/v1/modules" 2>/dev/null)
        if echo "$MODULES_RESPONSE" | grep -q "text2vec-ollama\|text2vec-openai\|text2vec-transformers"; then
            print_success "Weaviate has required vectorization modules"
        else
            print_warning "Weaviate may not have required vectorization modules"
            print_status "Consider using: docker run -p 8080:8080 -p 50051:50051 \\"
            echo "    -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \\"
            echo "    -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \\"
            echo "    -e ENABLE_MODULES='text2vec-ollama,generative-ollama' \\"
            echo "    -e CLUSTER_HOSTNAME='node1' \\"
            echo "    semitechnologies/weaviate:latest"
        fi
    else
        print_error "Weaviate is not responding at $WEAVIATE_URL"
        print_error "Please start Weaviate first:"
        echo ""
        echo "Docker command:"
        echo "  docker run -p 8080:8080 -p 50051:50051 \\"
        echo "    -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \\"
        echo "    -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \\"
        echo "    -e ENABLE_MODULES='text2vec-ollama,generative-ollama' \\"
        echo "    -e CLUSTER_HOSTNAME='node1' \\"
        echo "    semitechnologies/weaviate:latest"
        echo ""
        print_error "Cannot continue without Weaviate. Exiting."
        exit 1
    fi
}

# Function to create timestamped output directory
create_output_dir() {
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_DIR="output_${TIMESTAMP}"
    print_status "Creating output directory: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
    
    # Update .env file to use timestamped output directory
    if [ -f ".env" ]; then
        # Create a temporary .env file with updated OUTPUT_DIR
        sed "s|^OUTPUT_DIR=.*|OUTPUT_DIR=./$OUTPUT_DIR|" .env > .env.tmp
        mv .env.tmp .env
        print_success "Updated .env with output directory: $OUTPUT_DIR"
    fi
}

# Function to run the indexing process
run_indexing() {
    print_status "Starting indexing process (Step 1)..."
    print_status "This may take several minutes depending on your codebase size..."
    
    # Run indexing with progress indication
    if python -m src.cli --verbose index; then
        print_success "Indexing completed successfully"
    else
        print_error "Indexing failed"
        return 1
    fi
}

# Function to run requirements generation
run_requirements() {
    print_status "Starting requirements generation (Step 2)..."
    
    if python -m src.cli --verbose requirements; then
        print_success "Requirements generation completed successfully"
    else
        print_error "Requirements generation failed"
        return 1
    fi
}

# Function to show statistics
show_statistics() {
    print_status "Gathering statistics..."
    
    if python -m src.cli --verbose stats; then
        print_success "Statistics retrieved"
    else
        print_warning "Could not retrieve statistics"
    fi
}

# Function to create iteration summary
create_summary() {
    SUMMARY_FILE="$OUTPUT_DIR/iteration_summary.txt"
    
    print_status "Creating iteration summary..."
    
    cat > "$SUMMARY_FILE" << EOF
Java Codebase Analysis Tool - Iteration Summary
==============================================

Iteration Timestamp: $(date)
Output Directory: $OUTPUT_DIR
Source Directory: $(grep "^JAVA_SOURCE_DIR=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")

Process Steps Completed:
- [x] Environment setup and validation
- [x] Project discovery and file indexing
- [x] Requirements documentation generation
- [x] Statistics collection

Output Structure:
$OUTPUT_DIR/
├── projects/              # Per-project summaries
├── requirements/          # Generated requirements
├── logs/                  # Processing logs
├── catalog.index.json     # Global catalog
├── processing_report.json # Final processing report
└── iteration_summary.txt  # This file

Next Steps:
1. Review the generated requirements in $OUTPUT_DIR/requirements/
2. Check processing logs in $OUTPUT_DIR/logs/
3. Use 'python -m src.cli query' to search the indexed data
4. Use 'python -m src.cli stats' to view statistics

EOF

    print_success "Iteration summary created: $SUMMARY_FILE"
}

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    # Deactivate virtual environment if it was activated
    if [ -n "$VIRTUAL_ENV" ] && [ "$(type -t deactivate)" = "function" ]; then
        deactivate
    fi
}

# Set trap for cleanup on exit
trap cleanup EXIT

# Main execution
main() {
    echo "=========================================="
    echo "Java Codebase Analysis Tool - Iteration Runner"
    echo "=========================================="
    echo ""
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command_exists pip; then
        print_error "pip is required but not installed"
        exit 1
    fi
    
    if ! command_exists curl; then
        print_warning "curl not found - cannot check Weaviate connection"
    fi
    
    if ! command_exists docker; then
        print_warning "docker not found - you may need to install Docker to run Weaviate"
    fi
    
    print_success "Prerequisites check completed"
    echo ""
    
    # Parse arguments
    STEP3_MODE="both" # pgm|crewai|both
    OUTPUT_DIR_OVERRIDE=""
    ROTATE_OUTPUT="0"
    FORCE_STEP1="0"
    NO_STEP1="0"
    REPEAT_STEP2="0"
    STEP3_PARALLEL="--parallel"
    STEP3_MAX_WORKERS="3"
    STEP3_INCREMENTAL=""
    STEP3_FORCE=""
    CREWAI_VERBOSE_FLAG=""
    PGM_CLASSIFICATION_FLAG="--enhanced"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --output-dir)
                OUTPUT_DIR_OVERRIDE="$2"; shift 2;;
            --rotate-output)
                ROTATE_OUTPUT="1"; shift;;
            --force-step1)
                FORCE_STEP1="1"; shift;;
            --no-step1)
                NO_STEP1="1"; shift;;
            --repeat-step2)
                REPEAT_STEP2="1"; shift;;
            --step3=*)
                STEP3_MODE="${1#*=}"; shift;;
            --step3-parallel)
                STEP3_PARALLEL="--parallel"; shift;;
            --step3-sequential)
                STEP3_PARALLEL="--sequential"; shift;;
            --step3-max-workers)
                STEP3_MAX_WORKERS="$2"; shift 2;;
            --step3-incremental)
                STEP3_INCREMENTAL="--incremental"; shift;;
            --step3-force)
                STEP3_FORCE="--force"; shift;;
            --crewai-no-verbose)
                CREWAI_VERBOSE_FLAG="--no-verbose"; shift;;
            --pgm-pattern-based)
                PGM_CLASSIFICATION_FLAG="--pattern-based"; shift;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"; echo "";
                echo "  --output-dir PATH         Use PATH as OUTPUT_DIR for this run (no .env change)";
                echo "  --rotate-output           Use timestamped OUTPUT_DIR for this run only";
                echo "  --force-step1             Force re-run Step 1";
                echo "  --no-step1                Skip Step 1";
                echo "  --repeat-step2            Re-run Step 2 requirements";
                echo "  --step3=pgm|crewai|both   Choose Step 3 mode (default both)";
                echo "  --step3-parallel          Run Step 3 in parallel (default)";
                echo "  --step3-sequential        Run Step 3 sequentially";
                echo "  --step3-max-workers N     Max workers for Step 3 (default 3)";
                echo "  --step3-incremental       Incremental Step 3 (refactored)";
                echo "  --step3-force             Force regenerate with --step3-incremental";
                echo "  --crewai-no-verbose       Disable verbose in CrewAI script";
                echo "  --pgm-pattern-based       Use pattern-based classification in PGM";
                exit 0;;
            *) echo "Unknown option: $1"; exit 1;;
        esac
    done

    # Setup environment
    print_status "Setting up environment..."
    check_venv
    activate_venv
    install_dependencies
    check_env
    check_source_directory
    check_weaviate
    check_llm_services
    # Determine OUTPUT_DIR
    CURRENT_OUTPUT_DIR=$(grep "^OUTPUT_DIR=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -n "$OUTPUT_DIR_OVERRIDE" ]; then
        OUTPUT_DIR="$OUTPUT_DIR_OVERRIDE"
    elif [ "$ROTATE_OUTPUT" = "1" ]; then
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        OUTPUT_DIR="./output_${TIMESTAMP}"
    else
        if [ -n "$CURRENT_OUTPUT_DIR" ]; then
            OUTPUT_DIR="$CURRENT_OUTPUT_DIR"
        else
            TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
            OUTPUT_DIR="./output_${TIMESTAMP}"
            echo "OUTPUT_DIR=$OUTPUT_DIR" >> .env
        fi
    fi
    print_status "Using output directory: $OUTPUT_DIR"
    export OUTPUT_DIR  # ensure child scripts and Python see this OUTPUT_DIR
    mkdir -p "$OUTPUT_DIR"
    print_success "Environment setup completed"
    echo ""
    
    # Helper: write comparison index
    write_comparison_index() {
        local comp_dir="$OUTPUT_DIR/requirements/_comparison"
        mkdir -p "$comp_dir"
        local f="$comp_dir/index.md"
        echo "# Step 3 Comparison" > "$f"
        echo "\nOutput: $OUTPUT_DIR" >> "$f"
        if [ -d "$OUTPUT_DIR/requirements/pgm" ]; then
            echo "\n- PGM: requirements/pgm/" >> "$f"
        fi
        if [ -d "$OUTPUT_DIR/requirements/crewai" ]; then
            echo "\n- CrewAI: requirements/crewai/" >> "$f"
        fi
        print_success "Created comparison index: $f"
    }

    # Step1 artifact detection
    STEP1_MARKER="$OUTPUT_DIR/.step1_complete"

    # Run the iteration
    print_status "Starting complete iteration with CrewAI analysis..."
    echo ""
    
    # If step scripts exist, prefer three-step flow, else legacy functions
    if [ -x "./step1.sh" ] && [ -x "./step2.sh" ] && [ -x "./step3-crewai.sh" ]; then
        print_status "Running enhanced three-step workflow with CrewAI..."
        echo ""
        
        # Step 1: Index and Discovery (guarded)
        SHOULD_RUN_STEP1=1
        if [ -f "$STEP1_MARKER" ] && [ "$FORCE_STEP1" != "1" ] && [ "$NO_STEP1" != "1" ]; then
            print_status "Step 1 marker found; skipping Step 1 (use --force-step1 to re-run)"
            SHOULD_RUN_STEP1=0
        fi
        if [ "$NO_STEP1" = "1" ]; then SHOULD_RUN_STEP1=0; fi
        if [ $SHOULD_RUN_STEP1 -eq 1 ]; then
            print_status "=== Step 1: Project Discovery and Indexing ==="
            OUTPUT_DIR="$OUTPUT_DIR" STEP1_NO_UPSERT="${STEP1_NO_UPSERT:-0}" ./step1.sh
            if [ $? -ne 0 ]; then
                print_error "Step 1 failed - iteration aborted"; exit 1
            fi
            print_success "Step 1 completed successfully"
        fi
        echo ""
        
        # Step 2: Analysis
        RUN_STEP2=0
        if [ "$REPEAT_STEP2" = "1" ]; then RUN_STEP2=1; fi
        if [ ! -d "$OUTPUT_DIR/requirements" ]; then RUN_STEP2=1; fi
        if [ $RUN_STEP2 -eq 1 ]; then
            print_status "=== Step 2: Component Analysis ==="
            if OUTPUT_DIR="$OUTPUT_DIR" ./step2.sh; then
                print_success "Step 2 completed successfully"
            else
                print_error "Step 2 failed - iteration aborted"; exit 1
            fi
        else
            print_status "Skipping Step 2 (use --repeat-step2 to re-run)"
        fi
        echo ""
        
        # Step 3: Requirements Generation (PGM/CREWAI/BOTH)
        case "$STEP3_MODE" in
            pgm)
                print_status "=== Step 3: Programmatic Requirements Generation (PGM) ==="
                OUTPUT_DIR="$OUTPUT_DIR" ./step3-pgm.sh $([ "$STEP3_PARALLEL" = "--parallel" ] && echo "--parallel" || echo "--sequential") --max-workers "$STEP3_MAX_WORKERS" $PGM_CLASSIFICATION_FLAG || print_warning "Step 3-PGM failed"
                ;;
            crewai)
                print_status "=== Step 3: CrewAI Agent-Based Requirements Generation ==="
                OUTPUT_DIR="$OUTPUT_DIR" ./step3-crewai.sh $CREWAI_VERBOSE_FLAG || print_warning "Step 3-CrewAI failed"
                ;;
            both)
                print_status "=== Step 3: PGM then CrewAI (Comparison) ==="
                OUTPUT_DIR="$OUTPUT_DIR" ./step3-pgm.sh $([ "$STEP3_PARALLEL" = "--parallel" ] && echo "--parallel" || echo "--sequential") --max-workers "$STEP3_MAX_WORKERS" $PGM_CLASSIFICATION_FLAG || print_warning "Step 3-PGM failed"
                OUTPUT_DIR="$OUTPUT_DIR" ./step3-crewai.sh $CREWAI_VERBOSE_FLAG || print_warning "Step 3-CrewAI failed"
                write_comparison_index
                ;;
            *) print_warning "Unknown --step3 mode '$STEP3_MODE'";;
        esac
        echo ""
        
        # Step 4: Statistics
        print_status "=== Step 4: Statistics Collection ==="
        show_statistics
        echo ""
        
        # Create summary
        create_summary
        echo ""
        print_success "Enhanced iteration completed successfully!"
        print_success "Output saved to: $OUTPUT_DIR"
        echo ""
        echo "📊 Generated Outputs:"
        echo "  📁 Requirements (CrewAI): $OUTPUT_DIR/requirements/crewai/"
        echo "  📁 Component Analysis: $OUTPUT_DIR/projects/"
        echo "  📁 Vector Database: Weaviate collections"
        echo "  📄 Summary: $OUTPUT_DIR/iteration_summary.txt"
        echo ""
        echo "🔧 Next Steps:"
        echo "  python -m src.cli query       # Search indexed data"
        echo "  python -m src.cli stats       # View statistics"
        echo "  ./step3-pgm.sh               # Run programmatic requirements"
    elif [ -x "./step1.sh" ] && [ -x "./step2.sh" ]; then
        print_status "Detected step1.sh and step2.sh; running two-step workflow..."
        echo ""
        ./step1.sh
        echo ""
        ./step2.sh
        echo ""
        if [ -x "./step3.sh" ]; then
            print_status "Detected step3.sh; running step 3 synthesis..."
            ./step3.sh
            echo ""
        fi
        # Step 3: Statistics
        show_statistics
        echo ""
        # Create summary
        create_summary
        echo ""
        print_success "Iteration completed successfully!"
        print_success "Output saved to: $OUTPUT_DIR"
        echo ""
        echo "To query the indexed data, run:"
        echo "  python -m src.cli query"
        echo ""
        echo "To view statistics, run:"
        echo "  python -m src.cli stats"
    else
        # Step 1: Indexing
        if run_indexing; then
            echo ""
            # Step 2: Requirements generation
            if run_requirements; then
                echo ""
                # Step 3: Statistics
                show_statistics
                echo ""
                # Create summary
                create_summary
                echo ""
                print_success "Iteration completed successfully!"
                print_success "Output saved to: $OUTPUT_DIR"
                echo ""
                echo "To query the indexed data, run:"
                echo "  python -m src.cli query"
                echo ""
                echo "To view statistics, run:"
                echo "  python -m src.cli stats"
            else
                print_error "Requirements generation failed - iteration incomplete"
                exit 1
            fi
        else
            print_error "Indexing failed - iteration aborted"
            exit 1
        fi
    fi
}

# Run main function
main "$@"
