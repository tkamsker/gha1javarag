#!/usr/bin/env python3
"""
Clean Java Analysis Runner
Runs without import conflicts
"""

import asyncio
import logging
import sys
import os
import time
from pathlib import Path

# Ensure we only use the current project's modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Remove any conflicting paths
paths_to_remove = []
for path in sys.path:
    if 'cursorairagtest' in path or 'cursor' in path.lower():
        paths_to_remove.append(path)

for path in paths_to_remove:
    sys.path.remove(path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Direct imports without package structure
import re
import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional

# Inline Ollama integration to avoid import issues
import aiohttp
import psutil

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

class SimpleOllama:
    """Simplified Ollama client"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        self._session = None
        
    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    return response.status == 200
        except:
            return False
    
    async def analyze_code(self, content: str, analysis_type: str = "analysis") -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": content,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 2048
                    }
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=300)) as response:
                    if response.status == 200:
                        data = await response.json()
                        processing_time = time.time() - start_time
                        
                        return {
                            'analysis_content': data.get('response', ''),
                            'tokens_used': len(content) // 3 + len(data.get('response', '')) // 3,
                            'processing_time': processing_time,
                            'confidence_score': 0.8
                        }
                    else:
                        return {'error': f'HTTP {response.status}'}
        except Exception as e:
            return {'error': str(e)}

class CleanJavaProcessor:
    """Clean Java processor without external dependencies"""
    
    def __init__(self, java_root_path: str):
        self.java_root_path = Path(java_root_path)
        self.ollama = SimpleOllama()
        
        # Java parsing patterns
        self.java_patterns = {
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)', re.MULTILINE),
            'interface': re.compile(r'^\s*(?:public|private|protected)?\s*interface\s+(\w+)', re.MULTILINE),
            'method': re.compile(r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*\w+\s+(\w+)\s*\(', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+([\w\.\*]+)\s*;', re.MULTILINE),
        }
        
        logger.info(f"Clean Java processor initialized for: {self.java_root_path}")

    async def run_analysis(self, max_files: int = 20) -> Dict[str, Any]:
        """Run the complete analysis"""
        start_time = time.time()
        
        # Check Ollama health
        if not await self.ollama.health_check():
            raise RuntimeError("Ollama health check failed")
        
        logger.info("✅ Ollama is ready")
        
        # Discover Java files
        java_files = self._discover_java_files(max_files)
        
        if not java_files:
            raise RuntimeError("No Java files found!")
        
        logger.info(f"📊 Found {len(java_files)} Java files for analysis")
        
        # Show sample files
        logger.info("📋 Sample Java files:")
        for i, file_info in enumerate(java_files[:5]):
            logger.info(f"   {i+1}. {Path(file_info.file_path).name}")
            logger.info(f"      Package: {file_info.package_name}")
            logger.info(f"      Classes: {', '.join(file_info.class_names) if file_info.class_names else 'None'}")
            logger.info(f"      Complexity: {file_info.complexity}")
        
        # Process interesting files
        interesting_files = [f for f in java_files if f.complexity > 3 and len(f.class_names) > 0][:5]
        logger.info(f"🧠 Analyzing {len(interesting_files)} complex files with Qwen...")
        
        analyses = []
        for i, file_info in enumerate(interesting_files):
            logger.info(f"📝 Analyzing file {i+1}/{len(interesting_files)}: {Path(file_info.file_path).name}")
            
            try:
                analysis = await self._analyze_file_with_qwen(file_info)
                analyses.append({
                    'file': file_info.file_path,
                    'file_info': asdict(file_info),
                    'analysis': analysis
                })
                logger.info(f"   ✅ Analysis completed: {analysis.get('tokens_used', 0)} tokens")
            except Exception as e:
                logger.error(f"   ❌ Analysis failed: {e}")
        
        # Repository analysis
        repo_analysis = await self._analyze_repository(java_files)
        
        # Compile results
        results = {
            'java_files_found': len(java_files),
            'files_analyzed': len(analyses),
            'processing_time': time.time() - start_time,
            'individual_analyses': analyses,
            'repository_analysis': repo_analysis,
            'modules': list(set(f.module_name for f in java_files)),
            'packages': list(set(f.package_name for f in java_files if f.package_name != 'default'))
        }
        
        return results

    def _discover_java_files(self, max_files: int) -> List[SimpleJavaFile]:
        """Discover Java files"""
        java_files = []
        
        for file_path in self.java_root_path.rglob("*.java"):
            if len(java_files) >= max_files:
                break
                
            if file_path.is_file():
                try:
                    file_info = self._analyze_java_file(file_path)
                    if file_info:
                        java_files.append(file_info)
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")
        
        return java_files

    def _analyze_java_file(self, file_path: Path) -> Optional[SimpleJavaFile]:
        """Analyze a Java file"""
        try:
            if file_path.stat().st_size > 5_000_000:  # Skip files > 5MB
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract module name
            module_name = 'unknown'
            for part in file_path.parts:
                if any(keyword in part for keyword in ['cuco', 'administration', 'framework']):
                    module_name = part
                    break
            
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
            
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    async def _analyze_file_with_qwen(self, file_info: SimpleJavaFile) -> Dict[str, Any]:
        """Analyze file with Qwen"""
        try:
            # Read full content for analysis
            with open(file_info.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                full_content = f.read()
            
            # Limit content size for analysis
            if len(full_content) > 8000:
                content_for_analysis = full_content[:8000] + "\n... (truncated)"
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
            
            return await self.ollama.analyze_code(analysis_prompt, "file_analysis")
            
        except Exception as e:
            logger.error(f"Qwen analysis failed for {file_info.file_path}: {e}")
            return {'error': str(e), 'analysis_content': 'Analysis failed'}

    async def _analyze_repository(self, java_files: List[SimpleJavaFile]) -> Dict[str, Any]:
        """Repository-wide analysis"""
        try:
            logger.info("🏗️ Performing repository-wide analysis...")
            
            # Get modules and packages
            modules = list(set(f.module_name for f in java_files))
            packages = list(set(f.package_name for f in java_files if f.package_name != 'default'))
            
            # Get most complex files
            complex_files = sorted(java_files, key=lambda x: x.complexity, reverse=True)[:3]
            
            repo_context = f"""
Java Enterprise Application Analysis:

MODULES: {', '.join(modules)}
PACKAGES: {', '.join(packages[:10])}

STATISTICS:
- Total Java files: {len(java_files)}
- Average complexity: {sum(f.complexity for f in java_files) / len(java_files) if java_files else 0:.1f}

MOST COMPLEX CLASSES:
"""
            
            for i, cls in enumerate(complex_files):
                repo_context += f"""
{i+1}. {Path(cls.file_path).name}
   Package: {cls.package_name}
   Classes: {', '.join(cls.class_names)}
   Complexity: {cls.complexity}
   Preview: {cls.content_preview[:200]}...
"""
            
            repo_context += """
Please analyze this Java enterprise application:
1. Overall architecture
2. Technology stack
3. Business domain
4. Design patterns
5. Modernization opportunities
"""
            
            result = await self.ollama.analyze_code(repo_context, "repository_analysis")
            logger.info("✅ Repository analysis completed")
            
            return result
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            return {'error': str(e), 'analysis_content': 'Repository analysis failed'}

    def save_results(self, results: Dict[str, Any]):
        """Save results to files"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save JSON results
            with open(f"output/clean_java_analysis_{timestamp}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Save markdown report
            with open(f"output/clean_java_report_{timestamp}.md", 'w') as f:
                f.write(f"# Java Enterprise Analysis - {timestamp}\n\n")
                f.write(f"**Files Found:** {results['java_files_found']}\n")
                f.write(f"**Files Analyzed:** {results['files_analyzed']}\n")
                f.write(f"**Modules:** {', '.join(results['modules'])}\n")
                f.write(f"**Processing Time:** {results['processing_time']:.2f}s\n\n")
                
                repo_analysis = results.get('repository_analysis', {})
                if 'analysis_content' in repo_analysis:
                    f.write("## Repository Analysis\n\n")
                    f.write(repo_analysis['analysis_content'])
                    f.write("\n\n")
                
                f.write("## Individual File Analyses\n\n")
                for analysis in results['individual_analyses']:
                    file_name = Path(analysis['file']).name
                    f.write(f"### {file_name}\n\n")
                    file_analysis = analysis.get('analysis', {})
                    f.write(file_analysis.get('analysis_content', 'Analysis not available'))
                    f.write("\n\n---\n\n")
            
            logger.info(f"📁 Results saved to output/clean_java_analysis_{timestamp}.json")
            logger.info(f"📄 Report saved to output/clean_java_report_{timestamp}.md")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

async def main():
    """Main execution function"""
    logger.info("☕ Clean Java-Focused Enterprise Application Analysis")
    logger.info("=" * 60)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        processor = CleanJavaProcessor(java_root_path)
        
        logger.info(f"📁 Processing Java repository: {java_root_path}")
        
        # Run analysis
        results = await processor.run_analysis(max_files=20)
        
        # Save results
        processor.save_results(results)
        
        # Display summary
        logger.info("=" * 60)
        logger.info("🎉 CLEAN JAVA ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"📊 Java files found: {results['java_files_found']}")
        logger.info(f"🧠 Files analyzed: {results['files_analyzed']}")
        logger.info(f"🏢 Modules: {len(results['modules'])} ({', '.join(results['modules'])})")
        logger.info(f"📦 Packages: {len(results['packages'])}")
        logger.info(f"⏱️ Processing time: {results['processing_time']:.2f}s")
        logger.info("📁 Check output/ directory for detailed results")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)