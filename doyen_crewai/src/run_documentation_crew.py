#!/usr/bin/env python3
"""Main script for running the documentation crew."""

import logging
from pathlib import Path
from dotenv import load_dotenv
import os
from agents.documentation_crew import DocumentationCrew

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the documentation crew."""
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get XML input directory from environment variable
        xml_input_dir = os.getenv('XML_INPUT_DIR')
        if not xml_input_dir:
            raise ValueError("XML_INPUT_DIR environment variable not set")
        
        logger.info(f"XML input directory: {xml_input_dir}")
        
        # Initialize and run the documentation crew
        crew = DocumentationCrew(Path(xml_input_dir))
        result = crew.generate_documentation()
        logger.info(f"Documentation generation completed: {result}")
        
    except Exception as e:
        logger.error(f"Error during documentation generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 