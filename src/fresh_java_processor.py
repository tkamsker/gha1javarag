"""
Fresh Java Code Processor for Weaviate
Processes Java enterprise application directly into Weaviate with Qwen3-Coder analysis
Optimized for 1M token context window and repository-scale insights
"""

import os
import asyncio
import logging
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re

try:
    from ollama_integration import OllamaIntegration, QwenAnalysisResult
    from weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
    from weaviate_schemas import SchemaManager
    from code_chunker import CodeChunk, ChunkType
except ImportError:
    from .ollama_integration import OllamaIntegration, QwenAnalysisResult
    from .weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
    from .weaviate_schemas import SchemaManager
    from .code_chunker import CodeChunk, ChunkType

logger = logging.getLogger('java_analysis.fresh_java_processor')

@dataclass
class JavaFileInfo:
    """Information about a Java file"""
    file_path: str
    package_name: str
    class_names: List[str]
    imports: List[str]
    methods: List[str]
    annotations: List[str]
    size_bytes: int
    lines_of_code: int
    complexity_estimate: int
    file_type: str  # java, xml, sql, properties
    module_name: str

@dataclass
class ProcessingStats:
    """Statistics for processing operation"""
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    java_files: int = 0
    xml_files: int = 0
    sql_files: int = 0
    total_lines: int = 0
    total_size_bytes: int = 0
    processing_time: float = 0.0
    qwen_analysis_time: float = 0.0
    weaviate_insertion_time: float = 0.0

class FreshJavaProcessor:
    """
    Fresh processor for Java enterprise applications
    Direct processing into Weaviate with 1M context optimization
    """
    
    def __init__(self, 
                 java_root_path: str,
                 weaviate_config: WeaviateConfig = None,
                 ollama_integration: OllamaIntegration = None):
        
        self.java_root_path = Path(java_root_path)
        self.ollama = ollama_integration or OllamaIntegration()
        self.weaviate = EnhancedWeaviateConnector(weaviate_config)
        
        self.stats = ProcessingStats()
        self.processed_files = set()
        
        # File type mappings
        self.file_extensions = {
            '.java': 'java',
            '.xml': 'xml',
            '.sql': 'sql',
            '.properties': 'properties',
            '.wsdl': 'wsdl',
            '.xsd': 'xsd'
        }
        
        # Patterns for Java analysis
        self.java_patterns = {
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)', re.MULTILINE),
            'interface': re.compile(r'^\s*(?:public|private|protected)?\s*interface\s+(\w+)', re.MULTILINE),
            'method': re.compile(r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*\w+\s+(\w+)\s*\(', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+([\w\.\*]+)\s*;', re.MULTILINE),
            'annotation': re.compile(r'@(\w+)(?:\([^)]*\))?', re.MULTILINE)
        }
        
        logger.info(f"Fresh Java processor initialized for: {self.java_root_path}")

    async def process_repository(self, batch_size: int = 50) -> ProcessingStats:
        """
        Process the entire Java repository
        """
        start_time = time.time()
        logger.info(f"🚀 Starting fresh repository processing: {self.java_root_path}")
        
        try:
            # Initialize Weaviate schemas
            await self._initialize_weaviate()
            
            # Discover all files
            discovered_files = self._discover_files()
            self.stats.total_files = len(discovered_files)
            
            logger.info(f"📁 Discovered {self.stats.total_files} files for processing")
            
            # Process files in batches
            batches = [discovered_files[i:i + batch_size] 
                      for i in range(0, len(discovered_files), batch_size)]
            
            for batch_idx, batch in enumerate(batches):
                logger.info(f"📦 Processing batch {batch_idx + 1}/{len(batches)} ({len(batch)} files)")
                
                await self._process_file_batch(batch)
                
                # Progress update
                progress = (batch_idx + 1) / len(batches) * 100
                logger.info(f"✅ Batch {batch_idx + 1} complete ({progress:.1f}% overall)")
            
            # Repository-wide analysis with 1M context
            await self._perform_repository_analysis()
            
            # Finalize stats
            self.stats.processing_time = time.time() - start_time
            
            logger.info(f"🎉 Repository processing completed in {self.stats.processing_time:.2f}s")
            return self.stats
            
        except Exception as e:
            logger.error(f"❌ Repository processing failed: {e}")
            raise

    def _discover_files(self) -> List[JavaFileInfo]:
        """Discover and analyze all relevant files in the repository"""
        discovered_files = []
        
        for file_path in self.java_root_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.file_extensions:
                try:
                    file_info = self._analyze_file_metadata(file_path)
                    if file_info:
                        discovered_files.append(file_info)
                        
                        # Update stats
                        if file_info.file_type == 'java':
                            self.stats.java_files += 1
                        elif file_info.file_type == 'xml':
                            self.stats.xml_files += 1
                        elif file_info.file_type == 'sql':
                            self.stats.sql_files += 1
                        
                        self.stats.total_lines += file_info.lines_of_code
                        self.stats.total_size_bytes += file_info.size_bytes
                        
                except Exception as e:
                    logger.warning(f"Could not analyze file metadata for {file_path}: {e}")
        
        logger.info(f"📊 Discovery stats: {self.stats.java_files} Java, "
                   f"{self.stats.xml_files} XML, {self.stats.sql_files} SQL files")
        
        return discovered_files

    def _analyze_file_metadata(self, file_path: Path) -> Optional[JavaFileInfo]:
        """Analyze metadata for a single file"""
        try:
            if file_path.stat().st_size > 10_000_000:  # Skip files larger than 10MB
                logger.warning(f"Skipping large file: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_type = self.file_extensions.get(file_path.suffix, 'unknown')
            
            # Extract module name from path
            module_parts = file_path.parts
            module_name = 'unknown'
            for part in module_parts:
                if any(keyword in part for keyword in ['cuco', 'administration', 'framework']):
                    module_name = part
                    break
            
            # Java-specific analysis
            if file_type == 'java':
                return self._analyze_java_file(file_path, content, module_name)
            else:
                return self._analyze_non_java_file(file_path, content, module_name, file_type)
                
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    def _analyze_java_file(self, file_path: Path, content: str, module_name: str) -> JavaFileInfo:
        """Analyze a Java source file"""
        
        # Extract package name
        package_match = self.java_patterns['package'].search(content)
        package_name = package_match.group(1) if package_match else 'default'
        
        # Extract class names
        class_matches = self.java_patterns['class'].findall(content)
        interface_matches = self.java_patterns['interface'].findall(content)
        class_names = class_matches + interface_matches
        
        # Extract method names
        method_matches = self.java_patterns['method'].findall(content)
        methods = method_matches[:20]  # Limit to first 20 methods
        
        # Extract imports
        import_matches = self.java_patterns['import'].findall(content)
        imports = import_matches[:30]  # Limit to first 30 imports
        
        # Extract annotations
        annotation_matches = self.java_patterns['annotation'].findall(content)
        annotations = list(set(annotation_matches))  # Remove duplicates
        
        # Calculate complexity estimate
        complexity = self._estimate_complexity(content)
        
        return JavaFileInfo(
            file_path=str(file_path),
            package_name=package_name,
            class_names=class_names,
            imports=imports,
            methods=methods,
            annotations=annotations,
            size_bytes=len(content),
            lines_of_code=len(content.splitlines()),
            complexity_estimate=complexity,
            file_type='java',
            module_name=module_name
        )

    def _analyze_non_java_file(self, file_path: Path, content: str, 
                               module_name: str, file_type: str) -> JavaFileInfo:
        """Analyze non-Java files (XML, SQL, etc.)"""
        
        return JavaFileInfo(
            file_path=str(file_path),
            package_name='',
            class_names=[],
            imports=[],
            methods=[],
            annotations=[],
            size_bytes=len(content),
            lines_of_code=len(content.splitlines()),
            complexity_estimate=0,
            file_type=file_type,
            module_name=module_name
        )

    def _estimate_complexity(self, content: str) -> int:
        """Estimate code complexity based on various factors"""
        complexity = 0
        
        # Count control flow statements
        control_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch']
        for keyword in control_keywords:
            complexity += len(re.findall(r'\b' + keyword + r'\b', content))
        
        # Count method definitions
        complexity += len(self.java_patterns['method'].findall(content))
        
        # Count nested blocks (rough estimate)
        complexity += content.count('{') // 10
        
        return min(complexity, 100)  # Cap at 100

    async def _initialize_weaviate(self):
        """Initialize Weaviate connection and schemas"""
        health = await self.weaviate.health_check()
        if not health['overall']:
            raise RuntimeError(f"Weaviate health check failed: {health}")
        
        logger.info("✅ Weaviate connection established and schemas ready")

    async def _process_file_batch(self, batch: List[JavaFileInfo]):
        """Process a batch of files"""
        processed_chunks = []
        
        for file_info in batch:
            try:
                # Read file content
                with open(file_info.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Create code chunk
                chunk = await self._create_enhanced_code_chunk(file_info, content)
                if chunk:
                    processed_chunks.append(chunk)
                    self.stats.processed_files += 1
                else:
                    self.stats.failed_files += 1
                    
            except Exception as e:
                logger.error(f"Failed to process {file_info.file_path}: {e}")
                self.stats.failed_files += 1
        
        # Batch insert into Weaviate
        if processed_chunks:
            await self._batch_insert_chunks(processed_chunks)

    async def _create_enhanced_code_chunk(self, file_info: JavaFileInfo, content: str) -> Optional[CodeChunk]:
        """Create enhanced code chunk with Qwen analysis"""
        try:
            # Determine chunk type based on file analysis
            chunk_type = ChunkType.FILE  # Default
            
            if file_info.file_type == 'java':
                if len(file_info.class_names) == 1:
                    chunk_type = ChunkType.CLASS
                elif len(file_info.methods) > 0:
                    chunk_type = ChunkType.METHOD
            
            # Create unique chunk ID
            chunk_id = hashlib.md5(file_info.file_path.encode()).hexdigest()
            
            # Create base chunk
            chunk = CodeChunk(
                content=content,
                file_path=file_info.file_path,
                start_line=1,
                end_line=file_info.lines_of_code,
                language=file_info.file_type,
                chunk_type=chunk_type,
                chunk_id=chunk_id,
                class_name=file_info.class_names[0] if file_info.class_names else None,
                method_name=file_info.methods[0] if file_info.methods else None,
                complexity_score=float(file_info.complexity_estimate)
            )
            
            # Enhance with metadata
            chunk.metadata = {
                'package_name': file_info.package_name,
                'imports': file_info.imports,
                'annotations': file_info.annotations,
                'module_name': file_info.module_name,
                'file_type': file_info.file_type,
                'size_bytes': file_info.size_bytes,
                'lines_of_code': file_info.lines_of_code,
                'all_class_names': file_info.class_names,
                'all_methods': file_info.methods[:10]  # Limit methods
            }
            
            return chunk
            
        except Exception as e:
            logger.error(f"Failed to create enhanced chunk for {file_info.file_path}: {e}")
            return None

    async def _batch_insert_chunks(self, chunks: List[CodeChunk]):
        """Insert chunks into Weaviate in batch"""
        try:
            start_time = time.time()
            
            # Use the Weaviate connector's batch insert
            object_ids = self.weaviate.batch_insert_chunks(chunks)
            
            insertion_time = time.time() - start_time
            self.stats.weaviate_insertion_time += insertion_time
            
            successful_inserts = len([id for id in object_ids if id])
            logger.debug(f"Inserted {successful_inserts}/{len(chunks)} chunks in {insertion_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Batch insertion failed: {e}")
            raise

    async def _perform_repository_analysis(self):
        """Perform repository-wide analysis using 1M context window"""
        try:
            logger.info("🧠 Performing repository-wide analysis with 1M context...")
            start_time = time.time()
            
            # Get a sample of chunks for context assembly
            sample_query = await self.weaviate.semantic_search(
                query="java class method service controller",
                limit=100,  # Get top 100 most relevant chunks
                use_1m_context=True
            )
            
            if sample_query.objects:
                # Perform comprehensive analysis
                analysis_result = await self.weaviate.analyze_repository_with_qwen(
                    sample_query.objects
                )
                
                analysis_time = time.time() - start_time
                self.stats.qwen_analysis_time = analysis_time
                
                logger.info(f"✅ Repository analysis completed in {analysis_time:.2f}s")
                logger.info(f"📊 Analysis tokens: {analysis_result.tokens_used:,}")
                logger.info(f"🎯 Context utilization: {analysis_result.context_utilization:.1%}")
                
                # Store analysis results for later retrieval
                await self._store_repository_analysis(analysis_result)
                
            else:
                logger.warning("No chunks found for repository analysis")
                
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")

    async def _store_repository_analysis(self, analysis_result: QwenAnalysisResult):
        """Store repository analysis results in Weaviate"""
        try:
            # Create a special repository-level entry
            repo_chunk = CodeChunk(
                content=analysis_result.content,
                file_path="REPOSITORY_ANALYSIS",
                start_line=0,
                end_line=0,
                language="analysis",
                chunk_type=ChunkType.REPOSITORY,
                chunk_id="repository_analysis_" + str(int(time.time())),
                class_name="RepositoryAnalysis",
                method_name=None,
                complexity_score=0.0
            )
            
            repo_chunk.metadata = {
                'analysis_type': 'repository_wide',
                'tokens_used': analysis_result.tokens_used,
                'context_utilization': analysis_result.context_utilization,
                'processing_time': analysis_result.processing_time,
                'confidence_score': analysis_result.confidence_score,
                'analysis_timestamp': datetime.now().isoformat(),
                'total_files_analyzed': self.stats.total_files,
                'java_files': self.stats.java_files,
                'xml_files': self.stats.xml_files,
                'sql_files': self.stats.sql_files
            }
            
            # Insert repository analysis
            self.weaviate.insert_code_chunk(repo_chunk)
            logger.info("📥 Repository analysis stored in Weaviate")
            
        except Exception as e:
            logger.error(f"Failed to store repository analysis: {e}")

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get comprehensive processing summary"""
        return {
            'repository_path': str(self.java_root_path),
            'processing_stats': asdict(self.stats),
            'file_breakdown': {
                'java_files': self.stats.java_files,
                'xml_files': self.stats.xml_files, 
                'sql_files': self.stats.sql_files,
                'total_files': self.stats.total_files
            },
            'performance': {
                'total_processing_time': self.stats.processing_time,
                'qwen_analysis_time': self.stats.qwen_analysis_time,
                'weaviate_insertion_time': self.stats.weaviate_insertion_time,
                'files_per_second': self.stats.processed_files / self.stats.processing_time if self.stats.processing_time > 0 else 0
            },
            'repository_size': {
                'total_lines_of_code': self.stats.total_lines,
                'total_size_mb': self.stats.total_size_bytes / 1024 / 1024
            },
            'success_rate': self.stats.processed_files / self.stats.total_files * 100 if self.stats.total_files > 0 else 0
        }

    async def cleanup(self):
        """Cleanup resources"""
        try:
            await self.ollama.cleanup()
            self.weaviate.close()
            logger.info("✅ Fresh Java processor cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

# Convenience function for direct processing
async def process_java_repository(
    java_root_path: str,
    weaviate_config: WeaviateConfig = None,
    batch_size: int = 50
) -> ProcessingStats:
    """
    Convenience function to process Java repository directly
    """
    processor = FreshJavaProcessor(java_root_path, weaviate_config)
    
    try:
        stats = await processor.process_repository(batch_size)
        
        # Print summary
        summary = processor.get_processing_summary()
        logger.info("📋 Processing Summary:")
        logger.info(f"   📁 Repository: {summary['repository_path']}")
        logger.info(f"   ✅ Success rate: {summary['success_rate']:.1f}%")
        logger.info(f"   📊 Files: {summary['file_breakdown']['java_files']} Java, "
                   f"{summary['file_breakdown']['xml_files']} XML, "
                   f"{summary['file_breakdown']['sql_files']} SQL")
        logger.info(f"   ⏱️ Performance: {summary['performance']['files_per_second']:.1f} files/sec")
        logger.info(f"   💾 Size: {summary['repository_size']['total_size_mb']:.1f} MB, "
                   f"{summary['repository_size']['total_lines_of_code']:,} lines")
        
        return stats
        
    finally:
        await processor.cleanup()