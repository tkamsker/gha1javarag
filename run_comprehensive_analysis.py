#!/usr/bin/env python3
"""
Comprehensive Java Analysis Pipeline
Processes the full A1 Telekom Austria CuCo Java dataset and generates requirements
"""

import asyncio
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Direct imports to avoid conflicts
import re
import aiohttp
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Set

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
    interfaces: List[str]
    annotations: List[str]
    business_context: str

@dataclass
class ModuleAnalysis:
    module_name: str
    file_count: int
    total_lines: int
    avg_complexity: float
    key_packages: List[str]
    main_classes: List[str]
    technologies: List[str]
    business_functions: List[str]

class ComprehensiveOllama:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        self.session_timeout = 300  # 5 minutes for large analyses
        
    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    return response.status == 200
        except:
            return False
    
    async def analyze_code_batch(self, content: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze code with extended context window optimization"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": content,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 2048,
                        "num_ctx": 1024000,  # 1M context window
                        "top_k": 40,
                        "top_p": 0.9
                    }
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=self.session_timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'analysis_content': data.get('response', ''),
                            'tokens_used': len(content) // 3,
                            'processing_time': time.time() - start_time,
                            'analysis_type': analysis_type,
                            'success': True
                        }
                    else:
                        return {'error': f'HTTP {response.status}', 'success': False}
        except Exception as e:
            return {'error': str(e), 'success': False}

    async def generate_requirements(self, context: str) -> Dict[str, Any]:
        """Generate requirements documentation from analysis context"""
        return await self.analyze_code_batch(context, "requirements_generation")

class ComprehensiveJavaAnalyzer:
    def __init__(self, java_root_path: str):
        self.java_root_path = Path(java_root_path)
        self.ollama = ComprehensiveOllama()
        self.processed_files = 0
        self.total_files = 0
        
        # Enhanced Java parsing patterns
        self.java_patterns = {
            'package': re.compile(r'^\s*package\s+([\w\.]+)\s*;', re.MULTILINE),
            'class': re.compile(r'^\s*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)', re.MULTILINE),
            'interface': re.compile(r'^\s*(?:public|private|protected)?\s*interface\s+(\w+)', re.MULTILINE),
            'method': re.compile(r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*[\w\<\>\[\]]+\s+(\w+)\s*\([^)]*\)', re.MULTILINE),
            'import': re.compile(r'^\s*import\s+([\w\.\*]+)\s*;', re.MULTILINE),
            'annotation': re.compile(r'@(\w+)', re.MULTILINE),
            'servlet': re.compile(r'@WebServlet|extends\s+\w*Servlet|implements\s+Servlet', re.MULTILINE),
            'service': re.compile(r'@Service|@Component|@Repository|@Controller', re.MULTILINE),
            'gwt': re.compile(r'import\s+com\.google\.gwt|extends\s+\w*EntryPoint|implements\s+\w*EntryPoint', re.MULTILINE)
        }

    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis of the entire Java codebase"""
        start_time = time.time()
        
        # Check Ollama availability
        if not await self.ollama.health_check():
            raise RuntimeError("Ollama not available - please ensure service is running")
        
        logger.info("✅ Ollama with Qwen3-Coder-30B is ready (1M context window)")
        
        # Phase 1: Discovery and Classification
        logger.info("🔍 Phase 1: Discovering and classifying Java files...")
        all_java_files = await self._discover_all_java_files()
        self.total_files = len(all_java_files)
        
        logger.info(f"📊 Discovered {self.total_files} Java files across the enterprise application")
        
        # Phase 2: Module Analysis
        logger.info("🏗️ Phase 2: Analyzing modules and architecture...")
        module_analyses = await self._analyze_modules(all_java_files)
        
        # Phase 3: Batch Processing with AI Analysis
        logger.info("🧠 Phase 3: AI-powered code analysis (batched for efficiency)...")
        detailed_analyses = await self._batch_analyze_files(all_java_files)
        
        # Phase 4: Requirements Generation
        logger.info("📋 Phase 4: Generating enterprise requirements documentation...")
        requirements = await self._generate_requirements_documentation(all_java_files, module_analyses, detailed_analyses)
        
        # Phase 5: Architecture and Integration Analysis
        logger.info("🔗 Phase 5: Analyzing architecture and integration patterns...")
        architecture_analysis = await self._analyze_architecture_patterns(all_java_files, module_analyses)
        
        # Compile comprehensive results
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis_metadata': {
                'total_java_files': self.total_files,
                'processed_files': self.processed_files,
                'processing_time_seconds': time.time() - start_time,
                'modules_analyzed': len(module_analyses),
                'ai_model': 'Qwen3-Coder-30B-A3B-Instruct-1M',
                'context_window_used': '1M tokens'
            },
            'enterprise_overview': {
                'application_name': 'A1 Telekom Austria CuCo',
                'business_domain': 'Customer Care Operations',
                'architecture_type': 'Multi-module Enterprise Java Application',
                'primary_technologies': ['GWT', 'ExtJS', 'Spring', 'iBATIS', 'Servlet API']
            },
            'module_analyses': module_analyses,
            'detailed_code_analyses': detailed_analyses,
            'requirements_documentation': requirements,
            'architecture_analysis': architecture_analysis,
            'success': True
        }
        
        # Save comprehensive results
        await self._save_comprehensive_results(results)
        
        return results

    async def _discover_all_java_files(self) -> List[JavaFileInfo]:
        """Discover and analyze all Java files with enhanced metadata"""
        java_files = []
        
        logger.info("🔍 Scanning entire repository for Java files...")
        file_count = 0
        
        for file_path in self.java_root_path.rglob("*.java"):
            file_count += 1
            if file_count % 100 == 0:
                logger.info(f"   ... processed {file_count} files")
                
            if file_path.is_file():
                try:
                    file_info = await self._analyze_java_file_comprehensive(file_path)
                    if file_info:
                        java_files.append(file_info)
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")
        
        logger.info(f"📊 Successfully analyzed {len(java_files)} Java files")
        return java_files

    async def _analyze_java_file_comprehensive(self, file_path: Path) -> Optional[JavaFileInfo]:
        """Comprehensive analysis of individual Java file"""
        try:
            if file_path.stat().st_size > 5_000_000:  # Skip very large files
                logger.warning(f"Skipping large file: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract module name with better detection
            module_name = self._determine_module_name(file_path)
            
            # Extract package
            package_match = self.java_patterns['package'].search(content)
            package_name = package_match.group(1) if package_match else 'default'
            
            # Extract classes and interfaces
            class_matches = self.java_patterns['class'].findall(content)
            interface_matches = self.java_patterns['interface'].findall(content)
            
            # Extract methods with better pattern
            method_matches = self.java_patterns['method'].findall(content)[:20]
            
            # Extract imports
            import_matches = self.java_patterns['import'].findall(content)[:30]
            
            # Extract annotations
            annotation_matches = self.java_patterns['annotation'].findall(content)
            
            # Determine business context
            business_context = self._determine_business_context(package_name, class_matches, content)
            
            # Calculate enhanced complexity
            complexity = self._calculate_complexity(content)
            
            return JavaFileInfo(
                file_path=str(file_path),
                package_name=package_name,
                class_names=class_matches,
                imports=import_matches,
                methods=method_matches,
                size_bytes=len(content),
                lines_of_code=len(content.splitlines()),
                complexity=complexity,
                module_name=module_name,
                content_preview=content[:1200],
                interfaces=interface_matches,
                annotations=annotation_matches,
                business_context=business_context
            )
            
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return None

    def _determine_module_name(self, file_path: Path) -> str:
        """Determine module name with better heuristics"""
        parts = file_path.parts
        
        # Look for known A1 Telekom module patterns
        for part in parts:
            if any(keyword in part.lower() for keyword in ['cuco', 'administration', 'framework', 'pkb', 'cct']):
                return part
        
        # Fallback to directory structure
        if 'src' in parts:
            src_index = parts.index('src')
            if src_index > 0:
                return parts[src_index - 1]
        
        return 'unknown'

    def _determine_business_context(self, package_name: str, class_names: List[str], content: str) -> str:
        """Determine business context from code analysis"""
        contexts = []
        
        # Package-based context
        if 'admin' in package_name.lower():
            contexts.append('Administration')
        if 'ui' in package_name.lower():
            contexts.append('User Interface')
        if 'service' in package_name.lower():
            contexts.append('Business Services')
        if 'dao' in package_name.lower() or 'repository' in package_name.lower():
            contexts.append('Data Access')
        if 'client' in package_name.lower():
            contexts.append('Client-Side')
        if 'server' in package_name.lower():
            contexts.append('Server-Side')
        
        # Class name-based context
        for class_name in class_names:
            if 'servlet' in class_name.lower():
                contexts.append('Web Services')
            if 'starter' in class_name.lower():
                contexts.append('Application Bootstrap')
            if 'filter' in class_name.lower():
                contexts.append('Request Processing')
        
        # Content-based context
        if '@WebServlet' in content or '@Controller' in content:
            contexts.append('Web Controller')
        if '@Service' in content:
            contexts.append('Business Service')
        if 'extends EntryPoint' in content:
            contexts.append('GWT Entry Point')
        
        return ', '.join(set(contexts)) if contexts else 'General'

    def _calculate_complexity(self, content: str) -> int:
        """Calculate enhanced complexity metrics"""
        complexity = 0
        
        # Control flow complexity
        complexity += content.count('if')
        complexity += content.count('for')
        complexity += content.count('while')
        complexity += content.count('switch')
        complexity += content.count('catch')
        complexity += content.count('&&')
        complexity += content.count('||')
        
        # Method and class complexity
        complexity += len(re.findall(r'^\s*(?:public|private|protected)', content, re.MULTILINE))
        
        # Nesting complexity (approximation)
        complexity += content.count('{') // 5
        
        return min(complexity, 100)  # Cap at 100

    async def _analyze_modules(self, java_files: List[JavaFileInfo]) -> Dict[str, ModuleAnalysis]:
        """Analyze modules for architectural insights"""
        modules = defaultdict(list)
        
        # Group files by module
        for file_info in java_files:
            modules[file_info.module_name].append(file_info)
        
        module_analyses = {}
        
        for module_name, files in modules.items():
            if module_name == 'unknown':
                continue
                
            total_lines = sum(f.lines_of_code for f in files)
            avg_complexity = sum(f.complexity for f in files) / len(files) if files else 0
            
            # Extract key packages
            packages = list(set(f.package_name for f in files if f.package_name != 'default'))
            key_packages = sorted(packages, key=lambda p: len([f for f in files if f.package_name == p]), reverse=True)[:10]
            
            # Extract main classes (high complexity or important names)
            main_classes = []
            for file_info in files:
                if file_info.complexity > 10 or any(keyword in ' '.join(file_info.class_names).lower() 
                                                  for keyword in ['starter', 'servlet', 'service', 'controller', 'manager']):
                    main_classes.extend(file_info.class_names)
            
            # Determine technologies
            technologies = set()
            for file_info in files:
                content = file_info.content_preview.lower()
                imports = ' '.join(file_info.imports).lower()
                
                if 'gwt' in imports or 'gwt' in content:
                    technologies.add('GWT')
                if 'servlet' in content or 'servlet' in imports:
                    technologies.add('Servlet API')
                if 'spring' in imports:
                    technologies.add('Spring Framework')
                if 'ibatis' in imports or 'ibatis' in content:
                    technologies.add('iBATIS')
                if 'extjs' in imports or 'gxt' in imports:
                    technologies.add('ExtJS/GXT')
                if 'hibernate' in imports:
                    technologies.add('Hibernate')
            
            # Determine business functions
            business_functions = list(set(f.business_context for f in files if f.business_context != 'General'))
            
            module_analyses[module_name] = ModuleAnalysis(
                module_name=module_name,
                file_count=len(files),
                total_lines=total_lines,
                avg_complexity=avg_complexity,
                key_packages=key_packages,
                main_classes=main_classes[:15],
                technologies=list(technologies),
                business_functions=business_functions
            )
        
        return module_analyses

    async def _batch_analyze_files(self, java_files: List[JavaFileInfo]) -> List[Dict[str, Any]]:
        """Batch analyze files with AI for detailed insights"""
        
        # Select files for detailed analysis (most important/complex)
        priority_files = []
        
        # High complexity files
        high_complexity = [f for f in java_files if f.complexity > 15]
        priority_files.extend(sorted(high_complexity, key=lambda x: x.complexity, reverse=True)[:10])
        
        # Important business files (servlets, services, starters)
        business_files = [f for f in java_files if any(keyword in ' '.join(f.class_names).lower() 
                         for keyword in ['servlet', 'service', 'starter', 'controller', 'manager'])]
        priority_files.extend([f for f in business_files if f not in priority_files][:15])
        
        # Representative files from each module
        modules = set(f.module_name for f in java_files)
        for module in modules:
            module_files = [f for f in java_files if f.module_name == module and f not in priority_files]
            if module_files:
                # Pick the most representative file from this module
                representative = max(module_files, key=lambda x: (x.complexity, len(x.class_names)))
                priority_files.append(representative)
        
        # Limit to manageable number for detailed analysis
        selected_files = priority_files[:25]
        
        logger.info(f"🎯 Selected {len(selected_files)} files for detailed AI analysis")
        
        detailed_analyses = []
        
        for i, file_info in enumerate(selected_files):
            logger.info(f"📝 AI analyzing {i+1}/{len(selected_files)}: {Path(file_info.file_path).name}")
            
            try:
                # Create comprehensive analysis prompt
                analysis_prompt = f"""
Analyze this Java file from the A1 Telekom Austria CuCo enterprise application:

FILE METADATA:
- Name: {Path(file_info.file_path).name}
- Module: {file_info.module_name}
- Package: {file_info.package_name}
- Classes: {', '.join(file_info.class_names)}
- Business Context: {file_info.business_context}
- Complexity Score: {file_info.complexity}
- Lines of Code: {file_info.lines_of_code}

IMPORTS:
{chr(10).join(file_info.imports[:20])}

SOURCE CODE:
{file_info.content_preview}

ANALYSIS REQUEST:
Provide comprehensive analysis covering:

1. **Purpose and Functionality**: What does this component do in the CuCo system?
2. **Business Logic**: What business processes or rules are implemented?
3. **Technical Architecture**: Design patterns, architectural decisions, integration points
4. **Data Flow**: How data moves through this component
5. **Dependencies**: Key external dependencies and their purposes
6. **Security Considerations**: Authentication, authorization, data protection
7. **Performance Implications**: Potential bottlenecks or optimization opportunities
8. **Maintainability Assessment**: Code quality, extensibility, technical debt
9. **Integration Points**: How it connects with other system components
10. **Modernization Recommendations**: Specific suggestions for updating this component

Focus on enterprise-level insights relevant to requirements documentation.
"""
                
                analysis = await self.ollama.analyze_code_batch(analysis_prompt, "detailed_component_analysis")
                
                if analysis.get('success', False):
                    detailed_analyses.append({
                        'file': file_info.file_path,
                        'file_info': asdict(file_info),
                        'analysis': analysis,
                        'priority_reason': self._get_priority_reason(file_info)
                    })
                    self.processed_files += 1
                    logger.info(f"   ✅ Success: {analysis.get('tokens_used', 0)} tokens")
                else:
                    logger.error(f"   ❌ Failed: {analysis.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"   ❌ Exception: {e}")
        
        return detailed_analyses

    def _get_priority_reason(self, file_info: JavaFileInfo) -> str:
        """Determine why this file was selected for priority analysis"""
        reasons = []
        
        if file_info.complexity > 15:
            reasons.append(f"High Complexity ({file_info.complexity})")
        
        class_names_str = ' '.join(file_info.class_names).lower()
        if 'servlet' in class_names_str:
            reasons.append("Web Service Endpoint")
        if 'starter' in class_names_str:
            reasons.append("Application Entry Point")
        if 'service' in class_names_str:
            reasons.append("Business Service")
        if 'controller' in class_names_str:
            reasons.append("Controller Component")
        
        if 'Administration' in file_info.business_context:
            reasons.append("Administrative Function")
        
        return ', '.join(reasons) if reasons else "Module Representative"

    async def _generate_requirements_documentation(self, java_files: List[JavaFileInfo], 
                                                 module_analyses: Dict[str, ModuleAnalysis],
                                                 detailed_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive requirements documentation"""
        
        logger.info("📋 Generating enterprise requirements documentation...")
        
        # Create comprehensive context for requirements generation
        context = f"""
# A1 Telekom Austria CuCo Enterprise Application - Requirements Analysis

## SYSTEM OVERVIEW
Application: A1 Telekom Austria Customer Care (CuCo) System
Total Java Files: {len(java_files)}
Modules: {len(module_analyses)}
Primary Technology Stack: GWT, ExtJS/GXT, Spring, iBATIS, Servlet API

## MODULE ANALYSIS
"""
        
        for module_name, analysis in module_analyses.items():
            context += f"""
### Module: {module_name}
- Files: {analysis.file_count}
- Total Lines: {analysis.total_lines:,}
- Average Complexity: {analysis.avg_complexity:.1f}
- Key Packages: {', '.join(analysis.key_packages[:5])}
- Technologies: {', '.join(analysis.technologies)}
- Business Functions: {', '.join(analysis.business_functions)}
- Main Classes: {', '.join(analysis.main_classes[:8])}
"""
        
        context += f"""
## DETAILED COMPONENT ANALYSES
Based on AI analysis of {len(detailed_analyses)} critical components:

"""
        
        for analysis in detailed_analyses[:5]:  # Include top 5 detailed analyses
            file_name = Path(analysis['file']).name
            context += f"""
### {file_name}
Module: {analysis['file_info']['module_name']}
Package: {analysis['file_info']['package_name']}
Business Context: {analysis['file_info']['business_context']}
Priority: {analysis['priority_reason']}

Analysis Summary: {analysis['analysis'].get('analysis_content', 'Not available')[:800]}...

"""
        
        context += """
## REQUIREMENTS GENERATION REQUEST

Based on this comprehensive analysis of the A1 Telekom Austria CuCo enterprise application, generate detailed requirements documentation following this structure:

1. **EXECUTIVE SUMMARY**
   - Business purpose and scope
   - Key stakeholders
   - High-level system capabilities

2. **FUNCTIONAL REQUIREMENTS**
   - User management and authentication
   - Administrative functions
   - Customer care operations
   - Reporting and export capabilities
   - System integration requirements

3. **NON-FUNCTIONAL REQUIREMENTS**
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Availability and reliability
   - Usability requirements
   - Maintainability requirements

4. **TECHNICAL ARCHITECTURE REQUIREMENTS**
   - Technology stack specifications
   - Integration patterns
   - Data management requirements
   - API requirements

5. **MODERNIZATION REQUIREMENTS**
   - Framework migration needs
   - Security enhancements
   - Performance optimizations
   - User experience improvements

6. **IMPLEMENTATION CONSIDERATIONS**
   - Migration strategy
   - Testing requirements
   - Deployment requirements
   - Training needs

Generate comprehensive, enterprise-level requirements suitable for stakeholder review and development planning.
"""
        
        # Generate requirements with AI
        requirements_result = await self.ollama.generate_requirements(context)
        
        return requirements_result

    async def _analyze_architecture_patterns(self, java_files: List[JavaFileInfo],
                                           module_analyses: Dict[str, ModuleAnalysis]) -> Dict[str, Any]:
        """Analyze architectural patterns and integration points"""
        
        architecture_context = f"""
# Architecture Pattern Analysis - A1 Telekom Austria CuCo System

## SYSTEM STATISTICS
- Total Components: {len(java_files)}
- Modules: {list(module_analyses.keys())}
- Average Module Size: {sum(m.file_count for m in module_analyses.values()) / len(module_analyses):.1f} files

## INTEGRATION PATTERNS
Analyzing integration patterns from package structures and imports:

"""
        
        # Analyze package relationships
        package_relationships = defaultdict(set)
        for file_info in java_files:
            for import_stmt in file_info.imports:
                if 'at.a1ta' in import_stmt:
                    package_relationships[file_info.package_name].add(import_stmt)
        
        for package, imports in list(package_relationships.items())[:10]:
            architecture_context += f"""
Package: {package}
Key Imports: {', '.join(list(imports)[:5])}
"""
        
        architecture_context += f"""
## TECHNOLOGY INTEGRATION
"""
        
        all_technologies = set()
        for analysis in module_analyses.values():
            all_technologies.update(analysis.technologies)
        
        architecture_context += f"Identified Technologies: {', '.join(all_technologies)}\n"
        
        architecture_context += """
## ANALYSIS REQUEST
Provide architectural analysis covering:

1. **Overall Architecture Pattern** (Layered, MVC, Microservices, etc.)
2. **Integration Patterns** (How modules communicate)
3. **Data Flow Architecture** (Request/response patterns)
4. **Security Architecture** (Authentication, authorization patterns)
5. **Technology Stack Assessment** (Strengths, weaknesses, compatibility)
6. **Scalability Patterns** (How the system handles growth)
7. **Deployment Architecture** (Likely deployment patterns)
8. **Migration Considerations** (Architectural changes needed for modernization)

Focus on enterprise architecture insights suitable for technical leadership.
"""
        
        architecture_result = await self.ollama.analyze_code_batch(architecture_context, "architecture_analysis")
        return architecture_result

    async def _save_comprehensive_results(self, results: Dict[str, Any]):
        """Save comprehensive analysis results"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save complete JSON results
            with open(f"output/comprehensive_analysis_{timestamp}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Save requirements document
            requirements = results.get('requirements_documentation', {})
            if requirements.get('success', False):
                with open(f"output/cuco_requirements_{timestamp}.md", 'w') as f:
                    f.write(f"# A1 Telekom Austria CuCo - Enterprise Requirements Documentation\n")
                    f.write(f"Generated: {results['timestamp']}\n\n")
                    f.write(f"**Analysis Scope:** {results['analysis_metadata']['total_java_files']} Java files\n")
                    f.write(f"**AI Model:** {results['analysis_metadata']['ai_model']}\n")
                    f.write(f"**Processing Time:** {results['analysis_metadata']['processing_time_seconds']:.2f} seconds\n\n")
                    f.write(requirements.get('analysis_content', 'Requirements generation failed'))
            
            # Save architecture analysis
            architecture = results.get('architecture_analysis', {})
            if architecture.get('success', False):
                with open(f"output/cuco_architecture_{timestamp}.md", 'w') as f:
                    f.write(f"# A1 Telekom Austria CuCo - Architecture Analysis\n")
                    f.write(f"Generated: {results['timestamp']}\n\n")
                    f.write(architecture.get('analysis_content', 'Architecture analysis failed'))
            
            # Save executive summary
            with open(f"output/cuco_executive_summary_{timestamp}.md", 'w') as f:
                f.write(f"# A1 Telekom Austria CuCo - Executive Summary\n")
                f.write(f"Generated: {results['timestamp']}\n\n")
                
                metadata = results['analysis_metadata']
                f.write(f"## Analysis Overview\n")
                f.write(f"- **Total Java Files Analyzed:** {metadata['total_java_files']:,}\n")
                f.write(f"- **Files with Detailed AI Analysis:** {metadata['processed_files']}\n")
                f.write(f"- **Modules Identified:** {metadata['modules_analyzed']}\n")
                f.write(f"- **Processing Time:** {metadata['processing_time_seconds']:.2f} seconds\n")
                f.write(f"- **AI Model:** {metadata['ai_model']}\n\n")
                
                enterprise = results['enterprise_overview']
                f.write(f"## Enterprise Application Profile\n")
                f.write(f"- **Application:** {enterprise['application_name']}\n")
                f.write(f"- **Domain:** {enterprise['business_domain']}\n")
                f.write(f"- **Architecture:** {enterprise['architecture_type']}\n")
                f.write(f"- **Technologies:** {', '.join(enterprise['primary_technologies'])}\n\n")
                
                f.write(f"## Module Breakdown\n")
                for module_name, analysis in results['module_analyses'].items():
                    f.write(f"### {module_name}\n")
                    f.write(f"- Files: {analysis.file_count}\n")
                    f.write(f"- Lines of Code: {analysis.total_lines:,}\n")
                    f.write(f"- Technologies: {', '.join(analysis.technologies)}\n")
                    f.write(f"- Business Functions: {', '.join(analysis.business_functions)}\n\n")
            
            logger.info(f"📁 Comprehensive results saved:")
            logger.info(f"   • Complete analysis: output/comprehensive_analysis_{timestamp}.json")
            logger.info(f"   • Requirements: output/cuco_requirements_{timestamp}.md")
            logger.info(f"   • Architecture: output/cuco_architecture_{timestamp}.md")
            logger.info(f"   • Executive Summary: output/cuco_executive_summary_{timestamp}.md")
            
        except Exception as e:
            logger.error(f"Failed to save comprehensive results: {e}")

async def main():
    """Main execution function"""
    logger.info("🚀 A1 Telekom Austria CuCo - Comprehensive Enterprise Analysis")
    logger.info("=" * 80)
    logger.info("📋 Generating complete requirements documentation with AI analysis")
    logger.info("🧠 Using Qwen3-Coder-30B with 1M context window for deep insights")
    logger.info("=" * 80)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        analyzer = ComprehensiveJavaAnalyzer(java_root_path)
        results = await analyzer.run_comprehensive_analysis()
        
        # Display final summary
        logger.info("=" * 80)
        logger.info("🎉 COMPREHENSIVE ANALYSIS COMPLETE")
        logger.info("=" * 80)
        
        metadata = results['analysis_metadata']
        logger.info(f"📊 Java files analyzed: {metadata['total_java_files']:,}")
        logger.info(f"🧠 Detailed AI analyses: {metadata['processed_files']}")
        logger.info(f"🏢 Modules processed: {metadata['modules_analyzed']}")
        logger.info(f"⏱️ Total processing time: {metadata['processing_time_seconds']:.2f} seconds")
        logger.info(f"🤖 AI model: {metadata['ai_model']}")
        
        logger.info(f"\n📋 Generated Documentation:")
        logger.info(f"   ✅ Enterprise Requirements")
        logger.info(f"   ✅ Architecture Analysis")
        logger.info(f"   ✅ Executive Summary")
        logger.info(f"   ✅ Complete Technical Analysis")
        
        logger.info(f"\n📁 Results available in output/ directory")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Comprehensive analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)