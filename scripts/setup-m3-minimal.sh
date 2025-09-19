#!/bin/bash

# Minimal setup script for M3 Max development environment
# Uses local Ollama - minimal Docker overhead

set -e

echo "🚀 Setting up MINIMAL M3 Max development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on macOS with Apple Silicon
if [[ "$OSTYPE" != "darwin"* ]] || [[ $(uname -m) != "arm64" ]]; then
    echo -e "${RED}❌ This script requires macOS with Apple Silicon (M3 Max)${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Docker
if ! command_exists docker; then
    echo -e "${RED}❌ Docker is required but not installed${NC}"
    echo -e "${YELLOW}Install: brew install --cask docker${NC}"
    exit 1
fi

# Check Ollama
if ! command_exists ollama; then
    echo -e "${RED}❌ Ollama is required but not installed${NC}"
    echo -e "${YELLOW}Install: brew install ollama${NC}"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama is not running. Starting Ollama service...${NC}"
    brew services start ollama
    echo -e "${BLUE}⏱️  Waiting 5 seconds for Ollama to start...${NC}"
    sleep 5
    
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "${RED}❌ Failed to start Ollama. Please start manually:${NC}"
        echo -e "${YELLOW}   ollama serve${NC}"
        exit 1
    fi
fi

# Check available memory
MEMORY_GB=$(sysctl -n hw.memsize | awk '{print int($0/1024/1024/1024)}')
echo -e "${BLUE}💾 Detected ${MEMORY_GB}GB unified memory${NC}"

if [ "$MEMORY_GB" -lt 32 ]; then
    echo -e "${YELLOW}⚠️  Warning: Less than 32GB memory. Large models may run slowly${NC}"
fi

# Create minimal directories
echo -e "${BLUE}📁 Creating minimal project structure...${NC}"
mkdir -p web/templates
mkdir -p output

# Check if required models are installed
echo -e "${BLUE}🤖 Checking Ollama models...${NC}"

REQUIRED_MODELS=(
    "nomic-embed-text"
    "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
)

MISSING_MODELS=()

for model in "${REQUIRED_MODELS[@]}"; do
    if ! ollama list | grep -q "$model"; then
        MISSING_MODELS+=("$model")
    fi
done

if [ ${#MISSING_MODELS[@]} -gt 0 ]; then
    echo -e "${YELLOW}📦 Missing models detected. Installing...${NC}"
    for model in "${MISSING_MODELS[@]}"; do
        echo -e "${BLUE}⬇️  Pulling $model...${NC}"
        ollama pull "$model"
    done
else
    echo -e "${GREEN}✅ All required models are installed${NC}"
fi

# Create minimal environment file
echo -e "${BLUE}⚙️  Creating minimal development configuration...${NC}"
cat > .env.minimal << EOF
# Minimal M3 Max Development Environment
COMPOSE_PROJECT_NAME=java-analysis-minimal
COMPOSE_FILE=docker-compose.m3-dev-minimal.yml

# AI Provider Configuration (Local Ollama)
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
OLLAMA_TIMEOUT=300

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_COLLECTION=java_analysis_dev

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
RATE_LIMIT_ENV=development

# Output Configuration
OUTPUT_DIR=./output
JAVA_SOURCE_DIR=./test-projects
EOF

# Create startup script
cat > start-minimal.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting minimal Java Analysis Tool environment..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama not detected. Starting Ollama..."
    brew services start ollama
    sleep 3
fi

# Load minimal environment
if [ -f .env.minimal ]; then
    export $(cat .env.minimal | xargs)
fi

# Start minimal Docker services
docker-compose -f docker-compose.m3-dev-minimal.yml up -d

echo ""
echo "✅ Minimal environment started!"
echo ""
echo "🌐 Services:"
echo "   • Web Interface: http://localhost:8000"
echo "   • Weaviate: http://localhost:8080" 
echo "   • Local Ollama: http://localhost:11434"
echo "   • Redis: localhost:6379"
echo ""
echo "📊 Resource Usage:"
docker stats --no-stream --format "   • {{.Name}}: {{.MemUsage}} ({{.MemPerc}})"
echo ""
echo "🛠️  Commands:"
echo "   • View logs: docker-compose -f docker-compose.m3-dev-minimal.yml logs -f"
echo "   • Stop: ./stop-minimal.sh"
echo "   • Ollama models: ollama list"
EOF

chmod +x start-minimal.sh

# Create stop script
cat > stop-minimal.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping minimal Java Analysis Tool environment..."

docker-compose -f docker-compose.m3-dev-minimal.yml down

echo "✅ Docker services stopped!"
echo ""
echo "ℹ️  Local Ollama is still running (use 'brew services stop ollama' to stop)"
EOF

chmod +x stop-minimal.sh

# Create test script
cat > test-minimal.sh << 'EOF'
#!/bin/bash

echo "🧪 Testing minimal environment..."

# Test Ollama
echo -n "Ollama: "
if curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "✅ Running"
else
    echo "❌ Not responding"
fi

# Test Weaviate
echo -n "Weaviate: "
if curl -s http://localhost:8080/v1/.well-known/ready >/dev/null; then
    echo "✅ Running"  
else
    echo "❌ Not responding"
fi

# Test Redis
echo -n "Redis: "
if docker exec $(docker-compose -f docker-compose.m3-dev-minimal.yml ps -q redis 2>/dev/null) redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "✅ Running"
else
    echo "❌ Not responding" 
fi

# Test Web Interface
echo -n "Web Interface: "
if curl -s http://localhost:8000/api/health >/dev/null; then
    echo "✅ Running"
else
    echo "❌ Not responding"
fi

echo ""
echo "📊 Current Docker usage:"
docker stats --no-stream --format "{{.Name}}: {{.MemUsage}} CPU: {{.CPUPerc}}"
EOF

chmod +x test-minimal.sh

echo ""
echo -e "${GREEN}✅ Minimal M3 Max development environment setup complete!${NC}"
echo ""
echo -e "${BLUE}🚀 Next steps:${NC}"
echo -e "  1. Start the environment: ${GREEN}./start-minimal.sh${NC}"
echo -e "  2. Open web interface: ${GREEN}http://localhost:8000${NC}"
echo -e "  3. Test everything: ${GREEN}./test-minimal.sh${NC}"
echo ""
echo -e "${GREEN}💡 Benefits of this minimal setup:${NC}"
echo -e "  • ${GREEN}Uses local Ollama${NC} - no AI model Docker overhead"
echo -e "  • ${GREEN}Only 3 Docker containers${NC} vs 7+ in full setup"
echo -e "  • ${GREEN}~5GB total Docker memory${NC} vs 20GB+ in full setup"  
echo -e "  • ${GREEN}Faster startup${NC} - models already loaded in Ollama"
echo -e "  • ${GREEN}Direct model access${NC} - no container networking overhead"
echo ""
echo -e "${YELLOW}⚠️  Remember:${NC}"
echo -e "  • Keep Ollama running: ${YELLOW}ollama serve${NC}"
echo -e "  • Models are ~30GB - ensure sufficient disk space"
echo -e "  • Use Activity Monitor to track resource usage"
echo ""
echo -e "${GREEN}🎯 Ready for efficient M3 Max development!${NC}"