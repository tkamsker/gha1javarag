#!/usr/bin/env python3
"""Script to run the documentation generation process."""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from agents.documentation_crew import DocumentationCrew

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for documentation generation."""
    try:
        # Get XML input directory from environment variable
        xml_input_dir = os.getenv("XML_INPUT_DIR")
        if not xml_input_dir:
            raise ValueError("XML_INPUT_DIR environment variable not set")
        
        # Initialize documentation crew
        crew = DocumentationCrew(Path(xml_input_dir))
        
        # Generate documentation
        logger.info("Starting documentation generation...")
        result = crew.generate_documentation()
        logger.info(f"Documentation generation result: {result}")
        
    except Exception as e:
        logger.error(f"Error during documentation generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 