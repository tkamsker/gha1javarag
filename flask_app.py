"""
Deployment Notes:
- Ensure all dependencies (Flask, python-dotenv, chromadb_connector, etc.) are installed.
- Test the /chat endpoint with various queries to confirm correct ChromaDB access and LLM integration.
- Do not touch main.py, step2.py, or step3.py logic.
"""
from flask import Flask, request, jsonify, render_template
import os
import asyncio
from dotenv import load_dotenv
from src import chromadb_connector
from src.ai_providers import create_ai_provider

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()
AI_PROVIDER = os.getenv('AI_PROVIDER', 'default')

# Create AI provider instance
try:
    ai_provider = create_ai_provider()
    print(f"Initialized AI provider: {ai_provider.get_provider_name()} with model: {ai_provider.get_model_name()}")
except Exception as e:
    print(f"Warning: Could not initialize AI provider: {e}")
    ai_provider = None

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    
    # Get relevant context from ChromaDB
    context = chromadb_connector.query_chromadb(question)
    
    # Check if AI provider is available
    if ai_provider is None:
        return jsonify({
            'answer': 'AI provider not available. Please check your configuration.',
            'error': 'AI provider initialization failed'
        }), 500
    
    # Compose a focused prompt
    system_prompt = """You are an expert on this application. Only answer questions about this specific project, using the provided context and metadata. Do not answer questions outside the scope of this project. If the context doesn't contain relevant information, say so clearly."""
    
    user_prompt = f"""Context from project documentation:
{context}

Question: {question}

Please provide a clear, concise answer based only on the project context above."""
    
    # Prepare messages for AI provider
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        # Run async AI provider in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        answer = loop.run_until_complete(
            ai_provider.create_chat_completion(messages, temperature=0.2, max_tokens=1000)
        )
        loop.close()
        
        return jsonify({
            'answer': answer,
            'provider': ai_provider.get_provider_name(),
            'model': ai_provider.get_model_name()
        })
        
    except Exception as e:
        return jsonify({
            'answer': f'Error generating response: {str(e)}',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 