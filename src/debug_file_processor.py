import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv
import logging
from file_processor import FileProcessor
from ai_providers import create_ai_provider
import asyncio

logger = logging.getLogger('java_analysis.debug_file_processor')

class DebugFileProcessor(FileProcessor):
    """Enhanced file processor with debug mode and pom.xml analysis capabilities"""
    
    def __init__(self):
        super().__init__()
        load_dotenv()
        
        # Debug configuration
        self.debug_file = os.getenv('DEBUGFILE')
        self.debug_mode = bool(self.debug_file and os.path.exists(self.debug_file))
        
        # Initialize AI provider for pom.xml analysis
        self.ai_provider = create_ai_provider()
        logger.info(f"Debug mode: {'enabled' if self.debug_mode else 'disabled'}")
        if self.debug_mode:
            logger.info(f"Debug file: {self.debug_file}")
    
    def process_files(self) -> List[Dict[str, Any]]:
        """Process files based on debug mode or normal mode"""
        if self.debug_mode:
            return self._process_debug_files()
        else:
            return super().process_files()
    
    def _process_debug_files(self) -> List[Dict[str, Any]]:
        """Process only the files listed in DEBUGFILE"""
        logger.info("Processing files in debug mode")
        
        # Read debug file
        debug_files = self._read_debug_file()
        if not debug_files:
            logger.warning("No files found in debug file, falling back to normal processing")
            return super().process_files()
        
        metadata_list = []
        processed_count = 0
        
        for file_path in debug_files:
            if not os.path.exists(file_path):
                logger.warning(f"Debug file not found: {file_path}")
                continue
            
            try:
                # Get file extension
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext in self.SUPPORTED_EXTENSIONS:
                    metadata = self._extract_file_metadata(file_path, ext)
                    
                    # Enhanced metadata for debug mode
                    metadata = self._enhance_debug_metadata(metadata)
                    
                    metadata_list.append(metadata)
                    processed_count += 1
                    logger.info(f"Processed debug file {processed_count}/{len(debug_files)}: {file_path}")
                    
                    # Find and analyze pom.xml in the same directory
                    pom_metadata = self._find_and_analyze_pom_xml(file_path)
                    if pom_metadata:
                        metadata['pom_analysis'] = pom_metadata
                        logger.info(f"Added pom.xml analysis for: {file_path}")
                        
                else:
                    logger.warning(f"Unsupported file type in debug mode: {file_path}")
                    
            except Exception as e:
                logger.error(f"Error processing debug file {file_path}: {str(e)}")
                continue
        
        logger.info(f"Debug mode: Processed {processed_count} files")
        return metadata_list
    
    def _read_debug_file(self) -> List[str]:
        """Read the debug file and return list of file paths"""
        try:
            with open(self.debug_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out empty lines and comments
            file_paths = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    file_paths.append(line)
            
            logger.info(f"Read {len(file_paths)} file paths from debug file")
            return file_paths
            
        except Exception as e:
            logger.error(f"Error reading debug file {self.debug_file}: {str(e)}")
            return []
    
    def _enhance_debug_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance metadata for debug mode with additional information"""
        metadata['debug_mode'] = True
        metadata['debug_file_source'] = self.debug_file
        
        # Add file statistics
        file_path = metadata.get('absolute_path', '')
        if file_path and os.path.exists(file_path):
            stat = os.stat(file_path)
            metadata['file_stats'] = {
                'size_bytes': stat.st_size,
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime,
                'access_time': stat.st_atime
            }
        
        return metadata
    
    def _find_and_analyze_pom_xml(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Find pom.xml in the same directory as the file and analyze it"""
        try:
            file_dir = os.path.dirname(file_path)
            pom_path = os.path.join(file_dir, 'pom.xml')
            
            if not os.path.exists(pom_path):
                # Look in parent directories
                current_dir = file_dir
                while current_dir and current_dir != os.path.dirname(current_dir):
                    pom_path = os.path.join(current_dir, 'pom.xml')
                    if os.path.exists(pom_path):
                        break
                    current_dir = os.path.dirname(current_dir)
                
                if not os.path.exists(pom_path):
                    return None
            
            logger.info(f"Found pom.xml: {pom_path}")
            return self._analyze_pom_xml(pom_path)
            
        except Exception as e:
            logger.error(f"Error finding/analyzing pom.xml for {file_path}: {str(e)}")
            return None
    
    def _analyze_pom_xml(self, pom_path: str) -> Dict[str, Any]:
        """Analyze pom.xml file and extract metadata"""
        try:
            with open(pom_path, 'r', encoding='utf-8') as f:
                pom_content = f.read()
            
            # Parse XML
            root = ET.fromstring(pom_content)
            
            # Extract basic information
            pom_metadata = {
                'pom_path': pom_path,
                'project_info': self._extract_project_info(root),
                'dependencies': self._extract_dependencies(root),
                'build_info': self._extract_build_info(root),
                'properties': self._extract_properties(root)
            }
            
            # Use AI to analyze pom.xml for enhanced metadata
            ai_analysis = asyncio.run(self._analyze_pom_with_ai(pom_content, pom_metadata))
            if ai_analysis:
                pom_metadata['ai_analysis'] = ai_analysis
            
            return pom_metadata
            
        except Exception as e:
            logger.error(f"Error analyzing pom.xml {pom_path}: {str(e)}")
            return {
                'pom_path': pom_path,
                'error': str(e)
            }
    
    def _extract_project_info(self, root: ET.Element) -> Dict[str, str]:
        """Extract basic project information from pom.xml"""
        info = {}
        
        # Extract common project elements
        elements = ['groupId', 'artifactId', 'version', 'packaging', 'name', 'description', 'url']
        for element in elements:
            elem = root.find(element)
            if elem is not None and elem.text:
                info[element] = elem.text.strip()
        
        return info
    
    def _extract_dependencies(self, root: ET.Element) -> List[Dict[str, str]]:
        """Extract dependencies from pom.xml"""
        dependencies = []
        
        # Handle both direct dependencies and dependency management
        for deps_section in ['dependencies', 'dependencyManagement/dependencies']:
            deps_elem = root.find(deps_section)
            if deps_elem is not None:
                for dep in deps_elem.findall('dependency'):
                    dep_info = {}
                    for child in ['groupId', 'artifactId', 'version', 'scope', 'optional']:
                        child_elem = dep.find(child)
                        if child_elem is not None and child_elem.text:
                            dep_info[child] = child_elem.text.strip()
                    
                    if dep_info:
                        dependencies.append(dep_info)
        
        return dependencies
    
    def _extract_build_info(self, root: ET.Element) -> Dict[str, Any]:
        """Extract build information from pom.xml"""
        build_info = {}
        
        build_elem = root.find('build')
        if build_elem is not None:
            # Extract plugins
            plugins = []
            plugins_elem = build_elem.find('plugins')
            if plugins_elem is not None:
                for plugin in plugins_elem.findall('plugin'):
                    plugin_info = {}
                    for child in ['groupId', 'artifactId', 'version']:
                        child_elem = plugin.find(child)
                        if child_elem is not None and child_elem.text:
                            plugin_info[child] = child_elem.text.strip()
                    
                    if plugin_info:
                        plugins.append(plugin_info)
            
            build_info['plugins'] = plugins
            
            # Extract other build elements
            for elem_name in ['sourceDirectory', 'testSourceDirectory', 'outputDirectory', 'testOutputDirectory']:
                elem = build_elem.find(elem_name)
                if elem is not None and elem.text:
                    build_info[elem_name] = elem.text.strip()
        
        return build_info
    
    def _extract_properties(self, root: ET.Element) -> Dict[str, str]:
        """Extract properties from pom.xml"""
        properties = {}
        
        props_elem = root.find('properties')
        if props_elem is not None:
            for prop in props_elem:
                if prop.text:
                    properties[prop.tag] = prop.text.strip()
        
        return properties
    
    async def _analyze_pom_with_ai(self, pom_content: str, pom_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Use AI to analyze pom.xml for enhanced metadata"""
        try:
            prompt = f"""Analyze this Maven pom.xml file and provide enhanced metadata:

POM Content:
{pom_content}

Extracted Metadata:
{json.dumps(pom_metadata, indent=2)}

Provide analysis in JSON format with the following structure:
{{
    "project_type": "string (e.g., web application, library, microservice)",
    "technology_stack": ["string"],
    "build_tools": ["string"],
    "deployment_target": "string (e.g., application server, container, cloud)",
    "key_features": ["string"],
    "architecture_patterns": ["string"],
    "integration_points": ["string"],
    "security_considerations": ["string"],
    "performance_characteristics": "string",
    "scalability_aspects": "string"
}}

Focus on identifying:
1. What type of application this is
2. Key technologies and frameworks used
3. Build and deployment characteristics
4. Architecture patterns
5. Integration requirements
6. Security and performance considerations
"""

            analysis = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert in Java enterprise applications and Maven project analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            # Try to parse as JSON
            try:
                return json.loads(analysis)
            except json.JSONDecodeError:
                logger.warning("AI response is not valid JSON, returning None")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing pom.xml with AI: {str(e)}")
            return None 