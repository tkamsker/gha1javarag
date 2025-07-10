#!/bin/bash

# StrictDoc Server Setup and Validation Script
# This script validates SDoc files, sets up the requirements directory, and runs StrictDoc server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_DIR="$PROJECT_ROOT/output/requirements"
STRICTDOC_DIR="$SCRIPT_DIR"
VENV_DIR="$STRICTDOC_DIR/venv2"

echo -e "${BLUE}=== StrictDoc Server Setup and Validation ===${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to validate SDoc file syntax
validate_sdoc_file() {
    local file_path="$1"
    local file_name=$(basename "$file_path")
    
    print_status "Validating $file_name..."
    
    # Check if file exists
    if [[ ! -f "$file_path" ]]; then
        print_error "File not found: $file_path"
        return 1
    fi
    
    # Basic syntax validation
    local has_document_tag=false
    local has_title=false
    local line_number=0
    
    while IFS= read -r line; do
        ((line_number++))
        
        # Skip empty lines and comments
        if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
            continue
        fi
        
        # Check for required tags
        if [[ "$line" =~ ^\[DOCUMENT\] ]]; then
            has_document_tag=true
        elif [[ "$line" =~ ^TITLE: ]]; then
            has_title=true
        fi
        
        # Check for common syntax errors
        if [[ "$line" =~ ^[[:space:]]*\[.*\]$ && ! "$line" =~ ^[[:space:]]*\[(DOCUMENT|GRAMMAR|TEXT|REQUIREMENT|SECTION|NOTE)\] ]]; then
            print_warning "Line $line_number: Potentially invalid tag: $line"
        fi
        
        # Check for unclosed statements
        if [[ "$line" =~ ^[[:space:]]*>>> && ! "$line" =~ <<<$ ]]; then
            print_warning "Line $line_number: Unclosed statement block detected"
        fi
        
    done < "$file_path"
    
    if [[ "$has_document_tag" == false ]]; then
        print_error "$file_name: Missing [DOCUMENT] tag"
        return 1
    fi
    
    if [[ "$has_title" == false ]]; then
        print_warning "$file_name: Missing TITLE field"
    fi
    
    print_status "$file_name: Basic validation passed"
    return 0
}

# Function to fix common SDoc syntax issues
fix_sdoc_file() {
    local file_path="$1"
    local temp_file="${file_path}.tmp"
    
    print_status "Attempting to fix syntax issues in $(basename "$file_path")..."
    
    # Create backup
    cp "$file_path" "${file_path}.backup"
    
    # Fix common issues
    sed -E '
        # Fix unclosed statement blocks
        s/>>>([^<]*)$/>>>\1\n<<</g
        # Fix missing newlines after tags
        s/^(\[DOCUMENT\])/\1\n/g
        s/^(\[GRAMMAR\])/\1\n/g
        s/^(\[TEXT\])/\1\n/g
        s/^(\[REQUIREMENT\])/\1\n/g
        s/^(\[SECTION\])/\1\n/g
        s/^(\[\/SECTION\])/\1\n/g
        s/^(\[NOTE\])/\1\n/g
        # Fix malformed field definitions
        s/^([[:space:]]*[A-Z_]+):[[:space:]]*$/&\n/g
    ' "$file_path" > "$temp_file"
    
    # Replace original with fixed version
    mv "$temp_file" "$file_path"
    print_status "Applied basic fixes to $(basename "$file_path")"
}

# Function to create sample SDoc files if none exist
create_sample_sdoc_files() {
    print_status "Creating sample SDoc files..."
    
    # Create requirements directory if it doesn't exist
    mkdir -p "$REQUIREMENTS_DIR"
    
    # Create a sample SDoc file
    cat > "$REQUIREMENTS_DIR/sample_requirement.sdoc" << 'EOF'
[DOCUMENT]
TITLE: Sample Java Class Requirement
UID: SAMPLE_REQ_001
VERSION: 1.0
CLASSIFICATION: requirement
PREFIX: REQ

[GRAMMAR]
ELEMENTS:
- TAG: REQUIREMENT
  FIELDS:
  - TITLE: UID
    TYPE: String
    REQUIRED: True
  - TITLE: TITLE
    TYPE: String
    REQUIRED: True
  - TITLE: STATEMENT
    TYPE: String
    REQUIRED: True
  - TITLE: STATUS
    TYPE: String
    REQUIRED: False
  RELATIONS:
  - TYPE: Parent
  - TYPE: File

[REQUIREMENT]
UID: REQ_001
TITLE: User Authentication Service
STATEMENT: >>>
The system shall provide user authentication functionality with the following requirements:
- Support username/password authentication
- Implement secure session management
- Provide role-based access control
- Log all authentication attempts
<<<
STATUS: Active

[REQUIREMENT]
UID: REQ_002
TITLE: Data Validation
STATEMENT: >>>
All user input shall be validated before processing:
- Sanitize all input data
- Validate data types and formats
- Implement proper error handling
- Return meaningful error messages
<<<
STATUS: Active
EOF

    print_status "Created sample SDoc file: sample_requirement.sdoc"
}

# Function to activate virtual environment
activate_venv() {
    if [[ -d "$VENV_DIR" ]]; then
        print_status "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
    else
        print_error "Virtual environment not found at $VENV_DIR"
        print_status "Please run: python3 -m venv $VENV_DIR"
        print_status "Then install StrictDoc: pip install strictdoc"
        exit 1
    fi
}

# Function to validate all SDoc files
validate_all_sdoc_files() {
    print_status "Validating all SDoc files..."
    
    local validation_errors=0
    local files_processed=0
    
    # Find all .sdoc files
    while IFS= read -r -d '' file; do
        ((files_processed++))
        if ! validate_sdoc_file "$file"; then
            ((validation_errors++))
            print_warning "Attempting to fix $file..."
            if fix_sdoc_file "$file"; then
                print_status "Fixed $file"
            else
                print_error "Failed to fix $file"
            fi
        fi
    done < <(find "$REQUIREMENTS_DIR" -name "*.sdoc" -print0 2>/dev/null)
    
    if [[ $files_processed -eq 0 ]]; then
        print_warning "No SDoc files found in $REQUIREMENTS_DIR"
        create_sample_sdoc_files
        files_processed=1
    fi
    
    print_status "Processed $files_processed files, $validation_errors had issues"
    return $validation_errors
}

# Function to run StrictDoc server
run_strictdoc_server() {
    print_status "Starting StrictDoc server..."
    
    # Check if requirements directory exists and has files
    if [[ ! -d "$REQUIREMENTS_DIR" ]] || [[ -z "$(find "$REQUIREMENTS_DIR" -name "*.sdoc" 2>/dev/null)" ]]; then
        print_warning "No SDoc files found, creating sample files..."
        create_sample_sdoc_files
    fi
    
    # Change to the requirements directory
    cd "$REQUIREMENTS_DIR"
    
    print_status "Server will be available at: http://localhost:5111"
    print_status "Press Ctrl+C to stop the server"
    print_status "Requirements directory: $REQUIREMENTS_DIR"
    
    # Run StrictDoc server
    strictdoc server . --port 5111 --host 0.0.0.0
}

# Main execution
main() {
    # Check if we're in the right directory
    if [[ ! -d "$STRICTDOC_DIR" ]]; then
        print_error "StrictDoc directory not found: $STRICTDOC_DIR"
        exit 1
    fi
    
    # Create requirements directory if it doesn't exist
    mkdir -p "$REQUIREMENTS_DIR"
    
    # Validate SDoc files
    validate_all_sdoc_files
    
    # Activate virtual environment
    activate_venv
    
    # Run the server
    run_strictdoc_server
}

# Handle command line arguments
case "${1:-}" in
    "validate")
        validate_all_sdoc_files
        ;;
    "fix")
        print_status "Fixing SDoc files..."
        find "$REQUIREMENTS_DIR" -name "*.sdoc" -exec bash -c 'fix_sdoc_file "$1"' _ {} \;
        ;;
    "create-sample")
        create_sample_sdoc_files
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  validate      - Validate all SDoc files"
        echo "  fix          - Fix common syntax issues in SDoc files"
        echo "  create-sample - Create sample SDoc files"
        echo "  help         - Show this help message"
        echo ""
        echo "Default: Start StrictDoc server"
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 