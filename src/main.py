import os
import logging
from pathlib import Path
from typing import Dict, List, Any
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import chromadb
from chromadb.config import Settings
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DoxygenHTMLProcessor:
    def __init__(self, html_dir: str):
        """Initialize the Doxygen HTML processor."""
        self.html_dir = Path(html_dir)
        if not self.html_dir.exists():
            raise ValueError(f"HTML directory {html_dir} does not exist")
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="data/chromadb",
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="doxygen_docs",
            metadata={"description": "Doxygen documentation for requirements analysis"}
        )

    def extract_class_info(self, html_file: Path) -> Dict[str, Any]:
        """Extract class information from a Doxygen HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Try different patterns for class name
            class_name = None
            for pattern in ['h1.title', 'h1', 'div.title']:
                element = soup.select_one(pattern)
                if element:
                    class_name = element.text.strip()
                    break
            
            if not class_name:
                logger.warning(f"Could not find class name in {html_file}")
                return None
            
            # Try different patterns for brief description
            brief_desc = ""
            for pattern in ['div.brief', 'div.detailed', 'div.description']:
                element = soup.select_one(pattern)
                if element:
                    brief_desc = element.text.strip()
                    break
            
            # Try different patterns for detailed description
            detailed_desc = ""
            for pattern in ['div.detailed', 'div.description', 'div.documentation']:
                element = soup.select_one(pattern)
                if element:
                    detailed_desc = element.text.strip()
                    break
            
            # Extract methods with more flexible patterns
            methods = []
            for method_div in soup.find_all(['div', 'tr'], class_=['memitem', 'memproto']):
                method_name = None
                method_desc = None
                
                # Try different patterns for method name
                for name_pattern in ['div.memname', 'td.memname', 'td.memproto']:
                    name_elem = method_div.select_one(name_pattern)
                    if name_elem:
                        method_name = name_elem.text.strip()
                        break
                
                # Try different patterns for method description
                for desc_pattern in ['div.memdoc', 'td.memdoc', 'td.memdesc']:
                    desc_elem = method_div.select_one(desc_pattern)
                    if desc_elem:
                        method_desc = desc_elem.text.strip()
                        break
                
                if method_name and method_desc:
                    methods.append({
                        'name': method_name,
                        'description': method_desc
                    })
            
            # If no methods found, try alternative approach
            if not methods:
                for method_div in soup.find_all(['div', 'tr'], class_=['memitem', 'memproto']):
                    text = method_div.get_text(strip=True)
                    if text and len(text) > 10:  # Basic validation
                        methods.append({
                            'name': text.split('\n')[0],  # First line as name
                            'description': text  # Full text as description
                        })
            
            return {
                'name': class_name,
                'brief': brief_desc,
                'detailed': detailed_desc,
                'methods': methods,
                'file': str(html_file),
                'type': 'class'
            }
            
        except Exception as e:
            logger.error(f"Error processing {html_file}: {str(e)}")
            return None

    def process_html_files(self):
        """Process all HTML files in the Doxygen output directory."""
        logger.info("Processing Doxygen HTML files...")
        
        # Find all HTML files that might contain class information
        html_files = []
        for pattern in ['class*.html', '*.html']:
            html_files.extend(list(self.html_dir.glob(pattern)))
        
        # Remove duplicates while preserving order
        html_files = list(dict.fromkeys(html_files))
        logger.info(f"Found {len(html_files)} HTML files")
        
        # Process each HTML file
        processed_count = 0
        for html_file in html_files:
            try:
                class_info = self.extract_class_info(html_file)
                if class_info:
                    # Store in ChromaDB
                    self.collection.add(
                        documents=[json.dumps(class_info)],
                        metadatas=[{
                            'name': class_info['name'],
                            'type': class_info['type'],
                            'file': class_info['file'],
                            'timestamp': datetime.now().isoformat()
                        }],
                        ids=[f"class_{class_info['name']}"]
                    )
                    processed_count += 1
                    logger.info(f"Processed class: {class_info['name']}")
                else:
                    logger.warning(f"No class information found in {html_file}")
            
            except Exception as e:
                logger.error(f"Error processing {html_file}: {str(e)}")
                continue
        
        logger.info(f"Successfully processed {processed_count} out of {len(html_files)} files")

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get HTML output directory
        html_dir = os.getenv('HTML_OUTPUT_DIR')
        if not html_dir:
            raise ValueError("HTML_OUTPUT_DIR environment variable not set")
        
        # Initialize processor
        processor = DoxygenHTMLProcessor(html_dir)
        
        # Process HTML files
        processor.process_html_files()
        
        logger.info("Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in pipeline execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 