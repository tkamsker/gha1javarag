import os
from pathlib import Path
from typing import List, Dict, Any
import json
from dotenv import load_dotenv
import logging

logger = logging.getLogger('java_analysis.file_processor')

class FileProcessor:
    """Handles file traversal and metadata extraction from source code files"""
    
    SUPPORTED_EXTENSIONS = {
        '.java': 'Java source file',
        '.jsp': 'Java Server Page',
        '.xml': 'XML configuration',
        '.html': 'HTML file',
        '.js': 'JavaScript file',
        '.sql': 'SQL script'
    }

    def __init__(self):
        load_dotenv()
        logger.debug("Environment variables loaded")
        
        self.source_dir = os.getenv('JAVA_SOURCE_DIR')
        self.output_dir = os.getenv('OUTPUT_DIR')
        
        logger.debug(f"Source directory: {self.source_dir}")
        logger.debug(f"Output directory: {self.output_dir}")
        
        if not self.source_dir or not self.output_dir:
            raise ValueError("Required environment variables JAVA_SOURCE_DIR and OUTPUT_DIR must be set")
            
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def process_files(self) -> List[Dict[str, Any]]:
        """Process all files in the source directory and extract metadata"""
        logger.info(f"Processing files in {self.source_dir}")
        metadata_list = []
        
        try:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext in self.SUPPORTED_EXTENSIONS:
                        try:
                            metadata = self._extract_file_metadata(file_path, ext)
                            metadata_list.append(metadata)
                            logger.debug(f"Processed {file_path}")
                        except Exception as e:
                            logger.error(f"Error processing {file_path}: {str(e)}")
                            continue
        
        except Exception as e:
            logger.error(f"Error walking directory {self.source_dir}: {str(e)}")
            raise
            
        logger.info(f"Processed {len(metadata_list)} files")
        return metadata_list

    def _extract_file_metadata(self, file_path: str, extension: str) -> Dict[str, Any]:
        """Extract metadata from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            relative_path = os.path.relpath(file_path, self.source_dir)
            
            metadata = {
                'file_path': relative_path,
                'absolute_path': file_path,
                'file_type': self.SUPPORTED_EXTENSIONS[extension],
                'extension': extension,
                'size_bytes': os.path.getsize(file_path),
                'content': content,
                'last_modified': os.path.getmtime(file_path)
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {str(e)}")
            raise

    def save_metadata(self, metadata: List[Dict[str, Any]], output_file: str) -> None:
        """Save metadata to a JSON file"""
        logger.info(f"Saving metadata to: {output_file}")
        try:
            with open(output_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Successfully saved metadata to {output_file}")
        except Exception as e:
            logger.error(f"Error saving metadata: {str(e)}")
            raise 