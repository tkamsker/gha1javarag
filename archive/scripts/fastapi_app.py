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
    max_results: int = 10
    chunk_type: str = ''
    language: str = ''
    file_path: str = ''
    search_mode: str = 'semantic'

@app.post('/chat')
async def chat(request: ChatRequest):
    # Log the request details
    print(f"🔍 Chat request received:")
    print(f"   Question: {request.question}")
    print(f"   Max results: {request.max_results}")
    print(f"   Filters: chunk_type={request.chunk_type}, language={request.language}, file_path={request.file_path}")
    print(f"   Search mode: {request.search_mode}")
    
    # Build filters for enhanced querying
    filters = {}
    if request.chunk_type:
        filters['chunk_type'] = request.chunk_type
    if request.language:
        filters['language'] = request.language
    if request.file_path:
        filters['file_path'] = request.file_path
    
    # Create enhanced ChromaDB connector if not available
    if not hasattr(chat, 'chromadb_connector_instance'):
        try:
            chat.chromadb_connector_instance = chromadb_connector.EnhancedChromaDBConnector()
            print("Initialized enhanced ChromaDB connector")
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB connector: {e}")
            chat.chromadb_connector_instance = None
    
    # Get relevant context from ChromaDB with enhanced filtering
    if chat.chromadb_connector_instance:
        try:
            # Adjust query based on search mode
            if request.search_mode == 'keyword':
                # For keyword search, use the question as-is
                query = request.question
            elif request.search_mode == 'exact':
                # For exact match, wrap in quotes
                query = f'"{request.question}"'
            else:
                # For semantic search, use the question as-is
                query = request.question
            
            print(f"🔍 Querying ChromaDB with: '{query}'")
            print(f"   Filters: {filters}")
            print(f"   Max results: {request.max_results}")
            
            results = chat.chromadb_connector_instance.query_enhanced_similar(query, request.max_results, filters)
            
            if results and results.get('documents') and results['documents'][0]:
                print(f"✅ Found {len(results['documents'][0])} results from ChromaDB")
                context = chromadb_connector._format_enhanced_results(results)
            else:
                print("⚠️ No results found in ChromaDB")
                context = "No relevant context found in the database. Try a different search term or check if the database has been populated."
                
        except Exception as e:
            print(f"❌ ChromaDB query error: {str(e)}")
            context = f"Error querying ChromaDB: {str(e)}"
    else:
        # Fallback to legacy method
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
            'model': ai_provider.get_model_name(),
            'filters_applied': {
                'chunk_type': request.chunk_type,
                'language': request.language,
                'file_path': request.file_path,
                'search_mode': request.search_mode,
                'max_results': request.max_results
            }
        }
        
    except Exception as e:
        return {
            'answer': f'Error generating response: {str(e)}',
            'error': str(e)
        } 