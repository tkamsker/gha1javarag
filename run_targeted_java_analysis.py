#!/usr/bin/env python3
"""
Targeted Java Analysis - Process specifically Java files with incremental results
"""

import asyncio
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Direct imports to avoid conflicts
import re
import aiohttp
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

@dataclass
class JavaFileInfo:
    file_path: str
    package_name: str
    class_names: List[str]
    imports: List[str]
    methods: List[str]
    size_bytes: int
    lines_of_code: int
    complexity: int
    module_name: str
    content_preview: str

class SimpleOllama:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        
    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except:
            return False
    
    async def analyze_code(self, content: str) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": content,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 1024}
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=180)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'analysis_content': data.get('response', ''),
                            'tokens_used': len(content) // 3,
                            'processing_time': time.time() - start_time,
                            'success': True
                        }
                    else:
                        return {'error': f'HTTP {response.status}', 'success': False}
        except Exception as e:
            return {'error': str(e), 'success': False}

class TargetedJavaAnalyzer:
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

    async def run_analysis(self) -> Dict[str, Any]:
        start_time = time.time()
        
        # Check Ollama
        if not await self.ollama.health_check():
            raise RuntimeError("Ollama not available")
        
        logger.info("✅ Ollama is ready")
        
        # Discover Java files specifically
        java_files = self._discover_java_files_only()
        logger.info(f"📊 Found {len(java_files)} Java files")
        
        if not java_files:
            raise RuntimeError("No Java files found!")
        
        # Show sample files
        logger.info("📋 Sample Java files discovered:")
        for i, file_info in enumerate(java_files[:5]):
            logger.info(f"   {i+1}. {Path(file_info.file_path).name}")
            logger.info(f"      Module: {file_info.module_name}")
            logger.info(f"      Package: {file_info.package_name}")
            logger.info(f"      Classes: {', '.join(file_info.class_names)}")
            logger.info(f"      Complexity: {file_info.complexity}")
        
        # Select interesting files for analysis
        interesting_files = [f for f in java_files if f.complexity > 2 and len(f.class_names) > 0][:8]
        logger.info(f"🧠 Selected {len(interesting_files)} files for detailed Qwen analysis")
        
        # Analyze files incrementally
        analyses = []
        for i, file_info in enumerate(interesting_files):
            logger.info(f"📝 Analyzing {i+1}/{len(interesting_files)}: {Path(file_info.file_path).name}")
            
            try:
                analysis = await self._analyze_file_with_qwen(file_info)
                if analysis.get('success', False):
                    analyses.append({
                        'file': file_info.file_path,
                        'file_info': asdict(file_info),
                        'analysis': analysis
                    })
                    logger.info(f"   ✅ Success: {analysis.get('tokens_used', 0)} tokens")
                    
                    # Save incremental results
                    self._save_incremental_results(analyses, len(java_files))
                else:
                    logger.error(f"   ❌ Failed: {analysis.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"   ❌ Exception: {e}")
        
        # Repository overview
        repo_overview = await self._create_repository_overview(java_files, analyses)
        
        # Final results
        results = {
            'timestamp': datetime.now().isoformat(),
            'java_files_found': len(java_files),
            'files_analyzed': len(analyses),
            'processing_time': time.time() - start_time,
            'modules': list(set(f.module_name for f in java_files)),
            'packages': list(set(f.package_name for f in java_files if f.package_name != 'default')),
            'individual_analyses': analyses,
            'repository_overview': repo_overview,
            'success': True
        }
        
        # Save final results
        self._save_final_results(results)
        
        return results

    def _discover_java_files_only(self) -> List[JavaFileInfo]:
        """Discover only Java files"""
        java_files = []
        
        logger.info("🔍 Scanning for Java files...")
        for file_path in self.java_root_path.rglob("*.java"):
            if len(java_files) >= 25:  # Limit for manageable analysis
                break
                
            if file_path.is_file():
                try:
                    file_info = self._analyze_java_file_structure(file_path)
                    if file_info:
                        java_files.append(file_info)
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")
        
        return java_files

    def _analyze_java_file_structure(self, file_path: Path) -> Optional[JavaFileInfo]:
        """Analyze Java file structure"""
        try:
            if file_path.stat().st_size > 2_000_000:  # Skip very large files
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
            
            # Extract methods (limited)
            method_matches = self.java_patterns['method'].findall(content)[:8]
            
            # Extract imports (limited)
            import_matches = self.java_patterns['import'].findall(content)[:15]
            
            # Calculate complexity
            complexity = (content.count('if') + content.count('for') + 
                         content.count('while') + len(method_matches))
            
            return JavaFileInfo(
                file_path=str(file_path),
                package_name=package_name,
                class_names=class_names,
                imports=import_matches,
                methods=method_matches,
                size_bytes=len(content),
                lines_of_code=len(content.splitlines()),
                complexity=min(complexity, 50),
                module_name=module_name,
                content_preview=content[:800]
            )
            
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    async def _analyze_file_with_qwen(self, file_info: JavaFileInfo) -> Dict[str, Any]:
        """Analyze file with Qwen"""
        try:
            # Read full content
            with open(file_info.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                full_content = f.read()
            
            # Limit content for analysis
            if len(full_content) > 6000:
                content_for_analysis = full_content[:6000] + "\n... (truncated)"
            else:
                content_for_analysis = full_content
            
            analysis_prompt = f"""
Analyze this Java file from A1 Telekom Austria CuCo enterprise application:

File: {Path(file_info.file_path).name}
Module: {file_info.module_name}
Package: {file_info.package_name}
Classes: {', '.join(file_info.class_names)}

Code:
{content_for_analysis}

Provide concise analysis covering:
1. Purpose and functionality
2. Design patterns used
3. Business logic insights
4. Integration points
5. Code quality assessment
"""
            
            return await self.ollama.analyze_code(analysis_prompt)
            
        except Exception as e:
            return {'error': str(e), 'success': False}

    async def _create_repository_overview(self, java_files: List[JavaFileInfo], analyses: List[Dict]) -> Dict[str, Any]:
        """Create repository overview"""
        try:
            # Extract key information
            modules = list(set(f.module_name for f in java_files))
            packages = list(set(f.package_name for f in java_files if f.package_name != 'default'))
            
            # Most complex files
            complex_files = sorted(java_files, key=lambda x: x.complexity, reverse=True)[:3]
            
            overview_context = f"""
A1 Telekom Austria CuCo Enterprise Application Analysis:

REPOSITORY STATISTICS:
- Total Java files: {len(java_files)}
- Modules: {', '.join(modules)}
- Key packages: {', '.join(packages[:8])}
- Files analyzed: {len(analyses)}

MOST COMPLEX COMPONENTS:
"""
            
            for i, file_info in enumerate(complex_files):
                overview_context += f"""
{i+1}. {Path(file_info.file_path).name}
   Package: {file_info.package_name}
   Classes: {', '.join(file_info.class_names)}
   Complexity: {file_info.complexity}
   Preview: {file_info.content_preview[:150]}...
"""
            
            overview_context += """
Provide enterprise-level assessment:
1. Overall architecture
2. Technology stack
3. Business domain (A1 Telekom CuCo system)
4. Modernization opportunities
5. Technical assessment
"""
            
            result = await self.ollama.analyze_code(overview_context)
            return result
            
        except Exception as e:
            return {'error': str(e), 'success': False}

    def _save_incremental_results(self, analyses: List[Dict], total_files: int):
        """Save incremental results"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            incremental_data = {
                'timestamp': datetime.now().isoformat(),
                'progress': f"{len(analyses)} analyses completed",
                'total_files_found': total_files,
                'analyses': analyses
            }
            
            with open(f"output/incremental_java_analysis_{timestamp}.json", 'w') as f:
                json.dump(incremental_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save incremental results: {e}")

    def _save_final_results(self, results: Dict[str, Any]):
        """Save final results"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save JSON results
            with open(f"output/targeted_java_analysis_{timestamp}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Save markdown report
            with open(f"output/targeted_java_report_{timestamp}.md", 'w') as f:
                f.write(f"# A1 Telekom Austria CuCo Java Analysis - {timestamp}\n\n")
                f.write(f"**Files Found:** {results['java_files_found']}\n")
                f.write(f"**Files Analyzed:** {results['files_analyzed']}\n")
                f.write(f"**Modules:** {', '.join(results['modules'])}\n")
                f.write(f"**Processing Time:** {results['processing_time']:.2f}s\n\n")
                
                # Repository overview
                repo_overview = results.get('repository_overview', {})
                if repo_overview.get('success', False):
                    f.write("## Repository Overview\n\n")
                    f.write(repo_overview.get('analysis_content', 'No overview available'))
                    f.write("\n\n")
                
                # Individual analyses
                f.write("## Individual File Analyses\n\n")
                for analysis in results['individual_analyses']:
                    file_name = Path(analysis['file']).name
                    f.write(f"### {file_name}\n\n")
                    f.write(f"**Module:** {analysis['file_info']['module_name']}\n")
                    f.write(f"**Package:** {analysis['file_info']['package_name']}\n")
                    f.write(f"**Classes:** {', '.join(analysis['file_info']['class_names'])}\n\n")
                    f.write(analysis['analysis'].get('analysis_content', 'Analysis not available'))
                    f.write("\n\n---\n\n")
            
            logger.info(f"📁 Results saved to output/targeted_java_analysis_{timestamp}.json")
            logger.info(f"📄 Report saved to output/targeted_java_report_{timestamp}.md")
            
        except Exception as e:
            logger.error(f"Failed to save final results: {e}")

async def main():
    logger.info("☕ Targeted Java Enterprise Application Analysis")
    logger.info("=" * 60)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        analyzer = TargetedJavaAnalyzer(java_root_path)
        results = await analyzer.run_analysis()
        
        # Display summary
        logger.info("=" * 60)
        logger.info("🎉 TARGETED JAVA ANALYSIS COMPLETE")
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
    exit(0 if success else 1)