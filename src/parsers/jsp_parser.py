"""
JSP parser for extracting metadata from .jsp and .tsp files.
"""

import re
from typing import Dict, List, Any, Optional
import logging


class JSPParser:
    """Parser for JSP (JavaServer Pages) files."""
    
    def __init__(self):
        """Initialize the JSP parser."""
        self.logger = logging.getLogger(__name__)
        
        # Regex patterns for JSP elements
        self.jsp_directive_pattern = re.compile(r'<%@\s*(\w+)\s+([^%]+)%>', re.MULTILINE)
        self.jsp_declaration_pattern = re.compile(r'<%!\s*([^%]+)\s*%>', re.MULTILINE)
        self.jsp_scriptlet_pattern = re.compile(r'<%([^%]+)%>', re.MULTILINE)
        self.jsp_expression_pattern = re.compile(r'<%=([^%]+)%>', re.MULTILINE)
        self.jsp_action_pattern = re.compile(r'<jsp:(\w+)(?:\s+[^>]*)?>(?:.*?</jsp:\1>)?', re.MULTILINE | re.DOTALL)
        self.jsp_comment_pattern = re.compile(r'<%--(.*?)--%>', re.DOTALL)
        
        # HTML form patterns
        self.form_pattern = re.compile(r'<form[^>]*>.*?</form>', re.DOTALL | re.IGNORECASE)
        self.input_pattern = re.compile(r'<input[^>]*>', re.IGNORECASE)
        self.select_pattern = re.compile(r'<select[^>]*>.*?</select>', re.DOTALL | re.IGNORECASE)
        self.textarea_pattern = re.compile(r'<textarea[^>]*>.*?</textarea>', re.DOTALL | re.IGNORECASE)
        
        # JavaScript patterns
        self.script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        self.function_pattern = re.compile(r'function\s+(\w+)\s*\([^)]*\)', re.MULTILINE)
        self.event_handler_pattern = re.compile(r'on(\w+)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse a JSP file and extract metadata."""
        try:
            # Extract JSP elements
            directives = self._extract_directives(content)
            declarations = self._extract_declarations(content)
            scriptlets = self._extract_scriptlets(content)
            expressions = self._extract_expressions(content)
            actions = self._extract_actions(content)
            comments = self._extract_comments(content)
            
            # Extract HTML elements
            forms = self._extract_forms(content)
            inputs = self._extract_inputs(content)
            selects = self._extract_selects(content)
            textareas = self._extract_textareas(content)
            
            # Extract JavaScript
            scripts = self._extract_scripts(content)
            functions = self._extract_functions(content)
            event_handlers = self._extract_event_handlers(content)
            
            # Extract endpoints and navigation
            endpoints = self._extract_endpoints(content)
            navigation_targets = self._extract_navigation_targets(content)
            
            # Calculate complexity
            complexity_score = self._calculate_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'jsp',
                'directives': directives,
                'declarations': declarations,
                'scriptlets': scriptlets,
                'expressions': expressions,
                'actions': actions,
                'comments': comments,
                'forms': forms,
                'inputs': inputs,
                'selects': selects,
                'textareas': textareas,
                'scripts': scripts,
                'functions': functions,
                'event_handlers': event_handlers,
                'endpoints': endpoints,
                'navigation_targets': navigation_targets,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing JSP file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'jsp',
                'error': str(e)
            }
    
    def _extract_directives(self, content: str) -> List[Dict[str, str]]:
        """Extract JSP directives."""
        directives = []
        for match in self.jsp_directive_pattern.finditer(content):
            directive_type = match.group(1)
            directive_content = match.group(2).strip()
            directives.append({
                'type': directive_type,
                'content': directive_content
            })
        return directives
    
    def _extract_declarations(self, content: str) -> List[str]:
        """Extract JSP declarations."""
        declarations = []
        for match in self.jsp_declaration_pattern.finditer(content):
            declarations.append(match.group(1).strip())
        return declarations
    
    def _extract_scriptlets(self, content: str) -> List[str]:
        """Extract JSP scriptlets."""
        scriptlets = []
        for match in self.jsp_scriptlet_pattern.finditer(content):
            scriptlet = match.group(1).strip()
            if not scriptlet.startswith('!'):  # Skip declarations
                scriptlets.append(scriptlet)
        return scriptlets
    
    def _extract_expressions(self, content: str) -> List[str]:
        """Extract JSP expressions."""
        expressions = []
        for match in self.jsp_expression_pattern.finditer(content):
            expressions.append(match.group(1).strip())
        return expressions
    
    def _extract_actions(self, content: str) -> List[Dict[str, str]]:
        """Extract JSP actions."""
        actions = []
        for match in self.jsp_action_pattern.finditer(content):
            action_type = match.group(1)
            action_content = match.group(0)
            actions.append({
                'type': action_type,
                'content': action_content
            })
        return actions
    
    def _extract_comments(self, content: str) -> List[str]:
        """Extract JSP comments."""
        comments = []
        for match in self.jsp_comment_pattern.finditer(content):
            comments.append(match.group(1).strip())
        return comments
    
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
                'name': self._extract_attribute(form_content, 'name')
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
                'placeholder': self._extract_attribute(input_content, 'placeholder')
            }
            inputs.append(input_data)
        return inputs
    
    def _extract_selects(self, content: str) -> List[Dict[str, Any]]:
        """Extract HTML select elements."""
        selects = []
        for match in self.select_pattern.finditer(content):
            select_content = match.group(0)
            options = self._extract_options(select_content)
            select_data = {
                'content': select_content,
                'name': self._extract_attribute(select_content, 'name'),
                'id': self._extract_attribute(select_content, 'id'),
                'options': options
            }
            selects.append(select_data)
        return selects
    
    def _extract_textareas(self, content: str) -> List[Dict[str, str]]:
        """Extract HTML textarea elements."""
        textareas = []
        for match in self.textarea_pattern.finditer(content):
            textarea_content = match.group(0)
            textarea_data = {
                'name': self._extract_attribute(textarea_content, 'name'),
                'id': self._extract_attribute(textarea_content, 'id'),
                'rows': self._extract_attribute(textarea_content, 'rows'),
                'cols': self._extract_attribute(textarea_content, 'cols'),
                'placeholder': self._extract_attribute(textarea_content, 'placeholder')
            }
            textareas.append(textarea_data)
        return textareas
    
    def _extract_scripts(self, content: str) -> List[str]:
        """Extract JavaScript code from script tags."""
        scripts = []
        for match in self.script_pattern.finditer(content):
            script_content = match.group(1).strip()
            if script_content:
                scripts.append(script_content)
        return scripts
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract JavaScript function definitions."""
        functions = []
        for match in self.function_pattern.finditer(content):
            functions.append(match.group(1))
        return functions
    
    def _extract_event_handlers(self, content: str) -> List[Dict[str, str]]:
        """Extract JavaScript event handlers."""
        handlers = []
        for match in self.event_handler_pattern.finditer(content):
            handlers.append({
                'event': match.group(1),
                'handler': match.group(2)
            })
        return handlers
    
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
            r'ajax\s*\(\s*["\']([^"\']+)["\']'
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
            r'redirect\s*=\s*["\']([^"\']+)["\']'
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
    
    def _extract_options(self, select_content: str) -> List[Dict[str, str]]:
        """Extract options from a select element."""
        options = []
        option_pattern = re.compile(r'<option[^>]*>(.*?)</option>', re.DOTALL | re.IGNORECASE)
        for match in option_pattern.finditer(select_content):
            option_text = match.group(1).strip()
            option_value = self._extract_attribute(match.group(0), 'value')
            options.append({
                'text': option_text,
                'value': option_value
            })
        return options
    
    def _calculate_complexity(self, content: str) -> int:
        """Calculate complexity score for JSP file."""
        complexity = 1  # Base complexity
        
        # Count JSP elements
        complexity += len(self.jsp_directive_pattern.findall(content))
        complexity += len(self.jsp_declaration_pattern.findall(content))
        complexity += len(self.jsp_scriptlet_pattern.findall(content))
        complexity += len(self.jsp_expression_pattern.findall(content))
        complexity += len(self.jsp_action_pattern.findall(content))
        
        # Count JavaScript complexity
        complexity += len(self.function_pattern.findall(content))
        complexity += len(self.event_handler_pattern.findall(content))
        
        # Count form elements
        complexity += len(self.form_pattern.findall(content))
        complexity += len(self.input_pattern.findall(content))
        
        return complexity
