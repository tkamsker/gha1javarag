from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import sys
import os
import logging
from pathlib import Path
import time
from contextlib import asynccontextmanager
import requests

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.file_processor import FileProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
processor = None
startup_time = time.time()

def check_chromadb_health():
    """Check ChromaDB server health using v2 API."""
    try:
        response = requests.get(
            "https://chromadb.dev.motorenflug.at/api/v2/heartbeat",
            verify=True,
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"ChromaDB health check failed: {str(e)}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    global processor
    try:
        # Check ChromaDB health before initializing
        if not check_chromadb_health():
            raise Exception("ChromaDB server is not healthy")
            
        # Initialize processor on startup
        processor = FileProcessor()
        logger.info("Successfully initialized FileProcessor on startup")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize FileProcessor on startup: {str(e)}")
        yield
    finally:
        # Cleanup on shutdown
        if processor is not None:
            try:
                # Add any cleanup code here if needed
                pass
            except Exception as e:
                logger.error(f"Error during cleanup: {str(e)}")

app = FastAPI(
    title="Code Search API",
    description="API for semantic search in code using ChromaDB",
    version="1.0.0",
    lifespan=lifespan
)

def get_processor():
    """Dependency to get the FileProcessor instance."""
    global processor
    if processor is None:
        try:
            processor = FileProcessor()
        except Exception as e:
            logger.error(f"Failed to initialize FileProcessor: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable. Please try again later."
            )
    return processor

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="The search query")
    file_types: Optional[List[str]] = Field(
        default=None,
        description="List of file types to search in (e.g., ['java', 'xml', 'json', 'html', 'sql'])"
    )
    n_results: Optional[int] = Field(default=5, ge=1, le=20, description="Number of results to return")

class SearchResult(BaseModel):
    code: str
    metadata: Dict[str, Any]

class IngestRequest(BaseModel):
    directory_path: str = Field(..., description="Path to the directory containing code files")

@app.get("/")
async def root():
    """Health check endpoint."""
    global processor
    status = "healthy"
    message = "Code Search API is running"
    
    # Check ChromaDB connection
    try:
        if not check_chromadb_health():
            status = "degraded"
            message = "ChromaDB server is not healthy"
        elif processor is None:
            processor = FileProcessor()
    except Exception as e:
        status = "degraded"
        message = f"ChromaDB connection issue: {str(e)}"
    
    return {
        "status": status,
        "message": message,
        "version": "1.0.0",
        "uptime": time.time() - startup_time
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    try:
        # Check ChromaDB health
        if not check_chromadb_health():
            raise HTTPException(
                status_code=503,
                detail="ChromaDB server is not healthy"
            )
            
        # Check processor
        proc = get_processor()
        
        return {
            "status": "healthy",
            "chromadb": "connected",
            "tree_sitter": "initialized",
            "supported_file_types": ["java", "xml", "json", "html", "sql"],
            "uptime": time.time() - startup_time
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.post("/search", response_model=List[SearchResult])
async def search_code(query: SearchQuery, proc: FileProcessor = Depends(get_processor)):
    """Search for code segments using semantic similarity."""
    try:
        logger.info(f"Processing search query: {query.query}")
        results = proc.search_code(
            query.query,
            file_types=query.file_types,
            n_results=query.n_results
        )
        logger.info(f"Found {len(results)} results for query: {query.query}")
        return results
    except Exception as e:
        logger.error(f"Error processing search query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process search query: {str(e)}"
        )

@app.post("/ingest")
async def ingest_directory(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    proc: FileProcessor = Depends(get_processor)
):
    """Ingest code files from a directory."""
    try:
        directory_path = request.directory_path
        if not os.path.exists(directory_path):
            raise HTTPException(
                status_code=404,
                detail=f"Directory not found: {directory_path}"
            )
            
        # Check for supported files
        supported_extensions = {'.java', '.xml', '.json', '.html', '.htm', '.sql'}
        has_supported_files = any(
            Path(directory_path).rglob(f"*{ext}")
            for ext in supported_extensions
        )
        
        if not has_supported_files:
            raise HTTPException(
                status_code=400,
                detail=f"No supported files found in directory: {directory_path}"
            )
            
        # Process in background to avoid timeout
        background_tasks.add_task(proc.process_directory, directory_path)
        
        return {
            "message": f"Started processing directory: {directory_path}",
            "status": "processing",
            "supported_file_types": list(supported_extensions)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing ingest request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process directory: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    ) 