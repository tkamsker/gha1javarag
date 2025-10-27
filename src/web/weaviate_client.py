"""
Web client for querying Weaviate artifacts and generating GPT-like answers.
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import logging
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from store.weaviate_client import WeaviateClient

logger = logging.getLogger(__name__)

# HTML Template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codebase Assistant - Weaviate Search</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 1200px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
        }
        
        .status {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status.connected {
            background: rgba(76, 175, 80, 0.3);
        }
        
        .content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 20px;
            display: flex;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .message.bot .message-content {
            background: white;
            border-left: 4px solid #667eea;
        }
        
        .message-text {
            font-size: 14px;
            line-height: 1.6;
            word-wrap: break-word;
        }
        
        .artifact-card {
            background: #f8f9fa;
            border-left: 3px solid #667eea;
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            font-size: 12px;
        }
        
        .artifact-card strong {
            color: #667eea;
        }
        
        .input-area {
            padding: 20px 30px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        
        .input-area input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .input-area input:focus {
            border-color: #667eea;
        }
        
        .input-area button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .input-area button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .input-area button:active {
            transform: translateY(0);
        }
        
        .loading {
            display: none;
            padding: 10px;
            color: #667eea;
        }
        
        .loading.show {
            display: block;
        }
        
        .empty-state {
            text-align: center;
            color: #999;
            padding: 60px 20px;
        }
        
        .empty-state h3 {
            font-size: 18px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Codebase Assistant</h1>
            <div class="status" id="status">Connecting...</div>
        </div>
        
        <div class="content">
            <div class="chat-area" id="chatArea">
                <div class="empty-state">
                    <h3>Ask me anything about your codebase!</h3>
                    <p>Try asking about classes, methods, components, or any code patterns.</p>
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Ask a question about your codebase..." autocomplete="off" />
                <button id="sendBtn" onclick="sendMessage()">Send</button>
                <div class="loading" id="loading">Searching...</div>
            </div>
        </div>
    </div>
    
    <script>
        let conversationHistory = [];
        
        // Send message on Enter key
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const query = input.value.trim();
            
            if (!query) return;
            
            // Add user message to UI
            addMessage(query, 'user');
            input.value = '';
            
            // Show loading
            document.getElementById('loading').classList.add('show');
            document.getElementById('sendBtn').disabled = true;
            
            try {
                // Send request to backend
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                // Add bot response to UI
                addMessage(data.answer, 'bot', data.artifacts);
                
            } catch (error) {
                addMessage('Error: ' + error.message, 'bot');
            } finally {
                document.getElementById('loading').classList.remove('show');
                document.getElementById('sendBtn').disabled = false;
            }
        }
        
        function addMessage(text, type, artifacts = null) {
            const chatArea = document.getElementById('chatArea');
            const emptyState = chatArea.querySelector('.empty-state');
            if (emptyState) emptyState.remove();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            const textDiv = document.createElement('div');
            textDiv.className = 'message-text';
            textDiv.textContent = text;
            contentDiv.appendChild(textDiv);
            
            // Add artifacts if provided
            if (artifacts && artifacts.length > 0) {
                artifacts.forEach(artifact => {
                    const artifactDiv = document.createElement('div');
                    artifactDiv.className = 'artifact-card';
                    
                    const type = artifact.class || 'Unknown';
                    const path = artifact.path || 'N/A';
                    const summary = artifact.summary || artifact.text || 'No description';
                    
                    artifactDiv.innerHTML = `
                        <strong>Type:</strong> ${type}<br>
                        <strong>Path:</strong> ${path}<br>
                        <strong>Summary:</strong> ${summary.substring(0, 100)}${summary.length > 100 ? '...' : ''}
                    `;
                    
                    contentDiv.appendChild(artifactDiv);
                });
            }
            
            messageDiv.appendChild(contentDiv);
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // Check connection status on load
        fetch('/api/status')
            .then(res => res.json())
            .then(data => {
                const statusEl = document.getElementById('status');
                if (data.connected) {
                    statusEl.textContent = 'Connected';
                    statusEl.classList.add('connected');
                } else {
                    statusEl.textContent = 'Disconnected';
                }
            })
            .catch(() => {
                document.getElementById('status').textContent = 'Error';
            });
    </script>
</body>
</html>
"""

app = Flask(__name__)
CORS(app)

# Global Weaviate client
weaviate_client = None

def init_weaviate_client():
    """Initialize Weaviate client."""
    global weaviate_client
    try:
        weaviate_client = WeaviateClient(ensure_schema=False)
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Weaviate client: {e}")
        return False

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Check Weaviate connection status."""
    return jsonify({
        'connected': weaviate_client is not None
    })

@app.route('/api/query', methods=['POST'])
def query():
    """Handle search queries and generate answers."""
    try:
        data = request.json
        query_text = data.get('query', '')
        
        if not query_text:
            return jsonify({'error': 'Query is required'}), 400
        
        if weaviate_client is None:
            return jsonify({'error': 'Weaviate client not initialized'}), 500
        
        # Search across multiple artifact types
        all_artifacts = []
        
        # Search in different classes
        search_classes = [
            'BackendDoc', 'IbatisStatement', 'DaoCall', 
            'JspForm', 'GwtModule', 'GwtActivityPlace',
            'JsArtifact', 'FrontendRoute'
        ]
        
        for class_name in search_classes:
            try:
                artifacts = weaviate_client.search_artifacts(class_name, query_text, limit=5)
                for artifact in artifacts:
                    artifact['class'] = class_name
                    all_artifacts.append(artifact)
            except Exception as e:
                logger.warning(f"Failed to search {class_name}: {e}")
        
        # Generate an answer based on the artifacts found
        if all_artifacts:
            answer = generate_answer(query_text, all_artifacts[:10])  # Limit to top 10
            return jsonify({
                'answer': answer,
                'artifacts': all_artifacts[:5]  # Return top 5 artifacts for display
            })
        else:
            return jsonify({
                'answer': f"I couldn't find anything related to '{query_text}' in the codebase. Try rephrasing your query or searching for different terms.",
                'artifacts': []
            })
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

def generate_answer(query: str, artifacts: List[Dict[str, Any]]) -> str:
    """Generate a natural language answer based on found artifacts."""
    if not artifacts:
        return f"I found no matches for '{query}' in the codebase."
    
    # Group artifacts by class
    by_class = {}
    for artifact in artifacts:
        class_name = artifact.get('class', 'Unknown')
        if class_name not in by_class:
            by_class[class_name] = []
        by_class[class_name].append(artifact)
    
    # Build the answer
    answer_parts = [f"Based on your question about '{query}', I found {len(artifacts)} relevant artifact(s):\n"]
    
    for class_name, artifacts_list in by_class.items():
        answer_parts.append(f"\n📋 **{class_name}** ({len(artifacts_list)} found):")
        
        for i, artifact in enumerate(artifacts_list[:3], 1):  # Show top 3 per class
            path = artifact.get('path', 'Unknown path')
            summary = artifact.get('summary', '') or artifact.get('text', '')[:150]
            
            answer_parts.append(f"\n{i}. **{path}**")
            if summary:
                answer_parts.append(f"   {summary}")
    
    if len(artifacts) > 10:
        answer_parts.append(f"\n\n... and {len(artifacts) - 10} more results")
    
    return '\n'.join(answer_parts)

if __name__ == '__main__':
    import sys
    
    # Parse port from command line argument
    port = 8080  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}. Using default port 8080.")
            port = 8080
    
    # Initialize Weaviate client
    if init_weaviate_client():
        logger.info("Weaviate client initialized successfully")
        
        # Start the Flask app
        print("\n" + "="*60)
        print("🚀 Codebase Assistant Web Interface")
        print("="*60)
        print("✅ Weaviate connected")
        print(f"🌐 Starting web server on http://localhost:{port}")
        print("📝 Open your browser to start querying your codebase!")
        print("="*60 + "\n")
        
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        logger.error("Failed to initialize Weaviate client")
        print("❌ Error: Could not connect to Weaviate")
        print("Make sure Weaviate is running on http://localhost:8080")
