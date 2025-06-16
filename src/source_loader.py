import os
from pathlib import Path
import yaml
from typing import List, Dict, Tuple
from dotenv import load_dotenv

class SourceLoader:
    def __init__(self, config_path: str = "config/app.yaml"):
        # Load environment variables
        load_dotenv()
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Get source directory from environment variable
        source_dir = os.getenv('JAVA_SOURCE_DIR')
        if not source_dir:
            raise ValueError("JAVA_SOURCE_DIR environment variable is not set")
        
        self.source_dir = source_dir
        self.file_extensions = self.config['source']['file_extensions']
        
        # Validate source directory exists
        if not os.path.exists(self.source_dir):
            raise ValueError(f"Source directory does not exist: {self.source_dir}")

    def get_source_files(self) -> List[Path]:
        """Get all source files matching the configured extensions"""
        source_files = []
        for ext in self.file_extensions:
            source_files.extend(Path(self.source_dir).rglob(f"*{ext}"))
        return source_files

    def read_file_content(self, file_path: Path) -> str:
        """Read file content with proper encoding handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 fails
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def process_files(self) -> Tuple[List[str], List[Dict], List[str]]:
        """Process all source files and return documents, metadata, and IDs"""
        documents = []
        metadatas = []
        ids = []
        
        for file_path in self.get_source_files():
            content = self.read_file_content(file_path)
            relative_path = str(file_path.relative_to(self.source_dir))
            
            documents.append(content)
            metadatas.append({
                "source": relative_path,
                "file_type": file_path.suffix[1:],
                "file_size": os.path.getsize(file_path)
            })
            ids.append(f"doc_{len(ids)}")
        
        return documents, metadatas, ids 