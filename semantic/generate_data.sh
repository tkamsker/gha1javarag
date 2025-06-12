#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Create necessary directories
mkdir -p data/results
mkdir -p data/chroma_db

# Set default values if not in .env
export JAVA_SOURCE_DIR=${JAVA_SOURCE_DIR:-"java_codebase"}
export CHROMA_DB_DIR=${CHROMA_DB_DIR:-"data/chroma_db"}
export TEST_MODE=true

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the main application with force reanalysis
echo "Running semantic analysis with force reanalysis..."
python -m src.main --force-reanalysis

# Verify the output files exist
echo "Verifying generated files..."
if [ ! -f "data/results/clustering_results.json" ]; then
    echo "Error: clustering_results.json was not generated"
    exit 1
fi

if [ ! -f "data/results/clusters_by_class.json" ]; then
    echo "Error: clusters_by_class.json was not generated"
    exit 1
fi

if [ ! -f "data/results/analysis_report.md" ]; then
    echo "Error: analysis_report.md was not generated"
    exit 1
fi

echo "Test data generation completed successfully!"
echo "Generated files:"
echo "- data/results/clustering_results.json"
echo "- data/results/clusters_by_class.json"
echo "- data/results/analysis_report.md" 