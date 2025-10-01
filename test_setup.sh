#!/bin/bash

# Test script to verify the Java Codebase Analysis Tool setup
# This script performs basic checks without running the full iteration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

echo "=========================================="
echo "Java Codebase Analysis Tool - Setup Test"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found"
    print_status "Please run: cp .env.example .env"
    print_status "Then edit .env with your configuration"
    exit 1
fi

print_success ".env file found"

# Check if source directory is configured
JAVA_SOURCE_DIR=$(grep "^JAVA_SOURCE_DIR=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
if [ -z "$JAVA_SOURCE_DIR" ]; then
    print_error "JAVA_SOURCE_DIR not configured in .env file"
    exit 1
fi

print_success "JAVA_SOURCE_DIR configured: $JAVA_SOURCE_DIR"

# Check if source directory exists
if [ ! -d "$JAVA_SOURCE_DIR" ]; then
    print_error "Source directory does not exist: $JAVA_SOURCE_DIR"
    exit 1
fi

print_success "Source directory exists"

# Check for Java files
JAVA_FILE_COUNT=$(find "$JAVA_SOURCE_DIR" -name "*.java" -type f 2>/dev/null | wc -l)
if [ $JAVA_FILE_COUNT -eq 0 ]; then
    print_warning "No Java files found in source directory"
else
    print_success "Found $JAVA_FILE_COUNT Java files"
fi

# Check AI provider configuration
AI_PROVIDER=$(grep "^AI_PROVIDER=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
print_status "AI Provider: $AI_PROVIDER"

case "$AI_PROVIDER" in
    "openai")
        OPENAI_API_KEY=$(grep "^OPENAI_API_KEY=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-your-openai-api-key-here" ]; then
            print_error "OpenAI API key not configured"
        else
            print_success "OpenAI API key configured"
        fi
        ;;
    "ollama")
        OLLAMA_BASE_URL=$(grep "^OLLAMA_BASE_URL=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ -z "$OLLAMA_BASE_URL" ]; then
            OLLAMA_BASE_URL="http://localhost:11434"
        fi
        
        if curl -s --connect-timeout 5 "$OLLAMA_BASE_URL/api/tags" >/dev/null 2>&1; then
            print_success "Ollama is running at $OLLAMA_BASE_URL"
        else
            print_warning "Ollama is not running at $OLLAMA_BASE_URL"
        fi
        ;;
    "anthropic")
        ANTHROPIC_API_KEY=$(grep "^ANTHROPIC_API_KEY=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
        if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-your-anthropic-api-key-here" ]; then
            print_error "Anthropic API key not configured"
        else
            print_success "Anthropic API key configured"
        fi
        ;;
esac

# Check Weaviate
WEAVIATE_URL=$(grep "^WEAVIATE_URL=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
if [ -z "$WEAVIATE_URL" ]; then
    WEAVIATE_URL="http://localhost:8080"
fi

if curl -s --connect-timeout 5 "$WEAVIATE_URL/v1/meta" >/dev/null 2>&1; then
    print_success "Weaviate is running at $WEAVIATE_URL"
else
    print_warning "Weaviate is not running at $WEAVIATE_URL"
    print_status "Start Weaviate with:"
    echo "  docker run -p 8080:8080 -p 50051:50051 \\"
    echo "    -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \\"
    echo "    -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \\"
    echo "    -e ENABLE_MODULES='text2vec-ollama,generative-ollama' \\"
    echo "    -e CLUSTER_HOSTNAME='node1' \\"
    echo "    semitechnologies/weaviate:latest"
fi

# Check Python environment
if [ -d "venv" ]; then
    print_success "Python virtual environment exists"
else
    print_warning "Python virtual environment not found"
    print_status "Run: python3 -m venv venv"
fi

# Check requirements.txt
if [ -f "requirements.txt" ]; then
    print_success "requirements.txt found"
else
    print_error "requirements.txt not found"
    exit 1
fi

echo ""
print_success "Setup test completed!"
print_status "If all checks passed, you can run: ./run_iteration.sh"
