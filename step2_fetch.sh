#!/bin/bash

# =============================
# Step 2: Fetch and List Data Script
# =============================
# This script can be run often to fetch, index, and list data

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
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
    exit 1
}

# Check if we're in a virtual environment
check_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        print_info "Virtual environment detected: $VIRTUAL_ENV"
        PYTHON_CMD="python"
    else
        print_warning "No virtual environment detected. Please activate your virtual environment first:"
        echo "  source venv/bin/activate"
        exit 1
    fi
}

# Check if required services are running
check_services() {
    print_info "Checking required services..."
    
    # Check Weaviate
    if ! curl -s http://localhost:8080/v1/meta &> /dev/null; then
        print_error "Weaviate is not running. Please run ./step1_setup.sh first"
        exit 1
    fi
    print_success "Weaviate is running"
    
    # Check Ollama
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_error "Ollama is not running. Please run ./step1_setup.sh first"
        exit 1
    fi
    print_success "Ollama is running"
}

# Run discovery
run_discovery() {
    local project=$1
    local include_frontend=$2
    
    print_info "Running discovery for project: $project (frontend: $include_frontend)"
    
    if [ "$include_frontend" = "true" ]; then
        $PYTHON_CMD main.py discover --project "$project" --include-frontend
    else
        $PYTHON_CMD main.py discover --project "$project"
    fi
    
    print_success "Discovery completed"
}

# Run extraction
run_extraction() {
    local project=$1
    local include_frontend=$2
    
    print_info "Running extraction for project: $project (frontend: $include_frontend)"
    
    if [ "$include_frontend" = "true" ]; then
        $PYTHON_CMD main.py extract --project "$project" --include-frontend
    else
        $PYTHON_CMD main.py extract --project "$project"
    fi
    
    print_success "Extraction completed"
}

# Run indexing
run_indexing() {
    local project=$1
    
    print_info "Running indexing for project: $project"
    
    $PYTHON_CMD main.py index --project "$project"
    
    print_success "Indexing completed"
}

# List indexed data
list_data() {
    local project=$1
    
    print_info "Listing indexed data for project: $project"
    
    # Get counts for each class
    $PYTHON_CMD -c "
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute() / 'src'))
from store.weaviate_client import WeaviateClient

client = WeaviateClient(ensure_schema=False)

classes = ['GwtModule', 'GwtUiBinder', 'GwtActivityPlace', 'GwtEndpoint', 'JsArtifact', 'FrontendRoute', 
          'IbatisStatement', 'DaoCall', 'JspForm', 'DbTable', 'Flow', 'Requirement']

print('\\n=== Indexed Data Summary ===')
total = 0
for class_name in classes:
    try:
        result = client.client.query.get(class_name, ['*']).with_limit(1).do()
        count = len(result.get('data', {}).get('Get', {}).get(class_name, []))
        if count > 0:
            # Get actual count
            result = client.client.query.get(class_name, ['*']).do()
            actual_count = len(result.get('data', {}).get('Get', {}).get(class_name, []))
            print(f'{class_name}: {actual_count} records')
            total += actual_count
        else:
            print(f'{class_name}: 0 records')
    except Exception as e:
        print(f'{class_name}: Error - {e}')

print(f'\\nTotal indexed records: {total}')
"
}

# Search data
search_data() {
    local project=$1
    local query=$2
    local limit=${3:-5}
    
    print_info "Searching for: $query (limit: $limit)"
    
    $PYTHON_CMD main.py search --query "$query" --project "$project" --frontend --limit "$limit"
}

# Generate PRD
generate_prd() {
    local project=$1
    
    print_info "Generating PRD for project: $project"
    
    $PYTHON_CMD main.py prd --project "$project" --frontend
    
    print_success "PRD generation completed"
}

# Show help
show_help() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  all <project> <frontend>           - Run complete pipeline (discover, extract, index, list)"
    echo "  discover <project> <frontend>      - Run discovery only"
    echo "  extract <project> <frontend>       - Run extraction only"
    echo "  index <project>                    - Run indexing only"
    echo "  list <project>                     - List indexed data"
    echo "  search <project> <query> [limit]   - Search indexed data"
    echo "  prd <project>                      - Generate PRD"
    echo "  help                               - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 all 20251008_1034 true"
    echo "  $0 discover 20251008_1034 true"
    echo "  $0 search 20251008_1034 'product administration' 10"
    echo "  $0 list 20251008_1034"
    echo "  $0 prd 20251008_1034"
}

# Main execution
main() {
    local command=$1
    local project=$2
    local frontend=$3
    local query=$3
    local limit=$4
    
    # Check environment
    check_venv
    check_services
    
    case "$command" in
        "all")
            if [ -z "$project" ] || [ -z "$frontend" ]; then
                print_error "Usage: $0 all <project> <frontend>"
                exit 1
            fi
            run_discovery "$project" "$frontend"
            run_extraction "$project" "$frontend"
            run_indexing "$project"
            list_data "$project"
            ;;
        "discover")
            if [ -z "$project" ] || [ -z "$frontend" ]; then
                print_error "Usage: $0 discover <project> <frontend>"
                exit 1
            fi
            run_discovery "$project" "$frontend"
            ;;
        "extract")
            if [ -z "$project" ] || [ -z "$frontend" ]; then
                print_error "Usage: $0 extract <project> <frontend>"
                exit 1
            fi
            run_extraction "$project" "$frontend"
            ;;
        "index")
            if [ -z "$project" ]; then
                print_error "Usage: $0 index <project>"
                exit 1
            fi
            run_indexing "$project"
            ;;
        "list")
            if [ -z "$project" ]; then
                print_error "Usage: $0 list <project>"
                exit 1
            fi
            list_data "$project"
            ;;
        "search")
            if [ -z "$project" ] || [ -z "$query" ]; then
                print_error "Usage: $0 search <project> <query> [limit]"
                exit 1
            fi
            search_data "$project" "$query" "$limit"
            ;;
        "prd")
            if [ -z "$project" ]; then
                print_error "Usage: $0 prd <project>"
                exit 1
            fi
            generate_prd "$project"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
