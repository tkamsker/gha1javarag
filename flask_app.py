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
import src.chromadb_connector as chromadb_connector
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

# Create enhanced ChromaDB connector
try:
    chromadb_connector_instance = chromadb_connector.EnhancedChromaDBConnector()
    print("Initialized enhanced ChromaDB connector")
except Exception as e:
    print(f"Warning: Could not initialize ChromaDB connector: {e}")
    chromadb_connector_instance = None

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/stats')
def get_stats():
    """Get ChromaDB statistics"""
    if chromadb_connector_instance is None:
        return jsonify({'error': 'ChromaDB not available'}), 500
    
    try:
        stats = chromadb_connector_instance.get_chunk_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/chromadb')
def debug_chromadb():
    """Debug endpoint to examine ChromaDB contents"""
    if chromadb_connector_instance is None:
        return jsonify({'error': 'ChromaDB not available'}), 500
    
    try:
        # Get statistics
        stats = chromadb_connector_instance.get_chunk_statistics()
        
        # Get sample documents
        sample_results = chromadb_connector_instance.query_enhanced_similar("", n_results=10)
        
        debug_info = {
            'statistics': stats,
            'sample_documents': []
        }
        
        if sample_results and sample_results.get('documents') and sample_results['documents'][0]:
            documents = sample_results['documents'][0]
            metadatas = sample_results['metadatas'][0]
            
            for i, doc in enumerate(documents[:5]):  # Show first 5
                metadata = metadatas[i] if i < len(metadatas) else {}
                debug_info['sample_documents'].append({
                    'file_path': metadata.get('file_path', 'unknown'),
                    'chunk_type': metadata.get('chunk_type', 'unknown'),
                    'language': metadata.get('language', 'unknown'),
                    'content_preview': doc[:200] + '...' if len(doc) > 200 else doc
                })
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/query/<query>')
def debug_query(query):
    """Debug endpoint to test specific ChromaDB queries"""
    if chromadb_connector_instance is None:
        return jsonify({'error': 'ChromaDB not available'}), 500
    
    try:
        # URL decode the query
        import urllib.parse
        decoded_query = urllib.parse.unquote(query)
        
        print(f"🔍 DEBUG QUERY: '{decoded_query}'")
        
        # Test the query
        results = chromadb_connector_instance.query_enhanced_similar(decoded_query, n_results=5)
        
        debug_info = {
            'query': decoded_query,
            'raw_results': results,
            'formatted_context': chromadb_connector._format_enhanced_results(results) if results else "No results",
            'results': []
        }
        
        if results and results.get('documents') and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            
            for i, doc in enumerate(documents):
                metadata = metadatas[i] if i < len(metadatas) else {}
                debug_info['results'].append({
                    'file_path': metadata.get('file_path', 'unknown'),
                    'chunk_type': metadata.get('chunk_type', 'unknown'),
                    'language': metadata.get('language', 'unknown'),
                    'content': doc,
                    'content_length': len(doc)
                })
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    max_results = data.get('max_results', 10)
    chunk_type = data.get('chunk_type', '')
    language = data.get('language', '')
    file_path = data.get('file_path', '')
    search_mode = data.get('search_mode', 'semantic')
    
    # Log the request details
    print(f"🔍 Chat request received:")
    print(f"   Question: {question}")
    print(f"   Max results: {max_results}")
    print(f"   Filters: chunk_type={chunk_type}, language={language}, file_path={file_path}")
    print(f"   Search mode: {search_mode}")
    
    # Build filters for enhanced querying
    filters = {}
    if chunk_type:
        filters['chunk_type'] = chunk_type
    if language:
        filters['language'] = language
    if file_path:
        filters['file_path'] = file_path
    
    # Get relevant context from ChromaDB with enhanced filtering
    if chromadb_connector_instance:
        try:
            # Adjust query based on search mode
            if search_mode == 'keyword':
                # For keyword search, use the question as-is
                query = question
            elif search_mode == 'exact':
                # For exact match, wrap in quotes
                query = f'"{question}"'
            else:
                # For semantic search, use the question as-is
                query = question
            
            print(f"🔍 Querying ChromaDB with: '{query}'")
            print(f"   Filters: {filters}")
            print(f"   Max results: {max_results}")
            
            results = chromadb_connector_instance.query_enhanced_similar(query, max_results, filters)
            
            if results and results.get('documents') and results['documents'][0]:
                print(f"✅ Found {len(results['documents'][0])} results from ChromaDB")
                
                # Log detailed ChromaDB results for debugging
                print(f"\n📊 CHROMADB RESULTS DEBUG:")
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                
                for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
                    print(f"  Result {i+1}:")
                    print(f"    File: {metadata.get('file_path', 'unknown')}")
                    print(f"    Type: {metadata.get('chunk_type', 'unknown')}")
                    print(f"    Language: {metadata.get('language', 'unknown')}")
                    print(f"    Content Length: {len(doc)} characters")
                    print(f"    Content Preview: {doc[:200]}...")
                    print()
                
                context = chromadb_connector._format_enhanced_results(results)
                print(f"📝 FORMATTED CONTEXT DEBUG:")
                print(f"Context Length: {len(context)} characters")
                print(f"Context Preview: {context[:500]}...")
            else:
                print("⚠️ No results found in ChromaDB")
                context = "No relevant context found in the database. Try a different search term or check if the database has been populated."
                
        except Exception as e:
            print(f"❌ ChromaDB query error: {str(e)}")
            context = f"Error querying ChromaDB: {str(e)}"
    else:
        print("❌ ChromaDB connector not available")
        context = "ChromaDB not available"
    
    # Check if AI provider is available
    if ai_provider is None:
        print("❌ AI provider not available")
        return jsonify({
            'answer': 'AI provider not available. Please check your configuration.',
            'error': 'AI provider initialization failed'
        }), 500
    
    # Compose a focused prompt
    system_prompt = """You are an expert on this application. Only answer questions about this specific project, using the provided context and metadata. Do not answer questions outside the scope of this project. If the context doesn't contain relevant information, say so clearly."""
    
    user_prompt = f"""Context from project documentation (with enhanced chunking):
{context}

Question: {question}

Please provide a clear, concise answer based only on the project context above. If the context shows specific functions, classes, or code structures, mention them in your answer."""
    
    # Log the complete prompt for debugging
    print(f"\n🤖 AI PROMPT DEBUG:")
    print(f"System Prompt: {system_prompt}")
    print(f"User Prompt: {user_prompt}")
    print(f"Context Length: {len(context)} characters")
    print(f"Context Preview: {context[:500]}...")
    
    # Prepare messages for AI provider
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        print(f"🤖 Sending request to AI provider: {ai_provider.get_provider_name()}")
        # Run async AI provider in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        answer = loop.run_until_complete(
            ai_provider.create_chat_completion(messages, temperature=0.2, max_tokens=1000)
        )
        loop.close()
        print(f"✅ AI response received (length: {len(answer) if answer else 0} chars)")
        print(f"🤖 AI RESPONSE DEBUG:")
        print(f"Answer: {answer}")
        
        return jsonify({
            'answer': answer,
            'provider': ai_provider.get_provider_name(),
            'model': ai_provider.get_model_name(),
            'filters_applied': {
                'chunk_type': chunk_type,
                'language': language,
                'file_path': file_path,
                'search_mode': search_mode,
                'max_results': max_results
            }
        })
        
    except Exception as e:
        print(f"❌ AI ERROR DEBUG:")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'answer': f'Error generating response: {str(e)}',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 