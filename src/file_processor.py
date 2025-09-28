import os
import glob
from pathlib import Path
from typing import List, Dict, Any, Set
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
        '.sql': 'SQL script',
        '.properties': 'Properties file',
        '.yaml': 'YAML configuration',
        '.yml': 'YAML configuration'
    }
    
    # Enhanced Java source patterns for comprehensive discovery
    JAVA_SOURCE_PATTERNS = [
        "src/main/java/**/*.java",      # Standard Maven structure
        "src/java/**/*.java",           # Alternative Maven structure  
        "src/**/*.java",                # Generic source structure
        "webapp/WEB-INF/**/*.java",     # Web application classes
        "web-inf/**/*.java",            # Web-INF classes
        "**/*DAO*.java",               # Data Access Objects
        "**/*DTO*.java",               # Data Transfer Objects
        "**/*Repository*.java",        # Repository pattern
        "**/*Service*.java",           # Business services
        "**/*Entity*.java",            # Domain entities
        "**/*Model*.java",             # Data models
        "**/*Bean*.java",              # Enterprise/POJO beans
        "**/*Controller*.java",        # Web controllers
        "**/*Manager*.java",           # Business managers
        "**/*Processor*.java",         # Data processors
        "**/*Handler*.java",           # Event/request handlers
        "**/*Client*.java",            # External service clients
        "**/*Adapter*.java",           # Adapter pattern
        "**/*Facade*.java",            # Facade pattern
        "**/*Factory*.java",           # Factory pattern
        "src/test/java/**/*.java",     # Test files (keep for completeness)
        "test/java/**/*.java",         # Alternative test structure
    ]
    
    # Configuration file patterns
    CONFIG_PATTERNS = [
        "**/*.xml",                    # All XML files
        "**/*.properties",             # Properties files
        "**/*.yaml",                   # YAML config files
        "**/*.yml",                    # YAML config files
        "**/applicationContext*.xml",   # Spring contexts
        "**/web.xml",                  # Web deployment descriptor
        "**/persistence.xml",          # JPA configuration
        "**/struts*.xml",              # Struts configuration
        "**/hibernate*.xml",           # Hibernate configuration
        "**/mybatis*.xml",             # MyBatis configuration
    ]
    
    # Skip patterns for files that shouldn't be processed
    SKIP_PATTERNS = [
        "**/target/**",                # Maven build output
        "**/build/**",                 # Gradle build output
        "**/.git/**",                  # Git files
        "**/.svn/**",                  # SVN files
        "**/node_modules/**",          # Node.js modules
        "**/*.class",                  # Compiled Java classes
        "**/*.jar",                    # JAR files
        "**/*.war",                    # WAR files
        "**/*.ear",                    # EAR files
        "**/*.zip",                    # ZIP archives
        "**/.*",                       # Hidden files
    ]

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
        """Process all files using enhanced pattern-based discovery"""
        logger.info(f"Processing files in {self.source_dir} using enhanced discovery patterns")
        metadata_list = []
        processed_files: Set[str] = set()
        
        try:
            # Phase 1: Discover Java source files using priority patterns
            java_files = self._discover_java_files()
            logger.info(f"Found {len(java_files)} Java source files")
            
            # Phase 2: Discover configuration files
            config_files = self._discover_config_files()
            logger.info(f"Found {len(config_files)} configuration files")
            
            # Phase 3: Discover other supported files (JSP, HTML, JS, SQL)
            other_files = self._discover_other_files()
            logger.info(f"Found {len(other_files)} other supported files")
            
            # Combine all discovered files
            all_files = java_files + config_files + other_files
            
            # Process files with priority (Java first, then config, then others)
            priority_files = self._prioritize_files(all_files)
            
            for file_info in priority_files:
                file_path = file_info['path']
                if file_path not in processed_files:
                    try:
                        metadata = self._extract_file_metadata_enhanced(file_info)
                        metadata_list.append(metadata)
                        processed_files.add(file_path)
                        logger.debug(f"Processed {file_path} (category: {file_info['category']})")
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {str(e)}")
                        continue
        
        except Exception as e:
            logger.error(f"Error in enhanced file processing: {str(e)}")
            raise
            
        logger.info(f"Enhanced processing completed: {len(metadata_list)} files processed")
        return metadata_list

    def _discover_java_files(self) -> List[Dict[str, Any]]:
        """Discover Java files using comprehensive patterns"""
        java_files = []
        
        for pattern in self.JAVA_SOURCE_PATTERNS:
            pattern_path = os.path.join(self.source_dir, pattern)
            matches = glob.glob(pattern_path, recursive=True)
            
            for match in matches:
                if self._should_process_file(match):
                    # Determine file category based on naming patterns
                    category = self._categorize_java_file(match)
                    java_files.append({
                        'path': match,
                        'pattern': pattern,
                        'category': category,
                        'priority': self._get_file_priority(match, category)
                    })
                    
        # Remove duplicates while preserving the highest priority entry
        return self._deduplicate_files(java_files)

    def _discover_config_files(self) -> List[Dict[str, Any]]:
        """Discover configuration files"""
        config_files = []
        
        for pattern in self.CONFIG_PATTERNS:
            pattern_path = os.path.join(self.source_dir, pattern)
            matches = glob.glob(pattern_path, recursive=True)
            
            for match in matches:
                if self._should_process_file(match):
                    config_files.append({
                        'path': match,
                        'pattern': pattern,
                        'category': 'configuration',
                        'priority': 50  # Medium priority for config files
                    })
                    
        return self._deduplicate_files(config_files)

    def _discover_other_files(self) -> List[Dict[str, Any]]:
        """Discover other supported files (JSP, HTML, JS, SQL)"""
        other_files = []
        
        # Use traditional directory walk for remaining file types
        try:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if (ext in self.SUPPORTED_EXTENSIONS and 
                        ext != '.java' and ext not in ['.xml', '.properties', '.yaml', '.yml'] and
                        self._should_process_file(file_path)):
                        
                        category = self._categorize_non_java_file(file_path, ext)
                        other_files.append({
                            'path': file_path,
                            'pattern': 'directory_walk',
                            'category': category,
                            'priority': self._get_file_priority(file_path, category)
                        })
        except Exception as e:
            logger.warning(f"Error in directory walk for other files: {e}")
            
        return other_files

    def _should_process_file(self, file_path: str) -> bool:
        """Check if file should be processed based on skip patterns"""
        abs_path = os.path.abspath(file_path)
        
        for skip_pattern in self.SKIP_PATTERNS:
            # Convert glob pattern to path check
            if skip_pattern.startswith('**/'):
                # Pattern like "**/*.class"
                if skip_pattern.endswith('/**'):
                    # Directory pattern like "**/target/**"
                    dir_name = skip_pattern[3:-3]  # Remove **/ and /**
                    if f"/{dir_name}/" in abs_path or abs_path.endswith(f"/{dir_name}"):
                        return False
                else:
                    # File pattern like "**/*.class"
                    if abs_path.endswith(skip_pattern[3:]):  # Remove **/
                        return False
            elif skip_pattern.startswith('**/') and skip_pattern.endswith('/**'):
                # Handle directory patterns
                dir_name = skip_pattern[3:-3]
                if f"/{dir_name}/" in abs_path:
                    return False
                    
        return True

    def _categorize_java_file(self, file_path: str) -> str:
        """Categorize Java file based on naming conventions and path"""
        file_name = os.path.basename(file_path)
        path_lower = file_path.lower()
        
        # Entity/Model detection
        if any(pattern in file_name for pattern in ['Entity', 'Model']) or '/entity/' in path_lower:
            return 'entity'
        # DAO/Repository detection  
        elif any(pattern in file_name for pattern in ['DAO', 'Dao', 'Repository']) or '/dao/' in path_lower:
            return 'dao'
        # DTO detection
        elif any(pattern in file_name for pattern in ['DTO', 'Dto']) or '/dto/' in path_lower:
            return 'dto'
        # Service detection
        elif any(pattern in file_name for pattern in ['Service', 'Manager']) or '/service/' in path_lower:
            return 'service'
        # Controller detection
        elif any(pattern in file_name for pattern in ['Controller', 'Servlet']) or '/controller/' in path_lower:
            return 'controller'
        # Test files
        elif '/test/' in path_lower or file_name.endswith('Test.java'):
            return 'test'
        # Business logic
        elif any(pattern in file_name for pattern in ['Processor', 'Handler', 'Facade']):
            return 'business_logic'
        # Utility/Helper
        elif any(pattern in file_name for pattern in ['Util', 'Helper', 'Common']):
            return 'utility'
        else:
            return 'general_java'

    def _categorize_non_java_file(self, file_path: str, extension: str) -> str:
        """Categorize non-Java files"""
        if extension == '.jsp':
            return 'web_ui'
        elif extension in ['.html', '.js']:
            return 'web_static'
        elif extension == '.sql':
            return 'database'
        else:
            return 'other'

    def _get_file_priority(self, file_path: str, category: str) -> int:
        """Assign processing priority based on file category (lower = higher priority)"""
        priority_map = {
            'entity': 1,        # Highest priority
            'dao': 2,
            'dto': 3,
            'service': 10,
            'controller': 15,
            'business_logic': 20,
            'configuration': 50,
            'web_ui': 60,
            'web_static': 70,
            'database': 30,
            'utility': 80,
            'test': 90,        # Lower priority for tests
            'general_java': 40,
            'other': 100       # Lowest priority
        }
        return priority_map.get(category, 100)

    def _deduplicate_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate files, keeping the one with highest priority"""
        file_map = {}
        
        for file_info in files:
            path = file_info['path']
            if path not in file_map or file_info['priority'] < file_map[path]['priority']:
                file_map[path] = file_info
                
        return list(file_map.values())

    def _prioritize_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort files by processing priority"""
        return sorted(files, key=lambda x: x['priority'])

    def _extract_file_metadata_enhanced(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata with enhanced categorization"""
        file_path = file_info['path']
        extension = os.path.splitext(file_path)[1].lower()
        
        try:
            content = self._read_file_with_encoding_detection(file_path)
            relative_path = os.path.relpath(file_path, self.source_dir)
            
            metadata = {
                'file_path': relative_path,
                'absolute_path': file_path,
                'file_type': self.SUPPORTED_EXTENSIONS.get(extension, 'Unknown file type'),
                'extension': extension,
                'size_bytes': os.path.getsize(file_path),
                'content': content,
                'last_modified': os.path.getmtime(file_path),
                'category': file_info['category'],
                'discovery_pattern': file_info['pattern'],
                'processing_priority': file_info['priority']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting enhanced metadata from {file_path}: {str(e)}")
            raise

    def _extract_file_metadata(self, file_path: str, extension: str) -> Dict[str, Any]:
        """Extract metadata from a single file with robust encoding handling"""
        try:
            content = self._read_file_with_encoding_detection(file_path)
                
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

    def _read_file_with_encoding_detection(self, file_path: str) -> str:
        """Read file content with multiple encoding attempts"""
        # List of encodings to try in order
        encodings = [
            'utf-8',           # Standard UTF-8
            'utf-8-sig',       # UTF-8 with BOM
            'iso-8859-1',      # Latin-1 (very permissive)
            'cp1252',          # Windows Western European
            'cp1250',          # Windows Central European  
            'iso-8859-15',     # Latin-9 (includes Euro symbol)
            'ascii'            # Plain ASCII
        ]
        
        last_exception = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                logger.debug(f"Successfully read {file_path} with encoding: {encoding}")
                return content
            except UnicodeDecodeError as e:
                logger.debug(f"Failed to read {file_path} with {encoding}: {e}")
                last_exception = e
                continue
            except Exception as e:
                logger.debug(f"Unexpected error reading {file_path} with {encoding}: {e}")
                last_exception = e
                continue
        
        # If all encodings fail, try binary read and replace invalid chars
        try:
            logger.warning(f"All text encodings failed for {file_path}, trying binary mode with error replacement")
            with open(file_path, 'rb') as f:
                binary_content = f.read()
            
            # Try to decode as UTF-8 with error replacement
            content = binary_content.decode('utf-8', errors='replace')
            logger.warning(f"Used UTF-8 with character replacement for {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Complete failure reading {file_path}: {e}")
            # Return a placeholder content with error info
            return f"# File reading failed: {file_path}\n# Error: {str(e)}\n# Original exception: {str(last_exception)}"

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