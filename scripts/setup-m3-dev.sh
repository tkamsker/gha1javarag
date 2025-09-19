#!/bin/bash

# Setup script for M3 Max development environment
# Java JSP Application Reverse Engineering Tool - Iteration 13

set -e

echo "🚀 Setting up Iteration 13 development environment for Apple M3 Max..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is designed for macOS with Apple Silicon (M3 Max)${NC}"
    exit 1
fi

# Check for Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo -e "${RED}❌ This script requires Apple Silicon (ARM64) architecture${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Docker
if ! command_exists docker; then
    echo -e "${RED}❌ Docker is required but not installed${NC}"
    echo -e "${YELLOW}Please install Docker Desktop for Mac from https://docker.com${NC}"
    exit 1
fi

# Check Docker Compose
if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker Compose is required but not available${NC}"
    exit 1
fi

# Check available memory (M3 Max should have significant unified memory)
MEMORY_GB=$(sysctl -n hw.memsize | awk '{print int($0/1024/1024/1024)}')
echo -e "${BLUE}💾 Detected ${MEMORY_GB}GB unified memory${NC}"

if [ "$MEMORY_GB" -lt 32 ]; then
    echo -e "${YELLOW}⚠️  Warning: Less than 32GB memory detected. Qwen3-Coder-30B may run slowly${NC}"
    echo -e "${YELLOW}   Consider using a smaller model or adding more memory${NC}"
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating project directories...${NC}"
mkdir -p monitoring/grafana-dev
mkdir -p ollama-models ollama-config
mkdir -p weaviate-config
mkdir -p web
mkdir -p sql
mkdir -p backups
mkdir -p output

# Create development environment file
echo -e "${BLUE}⚙️  Creating development environment configuration...${NC}"
cat > .env.dev << EOF
# Development Environment Configuration for M3 Max
COMPOSE_PROJECT_NAME=java-analysis-dev
COMPOSE_FILE=docker-compose.m3-dev.yml

# AI Provider Configuration
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth
OLLAMA_TIMEOUT=300

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_COLLECTION=java_analysis_dev

# Database Configuration
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/java_analysis_dev

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
RATE_LIMIT_ENV=development

# Output Configuration
OUTPUT_DIR=./output
JAVA_SOURCE_DIR=./test-projects
EOF

# Create development SQL initialization
echo -e "${BLUE}🗄️  Creating database initialization script...${NC}"
cat > sql/init-dev.sql << EOF
-- Development database initialization for Java Analysis Tool

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis sessions table  
CREATE TABLE IF NOT EXISTS analysis_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending',
    files_processed INTEGER DEFAULT 0,
    total_files INTEGER DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name);
CREATE INDEX IF NOT EXISTS idx_sessions_project_id ON analysis_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON analysis_sessions(status);

-- Insert sample data for development
INSERT INTO projects (name, description, source_path) VALUES 
('Sample JSP Project', 'Development test project', './test-projects/sample-jsp')
ON CONFLICT DO NOTHING;
EOF

# Create basic web interface structure
echo -e "${BLUE}🌐 Setting up web interface structure...${NC}"
mkdir -p web/templates web/static web/src

# Create basic Flask app for development
cat > web/app.py << 'EOF'
from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Configuration from environment
app.config['WEAVIATE_URL'] = os.getenv('WEAVIATE_URL', 'http://weaviate:8080')
app.config['OLLAMA_URL'] = os.getenv('OLLAMA_URL', 'http://ollama:11434')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        # Check Weaviate
        weaviate_response = requests.get(f"{app.config['WEAVIATE_URL']}/v1/.well-known/ready", timeout=5)
        weaviate_status = weaviate_response.status_code == 200
    except:
        weaviate_status = False
        
    try:
        # Check Ollama
        ollama_response = requests.get(f"{app.config['OLLAMA_URL']}/api/tags", timeout=5)
        ollama_status = ollama_response.status_code == 200
    except:
        ollama_status = False
    
    return jsonify({
        'status': 'healthy' if weaviate_status and ollama_status else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'weaviate': 'up' if weaviate_status else 'down',
            'ollama': 'up' if ollama_status else 'down'
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
EOF

# Create requirements.txt for web interface
cat > web/requirements.txt << EOF
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
redis==5.0.1
weaviate-client==4.9.3
EOF

# Create basic HTML template
cat > web/templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Java Analysis Tool - Development</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .status.healthy { background: #d4edda; color: #155724; }
        .status.unhealthy { background: #f8d7da; color: #721c24; }
        .service { margin: 5px 0; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Java Analysis Tool - M3 Max Development</h1>
        <p>Welcome to the development environment for Iteration 13!</p>
        
        <div id="status">Loading system status...</div>
        
        <h2>Available Services</h2>
        <ul>
            <li><strong>Weaviate:</strong> <a href="http://localhost:8080" target="_blank">http://localhost:8080</a></li>
            <li><strong>Ollama:</strong> <a href="http://localhost:11434" target="_blank">http://localhost:11434</a></li>
            <li><strong>Grafana:</strong> <a href="http://localhost:3000" target="_blank">http://localhost:3000</a> (admin/dev123)</li>
            <li><strong>Prometheus:</strong> <a href="http://localhost:9090" target="_blank">http://localhost:9090</a></li>
        </ul>
        
        <h2>Development Notes</h2>
        <ul>
            <li>Qwen3-Coder-30B model will be automatically downloaded on first startup</li>
            <li>Model download may take 20-30 minutes depending on your internet connection</li>
            <li>Monitor resource usage in Activity Monitor during development</li>
            <li>Use <code>docker-compose -f docker-compose.m3-dev.yml logs -f</code> to view logs</li>
        </ul>
    </div>

    <script>
        async function checkHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                
                const statusDiv = document.getElementById('status');
                const isHealthy = data.status === 'healthy';
                
                statusDiv.className = `status ${isHealthy ? 'healthy' : 'unhealthy'}`;
                statusDiv.innerHTML = `
                    <strong>System Status: ${data.status.toUpperCase()}</strong><br>
                    <div class="service">Weaviate: ${data.services.weaviate}</div>
                    <div class="service">Ollama: ${data.services.ollama}</div>
                    <small>Last checked: ${new Date(data.timestamp).toLocaleString()}</small>
                `;
            } catch (error) {
                document.getElementById('status').innerHTML = `
                    <div class="status unhealthy">
                        <strong>Cannot connect to backend services</strong>
                    </div>
                `;
            }
        }
        
        // Check health on load and every 30 seconds
        checkHealth();
        setInterval(checkHealth, 30000);
    </script>
</body>
</html>
EOF

# Create Dockerfile for web interface
cat > web/Dockerfile.dev << 'EOF'
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application in development mode
CMD ["python", "app.py"]
EOF

# Create startup script
cat > start-dev.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting Java Analysis Tool development environment..."

# Load development environment
export $(cat .env.dev | xargs)

# Start services
docker-compose -f docker-compose.m3-dev.yml up -d

echo "✅ Services started! Check status at http://localhost:8000"
echo ""
echo "📊 Monitoring URLs:"
echo "   • Web Interface: http://localhost:8000"
echo "   • Weaviate: http://localhost:8080"
echo "   • Ollama: http://localhost:11434"
echo "   • Grafana: http://localhost:3000 (admin/dev123)"
echo "   • Prometheus: http://localhost:9090"
echo ""
echo "📋 Useful commands:"
echo "   • View logs: docker-compose -f docker-compose.m3-dev.yml logs -f"
echo "   • Stop services: docker-compose -f docker-compose.m3-dev.yml down"
echo "   • Check models: docker exec -it \$(docker-compose -f docker-compose.m3-dev.yml ps -q ollama) ollama list"
EOF

chmod +x start-dev.sh

# Create stop script
cat > stop-dev.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping Java Analysis Tool development environment..."

docker-compose -f docker-compose.m3-dev.yml down

echo "✅ All services stopped!"
EOF

chmod +x stop-dev.sh

echo -e "${GREEN}✅ M3 Max development environment setup complete!${NC}"
echo ""
echo -e "${BLUE}🚀 Next steps:${NC}"
echo -e "  1. Start the development environment: ${GREEN}./start-dev.sh${NC}"
echo -e "  2. Wait for model download (20-30 minutes for first run)"
echo -e "  3. Open http://localhost:8000 to check status"
echo -e "  4. Begin development!"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo -e "  • Monitor system resources in Activity Monitor"
echo -e "  • First startup will download ~20GB of AI models"
echo -e "  • Use './stop-dev.sh' to stop all services"
echo -e "  • Check logs with: docker-compose -f docker-compose.m3-dev.yml logs -f"
echo ""
echo -e "${GREEN}🎯 Ready for Iteration 13 development on M3 Max!${NC}"