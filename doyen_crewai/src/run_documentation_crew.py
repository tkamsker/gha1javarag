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
    """Main function to run documentation generation."""
    # Load environment variables
    load_dotenv()
    
    # Get XML input directory from environment
    xml_input_dir = os.getenv('XML_INPUT_DIR')
    if not xml_input_dir:
        logger.error("XML_INPUT_DIR environment variable not set")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path("generated_documentation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize and run documentation crew
        crew = DocumentationCrew(
            xml_input_dir=xml_input_dir,
            output_dir=str(output_dir)
        )
        
        # Generate documentation
        logger.info("Starting documentation generation...")
        crew.generate_documentation()
        
        logger.info("Documentation generation completed successfully")
        logger.info(f"Generated documentation can be found in: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error during documentation generation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 