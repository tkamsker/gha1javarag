"""
JavaScript static analysis for routes, XHR calls, and validations.
"""
import os
import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import esprima
from bs4 import BeautifulSoup

from config.settings import settings

logger = logging.getLogger(__name__)

class JavaScriptExtractor:
    """Extracts JavaScript patterns for routes, XHR calls, and validations."""
    
    def __init__(self):
        """Initialize JavaScript extractor."""
        self.output_dir = settings.build_dir / "js_artifacts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Common route patterns
        self.route_patterns = [
            r'router\.on\([\'"]([^\'"]+)[\'"]',
            r'router\.get\([\'"]([^\'"]+)[\'"]',
            r'router\.post\([\'"]([^\'"]+)[\'"]',
            r'router\.put\([\'"]([^\'"]+)[\'"]',
            r'router\.delete\([\'"]([^\'"]+)[\'"]',
            r'window\.location\.hash\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'history\.pushState\([^,]+,\s*[\'"]([^\'"]+)[\'"]',
            r'window\.onhashchange\s*=\s*function[^{]*\{[^}]*[\'"]([^\'"]+)[\'"]'
        ]
        
        # XHR/fetch patterns
        self.xhr_patterns = [
            r'fetch\([\'"]([^\'"]+)[\'"]',
            r'\$\.ajax\([^}]*url:\s*[\'"]([^\'"]+)[\'"]',
            r'\$\.get\([\'"]([^\'"]+)[\'"]',
            r'\$\.post\([\'"]([^\'"]+)[\'"]',
            r'XMLHttpRequest\(\)\.open\([\'"]([A-Z]+)[\'"],\s*[\'"]([^\'"]+)[\'"]',
            r'xhr\.open\([\'"]([A-Z]+)[\'"],\s*[\'"]([^\'"]+)[\'"]'
        ]
        
        # Validation patterns
        self.validation_patterns = [
            r'required\s*:\s*true',
            r'minLength\s*:\s*(\d+)',
            r'maxLength\s*:\s*(\d+)',
            r'pattern\s*:\s*[\'"]([^\'"]+)[\'"]',
            r'email\s*:\s*true',
            r'number\s*:\s*true',
            r'min\s*:\s*(\d+)',
            r'max\s*:\s*(\d+)'
        ]
    
    def extract_js_artifacts(self, js_files: List[str]) -> List[Dict[str, Any]]:
        """Extract JavaScript artifacts from JS files."""
        artifacts = []
        
        for js_file in js_files:
            try:
                logger.info(f"Processing JavaScript file: {js_file}")
                artifact = self._extract_single_js_file(js_file)
                if artifact:
                    artifacts.append(artifact)
                    
                    # Save individual JS artifact JSON
                    self._save_js_artifact_json(artifact)
                    
            except Exception as e:
                logger.error(f"Failed to process JavaScript file {js_file}: {e}")
                continue
        
        # Save all JS artifacts JSON
        self._save_all_js_artifacts_json(artifacts)
        
        logger.info(f"Extracted {len(artifacts)} JavaScript artifacts")
        return artifacts
    
    def extract_js_from_jsp(self, jsp_files: List[str]) -> List[Dict[str, Any]]:
        """Extract JavaScript from JSP files (inline scripts)."""
        artifacts = []
        
        for jsp_file in jsp_files:
            try:
                logger.info(f"Processing JSP file for inline JS: {jsp_file}")
                js_artifacts = self._extract_js_from_single_jsp(jsp_file)
                artifacts.extend(js_artifacts)
                
            except Exception as e:
                logger.error(f"Failed to process JSP file {jsp_file}: {e}")
                continue
        
        return artifacts
    
    def _extract_single_js_file(self, js_file: str) -> Optional[Dict[str, Any]]:
        """Extract information from a single JavaScript file."""
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JavaScript (with error handling)
            try:
                ast = esprima.parseScript(content, loc=True)
            except esprima.Error as e:
                logger.warning(f"Failed to parse JavaScript in {js_file}: {e}")
                # Fallback to regex-based extraction
                return self._extract_with_regex(js_file, content)
            
            # Extract routes
            routes = self._extract_routes_from_ast(ast)
            
            # Extract XHR calls
            xhr_calls = self._extract_xhr_calls_from_ast(ast)
            
            # Extract validations
            validations = self._extract_validations_from_ast(ast)
            
            # Extract global exports
            globals = self._extract_globals_from_ast(ast)
            
            # Create JS artifact
            artifact = {
                'project': self._get_project_name(js_file),
                'path': js_file,
                'lineStart': 1,
                'lineEnd': len(content.splitlines()),
                'text': f"[JS] {Path(js_file).name}",
                'meta': {
                    'fileName': Path(js_file).name,
                    'fileSize': len(content)
                },
                'scriptPath': js_file,
                'routesJson': json.dumps(routes),
                'xhrJson': json.dumps(xhr_calls),
                'validationsJson': json.dumps(validations),
                'globals': globals
            }
            
            return artifact
            
        except Exception as e:
            logger.error(f"Failed to extract JavaScript from {js_file}: {e}")
            return None
    
    def _extract_js_from_single_jsp(self, jsp_file: str) -> List[Dict[str, Any]]:
        """Extract JavaScript from a single JSP file."""
        artifacts = []
        
        try:
            with open(jsp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JSP with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find all script tags
            script_tags = soup.find_all('script')
            
            for i, script_tag in enumerate(script_tags):
                if script_tag.string:
                    js_content = script_tag.string.strip()
                    if js_content:
                        # Create a temporary JS artifact for inline script
                        artifact = {
                            'project': self._get_project_name(jsp_file),
                            'path': f"{jsp_file}#script_{i}",
                            'lineStart': 1,
                            'lineEnd': len(js_content.splitlines()),
                            'text': f"[JS Inline] {Path(jsp_file).name}#script_{i}",
                            'meta': {
                                'fileName': f"{Path(jsp_file).name}#script_{i}",
                                'sourceFile': jsp_file,
                                'scriptIndex': i
                            },
                            'scriptPath': f"{jsp_file}#script_{i}",
                            'routesJson': json.dumps(self._extract_routes_with_regex(js_content)),
                            'xhrJson': json.dumps(self._extract_xhr_with_regex(js_content)),
                            'validationsJson': json.dumps(self._extract_validations_with_regex(js_content)),
                            'globals': self._extract_globals_with_regex(js_content)
                        }
                        artifacts.append(artifact)
            
        except Exception as e:
            logger.error(f"Failed to extract JavaScript from JSP {jsp_file}: {e}")
        
        return artifacts
    
    def _extract_routes_from_ast(self, ast) -> List[Dict[str, str]]:
        """Extract routes from JavaScript AST."""
        routes = []
        
        def visit_node(node):
            if hasattr(node, 'type'):
                if node.type == 'CallExpression':
                    if (hasattr(node, 'callee') and 
                        hasattr(node.callee, 'property') and 
                        node.callee.property and 
                        node.callee.property.name in ['on', 'get', 'post', 'put', 'delete']):
                        
                        if (hasattr(node, 'arguments') and 
                            len(node.arguments) >= 1 and 
                            hasattr(node.arguments[0], 'value')):
                            
                            route_pattern = node.arguments[0].value
                            method = node.callee.property.name.upper()
                            
                            routes.append({
                                'pattern': route_pattern,
                                'method': method,
                                'handler': 'unknown'  # Would need more analysis
                            })
                
                # Recursively visit child nodes
                for child in node:
                    if hasattr(child, '__iter__') and not isinstance(child, str):
                        for item in child:
                            if hasattr(item, 'type'):
                                visit_node(item)
        
        visit_node(ast)
        return routes
    
    def _extract_xhr_calls_from_ast(self, ast) -> List[Dict[str, str]]:
        """Extract XHR/fetch calls from JavaScript AST."""
        xhr_calls = []
        
        def visit_node(node):
            if hasattr(node, 'type'):
                if node.type == 'CallExpression':
                    if (hasattr(node, 'callee') and 
                        hasattr(node.callee, 'name') and 
                        node.callee.name == 'fetch'):
                        
                        if (hasattr(node, 'arguments') and 
                            len(node.arguments) >= 1 and 
                            hasattr(node.arguments[0], 'value')):
                            
                            url = node.arguments[0].value
                            method = 'GET'  # Default for fetch
                            
                            # Try to extract method from options
                            if len(node.arguments) >= 2 and hasattr(node.arguments[1], 'properties'):
                                for prop in node.arguments[1].properties:
                                    if (hasattr(prop, 'key') and 
                                        hasattr(prop.key, 'name') and 
                                        prop.key.name == 'method' and
                                        hasattr(prop, 'value') and
                                        hasattr(prop.value, 'value')):
                                        method = prop.value.value.upper()
                                        break
                            
                            xhr_calls.append({
                                'method': method,
                                'url': url,
                                'type': 'fetch'
                            })
                
                # Recursively visit child nodes
                for child in node:
                    if hasattr(child, '__iter__') and not isinstance(child, str):
                        for item in child:
                            if hasattr(item, 'type'):
                                visit_node(item)
        
        visit_node(ast)
        return xhr_calls
    
    def _extract_validations_from_ast(self, ast) -> List[Dict[str, Any]]:
        """Extract validation rules from JavaScript AST."""
        validations = []
        
        def visit_node(node):
            if hasattr(node, 'type'):
                if node.type == 'ObjectExpression':
                    # Look for validation objects
                    validation_rules = {}
                    for prop in node.properties:
                        if (hasattr(prop, 'key') and 
                            hasattr(prop.key, 'name') and
                            hasattr(prop, 'value')):
                            
                            rule_name = prop.key.name
                            if rule_name in ['required', 'minLength', 'maxLength', 'pattern', 'email', 'number', 'min', 'max']:
                                if hasattr(prop.value, 'value'):
                                    validation_rules[rule_name] = prop.value.value
                                elif hasattr(prop.value, 'type') and prop.value.type == 'Literal':
                                    validation_rules[rule_name] = prop.value.value
                    
                    if validation_rules:
                        validations.append({
                            'field': 'unknown',  # Would need more context
                            'rules': validation_rules
                        })
                
                # Recursively visit child nodes
                for child in node:
                    if hasattr(child, '__iter__') and not isinstance(child, str):
                        for item in child:
                            if hasattr(item, 'type'):
                                visit_node(item)
        
        visit_node(ast)
        return validations
    
    def _extract_globals_from_ast(self, ast) -> List[str]:
        """Extract global exports from JavaScript AST."""
        globals = []
        
        def visit_node(node):
            if hasattr(node, 'type'):
                if node.type == 'AssignmentExpression':
                    if (hasattr(node, 'left') and 
                        hasattr(node.left, 'object') and
                        hasattr(node.left.object, 'name') and
                        node.left.object.name == 'window'):
                        
                        if hasattr(node.left, 'property') and hasattr(node.left.property, 'name'):
                            globals.append(node.left.property.name)
                
                # Recursively visit child nodes
                for child in node:
                    if hasattr(child, '__iter__') and not isinstance(child, str):
                        for item in child:
                            if hasattr(item, 'type'):
                                visit_node(item)
        
        visit_node(ast)
        return globals
    
    def _extract_with_regex(self, js_file: str, content: str) -> Dict[str, Any]:
        """Fallback regex-based extraction when AST parsing fails."""
        return {
            'project': self._get_project_name(js_file),
            'path': js_file,
            'lineStart': 1,
            'lineEnd': len(content.splitlines()),
            'text': f"[JS] {Path(js_file).name}",
            'meta': {
                'fileName': Path(js_file).name,
                'extractionMethod': 'regex_fallback'
            },
            'scriptPath': js_file,
            'routesJson': json.dumps(self._extract_routes_with_regex(content)),
            'xhrJson': json.dumps(self._extract_xhr_with_regex(content)),
            'validationsJson': json.dumps(self._extract_validations_with_regex(content)),
            'globals': self._extract_globals_with_regex(content)
        }
    
    def _extract_routes_with_regex(self, content: str) -> List[Dict[str, str]]:
        """Extract routes using regex patterns."""
        routes = []
        
        for pattern in self.route_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                if len(match.groups()) >= 1:
                    route_pattern = match.group(1)
                    routes.append({
                        'pattern': route_pattern,
                        'method': 'GET',  # Default
                        'handler': 'unknown'
                    })
        
        return routes
    
    def _extract_xhr_with_regex(self, content: str) -> List[Dict[str, str]]:
        """Extract XHR calls using regex patterns."""
        xhr_calls = []
        
        for pattern in self.xhr_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                if 'XMLHttpRequest' in pattern or 'xhr.open' in pattern:
                    if len(match.groups()) >= 2:
                        method = match.group(1)
                        url = match.group(2)
                        xhr_calls.append({
                            'method': method,
                            'url': url,
                            'type': 'XMLHttpRequest'
                        })
                else:
                    if len(match.groups()) >= 1:
                        url = match.group(1)
                        method = 'GET'  # Default for fetch/$.ajax
                        xhr_calls.append({
                            'method': method,
                            'url': url,
                            'type': 'fetch' if 'fetch' in pattern else 'jQuery'
                        })
        
        return xhr_calls
    
    def _extract_validations_with_regex(self, content: str) -> List[Dict[str, Any]]:
        """Extract validation rules using regex patterns."""
        validations = []
        
        for pattern in self.validation_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                rule_name = pattern.split(':')[0].strip()
                rule_value = match.group(1) if len(match.groups()) >= 1 else True
                validations.append({
                    'field': 'unknown',
                    'rule': rule_name,
                    'value': rule_value
                })
        
        return validations
    
    def _extract_globals_with_regex(self, content: str) -> List[str]:
        """Extract global exports using regex patterns."""
        globals = []
        
        # Look for window.property = value patterns
        window_pattern = r'window\.(\w+)\s*='
        matches = re.finditer(window_pattern, content)
        for match in matches:
            globals.append(match.group(1))
        
        # Look for function declarations at top level
        function_pattern = r'function\s+(\w+)\s*\('
        matches = re.finditer(function_pattern, content)
        for match in matches:
            globals.append(match.group(1))
        
        return list(set(globals))  # Remove duplicates
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'js', 'static']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_js_artifact_json(self, artifact: Dict[str, Any]):
        """Save individual JS artifact as JSON."""
        file_name = Path(artifact['scriptPath']).stem
        safe_name = file_name.replace('.', '_').replace('/', '_').replace('#', '_')
        output_file = self.output_dir / f"{safe_name}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(artifact, f, indent=2, ensure_ascii=False)
    
    def _save_all_js_artifacts_json(self, artifacts: List[Dict[str, Any]]):
        """Save all JS artifacts as a single JSON file."""
        output_file = self.output_dir / "all_js_artifacts.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(artifacts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(artifacts)} JavaScript artifacts to {output_file}")
