"""Script to generate documentation."""

import os
import logging
from pathlib import Path
from doc_generator import DocumentationGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Generate documentation for the codebase."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Set up paths
    template_dir = project_root / "documentation" / "templates"
    codebase_path = project_root / "src"
    output_dir = project_root / "documentation" / "generated"
    
    # Create documentation generator
    generator = DocumentationGenerator(str(template_dir))
    
    # Generate all documentation
    logger.info("Generating documentation...")
    generator.generate_all_docs(str(codebase_path), str(output_dir))
    logger.info(f"Documentation generated in {output_dir}")

if __name__ == "__main__":
    main() 