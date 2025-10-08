"""
Java code extraction for DAO calls and method analysis.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration, MethodInvocation, MemberReference
from javalang.parser import JavaSyntaxError

from config.settings import settings

logger = logging.getLogger(__name__)

class JavaCallsExtractor:
    """Extracts Java method calls and DAO patterns."""
    
    def __init__(self):
        """Initialize Java calls extractor."""
        self.output_dir = settings.build_dir / "java_calls"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Common DAO patterns
        self.dao_patterns = [
            'insert', 'update', 'delete', 'select', 'find', 'get', 'save', 'load',
            'create', 'remove', 'modify', 'query', 'search', 'fetch'
        ]
        
        # iBATIS statement reference patterns
        self.ibatis_patterns = [
            'selectOne', 'selectList', 'selectMap', 'insert', 'update', 'delete',
            'queryForObject', 'queryForList', 'queryForMap'
        ]
    
    def extract_java_calls(self, java_files: List[str]) -> List[Dict[str, Any]]:
        """Extract Java method calls from Java files."""
        dao_calls = []
        
        for java_file in java_files:
            try:
                logger.info(f"Processing Java file: {java_file}")
                file_calls = self._extract_from_single_java(java_file)
                dao_calls.extend(file_calls)
                
            except Exception as e:
                logger.error(f"Failed to process Java file {java_file}: {e}")
                continue
        
        # Save all DAO calls JSON
        self._save_all_calls_json(dao_calls)
        
        logger.info(f"Extracted {len(dao_calls)} Java method calls")
        return dao_calls
    
    def _extract_from_single_java(self, java_file: str) -> List[Dict[str, Any]]:
        """Extract method calls from a single Java file."""
        dao_calls = []
        
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Java code
            tree = javalang.parse.parse(content)
            
            # Extract DAO calls
            calls = self._extract_dao_calls_from_ast(tree, java_file)
            dao_calls.extend(calls)
            
        except JavaSyntaxError as e:
            logger.warning(f"Java syntax error in {java_file}: {e}")
        except Exception as e:
            logger.error(f"Failed to parse Java file {java_file}: {e}")
        
        return dao_calls
    
    def _extract_dao_calls_from_ast(self, tree, java_file: str) -> List[Dict[str, Any]]:
        """Extract DAO calls from Java AST."""
        dao_calls = []
        
        for path, node in tree:
            if isinstance(node, MethodDeclaration):
                # Analyze method for DAO calls
                method_calls = self._analyze_method_for_dao_calls(node, java_file)
                dao_calls.extend(method_calls)
        
        return dao_calls
    
    def _analyze_method_for_dao_calls(self, method_decl: MethodDeclaration, java_file: str) -> List[Dict[str, Any]]:
        """Analyze a method for DAO calls."""
        dao_calls = []
        
        # Get method information
        method_name = method_decl.name
        class_name = self._get_class_name_from_path(java_file)
        package_name = self._get_package_name_from_path(java_file)
        full_class_name = f"{package_name}.{class_name}" if package_name else class_name
        
        # Extract parameters
        parameters = []
        if method_decl.parameters:
            for param in method_decl.parameters:
                param_info = {
                    'name': param.name,
                    'type': param.type.name if param.type else 'unknown'
                }
                parameters.append(param_info)
        
        # Look for iBATIS statement references in method body
        statement_refs = self._extract_statement_references(method_decl)
        
        # Check if this method looks like a DAO method
        if self._is_dao_method(method_name, statement_refs):
            dao_call = {
                'project': self._get_project_name(java_file),
                'path': java_file,
                'lineStart': method_decl.position.line if method_decl.position else 1,
                'lineEnd': method_decl.position.line + 20 if method_decl.position else 20,
                'text': f"[DAO Call] {full_class_name}.{method_name}",
                'meta': {
                    'className': full_class_name,
                    'methodName': method_name,
                    'isDaoMethod': True
                },
                'daoClass': full_class_name,
                'methodName': method_name,
                'statementRefs': statement_refs,
                'parameters': parameters
            }
            dao_calls.append(dao_call)
            
            # Save individual DAO call JSON
            self._save_dao_call_json(dao_call)
        
        return dao_calls
    
    def _extract_statement_references(self, method_decl: MethodDeclaration) -> List[str]:
        """Extract iBATIS statement references from method body."""
        statement_refs = []
        
        # This is a simplified extraction - in practice, you'd need to traverse the method body
        # and look for string literals that match iBATIS statement patterns
        
        # For now, we'll look for common patterns in the method name
        method_name = method_decl.name.lower()
        
        # Check if method name suggests iBATIS statement usage
        for pattern in self.ibatis_patterns:
            if pattern.lower() in method_name:
                # Try to construct statement reference
                statement_ref = f"{self._get_package_name_from_path('')}.{method_name}"
                statement_refs.append(statement_ref)
        
        return statement_refs
    
    def _is_dao_method(self, method_name: str, statement_refs: List[str]) -> bool:
        """Check if a method is likely a DAO method."""
        method_name_lower = method_name.lower()
        
        # Check method name patterns
        for pattern in self.dao_patterns:
            if pattern in method_name_lower:
                return True
        
        # Check if it has statement references
        if statement_refs:
            return True
        
        # Check for common DAO return types (would need more analysis)
        return False
    
    def _get_class_name_from_path(self, java_file: str) -> str:
        """Extract class name from Java file path."""
        file_name = Path(java_file).stem
        return file_name
    
    def _get_package_name_from_path(self, java_file: str) -> str:
        """Extract package name from Java file path."""
        if not java_file:
            return ""
        
        path_parts = Path(java_file).parts
        
        # Look for src/main/java or similar structure
        java_index = -1
        for i, part in enumerate(path_parts):
            if part == 'java':
                java_index = i
                break
        
        if java_index >= 0 and java_index + 1 < len(path_parts):
            # Extract package from path after java directory
            package_parts = path_parts[java_index + 1:-1]  # Exclude the file name
            return '.'.join(package_parts)
        
        return ""
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'dao', 'service']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_dao_call_json(self, dao_call: Dict[str, Any]):
        """Save individual DAO call as JSON."""
        class_name = dao_call.get('daoClass', 'unknown').split('.')[-1]
        method_name = dao_call.get('methodName', 'unknown')
        safe_name = f"{class_name}_{method_name}".replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dao_call, f, indent=2, ensure_ascii=False)
    
    def _save_all_calls_json(self, dao_calls: List[Dict[str, Any]]):
        """Save all DAO calls as a single JSON file."""
        output_file = self.output_dir / "all_dao_calls.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dao_calls, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(dao_calls)} DAO calls to {output_file}")
