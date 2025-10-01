"""
XML and SQL parser for extracting metadata from configuration and database files.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
import logging


class XMLSQLParser:
    """Parser for XML and SQL files."""
    
    def __init__(self):
        """Initialize the XML/SQL parser."""
        self.logger = logging.getLogger(__name__)
        
        # SQL patterns
        self.create_table_pattern = re.compile(r'CREATE\s+TABLE\s+(\w+)', re.IGNORECASE)
        self.create_view_pattern = re.compile(r'CREATE\s+VIEW\s+(\w+)', re.IGNORECASE)
        self.column_pattern = re.compile(r'(\w+)\s+(\w+(?:\([^)]*\))?)', re.IGNORECASE)
        self.constraint_pattern = re.compile(r'(?:PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK)\s*\([^)]*\)', re.IGNORECASE)
        self.index_pattern = re.compile(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(\w+)', re.IGNORECASE)
        self.select_pattern = re.compile(r'SELECT\s+.*?FROM\s+(\w+)', re.IGNORECASE | re.DOTALL)
        self.insert_pattern = re.compile(r'INSERT\s+INTO\s+(\w+)', re.IGNORECASE)
        self.update_pattern = re.compile(r'UPDATE\s+(\w+)', re.IGNORECASE)
        self.delete_pattern = re.compile(r'DELETE\s+FROM\s+(\w+)', re.IGNORECASE)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse an XML or SQL file and extract metadata."""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'sql':
            return self._parse_sql_file(file_path, content)
        elif file_extension == 'xml':
            return self._parse_xml_file(file_path, content)
        else:
            return {
                'file_path': file_path,
                'language': 'unknown',
                'error': f'Unsupported file type: {file_extension}'
            }
    
    def _parse_sql_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse SQL file and extract database metadata."""
        try:
            # Extract database objects
            tables = self._extract_tables(content)
            views = self._extract_views(content)
            indexes = self._extract_indexes(content)
            
            # Extract queries
            selects = self._extract_select_queries(content)
            inserts = self._extract_insert_queries(content)
            updates = self._extract_update_queries(content)
            deletes = self._extract_delete_queries(content)
            
            # Extract constraints
            constraints = self._extract_constraints(content)
            
            # Calculate complexity
            complexity_score = self._calculate_sql_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'sql',
                'tables': tables,
                'views': views,
                'indexes': indexes,
                'selects': selects,
                'inserts': inserts,
                'updates': updates,
                'deletes': deletes,
                'constraints': constraints,
                'complexity_score': complexity_score,
                'line_count': line_count
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing SQL file {file_path}: {e}")
            return {
                'file_path': file_path,
                'language': 'sql',
                'error': str(e)
            }
    
    def _parse_xml_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse XML file and extract configuration metadata."""
        try:
            # Try to parse as XML
            root = ET.fromstring(content)
            
            # Extract basic structure
            elements = self._extract_xml_elements(root)
            attributes = self._extract_xml_attributes(root)
            text_content = self._extract_xml_text(root)
            
            # Extract specific configurations based on file type
            config_data = self._extract_configuration_data(root, file_path)
            
            # Calculate complexity
            complexity_score = self._calculate_xml_complexity(content)
            line_count = len(content.splitlines())
            
            return {
                'file_path': file_path,
                'language': 'xml',
                'root_element': root.tag,
                'elements': elements,
                'attributes': attributes,
                'text_content': text_content,
                'configuration': config_data,
                'complexity_score': complexity_score,
                'line_count': line_count
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
    
    def _extract_tables(self, content: str) -> List[Dict[str, Any]]:
        """Extract table definitions from SQL."""
        tables = []
        
        for match in self.create_table_pattern.finditer(content):
            table_name = match.group(1)
            
            # Find the table definition block
            table_start = match.start()
            table_end = self._find_matching_paren(content, table_start + content[table_start:].find('('))
            
            if table_end > table_start:
                table_definition = content[table_start:table_end + 1]
                
                # Extract columns
                columns = self._extract_columns(table_definition)
                
                # Extract constraints
                constraints = self._extract_table_constraints(table_definition)
                
                tables.append({
                    'name': table_name,
                    'columns': columns,
                    'constraints': constraints,
                    'definition': table_definition
                })
        
        return tables
    
    def _extract_views(self, content: str) -> List[Dict[str, str]]:
        """Extract view definitions from SQL."""
        views = []
        
        for match in self.create_view_pattern.finditer(content):
            view_name = match.group(1)
            views.append({
                'name': view_name,
                'definition': match.group(0)
            })
        
        return views
    
    def _extract_indexes(self, content: str) -> List[Dict[str, str]]:
        """Extract index definitions from SQL."""
        indexes = []
        
        for match in self.index_pattern.finditer(content):
            index_name = match.group(1)
            indexes.append({
                'name': index_name,
                'definition': match.group(0)
            })
        
        return indexes
    
    def _extract_select_queries(self, content: str) -> List[Dict[str, str]]:
        """Extract SELECT queries from SQL."""
        queries = []
        
        for match in self.select_pattern.finditer(content):
            table_name = match.group(1)
            queries.append({
                'type': 'SELECT',
                'table': table_name,
                'query': match.group(0)
            })
        
        return queries
    
    def _extract_insert_queries(self, content: str) -> List[Dict[str, str]]:
        """Extract INSERT queries from SQL."""
        queries = []
        
        for match in self.insert_pattern.finditer(content):
            table_name = match.group(1)
            queries.append({
                'type': 'INSERT',
                'table': table_name,
                'query': match.group(0)
            })
        
        return queries
    
    def _extract_update_queries(self, content: str) -> List[Dict[str, str]]:
        """Extract UPDATE queries from SQL."""
        queries = []
        
        for match in self.update_pattern.finditer(content):
            table_name = match.group(1)
            queries.append({
                'type': 'UPDATE',
                'table': table_name,
                'query': match.group(0)
            })
        
        return queries
    
    def _extract_delete_queries(self, content: str) -> List[Dict[str, str]]:
        """Extract DELETE queries from SQL."""
        queries = []
        
        for match in self.delete_pattern.finditer(content):
            table_name = match.group(1)
            queries.append({
                'type': 'DELETE',
                'table': table_name,
                'query': match.group(0)
            })
        
        return queries
    
    def _extract_constraints(self, content: str) -> List[str]:
        """Extract constraint definitions from SQL."""
        constraints = []
        
        for match in self.constraint_pattern.finditer(content):
            constraints.append(match.group(0))
        
        return constraints
    
    def _extract_columns(self, table_definition: str) -> List[Dict[str, str]]:
        """Extract column definitions from table definition."""
        columns = []
        
        # Find the column definitions between parentheses
        paren_start = table_definition.find('(')
        paren_end = table_definition.rfind(')')
        
        if paren_start != -1 and paren_end != -1:
            column_section = table_definition[paren_start + 1:paren_end]
            
            # Split by commas, but be careful about nested parentheses
            column_definitions = self._split_sql_columns(column_section)
            
            for col_def in column_definitions:
                col_def = col_def.strip()
                if col_def and not col_def.upper().startswith(('PRIMARY', 'FOREIGN', 'UNIQUE', 'CHECK')):
                    # Extract column name and type
                    parts = col_def.split()
                    if len(parts) >= 2:
                        column_name = parts[0]
                        column_type = parts[1]
                        
                        # Extract constraints
                        constraints = []
                        if 'NOT NULL' in col_def.upper():
                            constraints.append('NOT NULL')
                        if 'UNIQUE' in col_def.upper():
                            constraints.append('UNIQUE')
                        if 'PRIMARY KEY' in col_def.upper():
                            constraints.append('PRIMARY KEY')
                        
                        columns.append({
                            'name': column_name,
                            'type': column_type,
                            'constraints': constraints,
                            'definition': col_def
                        })
        
        return columns
    
    def _extract_table_constraints(self, table_definition: str) -> List[Dict[str, str]]:
        """Extract table-level constraints."""
        constraints = []
        
        # Look for constraint patterns
        constraint_patterns = [
            (r'PRIMARY\s+KEY\s*\([^)]+\)', 'PRIMARY KEY'),
            (r'FOREIGN\s+KEY\s*\([^)]+\)\s+REFERENCES\s+(\w+)\s*\([^)]+\)', 'FOREIGN KEY'),
            (r'UNIQUE\s*\([^)]+\)', 'UNIQUE'),
            (r'CHECK\s*\([^)]+\)', 'CHECK')
        ]
        
        for pattern, constraint_type in constraint_patterns:
            for match in re.finditer(pattern, table_definition, re.IGNORECASE):
                constraints.append({
                    'type': constraint_type,
                    'definition': match.group(0)
                })
        
        return constraints
    
    def _split_sql_columns(self, column_section: str) -> List[str]:
        """Split SQL column definitions by commas, respecting nested parentheses."""
        columns = []
        current_col = ""
        paren_count = 0
        
        for char in column_section:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                columns.append(current_col.strip())
                current_col = ""
                continue
            
            current_col += char
        
        if current_col.strip():
            columns.append(current_col.strip())
        
        return columns
    
    def _find_matching_paren(self, content: str, start_pos: int) -> int:
        """Find the matching closing parenthesis."""
        if start_pos >= len(content) or content[start_pos] != '(':
            return -1
        
        paren_count = 1
        pos = start_pos + 1
        
        while pos < len(content) and paren_count > 0:
            if content[pos] == '(':
                paren_count += 1
            elif content[pos] == ')':
                paren_count -= 1
            pos += 1
        
        return pos - 1 if paren_count == 0 else -1
    
    def _extract_xml_elements(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extract XML element structure."""
        elements = []
        
        def process_element(element: ET.Element, depth: int = 0):
            element_info = {
                'tag': element.tag,
                'depth': depth,
                'attributes': dict(element.attrib),
                'text': element.text.strip() if element.text else '',
                'children_count': len(element)
            }
            elements.append(element_info)
            
            for child in element:
                process_element(child, depth + 1)
        
        process_element(root)
        return elements
    
    def _extract_xml_attributes(self, root: ET.Element) -> Dict[str, List[str]]:
        """Extract all XML attributes and their values."""
        attributes = {}
        
        def collect_attributes(element: ET.Element):
            for attr_name, attr_value in element.attrib.items():
                if attr_name not in attributes:
                    attributes[attr_name] = []
                if attr_value not in attributes[attr_name]:
                    attributes[attr_name].append(attr_value)
            
            for child in element:
                collect_attributes(child)
        
        collect_attributes(root)
        return attributes
    
    def _extract_xml_text(self, root: ET.Element) -> str:
        """Extract all text content from XML."""
        text_parts = []
        
        def collect_text(element: ET.Element):
            if element.text and element.text.strip():
                text_parts.append(element.text.strip())
            
            for child in element:
                collect_text(child)
        
        collect_text(root)
        return ' '.join(text_parts)
    
    def _extract_configuration_data(self, root: ET.Element, file_path: str) -> Dict[str, Any]:
        """Extract configuration-specific data based on file type."""
        config_data = {}
        
        # Web.xml specific extraction
        if 'web.xml' in file_path.lower():
            config_data.update(self._extract_web_xml_config(root))
        
        # Spring configuration
        elif any(tag in root.tag.lower() for tag in ['beans', 'configuration']):
            config_data.update(self._extract_spring_config(root))
        
        # Maven POM
        elif root.tag == 'project':
            config_data.update(self._extract_maven_config(root))
        
        return config_data
    
    def _extract_web_xml_config(self, root: ET.Element) -> Dict[str, Any]:
        """Extract web.xml specific configuration."""
        config = {
            'servlets': [],
            'filters': [],
            'listeners': [],
            'context_params': []
        }
        
        # Extract servlets
        for servlet in root.findall('.//servlet'):
            servlet_info = {
                'name': servlet.find('servlet-name').text if servlet.find('servlet-name') is not None else '',
                'class': servlet.find('servlet-class').text if servlet.find('servlet-class') is not None else '',
                'init_params': {}
            }
            
            for param in servlet.findall('init-param'):
                param_name = param.find('param-name').text if param.find('param-name') is not None else ''
                param_value = param.find('param-value').text if param.find('param-value') is not None else ''
                servlet_info['init_params'][param_name] = param_value
            
            config['servlets'].append(servlet_info)
        
        # Extract filters
        for filter_elem in root.findall('.//filter'):
            filter_info = {
                'name': filter_elem.find('filter-name').text if filter_elem.find('filter-name') is not None else '',
                'class': filter_elem.find('filter-class').text if filter_elem.find('filter-class') is not None else ''
            }
            config['filters'].append(filter_info)
        
        # Extract context parameters
        for param in root.findall('.//context-param'):
            param_name = param.find('param-name').text if param.find('param-name') is not None else ''
            param_value = param.find('param-value').text if param.find('param-value') is not None else ''
            config['context_params'].append({
                'name': param_name,
                'value': param_value
            })
        
        return config
    
    def _extract_spring_config(self, root: ET.Element) -> Dict[str, Any]:
        """Extract Spring configuration data."""
        config = {
            'beans': [],
            'properties': []
        }
        
        # Extract bean definitions
        for bean in root.findall('.//bean'):
            bean_info = {
                'id': bean.get('id', ''),
                'class': bean.get('class', ''),
                'scope': bean.get('scope', 'singleton'),
                'properties': []
            }
            
            for prop in bean.findall('property'):
                prop_info = {
                    'name': prop.get('name', ''),
                    'value': prop.get('value', ''),
                    'ref': prop.get('ref', '')
                }
                bean_info['properties'].append(prop_info)
            
            config['beans'].append(bean_info)
        
        return config
    
    def _extract_maven_config(self, root: ET.Element) -> Dict[str, Any]:
        """Extract Maven POM configuration."""
        config = {
            'groupId': '',
            'artifactId': '',
            'version': '',
            'dependencies': []
        }
        
        # Extract basic project info
        if root.find('groupId') is not None:
            config['groupId'] = root.find('groupId').text
        if root.find('artifactId') is not None:
            config['artifactId'] = root.find('artifactId').text
        if root.find('version') is not None:
            config['version'] = root.find('version').text
        
        # Extract dependencies
        for dep in root.findall('.//dependency'):
            dep_info = {
                'groupId': dep.find('groupId').text if dep.find('groupId') is not None else '',
                'artifactId': dep.find('artifactId').text if dep.find('artifactId') is not None else '',
                'version': dep.find('version').text if dep.find('version') is not None else ''
            }
            config['dependencies'].append(dep_info)
        
        return config
    
    def _calculate_sql_complexity(self, content: str) -> int:
        """Calculate complexity score for SQL file."""
        complexity = 1  # Base complexity
        
        # Count various SQL constructs
        complexity += len(self.create_table_pattern.findall(content))
        complexity += len(self.create_view_pattern.findall(content))
        complexity += len(self.select_pattern.findall(content))
        complexity += len(self.insert_pattern.findall(content))
        complexity += len(self.update_pattern.findall(content))
        complexity += len(self.delete_pattern.findall(content))
        complexity += len(self.constraint_pattern.findall(content))
        
        return complexity
    
    def _calculate_xml_complexity(self, content: str) -> int:
        """Calculate complexity score for XML file."""
        complexity = 1  # Base complexity
        
        # Count XML elements and attributes
        complexity += content.count('<')  # Rough count of elements
        complexity += content.count('=')  # Rough count of attributes
        
        return complexity
