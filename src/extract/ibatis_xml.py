"""
iBATIS XML extraction for SQL statements and mappings.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from lxml import etree

from config.settings import settings

logger = logging.getLogger(__name__)

class IbatisXmlExtractor:
    """Extracts iBATIS SQL statements and mappings from XML files."""
    
    def __init__(self):
        """Initialize iBATIS XML extractor."""
        self.output_dir = settings.build_dir / "ibatis_statements"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_ibatis_statements(self, xml_files: List[str]) -> List[Dict[str, Any]]:
        """Extract iBATIS statements from XML files."""
        statements = []
        
        for xml_file in xml_files:
            try:
                logger.info(f"Processing iBATIS XML file: {xml_file}")
                file_statements = self._extract_from_single_xml(xml_file)
                statements.extend(file_statements)
                
            except Exception as e:
                logger.error(f"Failed to process iBATIS XML file {xml_file}: {e}")
                continue
        
        # Save all statements JSON
        self._save_all_statements_json(statements)
        
        logger.info(f"Extracted {len(statements)} iBATIS statements")
        return statements
    
    def _extract_from_single_xml(self, xml_file: str) -> List[Dict[str, Any]]:
        """Extract iBATIS statements from a single XML file."""
        statements = []
        
        try:
            # Parse XML
            tree = etree.parse(xml_file)
            root = tree.getroot()
            
            # Check if this is an iBATIS mapper file
            if not self._is_ibatis_mapper(root):
                return statements
            
            # Extract namespace
            namespace = root.get('namespace', '')
            
            # Extract all statement elements
            statement_elements = root.findall('.//select') + root.findall('.//insert') + \
                               root.findall('.//update') + root.findall('.//delete')
            
            for stmt_elem in statement_elements:
                statement = self._extract_single_statement(stmt_elem, xml_file, namespace)
                if statement:
                    statements.append(statement)
                    
                    # Save individual statement JSON
                    self._save_statement_json(statement)
            
        except Exception as e:
            logger.error(f"Failed to extract iBATIS statements from {xml_file}: {e}")
        
        return statements
    
    def _is_ibatis_mapper(self, root) -> bool:
        """Check if the XML root is an iBATIS mapper."""
        # Check for iBATIS mapper namespace or DOCTYPE
        if root.tag == 'mapper' or 'mapper' in root.tag:
            return True
        
        # Check for iBATIS-specific elements
        ibatis_elements = ['select', 'insert', 'update', 'delete', 'resultMap', 'parameterMap']
        for elem in ibatis_elements:
            if root.find(f'.//{elem}') is not None:
                return True
        
        return False
    
    def _extract_single_statement(self, stmt_elem, xml_file: str, namespace: str) -> Optional[Dict[str, Any]]:
        """Extract a single iBATIS statement."""
        try:
            statement_id = stmt_elem.get('id', '')
            statement_type = stmt_elem.tag.upper()
            
            # Get SQL content
            sql_content = etree.tostring(stmt_elem, encoding='unicode', method='text').strip()
            
            # Extract parameter map
            parameter_map = self._extract_parameter_map(stmt_elem)
            
            # Extract result map
            result_map = self._extract_result_map(stmt_elem)
            
            # Extract parameter type
            parameter_type = stmt_elem.get('parameterType', '')
            
            # Extract result type
            result_type = stmt_elem.get('resultType', '')
            
            # Create statement artifact
            statement = {
                'project': self._get_project_name(xml_file),
                'path': xml_file,
                'lineStart': stmt_elem.sourceline if hasattr(stmt_elem, 'sourceline') else 1,
                'lineEnd': stmt_elem.sourceline + 50 if hasattr(stmt_elem, 'sourceline') else 50,
                'text': f"[iBATIS {statement_type}] {namespace}.{statement_id}",
                'meta': {
                    'namespace': namespace,
                    'statementId': statement_id,
                    'statementType': statement_type,
                    'parameterType': parameter_type,
                    'resultType': result_type
                },
                'statementId': f"{namespace}.{statement_id}",
                'statementType': statement_type,
                'sqlContent': sql_content,
                'parameterMap': parameter_map,
                'resultMap': result_map
            }
            
            return statement
            
        except Exception as e:
            logger.error(f"Failed to extract statement from element: {e}")
            return None
    
    def _extract_parameter_map(self, stmt_elem) -> Dict[str, Any]:
        """Extract parameter mapping information."""
        parameter_map = {
            'parameters': [],
            'parameterType': stmt_elem.get('parameterType', ''),
            'parameterMap': stmt_elem.get('parameterMap', '')
        }
        
        # Look for parameter elements
        param_elements = stmt_elem.findall('.//parameter')
        for param_elem in param_elements:
            param_info = {
                'property': param_elem.get('property', ''),
                'jdbcType': param_elem.get('jdbcType', ''),
                'javaType': param_elem.get('javaType', ''),
                'typeHandler': param_elem.get('typeHandler', '')
            }
            parameter_map['parameters'].append(param_info)
        
        return parameter_map
    
    def _extract_result_map(self, stmt_elem) -> Dict[str, Any]:
        """Extract result mapping information."""
        result_map = {
            'resultType': stmt_elem.get('resultType', ''),
            'resultMap': stmt_elem.get('resultMap', ''),
            'columns': []
        }
        
        # Look for result elements
        result_elements = stmt_elem.findall('.//result')
        for result_elem in result_elements:
            result_info = {
                'property': result_elem.get('property', ''),
                'column': result_elem.get('column', ''),
                'jdbcType': result_elem.get('jdbcType', ''),
                'javaType': result_elem.get('javaType', '')
            }
            result_map['columns'].append(result_info)
        
        return result_map
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'mapper', 'sql']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_statement_json(self, statement: Dict[str, Any]):
        """Save individual statement as JSON."""
        statement_id = statement.get('statementId', 'unknown')
        safe_id = statement_id.replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(statement, f, indent=2, ensure_ascii=False)
    
    def _save_all_statements_json(self, statements: List[Dict[str, Any]]):
        """Save all statements as a single JSON file."""
        output_file = self.output_dir / "all_statements.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(statements, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(statements)} iBATIS statements to {output_file}")
