#!/bin/bash
# Database Query Scripts Runner
# Runs all database query and analysis scripts

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    print_status "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    print_status "Activating virtual environment..."
    source .venv/bin/activate
else
    print_warning "No virtual environment found. Using system Python."
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please create it from env.example"
    exit 1
fi

# Check if ChromaDB data exists
if [ ! -d "data/chromadb" ]; then
    print_error "ChromaDB data directory not found. Please run Step1.sh first to process source files."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p output

print_header "Database Query and Analysis Suite"
echo "Starting comprehensive database analysis..."

# Function to run script with error handling
run_script() {
    local script_name="$1"
    local description="$2"
    
    print_status "Running $description..."
    
    if [ -f "$script_name" ]; then
        # Try python3 first, then python
        if command -v python3 >/dev/null 2>&1; then
            if python3 "$script_name"; then
                print_status "$description completed successfully"
                return 0
            else
                print_error "$description failed"
                return 1
            fi
        elif command -v python >/dev/null 2>&1; then
            if python "$script_name"; then
                print_status "$description completed successfully"
                return 0
            else
                print_error "$description failed"
                return 1
            fi
        else
            print_error "Neither python nor python3 command found"
            return 1
        fi
    else
        print_error "Script $script_name not found"
        return 1
    fi
}

# Array to track results
declare -a results

print_header "Step 1: DAO Elements Analysis"
if run_script "query_dao_elements.py" "DAO Elements Analysis"; then
    results+=("✅ DAO Elements Analysis")
else
    results+=("❌ DAO Elements Analysis")
fi

echo ""

print_header "Step 2: Data Structures Analysis"
if run_script "analyze_data_structures.py" "Data Structures and Business Rules Analysis"; then
    results+=("✅ Data Structures Analysis")
else
    results+=("❌ Data Structures Analysis")
fi

echo ""

print_header "Step 3: Comprehensive Database Analysis"
if run_script "query_database_comprehensive.py" "Comprehensive Database Analysis"; then
    results+=("✅ Comprehensive Analysis")
else
    results+=("❌ Comprehensive Analysis")
fi

echo ""

# Print summary
print_header "Analysis Results Summary"
for result in "${results[@]}"; do
    echo "$result"
done

# List generated files
print_header "Generated Output Files"
if [ -d "output" ]; then
    echo "Files in ./output/:"
    ls -la output/ | grep -E "(dao_elements|data_structures|comprehensive)" | tail -10
else
    print_warning "No output directory found"
fi

print_status "Database analysis complete!"

# Optional: Generate a combined summary report
if [ "$1" = "--summary" ] || [ "$1" = "-s" ]; then
    print_header "Generating Combined Summary Report"
    
    timestamp=$(date +"%Y%m%d_%H%M%S")
    summary_file="output/database_analysis_summary_${timestamp}.txt"
    
    {
        echo "=== Database Analysis Summary ==="
        echo "Generated: $(date)"
        echo ""
        echo "Analysis Results:"
        for result in "${results[@]}"; do
            echo "$result"
        done
        echo ""
        echo "Latest Output Files:"
        ls -la output/ | grep -E "(dao_elements|data_structures|comprehensive)" | tail -10
    } > "$summary_file"
    
    print_status "Summary report saved to: $summary_file"
fi

echo ""
print_status "To run individual scripts:"
echo "  python3 query_dao_elements.py          - DAO elements analysis"
echo "  python3 analyze_data_structures.py     - Data structures analysis" 
echo "  python3 query_database_comprehensive.py - Comprehensive analysis"
echo ""
print_status "To generate summary report:"
echo "  ./run_database_queries.sh --summary"