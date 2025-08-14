"""
Intelligent Code Chunking Module

This module provides intelligent code chunking capabilities that:
- Detect programming language automatically
- Chunk code based on semantic boundaries (functions, classes, methods)
- Preserve context across chunks
- Generate enhanced metadata for better search
- Handle different file types appropriately
"""

import re
import ast
import javalang
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger('java_analysis.code_chunker')

@dataclass
class CodeChunk:
    """Represents a chunk of code with enhanced metadata"""
    content: str
    chunk_id: str
    file_path: str
    language: str
    chunk_type: str  # 'function', 'class', 'method', 'import', 'comment', 'other'
    start_line: int
    end_line: int
    parent_context: Optional[str] = None  # e.g., class name for methods
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    imports: List[str] = None
    dependencies: List[str] = None
    complexity_score: float = 0.0
    metadata: Dict[str, Any] = None

class IntelligentCodeChunker:
    """Intelligent code chunking with language-aware parsing"""
    
    def __init__(self):
        self.language_patterns = {
            'python': [r'\.py$', r'def\s+\w+', r'class\s+\w+', r'import\s+', r'from\s+'],
            'java': [r'\.java$', r'public\s+class', r'private\s+', r'public\s+', r'import\s+'],
            'javascript': [r'\.js$', r'function\s+\w+', r'const\s+', r'let\s+', r'import\s+', r'export\s+', r'class\s+\w+'],
            'typescript': [r'\.ts$', r'function\s+\w+', r'interface\s+', r'class\s+', r'import\s+', r'export\s+', r'type\s+'],
            'xml': [r'\.xml$', r'<\?xml', r'<[^>]+>'],
            'yaml': [r'\.ya?ml$', r'^\s*[a-zA-Z_][a-zA-Z0-9_]*:'],
            'json': [r'\.json$', r'^\s*\{', r'^\s*\['],
            'markdown': [r'\.md$', r'^#', r'^##', r'^\*', r'^`'],
            'properties': [r'\.properties$', r'^\s*[a-zA-Z_][a-zA-Z0-9_.]*\s*='],
            'sql': [r'\.sql$', r'SELECT\s+', r'INSERT\s+', r'UPDATE\s+', r'CREATE\s+', r'DROP\s+', r'ALTER\s+'],
            'html': [r'\.html?$', r'<!DOCTYPE', r'<html', r'<head', r'<body'],
            'css': [r'\.css$', r'^\s*[.#]?\w+\s*\{', r'@media', r'@import'],
            'php': [r'\.php$', r'<\?php', r'function\s+\w+', r'class\s+\w+'],
            'ruby': [r'\.rb$', r'def\s+\w+', r'class\s+\w+', r'module\s+\w+', r'require\s+'],
            'go': [r'\.go$', r'func\s+\w+', r'type\s+\w+', r'package\s+', r'import\s+'],
            'rust': [r'\.rs$', r'fn\s+\w+', r'struct\s+\w+', r'impl\s+\w+', r'use\s+'],
            'csharp': [r'\.cs$', r'public\s+class', r'private\s+', r'using\s+', r'namespace\s+'],
            'cpp': [r'\.(cpp|cc|cxx|h|hpp)$', r'class\s+\w+', r'int\s+main', r'#include', r'namespace\s+']
        }
    
    def detect_language(self, file_path: str, content: str = "") -> str:
        """Detect programming language based on file extension and content"""
        # Handle None content
        if content is None:
            content = ""
        
        # Ensure content is string
        if not isinstance(content, str):
            content = str(content)
        
        try:
            # Check file extension first
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Extension-based detection
            if file_extension in ['.py', '.pyw']:
                return 'python'
            elif file_extension in ['.java']:
                return 'java'
            elif file_extension in ['.js']:
                return 'javascript'
            elif file_extension in ['.ts']:
                return 'typescript'
            elif file_extension in ['.sql']:
                return 'sql'
            elif file_extension in ['.xml']:
                return 'xml'
            elif file_extension in ['.yaml', '.yml']:
                return 'yaml'
            elif file_extension in ['.json']:
                return 'json'
            elif file_extension in ['.md']:
                return 'markdown'
            elif file_extension in ['.properties']:
                return 'properties'
            elif file_extension in ['.html', '.htm']:
                return 'html'
            elif file_extension in ['.css']:
                return 'css'
            elif file_extension in ['.php']:
                return 'php'
            elif file_extension in ['.rb']:
                return 'ruby'
            elif file_extension in ['.go']:
                return 'go'
            elif file_extension in ['.rs']:
                return 'rust'
            elif file_extension in ['.cs']:
                return 'csharp'
            elif file_extension in ['.cpp', '.cc', '.cxx', '.h', '.hpp']:
                return 'cpp'
            
            # Content-based detection if extension doesn't match
            for language, patterns in self.language_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return language
            
            return 'unknown'
        except Exception as e:
            logger.error(f"Error detecting language for {file_path}: {e}")
            return 'unknown'
    
    def chunk_python_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk Python code based on AST analysis"""
        chunks = []
        import_counter = 0
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                chunk = None
                
                if isinstance(node, ast.FunctionDef):
                    chunk = CodeChunk(
                        content=ast.unparse(node),
                        chunk_id=f"{file_path}:function:{node.name}:{node.lineno}",
                        file_path=file_path,
                        language='python',
                        chunk_type='function',
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        function_name=node.name,
                        parent_context=getattr(node, 'parent_class', None),
                        complexity_score=self._calculate_complexity(node),
                        metadata=self._extract_python_metadata(node)
                    )
                
                elif isinstance(node, ast.ClassDef):
                    chunk = CodeChunk(
                        content=ast.unparse(node),
                        chunk_id=f"{file_path}:class:{node.name}:{node.lineno}",
                        file_path=file_path,
                        language='python',
                        chunk_type='class',
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        class_name=node.name,
                        complexity_score=self._calculate_complexity(node),
                        metadata=self._extract_python_metadata(node)
                    )
                
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    import_counter += 1
                    chunk = CodeChunk(
                        content=ast.unparse(node),
                        chunk_id=f"{file_path}:import:{import_counter}",
                        file_path=file_path,
                        language='python',
                        chunk_type='import',
                        start_line=node.lineno,
                        end_line=node.lineno,
                        metadata={'imports': self._extract_imports(node)}
                    )
                
                if chunk:
                    chunks.append(chunk)
            
            # Add any remaining content as general chunks
            self._add_remaining_chunks(content, chunks, file_path, 'python')
            
        except SyntaxError as e:
            logger.warning(f"Syntax error in Python file {file_path}: {e}")
            # Fallback to line-based chunking
            chunks = self._fallback_chunking(content, file_path, 'python')
        
        return chunks
    
    def chunk_java_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk Java code based on javalang parsing"""
        chunks = []
        try:
            # Handle None or invalid content
            if content is None:
                logger.warning(f"Content is None for Java file {file_path}, using fallback")
                return self._fallback_chunking("", file_path, 'java')
            
            if not isinstance(content, str):
                logger.warning(f"Content is not string for Java file {file_path}, converting")
                content = str(content)
            
            if not content.strip():
                logger.warning(f"Content is empty for Java file {file_path}, using fallback")
                return self._fallback_chunking(content, file_path, 'java')
            
            tree = javalang.parse.parse(content)
            
            # Check if tree is valid
            if tree is None:
                logger.warning(f"Java parse tree is None for {file_path}, using fallback")
                return self._fallback_chunking(content, file_path, 'java')
            
            # Extract classes
            for path, node in tree:
                if isinstance(node, javalang.tree.ClassDeclaration):
                    chunk = CodeChunk(
                        content=self._extract_java_node_content(content, node),
                        chunk_id=f"{file_path}:class:{node.name}",
                        file_path=file_path,
                        language='java',
                        chunk_type='class',
                        start_line=node.position.line if node.position else 0,
                        end_line=node.position.line if node.position else 0,
                        class_name=node.name,
                        complexity_score=self._calculate_java_complexity(node),
                        metadata=self._extract_java_metadata(node)
                    )
                    chunks.append(chunk)
                
                elif isinstance(node, javalang.tree.MethodDeclaration):
                    chunk = CodeChunk(
                        content=self._extract_java_node_content(content, node),
                        chunk_id=f"{file_path}:method:{node.name}",
                        file_path=file_path,
                        language='java',
                        chunk_type='method',
                        start_line=node.position.line if node.position else 0,
                        end_line=node.position.line if node.position else 0,
                        function_name=node.name,
                        parent_context=getattr(node, 'parent_class', None),
                        complexity_score=self._calculate_java_complexity(node),
                        metadata=self._extract_java_metadata(node)
                    )
                    chunks.append(chunk)
            
            # Add imports safely
            import_counter = 0
            if hasattr(tree, 'imports') and tree.imports:
                for import_decl in tree.imports:
                    if import_decl and hasattr(import_decl, 'path'):
                        import_counter += 1
                        chunk = CodeChunk(
                            content=f"import {import_decl.path};",
                            chunk_id=f"{file_path}:import:{import_counter}",
                            file_path=file_path,
                            language='java',
                            chunk_type='import',
                            start_line=import_decl.position.line if (import_decl.position and hasattr(import_decl.position, 'line')) else 0,
                            end_line=import_decl.position.line if (import_decl.position and hasattr(import_decl.position, 'line')) else 0,
                            metadata={'imports': [str(import_decl.path)]}
                        )
                        chunks.append(chunk)
            
            # Add any remaining content
            self._add_remaining_chunks(content, chunks, file_path, 'java')
            
        except Exception as e:
            logger.warning(f"Error parsing Java file {file_path}: {e}")
            chunks = self._fallback_chunking(content, file_path, 'java')
        
        return chunks
    
    def chunk_javascript_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk JavaScript code based on function and class patterns"""
        chunks = []
        lines = content.split('\n')
        chunk_counter = 0
        
        # Patterns for JavaScript
        function_pattern = r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)'
        class_pattern = r'^(?:export\s+)?class\s+(\w+)'
        const_function_pattern = r'^(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
        let_function_pattern = r'^(?:export\s+)?let\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
        import_pattern = r'^(?:import|export)'
        
        current_chunk = []
        current_type = None
        current_name = None
        brace_count = 0
        in_chunk = False
        
        for line_num, line in enumerate(lines, 1):
            import_match = re.match(import_pattern, line.strip())
            if import_match:
                # Save previous chunk if exists
                if current_chunk and current_type:
                    chunk_counter += 1
                    chunks.append(CodeChunk(
                        content='\n'.join(current_chunk),
                        chunk_id=f"{file_path}:{current_type}:{chunk_counter}",
                        file_path=file_path,
                        language='javascript',
                        chunk_type=current_type,
                        start_line=line_num - len(current_chunk),
                        end_line=line_num - 1,
                        function_name=current_name if current_type == 'function' else None,
                        class_name=current_name if current_type == 'class' else None,
                        complexity_score=len(current_chunk) * 0.5
                    ))
                
                # Start new import chunk
                current_chunk = [line]
                current_type = 'import'
                current_name = None
                in_chunk = True
                continue
            
            # Check for function/class start
            func_match = re.match(function_pattern, line.strip())
            class_match = re.match(class_pattern, line.strip())
            const_func_match = re.match(const_function_pattern, line.strip())
            let_func_match = re.match(let_function_pattern, line.strip())
            
            if func_match or class_match or const_func_match or let_func_match:
                # Save previous chunk
                if current_chunk and current_type:
                    chunk_counter += 1
                    chunks.append(CodeChunk(
                        content='\n'.join(current_chunk),
                        chunk_id=f"{file_path}:{current_type}:{chunk_counter}",
                        file_path=file_path,
                        language='javascript',
                        chunk_type=current_type,
                        start_line=line_num - len(current_chunk),
                        end_line=line_num - 1,
                        function_name=current_name if current_type == 'function' else None,
                        class_name=current_name if current_type == 'class' else None,
                        complexity_score=len(current_chunk) * 0.5
                    ))
                
                # Start new chunk
                current_chunk = [line]
                if func_match:
                    current_type = 'function'
                    current_name = func_match.group(1)
                elif class_match:
                    current_type = 'class'
                    current_name = class_match.group(1)
                elif const_func_match or let_func_match:
                    current_type = 'function'
                    current_name = (const_func_match or let_func_match).group(1)
                
                in_chunk = True
                brace_count = line.count('{') - line.count('}')
                continue
            
            if in_chunk:
                current_chunk.append(line)
                brace_count += line.count('{') - line.count('}')
                
                # End of chunk
                if brace_count == 0 and line.strip():
                    chunk_counter += 1
                    chunks.append(CodeChunk(
                        content='\n'.join(current_chunk),
                        chunk_id=f"{file_path}:{current_type}:{chunk_counter}",
                        file_path=file_path,
                        language='javascript',
                        chunk_type=current_type,
                        start_line=line_num - len(current_chunk) + 1,
                        end_line=line_num,
                        function_name=current_name if current_type == 'function' else None,
                        class_name=current_name if current_type == 'class' else None,
                        complexity_score=len(current_chunk) * 0.5
                    ))
                    current_chunk = []
                    current_type = None
                    current_name = None
                    in_chunk = False
        
        # Add any remaining content
        if current_chunk:
            chunks.append(CodeChunk(
                content='\n'.join(current_chunk),
                chunk_id=f"{file_path}:{current_type or 'other'}:{current_name or 'content'}",
                file_path=file_path,
                language='javascript',
                chunk_type=current_type or 'other',
                start_line=line_num - len(current_chunk) + 1,
                end_line=line_num,
                function_name=current_name if current_type == 'function' else None,
                class_name=current_name if current_type == 'class' else None,
                complexity_score=len(current_chunk) * 0.5
            ))
        
        return chunks
    
    def chunk_typescript_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk TypeScript code (similar to JavaScript but with type annotations)"""
        chunks = self.chunk_javascript_code(content, file_path)
        
        # Update language to TypeScript
        for chunk in chunks:
            chunk.language = 'typescript'
            chunk.chunk_id = chunk.chunk_id.replace('javascript', 'typescript')
        
        return chunks
    
    def chunk_sql_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk SQL code by statements"""
        chunks = []
        lines = content.split('\n')
        
        # SQL statement patterns
        statement_patterns = [
            (r'^SELECT\s+', 'select'),
            (r'^INSERT\s+', 'insert'),
            (r'^UPDATE\s+', 'update'),
            (r'^DELETE\s+', 'delete'),
            (r'^CREATE\s+', 'create'),
            (r'^ALTER\s+', 'alter'),
            (r'^DROP\s+', 'drop'),
            (r'^GRANT\s+', 'grant'),
            (r'^REVOKE\s+', 'revoke')
        ]
        
        current_chunk = []
        current_type = None
        in_statement = False
        chunk_counter = 0
        
        for line_num, line in enumerate(lines, 1):
            # Check for statement start
            statement_start = False
            for pattern, stmt_type in statement_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    # Save previous chunk
                    if current_chunk and current_type:
                        chunk_counter += 1
                        chunks.append(CodeChunk(
                            content='\n'.join(current_chunk),
                            chunk_id=f"{file_path}:{current_type}:{chunk_counter}",
                            file_path=file_path,
                            language='sql',
                            chunk_type=current_type,
                            start_line=line_num - len(current_chunk),
                            end_line=line_num - 1,
                            complexity_score=len(current_chunk) * 0.3
                        ))
                    
                    # Start new statement
                    current_chunk = [line]
                    current_type = stmt_type
                    in_statement = True
                    statement_start = True
                    break
            
            if not statement_start and in_statement:
                current_chunk.append(line)
                
                # End of statement (semicolon)
                if line.strip().endswith(';'):
                    chunk_counter += 1
                    chunks.append(CodeChunk(
                        content='\n'.join(current_chunk),
                        chunk_id=f"{file_path}:{current_type}:{chunk_counter}",
                        file_path=file_path,
                        language='sql',
                        chunk_type=current_type,
                        start_line=line_num - len(current_chunk) + 1,
                        end_line=line_num,
                        complexity_score=len(current_chunk) * 0.3
                    ))
                    current_chunk = []
                    current_type = None
                    in_statement = False
        
        # Add any remaining content
        if current_chunk:
            chunk_counter += 1
            chunks.append(CodeChunk(
                content='\n'.join(current_chunk),
                chunk_id=f"{file_path}:{current_type or 'other'}:{chunk_counter}",
                file_path=file_path,
                language='sql',
                chunk_type=current_type or 'other',
                start_line=len(lines) - len(current_chunk) + 1,
                end_line=len(lines),
                complexity_score=len(current_chunk) * 0.3
            ))
        
        return chunks
    
    def chunk_generic_file(self, content: str, file_path: str, language: str) -> List[CodeChunk]:
        """Generic chunking for other file types"""
        if language == 'markdown':
            return self._chunk_markdown(content, file_path)
        elif language in ['yaml', 'properties']:
            return self._chunk_config_file(content, file_path, language)
        else:
            return self._fallback_chunking(content, file_path, language)
    
    def chunk_code(self, content: str, file_path: str) -> List[CodeChunk]:
        """Main method to chunk code based on detected language"""
        # Handle None content
        if content is None:
            logger.warning(f"Content is None for {file_path}, returning empty chunks")
            return []
        
        # Ensure content is string
        if not isinstance(content, str):
            logger.warning(f"Content is not string for {file_path}, converting")
            content = str(content)
        
        # Handle empty content
        if not content.strip():
            logger.warning(f"Content is empty for {file_path}, returning empty chunks")
            return []
        
        language = self.detect_language(file_path, content)
        
        try:
            if language == 'python':
                return self.chunk_python_code(content, file_path)
            elif language == 'java':
                return self.chunk_java_code(content, file_path)
            elif language == 'javascript':
                return self.chunk_javascript_code(content, file_path)
            elif language == 'typescript':
                return self.chunk_typescript_code(content, file_path)
            elif language == 'sql':
                return self.chunk_sql_code(content, file_path)
            else:
                return self.chunk_generic_file(content, file_path, language)
        except Exception as e:
            logger.error(f"Error chunking code for {file_path}: {e}")
            # Return a fallback chunk
            return [CodeChunk(
                content=content[:1000] + "..." if len(content) > 1000 else content,
                chunk_id=f"{file_path}:fallback:1",
                file_path=file_path,
                language=language or 'unknown',
                chunk_type='fallback',
                start_line=1,
                end_line=1,
                complexity_score=1.0
            )]
    
    def _calculate_complexity(self, node) -> float:
        """Calculate complexity score for a code node"""
        # Simple complexity calculation based on node depth and size
        complexity = 1.0
        
        if hasattr(node, 'body'):
            complexity += len(node.body) * 0.5
        
        if hasattr(node, 'args'):
            # args is an arguments object, not a list
            if hasattr(node.args, 'args'):
                complexity += len(node.args.args) * 0.2
        
        return complexity
    
    def _calculate_java_complexity(self, node) -> float:
        """Calculate complexity for Java nodes"""
        complexity = 1.0
        
        if hasattr(node, 'body'):
            complexity += len(node.body) * 0.5
        
        if hasattr(node, 'parameters'):
            complexity += len(node.parameters) * 0.2
        
        return complexity
    
    def _extract_python_metadata(self, node) -> Dict[str, Any]:
        """Extract metadata from Python AST node"""
        metadata = {}
        
        if hasattr(node, 'name'):
            metadata['name'] = node.name
        
        if hasattr(node, 'args'):
            metadata['parameters'] = [arg.arg for arg in node.args.args]
        
        if hasattr(node, 'decorator_list'):
            metadata['decorators'] = [ast.unparse(dec) for dec in node.decorator_list]
        
        return metadata
    
    def _extract_java_metadata(self, node) -> Dict[str, Any]:
        """Extract metadata from Java node"""
        metadata = {}
        
        if hasattr(node, 'name'):
            metadata['name'] = node.name
        
        if hasattr(node, 'parameters'):
            metadata['parameters'] = [str(param.type) for param in node.parameters]
        
        if hasattr(node, 'modifiers'):
            metadata['modifiers'] = [str(mod) for mod in node.modifiers]
        
        return metadata
    
    def _extract_imports(self, node) -> List[str]:
        """Extract import information from Python import node"""
        if isinstance(node, ast.Import):
            return [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            return [f"{node.module}.{alias.name}" for alias in node.names]
        return []
    
    def _extract_java_node_content(self, content: str, node) -> str:
        """Extract the actual content for a Java node with robust error handling"""
        try:
            # Handle None content
            if content is None:
                logger.warning(f"Content is None for Java node: {getattr(node, 'name', 'unknown')}")
                return f"// Content not available for {getattr(node, 'name', 'unknown')}"
            
            # Ensure content is string
            if not isinstance(content, str):
                logger.warning(f"Content is not string for Java node: {getattr(node, 'name', 'unknown')}")
                content = str(content)
            
            # Split into lines safely
            lines = content.split('\n')
            if not lines:
                return f"// Empty content for {getattr(node, 'name', 'unknown')}"
            
            # Check if node has position information
            if hasattr(node, 'position') and node.position and hasattr(node.position, 'line'):
                start_line = max(0, node.position.line - 1)  # Ensure non-negative
                
                # Bounds check
                if start_line >= len(lines):
                    logger.warning(f"Start line {start_line} exceeds content length {len(lines)} for node {getattr(node, 'name', 'unknown')}")
                    return f"// Node position out of bounds: {getattr(node, 'name', 'unknown')}"
                
                # Find the end by looking for closing brace
                end_line = start_line
                brace_count = 0
                
                for i in range(start_line, len(lines)):
                    line = lines[i]
                    if line is not None:  # Safety check
                        brace_count += line.count('{') - line.count('}')
                        if brace_count == 0 and i > start_line:
                            end_line = i
                            break
                
                # Extract content safely
                if start_line <= end_line < len(lines):
                    extracted_lines = lines[start_line:end_line + 1]
                    return '\n'.join(extracted_lines)
                else:
                    # Fallback to just the start line if range is invalid
                    if start_line < len(lines):
                        return lines[start_line]
                    else:
                        logger.warning(f"Invalid line range for Java node: {getattr(node, 'name', 'unknown')}")
                        return f"// Invalid line range for {getattr(node, 'name', 'unknown')}"
            
            # Fallback to string representation of node
            try:
                return str(node)
            except Exception as e:
                logger.warning(f"Could not convert Java node to string: {e}")
                return f"// Node conversion failed: {getattr(node, 'name', 'unknown')}"
                
        except Exception as e:
            logger.error(f"Error extracting Java node content: {e}")
            return f"// Error extracting content: {str(e)}"
    
    def _chunk_markdown(self, content: str, file_path: str) -> List[CodeChunk]:
        """Chunk markdown files by headers"""
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_header = None
        line_number = 0
        
        for line in lines:
            line_number += 1
            
            if line.startswith('#'):
                # Save previous chunk
                if current_chunk and current_header:
                    chunks.append(CodeChunk(
                        content='\n'.join(current_chunk),
                        chunk_id=f"{file_path}:section:{current_header}",
                        file_path=file_path,
                        language='markdown',
                        chunk_type='section',
                        start_line=line_number - len(current_chunk),
                        end_line=line_number - 1,
                        metadata={'header': current_header}
                    ))
                
                current_header = line.strip('#').strip()
                current_chunk = [line]
            else:
                current_chunk.append(line)
        
        # Add final chunk
        if current_chunk:
            chunks.append(CodeChunk(
                content='\n'.join(current_chunk),
                chunk_id=f"{file_path}:section:{current_header or 'content'}",
                file_path=file_path,
                language='markdown',
                chunk_type='section',
                start_line=line_number - len(current_chunk) + 1,
                end_line=line_number,
                metadata={'header': current_header}
            ))
        
        return chunks
    
    def _chunk_config_file(self, content: str, file_path: str, language: str) -> List[CodeChunk]:
        """Chunk configuration files by sections"""
        chunks = []
        
        if language == 'yaml':
            # Simple YAML chunking by top-level keys
            lines = content.split('\n')
            current_chunk = []
            current_section = None
            
            for line in lines:
                if line.strip() and not line.startswith(' ') and line.endswith(':'):
                    # New section
                    if current_chunk and current_section:
                        chunks.append(CodeChunk(
                            content='\n'.join(current_chunk),
                            chunk_id=f"{file_path}:section:{current_section}",
                            file_path=file_path,
                            language=language,
                            chunk_type='section',
                            start_line=0,
                            end_line=len(current_chunk),
                            metadata={'section': current_section}
                        ))
                    
                    current_section = line.strip()[:-1]
                    current_chunk = [line]
                else:
                    current_chunk.append(line)
            
            # Add final chunk
            if current_chunk:
                chunks.append(CodeChunk(
                    content='\n'.join(current_chunk),
                    chunk_id=f"{file_path}:section:{current_section or 'config'}",
                    file_path=file_path,
                    language=language,
                    chunk_type='section',
                    start_line=0,
                    end_line=len(current_chunk),
                    metadata={'section': current_section}
                ))
        
        return chunks
    
    def _fallback_chunking(self, content: str, file_path: str, language: str) -> List[CodeChunk]:
        """Fallback chunking method for unsupported languages"""
        chunks = []
        lines = content.split('\n')
        chunk_size = 50  # lines per chunk
        
        for i in range(0, len(lines), chunk_size):
            chunk_lines = lines[i:i + chunk_size]
            chunks.append(CodeChunk(
                content='\n'.join(chunk_lines),
                chunk_id=f"{file_path}:chunk:{i//chunk_size}",
                file_path=file_path,
                language=language,
                chunk_type='other',
                start_line=i + 1,
                end_line=min(i + chunk_size, len(lines)),
                metadata={'chunk_index': i // chunk_size}
            ))
        
        return chunks
    
    def _add_remaining_chunks(self, content: str, existing_chunks: List[CodeChunk], file_path: str, language: str):
        """Add chunks for remaining content not covered by structured parsing"""
        # This is a simplified implementation
        # In practice, you'd want to identify uncovered lines and create appropriate chunks
        pass 