"""
Content-based Component Classification System
Replaces pattern-matching with LLM-based content analysis
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ComponentType(Enum):
    """Standardized component types for classification"""
    DAO = "dao"
    DTO = "dto" 
    SERVICE = "service"
    CONTROLLER = "controller"
    FRONTEND_VIEW = "frontend_view"
    FRONTEND_SCRIPT = "frontend_script"
    FRONTEND_STYLE = "frontend_style"
    CONFIGURATION = "configuration"
    BUILD_SCRIPT = "build_script"
    DOCUMENTATION = "documentation"
    TEST = "test"
    UNKNOWN = "unknown"
    EXCLUDE = "exclude"

@dataclass
class FileAnalysis:
    """Result of file content analysis"""
    file_path: str
    component_type: ComponentType
    confidence: float  # 0.0 to 1.0
    purpose: str
    business_logic: str
    api_endpoints: List[str]
    dependencies: List[str]
    annotations: List[str]
    key_methods: List[str]
    error_message: Optional[str] = None

class FileTypeDetector:
    """Detects file type and determines analysis strategy"""
    
    @staticmethod
    def get_file_category(file_path: str) -> str:
        """Categorize file by extension for targeted analysis"""
        extension = Path(file_path).suffix.lower()
        
        java_extensions = {'.java'}
        frontend_markup = {'.jsp', '.html', '.htm', '.xhtml'}
        frontend_script = {'.js', '.jsx', '.ts', '.tsx', '.vue'}
        frontend_style = {'.css', '.scss', '.sass', '.less'}
        config_files = {'.xml', '.json', '.properties', '.yml', '.yaml', '.conf'}
        build_files = {'.gradle', '.maven', '.pom'} 
        docs = {'.md', '.txt', '.rst', '.adoc'}
        exclude_files = {'.class', '.jar', '.war', '.log', '.tmp', '.bak'}
        
        if extension in java_extensions:
            return 'java'
        elif extension in frontend_markup:
            return 'frontend_markup'
        elif extension in frontend_script:
            return 'frontend_script'
        elif extension in frontend_style:
            return 'frontend_style'
        elif extension in config_files or 'pom.xml' in file_path.lower():
            return 'configuration'
        elif extension in build_files:
            return 'build'
        elif extension in docs:
            return 'documentation'
        elif extension in exclude_files:
            return 'exclude'
        else:
            return 'unknown'

class ContentAnalyzer:
    """LLM-based content analysis for component classification"""
    
    def __init__(self, llm_client, logger: logging.Logger):
        self.llm_client = llm_client
        self.logger = logger
        self.file_type_detector = FileTypeDetector()
        
        # Analysis prompts by file category
        self.analysis_prompts = {
            'java': self._create_java_analysis_prompt,
            'frontend_markup': self._create_markup_analysis_prompt,
            'frontend_script': self._create_script_analysis_prompt,
            'frontend_style': self._create_style_analysis_prompt,
            'configuration': self._create_config_analysis_prompt
        }
    
    def analyze_file_content(self, file_path: str, content: str, 
                           metadata: Optional[Dict[str, Any]] = None) -> FileAnalysis:
        """
        Analyze file content using LLM to determine component type and extract details
        """
        if not content or not content.strip():
            return FileAnalysis(
                file_path=file_path,
                component_type=ComponentType.EXCLUDE,
                confidence=1.0,
                purpose="Empty file",
                business_logic="",
                api_endpoints=[],
                dependencies=[],
                annotations=[],
                key_methods=[],
                error_message="File is empty or unreadable"
            )
        
        # Determine file category for targeted analysis
        file_category = self.file_type_detector.get_file_category(file_path)
        
        # Skip excluded file types
        if file_category == 'exclude':
            return self._create_excluded_analysis(file_path, "File type excluded from analysis")
        
        # Use targeted analysis based on file type
        try:
            if file_category in self.analysis_prompts:
                return self.analysis_prompts[file_category](file_path, content, metadata)
            else:
                return self._create_generic_analysis(file_path, content, file_category)
                
        except Exception as e:
            self.logger.error(f"Content analysis failed for {file_path}: {e}")
            return self._create_error_analysis(file_path, str(e))
    
    def _create_java_analysis_prompt(self, file_path: str, content: str, 
                                   metadata: Optional[Dict[str, Any]]) -> FileAnalysis:
        """Create targeted analysis for Java files"""
        
        # Truncate content if too long (keep imports, class declaration, key methods)
        analyzed_content = self._prepare_java_content_for_analysis(content)
        
        prompt = f"""Analyze this Java file and classify it precisely:

File: {file_path}
Content (first 2000 chars):
```java
{analyzed_content}
```

Classify this Java file into ONE of these categories:
- DAO: Data Access Object (contains @Repository, database queries, JPA/Hibernate code)
- DTO: Data Transfer Object (simple data containers, POJOs, entities with @Entity)  
- SERVICE: Business logic layer (@Service, @Component, complex business methods)
- CONTROLLER: Web controllers (@Controller, @RestController, HTTP endpoints)
- TEST: Test files (contains @Test, test methods, test classes)
- CONFIGURATION: Configuration classes (@Configuration, @ConfigurationProperties)
- EXCLUDE: Build files, generated code, or non-functional code

Return JSON response:
{{
  "component_type": "one of: dao, dto, service, controller, test, configuration, exclude",
  "confidence": 0.95,
  "purpose": "Brief description of what this class does",
  "business_logic": "Key business logic or 'none' if just data/config",
  "api_endpoints": ["list of HTTP endpoints if controller, empty otherwise"],
  "dependencies": ["key dependencies or injected services"],
  "annotations": ["@Repository", "@Service", etc.],
  "key_methods": ["important method names"]
}}

Be precise - don't guess. If unsure, use lower confidence and explain in purpose."""
        
        try:
            response = self.llm_client.generate_text(prompt, max_tokens=500)
            return self._parse_llm_response(file_path, response)
        except Exception as e:
            self.logger.error(f"LLM analysis failed for Java file {file_path}: {e}")
            return self._create_error_analysis(file_path, str(e))
    
    def _create_markup_analysis_prompt(self, file_path: str, content: str, 
                                     metadata: Optional[Dict[str, Any]]) -> FileAnalysis:
        """Create targeted analysis for HTML/JSP/markup files"""
        
        analyzed_content = content[:1500]  # Truncate for analysis
        
        prompt = f"""Analyze this web markup file:

File: {file_path}
Content (first 1500 chars):
```
{analyzed_content}
```

Classify as:
- FRONTEND_VIEW: User interface pages, forms, displays
- CONFIGURATION: Config templates, error pages
- EXCLUDE: Generated files, temporary files

Return JSON:
{{
  "component_type": "frontend_view, configuration, or exclude",
  "confidence": 0.90,
  "purpose": "What this page/template does",
  "business_logic": "UI business logic if any",
  "api_endpoints": ["AJAX/API calls found"],
  "dependencies": ["referenced scripts, includes"],
  "annotations": [],
  "key_methods": ["JavaScript functions if found"]
}}"""

        try:
            response = self.llm_client.generate_text(prompt, max_tokens=400)
            return self._parse_llm_response(file_path, response)
        except Exception as e:
            return self._create_error_analysis(file_path, str(e))
    
    def _create_script_analysis_prompt(self, file_path: str, content: str, 
                                     metadata: Optional[Dict[str, Any]]) -> FileAnalysis:
        """Create targeted analysis for JavaScript/TypeScript files"""
        
        analyzed_content = content[:2000]  # First 2000 chars for analysis
        
        prompt = f"""Analyze this JavaScript/TypeScript file:

File: {file_path}  
Content (first 2000 chars):
```javascript
{analyzed_content}
```

Classify as:
- FRONTEND_SCRIPT: UI logic, user interactions, form handling
- CONFIGURATION: Build configs, webpack, etc.
- TEST: Test files  
- EXCLUDE: Generated/minified files

Return JSON:
{{
  "component_type": "frontend_script, configuration, test, or exclude",
  "confidence": 0.85,
  "purpose": "What this script does",
  "business_logic": "Key UI/business logic",
  "api_endpoints": ["API calls made by this script"],
  "dependencies": ["imported modules/libraries"],
  "annotations": [],
  "key_methods": ["main functions"]
}}"""

        try:
            response = self.llm_client.generate_text(prompt, max_tokens=400)
            return self._parse_llm_response(file_path, response)
        except Exception as e:
            return self._create_error_analysis(file_path, str(e))
    
    def _create_style_analysis_prompt(self, file_path: str, content: str,
                                    metadata: Optional[Dict[str, Any]]) -> FileAnalysis:
        """Create analysis for CSS/SCSS files"""
        return FileAnalysis(
            file_path=file_path,
            component_type=ComponentType.FRONTEND_STYLE,
            confidence=0.95,
            purpose="Stylesheet for UI styling",
            business_logic="",
            api_endpoints=[],
            dependencies=[],
            annotations=[],
            key_methods=[]
        )
    
    def _create_config_analysis_prompt(self, file_path: str, content: str,
                                     metadata: Optional[Dict[str, Any]]) -> FileAnalysis:
        """Create analysis for configuration files"""
        
        # Quick content check for XML files that might be misclassified
        if 'pom.xml' in file_path.lower() or 'build.gradle' in file_path.lower():
            return FileAnalysis(
                file_path=file_path,
                component_type=ComponentType.BUILD_SCRIPT,
                confidence=0.98,
                purpose="Build configuration file",
                business_logic="",
                api_endpoints=[],
                dependencies=[],
                annotations=[],
                key_methods=[]
            )
        
        return FileAnalysis(
            file_path=file_path,
            component_type=ComponentType.CONFIGURATION,
            confidence=0.90,
            purpose="Configuration file",
            business_logic="",
            api_endpoints=[],
            dependencies=[],
            annotations=[],
            key_methods=[]
        )
    
    def _prepare_java_content_for_analysis(self, content: str) -> str:
        """Prepare Java content for LLM analysis by keeping important parts"""
        lines = content.split('\n')
        
        # Keep imports, package, class declaration, annotations, and key methods
        important_lines = []
        in_method = False
        method_count = 0
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Always include package, imports, class declarations, annotations
            if (line.startswith('package ') or 
                line.startswith('import ') or
                '@' in line or 
                'class ' in line or
                'interface ' in line or
                'enum ' in line):
                important_lines.append(line)
            
            # Include method signatures (limit to prevent token overflow)
            elif ('public ' in line or 'private ' in line or 'protected ' in line) and '(' in line:
                if method_count < 10:  # Limit method signatures
                    important_lines.append(line)
                    method_count += 1
        
        # Limit total length
        result = '\n'.join(important_lines)
        return result[:2000] if len(result) > 2000 else result
    
    def _parse_llm_response(self, file_path: str, response: str) -> FileAnalysis:
        """Parse LLM JSON response into FileAnalysis object"""
        try:
            # Clean response and extract JSON
            response = response.strip()
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0]
            elif '```' in response:
                response = response.split('```')[1].split('```')[0]
            
            data = json.loads(response)
            
            # Map component type string to enum
            component_type_str = data.get('component_type', 'unknown').lower()
            component_type = ComponentType.UNKNOWN
            
            for ct in ComponentType:
                if ct.value == component_type_str:
                    component_type = ct
                    break
            
            return FileAnalysis(
                file_path=file_path,
                component_type=component_type,
                confidence=float(data.get('confidence', 0.5)),
                purpose=data.get('purpose', ''),
                business_logic=data.get('business_logic', ''),
                api_endpoints=data.get('api_endpoints', []),
                dependencies=data.get('dependencies', []),
                annotations=data.get('annotations', []),
                key_methods=data.get('key_methods', [])
            )
            
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response for {file_path}: {e}")
            self.logger.debug(f"Raw response: {response}")
            return self._create_error_analysis(file_path, f"LLM response parsing error: {e}")
    
    def _create_excluded_analysis(self, file_path: str, reason: str) -> FileAnalysis:
        """Create analysis for excluded files"""
        return FileAnalysis(
            file_path=file_path,
            component_type=ComponentType.EXCLUDE,
            confidence=1.0,
            purpose=reason,
            business_logic="",
            api_endpoints=[],
            dependencies=[],
            annotations=[],
            key_methods=[]
        )
    
    def _create_error_analysis(self, file_path: str, error: str) -> FileAnalysis:
        """Create analysis for files that failed to analyze"""
        return FileAnalysis(
            file_path=file_path,
            component_type=ComponentType.UNKNOWN,
            confidence=0.0,
            purpose="Analysis failed",
            business_logic="",
            api_endpoints=[],
            dependencies=[],
            annotations=[],
            key_methods=[],
            error_message=error
        )
    
    def _create_generic_analysis(self, file_path: str, content: str, file_category: str) -> FileAnalysis:
        """Fallback analysis for unknown file types"""
        if file_category == 'documentation':
            component_type = ComponentType.DOCUMENTATION
            purpose = "Documentation file"
        elif file_category == 'build':
            component_type = ComponentType.BUILD_SCRIPT  
            purpose = "Build script"
        else:
            component_type = ComponentType.UNKNOWN
            purpose = f"Unknown file type: {file_category}"
        
        return FileAnalysis(
            file_path=file_path,
            component_type=component_type,
            confidence=0.8,
            purpose=purpose,
            business_logic="",
            api_endpoints=[],
            dependencies=[],
            annotations=[],
            key_methods=[]
        )