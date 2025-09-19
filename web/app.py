from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Configuration from environment  
app.config['WEAVIATE_URL'] = os.getenv('WEAVIATE_URL', 'http://weaviate:8080')
app.config['OLLAMA_URL'] = os.getenv('OLLAMA_URL', 'http://host.docker.internal:11434')
app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://redis:6379/0')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    services = {}
    
    # Check Weaviate
    try:
        weaviate_response = requests.get(f"{app.config['WEAVIATE_URL']}/v1/.well-known/ready", timeout=3)
        services['weaviate'] = 'up' if weaviate_response.status_code == 200 else 'down'
    except:
        services['weaviate'] = 'down'
        
    # Check Ollama (running on host)
    try:
        ollama_response = requests.get(f"{app.config['OLLAMA_URL']}/api/tags", timeout=3)
        services['ollama'] = 'up' if ollama_response.status_code == 200 else 'down'
    except:
        services['ollama'] = 'down'
        
    # Check Redis
    try:
        import redis
        r = redis.from_url(app.config['REDIS_URL'], socket_timeout=3)
        r.ping()
        services['redis'] = 'up'
    except:
        services['redis'] = 'down'
    
    overall_status = 'healthy' if all(status == 'up' for status in services.values()) else 'degraded'
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'services': services,
        'environment': 'development-minimal'
    })

@app.route('/api/ollama/models')
def ollama_models():
    """Get available Ollama models"""
    try:
        response = requests.get(f"{app.config['OLLAMA_URL']}/api/tags", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({'error': 'Failed to connect to Ollama'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)