"""Main entry point for the Doyen CrewAI application."""

import logging
import os
from pathlib import Path
import json

from dotenv import load_dotenv

from .agents.parser_agent import ParserAgent
from .preprocessing.chroma_loader import ChromaDBLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    try:
        # Initialize ChromaDB loader
        logger.info("Initializing ChromaDB loader...")
        chroma_loader = ChromaDBLoader(persist_directory=chroma_persist_dir)
        
        # Get collection stats
        stats = chroma_loader.get_collection_stats()
        if stats.get("total_entities", 0) == 0:
            raise ValueError(
                "No entities found in ChromaDB. Please run load_embeddings.py first."
            )
        logger.info(f"Found {stats['total_entities']} entities in ChromaDB")
        
        # Initialize and run parser agent
        logger.info("Initializing parser agent...")
        parser_agent = ParserAgent(chroma_loader)
        
        # Analyze codebase
        logger.info("Analyzing codebase...")
        results = parser_agent.analyze_codebase()
        
        # Save results
        output_dir = Path("docs")
        output_dir.mkdir(exist_ok=True)
        
        # Save analysis results
        with open(output_dir / "analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info("Analysis complete. Results saved to docs/analysis_results.json")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main() 