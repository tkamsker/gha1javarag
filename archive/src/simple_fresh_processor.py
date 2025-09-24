"""
Simplified Fresh Java Processor
Direct processing of Java files with Ollama analysis and simple storage
Bypasses complex Weaviate client issues for now
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
except ImportError:
    from .ollama_integration import OllamaIntegration, QwenAnalysisResult

logger = logging.getLogger('java_analysis.simple_fresh_processor')

@dataclass
class SimpleJavaFile:
    """Simple Java file information"""
    file_path: str
    package_name: str
    class_names: List[str]
    imports: List[str]
    methods: List[str]
    size_bytes: int
    lines_of_code: int
    complexity: int
    file_type: str
    module_name: str
    content_preview: str

@dataclass
class ProcessingResults:
    """Results of processing operation"""
    total_files: int = 0
    processed_files: int = 0
    java_files: int = 0
    xml_files: int = 0
    sql_files: int = 0
    processing_time: float = 0.0
    analysis_results: List[Dict[str, Any]] = None
    repository_analysis: Optional[str] = None

class SimpleFreshProcessor:
    """
    Simplified processor for Java files
    Focus on analysis and insights without complex Weaviate integration
    """
    
    def __init__(self, java_root_path: str):
        self.java_root_path = Path(java_root_path)
        self.ollama = OllamaIntegration()
        
        # File type patterns
        self.file_extensions = {
            '.java': 'java',
            '.xml': 'xml',
            '.sql': 'sql',
            '.properties': 'properties'
        }
        
        # Java parsing patterns
        self.java_patterns = {
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)', re.MULTILINE),
            'interface': re.compile(r'^\s*(?:public|private|protected)?\s*interface\s+(\w+)', re.MULTILINE),
            'method': re.compile(r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*\w+\s+(\w+)\s*\(', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+([\w\.\*]+)\s*;', re.MULTILINE),
        }
        
        logger.info(f"Simple fresh processor initialized for: {self.java_root_path}")

    async def process_repository_sample(self, max_files: int = 50) -> ProcessingResults:
        """
        Process a sample of the repository for analysis
        """
        start_time = time.time()
        logger.info(f"🚀 Processing repository sample (max {max_files} files)")
        
        try:
            # Check Ollama health
            if not await self.ollama.health_check():
                raise RuntimeError("Ollama health check failed")
            
            # Discover files
            discovered_files = self._discover_files(max_files)
            
            results = ProcessingResults()
            results.total_files = len(discovered_files)
            results.analysis_results = []
            
            # Count file types
            for file_info in discovered_files:
                if file_info.file_type == 'java':
                    results.java_files += 1
                elif file_info.file_type == 'xml':
                    results.xml_files += 1
                elif file_info.file_type == 'sql':
                    results.sql_files += 1
            
            logger.info(f"📊 Discovered {results.total_files} files: "
                       f"{results.java_files} Java, {results.xml_files} XML, {results.sql_files} SQL")
            
            # Process files in smaller batches
            batch_size = 10
            for i in range(0, len(discovered_files), batch_size):
                batch = discovered_files[i:i + batch_size]
                batch_results = await self._process_batch(batch)
                results.analysis_results.extend(batch_results)
                results.processed_files += len(batch_results)
                
                logger.info(f"✅ Processed batch {i//batch_size + 1} "
                           f"({len(batch_results)}/{len(batch)} files successful)")
            
            # Perform repository-level analysis
            results.repository_analysis = await self._analyze_repository_structure(discovered_files)
            
            results.processing_time = time.time() - start_time
            
            logger.info(f"🎉 Processing completed in {results.processing_time:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")
            raise

    def _discover_files(self, max_files: int) -> List[SimpleJavaFile]:
        """Discover and analyze files"""
        discovered_files = []
        
        for file_path in self.java_root_path.rglob('*'):
            if len(discovered_files) >= max_files:
                break
                
            if file_path.is_file() and file_path.suffix in self.file_extensions:
                try:
                    file_info = self._analyze_file_basic(file_path)
                    if file_info:
                        discovered_files.append(file_info)
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")
        
        return discovered_files

    def _analyze_file_basic(self, file_path: Path) -> Optional[SimpleJavaFile]:
        """Basic file analysis"""
        try:
            if file_path.stat().st_size > 5_000_000:  # Skip files > 5MB
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_type = self.file_extensions.get(file_path.suffix, 'unknown')
            
            # Extract module name
            module_name = 'unknown'
            for part in file_path.parts:
                if any(keyword in part for keyword in ['cuco', 'administration', 'framework']):
                    module_name = part
                    break
            
            if file_type == 'java':
                return self._analyze_java_file_basic(file_path, content, module_name)
            else:
                return SimpleJavaFile(
                    file_path=str(file_path),
                    package_name='',
                    class_names=[],
                    imports=[],
                    methods=[],
                    size_bytes=len(content),
                    lines_of_code=len(content.splitlines()),
                    complexity=0,
                    file_type=file_type,
                    module_name=module_name,
                    content_preview=content[:500]
                )
                
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    def _analyze_java_file_basic(self, file_path: Path, content: str, module_name: str) -> SimpleJavaFile:
        """Analyze Java file"""
        
        # Extract package
        package_match = self.java_patterns['package'].search(content)
        package_name = package_match.group(1) if package_match else 'default'
        
        # Extract classes and interfaces
        class_matches = self.java_patterns['class'].findall(content)
        interface_matches = self.java_patterns['interface'].findall(content)
        class_names = class_matches + interface_matches
        
        # Extract methods (first 10)
        method_matches = self.java_patterns['method'].findall(content)[:10]
        
        # Extract imports (first 20)
        import_matches = self.java_patterns['import'].findall(content)[:20]
        
        # Simple complexity estimate
        complexity = content.count('if') + content.count('for') + content.count('while') + len(method_matches)
        
        return SimpleJavaFile(
            file_path=str(file_path),
            package_name=package_name,
            class_names=class_names,
            imports=import_matches,
            methods=method_matches,
            size_bytes=len(content),
            lines_of_code=len(content.splitlines()),
            complexity=min(complexity, 100),
            file_type='java',
            module_name=module_name,
            content_preview=content[:1000]
        )

    async def _process_batch(self, batch: List[SimpleJavaFile]) -> List[Dict[str, Any]]:
        """Process a batch of files"""
        batch_results = []
        
        for file_info in batch:
            try:
                # For interesting Java files, perform Qwen analysis
                if (file_info.file_type == 'java' and 
                    len(file_info.class_names) > 0 and 
                    file_info.complexity > 5):
                    
                    analysis = await self._analyze_with_qwen(file_info)
                    
                    result = {
                        'file_path': file_info.file_path,
                        'file_info': asdict(file_info),
                        'qwen_analysis': analysis,
                        'processed_at': datetime.now().isoformat()
                    }
                else:
                    # Basic processing for simpler files
                    result = {
                        'file_path': file_info.file_path,
                        'file_info': asdict(file_info),
                        'processed_at': datetime.now().isoformat(),
                        'analysis_type': 'basic'
                    }
                
                batch_results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to process {file_info.file_path}: {e}")
        
        return batch_results

    async def _analyze_with_qwen(self, file_info: SimpleJavaFile) -> Dict[str, Any]:
        """Analyze file content with Qwen3-Coder"""
        try:
            # Read full content for analysis
            with open(file_info.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                full_content = f.read()
            
            # Limit content size for analysis
            if len(full_content) > 10000:
                content_for_analysis = full_content[:10000] + "\n... (truncated)"
            else:
                content_for_analysis = full_content
            
            analysis_prompt = f"""
            Analyze this Java file from an enterprise application:
            
            File: {Path(file_info.file_path).name}
            Module: {file_info.module_name}
            Package: {file_info.package_name}
            Classes: {', '.join(file_info.class_names)}
            
            Code:
            {content_for_analysis}
            
            Please provide:
            1. Purpose and functionality
            2. Design patterns used
            3. Business logic insights
            4. Integration points
            5. Potential improvements
            6. Technical debt assessment
            """
            
            result = await self.ollama.analyze_code_repository(
                repository_context=analysis_prompt,
                analysis_type="single_file_analysis"
            )
            
            return {
                'analysis_content': result.content,
                'tokens_used': result.tokens_used,
                'processing_time': result.processing_time,
                'confidence_score': result.confidence_score,
                'context_utilization': result.context_utilization
            }
            
        except Exception as e:
            logger.error(f"Qwen analysis failed for {file_info.file_path}: {e}")
            return {
                'error': str(e),
                'analysis_content': 'Analysis failed'
            }

    async def _analyze_repository_structure(self, files: List[SimpleJavaFile]) -> str:
        """Perform repository-level analysis"""
        try:
            logger.info("🧠 Performing repository-level analysis...")
            
            # Compile repository overview
            java_files = [f for f in files if f.file_type == 'java']
            
            # Get modules and packages
            modules = list(set(f.module_name for f in java_files))
            packages = list(set(f.package_name for f in java_files if f.package_name != 'default'))
            
            # Get most complex classes
            complex_classes = sorted(java_files, key=lambda x: x.complexity, reverse=True)[:10]
            
            # Prepare comprehensive context
            repo_context = f"""
            Repository Analysis Context:
            
            MODULES: {', '.join(modules)}
            
            PACKAGES: {', '.join(packages[:20])}
            
            STATISTICS:
            - Total Java files: {len(java_files)}
            - Total lines of code: {sum(f.lines_of_code for f in java_files)}
            - Average complexity: {sum(f.complexity for f in java_files) / len(java_files) if java_files else 0:.1f}
            
            MOST COMPLEX CLASSES:
            """
            
            for i, cls in enumerate(complex_classes[:5]):
                repo_context += f"""
            {i+1}. {Path(cls.file_path).name}
               Package: {cls.package_name}
               Classes: {', '.join(cls.class_names)}
               Complexity: {cls.complexity}
               Preview: {cls.content_preview[:200]}...
            """
            
            repo_context += """
            
            Please provide a comprehensive analysis of this Java enterprise application:
            1. Overall architecture and design patterns
            2. Business domain and functionality
            3. Technology stack and frameworks used
            4. Integration patterns and external dependencies
            5. Code quality assessment
            6. Modernization opportunities
            7. Performance considerations
            8. Security aspects
            9. Maintainability concerns
            10. Recommended improvements
            """
            
            # Perform analysis with large context
            analysis_result = await self.ollama.analyze_code_repository(
                repository_context=repo_context,
                analysis_type="comprehensive_repository_analysis"
            )
            
            logger.info(f"✅ Repository analysis completed: {analysis_result.tokens_used} tokens, "
                       f"{analysis_result.context_utilization:.1%} context utilization")
            
            return analysis_result.content
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            return f"Repository analysis failed: {str(e)}"

    async def save_results(self, results: ProcessingResults, output_dir: str = "output"):
        """Save processing results"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save main results
            results_file = f"{output_dir}/fresh_analysis_{timestamp}.json"
            with open(results_file, 'w') as f:
                json.dump({
                    'processing_stats': asdict(results),
                    'analysis_results': results.analysis_results,
                    'repository_analysis': results.repository_analysis
                }, f, indent=2, default=str)
            
            # Save repository analysis separately
            if results.repository_analysis:
                repo_file = f"{output_dir}/repository_analysis_{timestamp}.md"
                with open(repo_file, 'w') as f:
                    f.write(f"# Repository Analysis - {timestamp}\n\n")
                    f.write(results.repository_analysis)
            
            logger.info(f"📁 Results saved to {results_file}")
            logger.info(f"📄 Repository analysis saved to {repo_file}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    async def cleanup(self):
        """Cleanup resources"""
        await self.ollama.cleanup()

# Convenience function
async def process_java_sample(java_root_path: str, max_files: int = 50) -> ProcessingResults:
    """Process Java repository sample"""
    processor = SimpleFreshProcessor(java_root_path)
    
    try:
        results = await processor.process_repository_sample(max_files)
        await processor.save_results(results)
        return results
    finally:
        await processor.cleanup()