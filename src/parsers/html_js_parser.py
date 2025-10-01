"""
HTML and JavaScript parser for extracting metadata from .html and .js files.
"""

import re
from typing import Dict, List, Any, Optional
import logging


class HTMLJSParser:
    """Parser for HTML and JavaScript files."""
    
    def __init__(self):
        """Initialize the HTML/JS parser."""
        self.logger = logging.getLogger(__name__)
        
        # HTML patterns
        self.tag_pattern = re.compile(r'<(\w+)(?:\s+[^>]*)?>', re.IGNORECASE)
        self.attribute_pattern = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
        self.form_pattern = re.compile(r'<form[^>]*>.*?</form>', re.DOTALL | re.IGNORECASE)
        self.input_pattern = re.compile(r'<input[^>]*>', re.IGNORECASE)
        self.link_pattern = re.compile(r'<a[^>]*href\s*=\s*["\']([^"\']*)["\'][^>]*>', re.IGNORECASE)
        self.script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        self.style_pattern = re.compile(r'<style[^>]*>(.*?)</style>', re.DOTALL | re.IGNORECASE)
        
        # JavaScript patterns
        self.function_pattern = re.compile(r'function\s+(\w+)\s*\([^)]*\)', re.MULTILINE)
        self.arrow_function_pattern = re.compile(r'(\w+)\s*=\s*\([^)]*\)\s*=>', re.MULTILINE)
        self.class_pattern = re.compile(r'class\s+(\w+)', re.MULTILINE)
        self.variable_pattern = re.compile(r'(?:var|let|const)\s+(\w+)', re.MULTILINE)
        self.event_handler_pattern = re.compile(r'on(\w+)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
        self.ajax_pattern = re.compile(r'\.ajax\s*\([^)]*\)', re.MULTILINE | re.DOTALL)
        self.fetch_pattern = re.compile(r'fetch\s*\([^)]*\)', re.MULTILINE | re.DOTALL)
        
        # CSS patterns
        self.css_rule_pattern = re.compile(r'([.#]?\w+)\s*\{[^}]*\}', re.MULTILINE | re.DOTALL)
        self.css_class_pattern = re.compile(r'\.(\w+)', re.MULTILINE)
        self.css_id_pattern = re.compile(r'#(\w+)', re.MULTILINE)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse an HTML or JS file and extract metadata."""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'html':
            return self._parse_html_file(file_path, content)
        elif file_extension == 'js':
            return self._parse_js_file(file_path, content)
        elif file_extension == 'css':
            return self._parse_css_file(file_path, content)
        else:
            return {
                'file_path': file_path,
                'language': 'unknown',
                'error': f'Unsupported file type: {file_extension}'
            }
    
    def _parse_html_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse HTML file and extract metadata."""
        try:
            # Extract HTML elements
            tags = self._extract_tags(content)
            attributes = self._extract_attributes(content)
            forms = self._extract_forms(content)
            inputs = self._extract_inputs(content)
            links = self._extract_links(content)
            
            # Extract embedded scripts and styles
            scripts = self._extract_scripts(content)
            styles = self._extract_styles(content)
            
            # Extract JavaScript from scripts
            js_functions = []
            js_variables = []
            js_event_handlers = []
            
            for script_content in scripts:
                js_functions.extend(self._extract_js_functions(script_content))
                js_variables.extend(self._extract_js_variables(script_content))
                js_event_handlers.extend(self._extract_js_event_handlers(script_content))
            
            # Extract CSS from styles
            css_rules = []
            css_classes = []
            css_ids = []
            
            for style_content in styles:
                css_rules.extend(self._extract_css_rules(style_content))
                css_classes.extend(self._extract_css_classes(style_content))
                css_ids.extend(self._extract_css_ids(style_content))
            
            # Extract endpoints and navigation
            endpoints = self._extract_endpoints(content)
            navigation_targets = self._extract_navigation_targets(content)
            
            # Calculate complexity
            complexity_score = self._calculate_html_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'html',
                'tags': tags,
                'attributes': attributes,
                'forms': forms,
                'inputs': inputs,
                'links': links,
                'scripts': scripts,
                'styles': styles,
                'js_functions': js_functions,
                'js_variables': js_variables,
                'js_event_handlers': js_event_handlers,
                'css_rules': css_rules,
                'css_classes': css_classes,
                'css_ids': css_ids,
                'endpoints': endpoints,
                'navigation_targets': navigation_targets,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing HTML file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'html',
                'error': str(e)
            }
    
    def _parse_js_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse JavaScript file and extract metadata."""
        try:
            # Extract JavaScript elements
            functions = self._extract_js_functions(content)
            arrow_functions = self._extract_arrow_functions(content)
            classes = self._extract_js_classes(content)
            variables = self._extract_js_variables(content)
            event_handlers = self._extract_js_event_handlers(content)
            
            # Extract API calls
            ajax_calls = self._extract_ajax_calls(content)
            fetch_calls = self._extract_fetch_calls(content)
            
            # Extract endpoints
            endpoints = self._extract_endpoints(content)
            
            # Calculate complexity
            complexity_score = self._calculate_js_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'javascript',
                'functions': functions,
                'arrow_functions': arrow_functions,
                'classes': classes,
                'variables': variables,
                'event_handlers': event_handlers,
                'ajax_calls': ajax_calls,
                'fetch_calls': fetch_calls,
                'endpoints': endpoints,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing JavaScript file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'javascript',
                'error': str(e)
            }
    
    def _parse_css_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse CSS file and extract metadata."""
        try:
            # Extract CSS elements
            rules = self._extract_css_rules(content)
            classes = self._extract_css_classes(content)
            ids = self._extract_css_ids(content)
            
            # Calculate complexity
            complexity_score = self._calculate_css_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'css',
                'rules': rules,
                'classes': classes,
                'ids': ids,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing CSS file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'css',
                'error': str(e)
            }
    
    def _extract_tags(self, content: str) -> List[Dict[str, str]]:
        """Extract HTML tags and their attributes."""
        tags = []
        
        for match in self.tag_pattern.finditer(content):
            tag_name = match.group(1).lower()
            tag_content = match.group(0)
            
            # Extract attributes
            attributes = {}
            for attr_match in self.attribute_pattern.finditer(tag_content):
                attr_name = attr_match.group(1).lower()
                attr_value = attr_match.group(2)
                attributes[attr_name] = attr_value
            
            tags.append({
                'name': tag_name,
                'attributes': attributes,
                'content': tag_content
            })
        
        return tags
    
    def _extract_attributes(self, content: str) -> Dict[str, List[str]]:
        """Extract all HTML attributes and their values."""
        attributes = {}
        
        for match in self.attribute_pattern.finditer(content):
            attr_name = match.group(1).lower()
            attr_value = match.group(2)
            
            if attr_name not in attributes:
                attributes[attr_name] = []
            if attr_value not in attributes[attr_name]:
                attributes[attr_name].append(attr_value)
        
        return attributes
    
    def _extract_forms(self, content: str) -> List[Dict[str, Any]]:
        """Extract HTML forms."""
        forms = []
        
        for match in self.form_pattern.finditer(content):
            form_content = match.group(0)
            form_data = {
                'content': form_content,
                'action': self._extract_attribute(form_content, 'action'),
                'method': self._extract_attribute(form_content, 'method'),
                'id': self._extract_attribute(form_content, 'id'),
                'name': self._extract_attribute(form_content, 'name'),
                'enctype': self._extract_attribute(form_content, 'enctype')
            }
            forms.append(form_data)
        
        return forms
    
    def _extract_inputs(self, content: str) -> List[Dict[str, str]]:
        """Extract HTML input elements."""
        inputs = []
        
        for match in self.input_pattern.finditer(content):
            input_content = match.group(0)
            input_data = {
                'type': self._extract_attribute(input_content, 'type'),
                'name': self._extract_attribute(input_content, 'name'),
                'id': self._extract_attribute(input_content, 'id'),
                'value': self._extract_attribute(input_content, 'value'),
                'placeholder': self._extract_attribute(input_content, 'placeholder'),
                'required': self._extract_attribute(input_content, 'required')
            }
            inputs.append(input_data)
        
        return inputs
    
    def _extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract HTML links."""
        links = []
        
        for match in self.link_pattern.finditer(content):
            link_content = match.group(0)
            href = match.group(1)
            link_data = {
                'href': href,
                'text': self._extract_link_text(link_content),
                'id': self._extract_attribute(link_content, 'id'),
                'class': self._extract_attribute(link_content, 'class'),
                'target': self._extract_attribute(link_content, 'target')
            }
            links.append(link_data)
        
        return links
    
    def _extract_scripts(self, content: str) -> List[str]:
        """Extract JavaScript code from script tags."""
        scripts = []
        
        for match in self.script_pattern.finditer(content):
            script_content = match.group(1).strip()
            if script_content:
                scripts.append(script_content)
        
        return scripts
    
    def _extract_styles(self, content: str) -> List[str]:
        """Extract CSS code from style tags."""
        styles = []
        
        for match in self.style_pattern.finditer(content):
            style_content = match.group(1).strip()
            if style_content:
                styles.append(style_content)
        
        return styles
    
    def _extract_js_functions(self, content: str) -> List[str]:
        """Extract JavaScript function definitions."""
        functions = []
        
        for match in self.function_pattern.finditer(content):
            functions.append(match.group(1))
        
        return functions
    
    def _extract_arrow_functions(self, content: str) -> List[str]:
        """Extract JavaScript arrow function definitions."""
        arrow_functions = []
        
        for match in self.arrow_function_pattern.finditer(content):
            arrow_functions.append(match.group(1))
        
        return arrow_functions
    
    def _extract_js_classes(self, content: str) -> List[str]:
        """Extract JavaScript class definitions."""
        classes = []
        
        for match in self.class_pattern.finditer(content):
            classes.append(match.group(1))
        
        return classes
    
    def _extract_js_variables(self, content: str) -> List[str]:
        """Extract JavaScript variable declarations."""
        variables = []
        
        for match in self.variable_pattern.finditer(content):
            variables.append(match.group(1))
        
        return variables
    
    def _extract_js_event_handlers(self, content: str) -> List[Dict[str, str]]:
        """Extract JavaScript event handlers."""
        handlers = []
        
        for match in self.event_handler_pattern.finditer(content):
            handlers.append({
                'event': match.group(1),
                'handler': match.group(2)
            })
        
        return handlers
    
    def _extract_ajax_calls(self, content: str) -> List[str]:
        """Extract jQuery AJAX calls."""
        ajax_calls = []
        
        for match in self.ajax_pattern.finditer(content):
            ajax_calls.append(match.group(0))
        
        return ajax_calls
    
    def _extract_fetch_calls(self, content: str) -> List[str]:
        """Extract fetch API calls."""
        fetch_calls = []
        
        for match in self.fetch_pattern.finditer(content):
            fetch_calls.append(match.group(0))
        
        return fetch_calls
    
    def _extract_css_rules(self, content: str) -> List[str]:
        """Extract CSS rules."""
        rules = []
        
        for match in self.css_rule_pattern.finditer(content):
            rules.append(match.group(0))
        
        return rules
    
    def _extract_css_classes(self, content: str) -> List[str]:
        """Extract CSS class names."""
        classes = []
        
        for match in self.css_class_pattern.finditer(content):
            classes.append(match.group(1))
        
        return list(set(classes))  # Remove duplicates
    
    def _extract_css_ids(self, content: str) -> List[str]:
        """Extract CSS ID names."""
        ids = []
        
        for match in self.css_id_pattern.finditer(content):
            ids.append(match.group(1))
        
        return list(set(ids))  # Remove duplicates
    
    def _extract_endpoints(self, content: str) -> List[str]:
        """Extract REST endpoints and URLs."""
        endpoints = []
        
        # Look for common URL patterns
        url_patterns = [
            r'action\s*=\s*["\']([^"\']+)["\']',
            r'href\s*=\s*["\']([^"\']+)["\']',
            r'src\s*=\s*["\']([^"\']+)["\']',
            r'url\s*:\s*["\']([^"\']+)["\']',
            r'fetch\s*\(\s*["\']([^"\']+)["\']',
            r'ajax\s*\(\s*["\']([^"\']+)["\']',
            r'\.get\s*\(\s*["\']([^"\']+)["\']',
            r'\.post\s*\(\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in url_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                url = match.group(1)
                if url and not url.startswith('#') and not url.startswith('javascript:'):
                    endpoints.append(url)
        
        return list(set(endpoints))  # Remove duplicates
    
    def _extract_navigation_targets(self, content: str) -> List[str]:
        """Extract navigation targets and page references."""
        targets = []
        
        # Look for page references
        page_patterns = [
            r'page\s*=\s*["\']([^"\']+)["\']',
            r'forward\s*=\s*["\']([^"\']+)["\']',
            r'include\s*=\s*["\']([^"\']+)["\']',
            r'redirect\s*=\s*["\']([^"\']+)["\']',
            r'window\.location\s*=\s*["\']([^"\']+)["\']',
            r'location\.href\s*=\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in page_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                target = match.group(1)
                if target:
                    targets.append(target)
        
        return list(set(targets))  # Remove duplicates
    
    def _extract_attribute(self, content: str, attr_name: str) -> str:
        """Extract value of a specific HTML attribute."""
        pattern = rf'{attr_name}\s*=\s*["\']([^"\']*)["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_link_text(self, link_content: str) -> str:
        """Extract text content from a link."""
        # Simple extraction of text between tags
        text_match = re.search(r'>([^<]+)<', link_content)
        return text_match.group(1).strip() if text_match else ""
    
    def _calculate_html_complexity(self, content: str) -> int:
        """Calculate complexity score for HTML file."""
        complexity = 1  # Base complexity
        
        # Count HTML elements
        complexity += len(self.tag_pattern.findall(content))
        complexity += len(self.form_pattern.findall(content))
        complexity += len(self.input_pattern.findall(content))
        complexity += len(self.link_pattern.findall(content))
        
        # Count JavaScript complexity
        complexity += len(self.function_pattern.findall(content))
        complexity += len(self.event_handler_pattern.findall(content))
        
        # Count CSS complexity
        complexity += len(self.css_rule_pattern.findall(content))
        
        return complexity
    
    def _calculate_js_complexity(self, content: str) -> int:
        """Calculate complexity score for JavaScript file."""
        complexity = 1  # Base complexity
        
        # Count JavaScript constructs
        complexity += len(self.function_pattern.findall(content))
        complexity += len(self.arrow_function_pattern.findall(content))
        complexity += len(self.class_pattern.findall(content))
        complexity += len(self.variable_pattern.findall(content))
        complexity += len(self.ajax_pattern.findall(content))
        complexity += len(self.fetch_pattern.findall(content))
        
        # Count control flow statements
        control_flow_keywords = ['if', 'else', 'for', 'while', 'do', 'switch', 'case', 'try', 'catch']
        for keyword in control_flow_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        return complexity
    
    def _calculate_css_complexity(self, content: str) -> int:
        """Calculate complexity score for CSS file."""
        complexity = 1  # Base complexity
        
        # Count CSS rules and selectors
        complexity += len(self.css_rule_pattern.findall(content))
        complexity += len(self.css_class_pattern.findall(content))
        complexity += len(self.css_id_pattern.findall(content))
        
        return complexity
