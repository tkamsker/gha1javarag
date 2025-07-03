"""
Deployment Notes:
- Ensure all dependencies (fastapi, uvicorn, python-dotenv, chromadb_connector, etc.) are installed.
- Test the /chat endpoint with various queries to confirm correct ChromaDB access and LLM integration.
- Do not touch main.py, step2.py, or step3.py logic.
"""
import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import src.chromadb_connector as chromadb_connector
from src.ai_providers import create_ai_provider

# Load environment variables from .env
load_dotenv()
AI_PROVIDER = os.getenv('AI_PROVIDER', 'default')

app = FastAPI()

# Create AI provider instance
try:
    ai_provider = create_ai_provider()
    print(f"Initialized AI provider: {ai_provider.get_provider_name()} with model: {ai_provider.get_model_name()}")
except Exception as e:
    print(f"Warning: Could not initialize AI provider: {e}")
    ai_provider = None

@app.get('/')
async def index():
    """Serve the web interface"""
    return FileResponse('templates/index.html')

class ChatRequest(BaseModel):
    question: str

@app.post('/chat')
async def chat(request: ChatRequest):
    # Get relevant context from ChromaDB
    context = chromadb_connector.query_chromadb(request.question)
    
    # Check if AI provider is available
    if ai_provider is None:
        return {
            'answer': 'AI provider not available. Please check your configuration.',
            'error': 'AI provider initialization failed'
        }
    
    # Compose a focused prompt
    system_prompt = """You are an expert on this application. Only answer questions about this specific project, using the provided context and metadata. Do not answer questions outside the scope of this project. If the context doesn't contain relevant information, say so clearly."""
    
    user_prompt = f"""Context from project documentation:
{context}

Question: {request.question}

Please provide a clear, concise answer based only on the project context above."""
    
    # Prepare messages for AI provider
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        # Use async AI provider directly
        answer = await ai_provider.create_chat_completion(messages, temperature=0.2, max_tokens=1000)
        
        return {
            'answer': answer,
            'provider': ai_provider.get_provider_name(),
            'model': ai_provider.get_model_name()
        }
        
    except Exception as e:
        return {
            'answer': f'Error generating response: {str(e)}',
            'error': str(e)
        } 