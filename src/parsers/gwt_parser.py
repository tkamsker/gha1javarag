"""
GWT parser for extracting metadata from GWT UiBinder and configuration files.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
import logging


class GWTParser:
    """Parser for GWT (Google Web Toolkit) files."""
    
    def __init__(self):
        """Initialize the GWT parser."""
        self.logger = logging.getLogger(__name__)
        
        # GWT Java patterns
        self.ui_field_pattern = re.compile(r'@UiField\s+(\w+)\s+(\w+)', re.MULTILINE)
        self.ui_handler_pattern = re.compile(r'@UiHandler\s*\(\s*["\']([^"\']+)["\']\s*\)', re.MULTILINE)
        self.ui_template_pattern = re.compile(r'@UiTemplate\s*\(\s*["\']([^"\']+)["\']\s*\)', re.MULTILINE)
        self.gwt_create_pattern = re.compile(r'GWT\.create\s*\(\s*(\w+)\.class\s*\)', re.MULTILINE)
        self.gwt_log_pattern = re.compile(r'GWT\.log\s*\([^)]*\)', re.MULTILINE)
        
        # GWT XML patterns
        self.gwt_module_pattern = re.compile(r'<module\s+rename-to=["\']([^"\']+)["\']', re.IGNORECASE)
        self.gwt_entry_point_pattern = re.compile(r'<entry-point\s+class=["\']([^"\']+)["\']', re.IGNORECASE)
        self.gwt_inherits_pattern = re.compile(r'<inherits\s+name=["\']([^"\']+)["\']', re.IGNORECASE)
        self.gwt_source_pattern = re.compile(r'<source\s+path=["\']([^"\']+)["\']', re.IGNORECASE)
        self.gwt_public_pattern = re.compile(r'<public\s+path=["\']([^"\']+)["\']', re.IGNORECASE)
        
        # UiBinder patterns
        self.uibinder_widget_pattern = re.compile(r'<(\w+)(?:\s+[^>]*)?>', re.IGNORECASE)
        self.uibinder_attribute_pattern = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
        self.uibinder_ui_field_pattern = re.compile(r'ui:field\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
        self.uibinder_ui_handler_pattern = re.compile(r'ui:handler\s+field\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse a GWT file and extract metadata."""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'java':
            return self._parse_gwt_java_file(file_path, content)
        elif file_extension == 'xml':
            if 'gwt.xml' in file_path.lower():
                return self._parse_gwt_config_file(file_path, content)
            elif 'ui.xml' in file_path.lower():
                return self._parse_uibinder_file(file_path, content)
            else:
                return self._parse_generic_xml_file(file_path, content)
        else:
            return {
                'file_path': file_path,
                'language': 'unknown',
                'error': f'Unsupported GWT file type: {file_extension}'
            }
    
    def _parse_gwt_java_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse GWT Java file and extract GWT-specific metadata."""
        try:
            # Extract GWT-specific annotations and patterns
            ui_fields = self._extract_ui_fields(content)
            ui_handlers = self._extract_ui_handlers(content)
            ui_templates = self._extract_ui_templates(content)
            gwt_creates = self._extract_gwt_creates(content)
            gwt_logs = self._extract_gwt_logs(content)
            
            # Extract widget hierarchy and navigation
            widget_hierarchy = self._extract_widget_hierarchy(content)
            navigation_flows = self._extract_navigation_flows(content)
            
            # Extract business domains and user roles
            business_domains = self._extract_business_domains(content)
            user_roles = self._extract_user_roles(content)
            
            # Calculate complexity
            complexity_score = self._calculate_gwt_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'gwt_java',
                'ui_fields': ui_fields,
                'ui_handlers': ui_handlers,
                'ui_templates': ui_templates,
                'gwt_creates': gwt_creates,
                'gwt_logs': gwt_logs,
                'widget_hierarchy': widget_hierarchy,
                'navigation_flows': navigation_flows,
                'business_domains': business_domains,
                'user_roles': user_roles,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing GWT Java file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'gwt_java',
                'error': str(e)
            }
    
    def _parse_gwt_config_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse GWT configuration file (.gwt.xml)."""
        try:
            root = ET.fromstring(content)
            
            # Extract module configuration
            module_name = root.get('rename-to', '')
            entry_points = []
            inherits = []
            sources = []
            public_paths = []
            
            # Extract entry points
            for entry_point in root.findall('.//entry-point'):
                class_name = entry_point.get('class', '')
                if class_name:
                    entry_points.append(class_name)
            
            # Extract inherits
            for inherit in root.findall('.//inherits'):
                name = inherit.get('name', '')
                if name:
                    inherits.append(name)
            
            # Extract sources
            for source in root.findall('.//source'):
                path = source.get('path', '')
                if path:
                    sources.append(path)
            
            # Extract public paths
            for public in root.findall('.//public'):
                path = public.get('path', '')
                if path:
                    public_paths.append(path)
            
            return {
                'file_path': file_path,
                'language': 'gwt_config',
                'module_name': module_name,
                'entry_points': entry_points,
                'inherits': inherits,
                'sources': sources,
                'public_paths': public_paths
            }
        
        except ET.ParseError as e:
            self.logger.error(f"Error parsing GWT config file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'gwt_config',
                'error': f'XML parse error: {str(e)}'
            }
        except Exception as e:
            self.logger.error(f"Error processing GWT config file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'gwt_config',
                'error': str(e)
            }
    
    def _parse_uibinder_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse UiBinder file (.ui.xml)."""
        try:
            root = ET.fromstring(content)
            
            # Extract widget hierarchy
            widgets = self._extract_uibinder_widgets(root)
            ui_fields = self._extract_uibinder_ui_fields(content)
            ui_handlers = self._extract_uibinder_ui_handlers(content)
            
            # Extract styling and theming
            styles = self._extract_uibinder_styles(content)
            themes = self._extract_uibinder_themes(content)
            
            # Extract event handlers
            event_handlers = self._extract_uibinder_event_handlers(content)
            
            # Calculate complexity
            complexity_score = self._calculate_uibinder_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'gwt_uibinder',
                'widgets': widgets,
                'ui_fields': ui_fields,
                'ui_handlers': ui_handlers,
                'styles': styles,
                'themes': themes,
                'event_handlers': event_handlers,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except ET.ParseError as e:
            self.logger.error(f"Error parsing UiBinder file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'gwt_uibinder',
                'error': f'XML parse error: {str(e)}'
            }
        except Exception as e:
            self.logger.error(f"Error processing UiBinder file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'gwt_uibinder',
                'error': str(e)
            }
    
    def _parse_generic_xml_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse generic XML file (fallback)."""
        try:
            root = ET.fromstring(content)
            
            return {
                'file_path': file_path,
                'language': 'xml',
                'root_element': root.tag,
                'element_count': len(list(root.iter())),
                'attributes': dict(root.attrib)
            }
        
        except ET.ParseError as e:
            self.logger.error(f"Error parsing XML file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'xml',
                'error': f'XML parse error: {str(e)}'
            }
        except Exception as e:
            self.logger.error(f"Error processing XML file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'xml',
                'error': str(e)
            }
    
    def _extract_ui_fields(self, content: str) -> List[Dict[str, str]]:
        """Extract @UiField annotations."""
        ui_fields = []
        
        for match in self.ui_field_pattern.finditer(content):
            ui_fields.append({
                'type': match.group(1),
                'name': match.group(2)
            })
        
        return ui_fields
    
    def _extract_ui_handlers(self, content: str) -> List[str]:
        """Extract @UiHandler annotations."""
        ui_handlers = []
        
        for match in self.ui_handler_pattern.finditer(content):
            ui_handlers.append(match.group(1))
        
        return ui_handlers
    
    def _extract_ui_templates(self, content: str) -> List[str]:
        """Extract @UiTemplate annotations."""
        ui_templates = []
        
        for match in self.ui_template_pattern.finditer(content):
            ui_templates.append(match.group(1))
        
        return ui_templates
    
    def _extract_gwt_creates(self, content: str) -> List[str]:
        """Extract GWT.create() calls."""
        gwt_creates = []
        
        for match in self.gwt_create_pattern.finditer(content):
            gwt_creates.append(match.group(1))
        
        return gwt_creates
    
    def _extract_gwt_logs(self, content: str) -> List[str]:
        """Extract GWT.log() calls."""
        gwt_logs = []
        
        for match in self.gwt_log_pattern.finditer(content):
            gwt_logs.append(match.group(0))
        
        return gwt_logs
    
    def _extract_widget_hierarchy(self, content: str) -> List[Dict[str, Any]]:
        """Extract widget hierarchy from GWT Java code."""
        hierarchy = []
        
        # Look for widget creation patterns
        widget_patterns = [
            r'new\s+(\w+)\s*\(',
            r'\.add\s*\(\s*new\s+(\w+)\s*\(',
            r'\.setWidget\s*\(\s*new\s+(\w+)\s*\('
        ]
        
        for pattern in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_type = match.group(1)
                hierarchy.append({
                    'type': widget_type,
                    'creation_pattern': match.group(0)
                })
        
        return hierarchy
    
    def _extract_navigation_flows(self, content: str) -> List[Dict[str, str]]:
        """Extract navigation flows from GWT code."""
        flows = []
        
        # Look for navigation patterns
        navigation_patterns = [
            (r'History\.newItem\s*\(\s*["\']([^"\']+)["\']', 'History.newItem'),
            (r'Window\.open\s*\(\s*["\']([^"\']+)["\']', 'Window.open'),
            (r'\.setUrl\s*\(\s*["\']([^"\']+)["\']', 'setUrl'),
            (r'\.setHref\s*\(\s*["\']([^"\']+)["\']', 'setHref')
        ]
        
        for pattern, method in navigation_patterns:
            for match in re.finditer(pattern, content):
                flows.append({
                    'method': method,
                    'target': match.group(1)
                })
        
        return flows
    
    def _extract_business_domains(self, content: str) -> List[str]:
        """Extract business domain hints from GWT code."""
        domains = []
        
        # Look for domain-related patterns
        domain_patterns = [
            r'(\w*Domain\w*)',
            r'(\w*Service\w*)',
            r'(\w*Manager\w*)',
            r'(\w*Controller\w*)',
            r'(\w*Handler\w*)'
        ]
        
        for pattern in domain_patterns:
            for match in re.finditer(pattern, content):
                domain = match.group(1)
                if len(domain) > 3:  # Filter out very short matches
                    domains.append(domain)
        
        return list(set(domains))  # Remove duplicates
    
    def _extract_user_roles(self, content: str) -> List[str]:
        """Extract user role hints from GWT code."""
        roles = []
        
        # Look for role-related patterns
        role_patterns = [
            r'(\w*Role\w*)',
            r'(\w*Permission\w*)',
            r'(\w*Access\w*)',
            r'(\w*Auth\w*)',
            r'(\w*User\w*)',
            r'(\w*Admin\w*)'
        ]
        
        for pattern in role_patterns:
            for match in re.finditer(pattern, content):
                role = match.group(1)
                if len(role) > 3:  # Filter out very short matches
                    roles.append(role)
        
        return list(set(roles))  # Remove duplicates
    
    def _extract_uibinder_widgets(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extract widget hierarchy from UiBinder XML."""
        widgets = []
        
        def process_element(element: ET.Element, depth: int = 0):
            widget_info = {
                'tag': element.tag,
                'depth': depth,
                'attributes': dict(element.attrib),
                'ui_field': element.get('ui:field', ''),
                'ui_handler': element.get('ui:handler', ''),
                'children_count': len(element)
            }
            widgets.append(widget_info)
            
            for child in element:
                process_element(child, depth + 1)
        
        process_element(root)
        return widgets
    
    def _extract_uibinder_ui_fields(self, content: str) -> List[str]:
        """Extract ui:field attributes from UiBinder."""
        ui_fields = []
        
        for match in self.uibinder_ui_field_pattern.finditer(content):
            ui_fields.append(match.group(1))
        
        return ui_fields
    
    def _extract_uibinder_ui_handlers(self, content: str) -> List[str]:
        """Extract ui:handler attributes from UiBinder."""
        ui_handlers = []
        
        for match in self.uibinder_ui_handler_pattern.finditer(content):
            ui_handlers.append(match.group(1))
        
        return ui_handlers
    
    def _extract_uibinder_styles(self, content: str) -> List[str]:
        """Extract styling information from UiBinder."""
        styles = []
        
        # Look for style-related patterns
        style_patterns = [
            r'style\s*=\s*["\']([^"\']+)["\']',
            r'class\s*=\s*["\']([^"\']+)["\']',
            r'ui:style\s+type=["\']([^"\']+)["\']'
        ]
        
        for pattern in style_patterns:
            for match in re.finditer(pattern, content):
                styles.append(match.group(1))
        
        return styles
    
    def _extract_uibinder_themes(self, content: str) -> List[str]:
        """Extract theming information from UiBinder."""
        themes = []
        
        # Look for theme-related patterns
        theme_patterns = [
            r'theme\s*=\s*["\']([^"\']+)["\']',
            r'ui:with\s+type=["\']([^"\']+)["\']'
        ]
        
        for pattern in theme_patterns:
            for match in re.finditer(pattern, content):
                themes.append(match.group(1))
        
        return themes
    
    def _extract_uibinder_event_handlers(self, content: str) -> List[Dict[str, str]]:
        """Extract event handlers from UiBinder."""
        handlers = []
        
        # Look for event handler patterns
        handler_patterns = [
            (r'onClick\s*=\s*["\']([^"\']+)["\']', 'onClick'),
            (r'onChange\s*=\s*["\']([^"\']+)["\']', 'onChange'),
            (r'onBlur\s*=\s*["\']([^"\']+)["\']', 'onBlur'),
            (r'onFocus\s*=\s*["\']([^"\']+)["\']', 'onFocus')
        ]
        
        for pattern, event_type in handler_patterns:
            for match in re.finditer(pattern, content):
                handlers.append({
                    'event': event_type,
                    'handler': match.group(1)
                })
        
        return handlers
    
    def _calculate_gwt_complexity(self, content: str) -> int:
        """Calculate complexity score for GWT Java file."""
        complexity = 1  # Base complexity
        
        # Count GWT-specific constructs
        complexity += len(self.ui_field_pattern.findall(content))
        complexity += len(self.ui_handler_pattern.findall(content))
        complexity += len(self.ui_template_pattern.findall(content))
        complexity += len(self.gwt_create_pattern.findall(content))
        complexity += len(self.gwt_log_pattern.findall(content))
        
        # Count widget creation
        widget_patterns = [
            r'new\s+\w+\s*\(',
            r'\.add\s*\(',
            r'\.setWidget\s*\('
        ]
        
        for pattern in widget_patterns:
            complexity += len(re.findall(pattern, content))
        
        return complexity
    
    def _calculate_uibinder_complexity(self, content: str) -> int:
        """Calculate complexity score for UiBinder file."""
        complexity = 1  # Base complexity
        
        # Count XML elements
        complexity += content.count('<')  # Rough count of elements
        complexity += content.count('=')  # Rough count of attributes
        
        # Count GWT-specific attributes
        complexity += len(self.uibinder_ui_field_pattern.findall(content))
        complexity += len(self.uibinder_ui_handler_pattern.findall(content))
        
        return complexity
