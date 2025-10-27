# Web Client for Weaviate Search

A beautiful web interface for querying your indexed codebase using natural language.

## 🚀 Quick Start

### Prerequisites
- Weaviate running on `http://localhost:8080`
- Virtual environment activated
- Dependencies installed

### Starting the Web Client

#### On macOS:
```bash
./start_web_client.sh
```

#### On Ubuntu/Linux:
```bash
./start_web_client.sh
```

The script will:
1. ✅ Check if Weaviate is running
2. ✅ Activate the virtual environment
3. ✅ Install missing dependencies (Flask, Flask-CORS)
4. ✅ Start the web server on `http://localhost:5000`

### Using the Interface

1. **Open your browser** to `http://localhost:5000`
2. **Type your question** in the search box
3. **View results** with artifact cards showing:
   - Type (BackendDoc, IbatisStatement, etc.)
   - File path
   - Summary/description

## 🎯 Example Queries

- "Show me all database tables"
- "Find all GWT activities"
- "What DAO methods exist?"
- "List all JSP forms"
- "Find API endpoints"
- "Show GWT module configurations"

## 🔍 Search Features

### Search Across Multiple Artifact Types
The web client searches across:
- **BackendDoc** - LLM-generated summaries of backend files
- **IbatisStatement** - SQL statements
- **DaoCall** - Data access object method calls
- **JspForm** - JSP form definitions
- **GwtModule** - GWT module descriptors
- **GwtActivityPlace** - GWT navigation patterns
- **JsArtifact** - JavaScript code artifacts
- **FrontendRoute** - Frontend routing information

### Natural Language Answers
The web client generates GPT-like answers based on found artifacts, providing:
- Summary of what was found
- Grouped results by artifact type
- File paths and descriptions
- Top matches with context

## 📁 File Structure

```
src/web/
  └── weaviate_client.py  # Flask web application

start_web_client.sh        # Cross-platform start script
```

## 🛠️ Manual Start

If you prefer to start manually:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install flask flask-cors

# Start the server
python src/web/weaviate_client.py
```

## 🌐 API Endpoints

### `GET /`
Returns the main chat interface (HTML)

### `GET /api/status`
Check Weaviate connection status
```json
{
  "connected": true
}
```

### `POST /api/query`
Query the codebase
```json
{
  "query": "show me all databases"
}
```

Response:
```json
{
  "answer": "Based on your question...",
  "artifacts": [
    {
      "class": "BackendDoc",
      "path": "...",
      "summary": "...",
      "text": "..."
    }
  ]
}
```

## 🎨 Features

- **Modern, beautiful UI** with gradient design
- **Real-time search** across your entire codebase
- **Natural language answers** similar to ChatGPT
- **Artifact cards** showing relevant code snippets
- **Chat-like interface** for easy interaction
- **Responsive design** works on desktop and mobile

## 🔧 Troubleshooting

### Weaviate Not Running
```
Error: Weaviate is not running!
```
**Solution:** Start Weaviate first:
```bash
./start_weaviate_simple.sh
```

### Port 5000 Already in Use
**Solution:** Change the port in `src/web/weaviate_client.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=False)
```

### Dependencies Missing
**Solution:** Install manually:
```bash
pip install flask flask-cors
```

## 💡 Tips

1. **Be specific** - More specific queries yield better results
2. **Use keywords** - Include class names, method names, or file types
3. **Try variations** - If one query doesn't work, try rephrasing
4. **Check artifact types** - Look at the artifact cards to understand what types are available

## 🎯 Next Steps

- Run the full pipeline to index your code:
  ```bash
  ./new_run.sh
  ```
  
- Search your indexed data:
  ```bash
  ./start_web_client.sh
  ```
  
- Open browser to `http://localhost:5000` and start exploring!
