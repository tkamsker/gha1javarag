"""
Java-Focused Analysis
Process specifically Java files from the enterprise application
"""

import asyncio
import logging
import sys
import os
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def main():
    """Run Java-focused analysis"""
    logger.info("☕ Java-Focused Enterprise Application Analysis")
    logger.info("=" * 60)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        from src.simple_fresh_processor import SimpleFreshProcessor
        
        # Initialize processor
        processor = SimpleFreshProcessor(java_root_path)
        
        # Check health first
        if not await processor.ollama.health_check():
            logger.error("❌ Ollama health check failed")
            return False
        
        logger.info("✅ Ollama is ready")
        
        # Discover Java files specifically
        logger.info("🔍 Discovering Java files...")
        java_files = []
        
        for file_path in Path(java_root_path).rglob("*.java"):
            if file_path.is_file():
                try:
                    file_info = processor._analyze_file_basic(file_path)
                    if file_info and file_info.file_type == 'java':
                        java_files.append(file_info)
                        
                        if len(java_files) >= 20:  # Limit for testing
                            break
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")
        
        logger.info(f"📊 Found {len(java_files)} Java files for analysis")
        
        # Show some sample files
        logger.info("📋 Sample Java files:")
        for i, file_info in enumerate(java_files[:10]):
            logger.info(f"   {i+1}. {Path(file_info.file_path).name}")
            logger.info(f"      Package: {file_info.package_name}")
            logger.info(f"      Classes: {', '.join(file_info.class_names) if file_info.class_names else 'None'}")
            logger.info(f"      Complexity: {file_info.complexity}")
        
        if not java_files:
            logger.error("❌ No Java files found!")
            return False
        
        # Process interesting Java files with Qwen analysis
        logger.info("🧠 Analyzing selected Java files with Qwen...")
        
        interesting_files = [f for f in java_files if f.complexity > 3 and len(f.class_names) > 0][:10]
        
        logger.info(f"🎯 Selected {len(interesting_files)} complex files for detailed analysis")
        
        analyses = []
        for i, file_info in enumerate(interesting_files):
            logger.info(f"📝 Analyzing file {i+1}/{len(interesting_files)}: {Path(file_info.file_path).name}")
            
            try:
                analysis = await processor._analyze_with_qwen(file_info)
                analyses.append({
                    'file': file_info.file_path,
                    'analysis': analysis
                })
                
                logger.info(f"   ✅ Analysis completed: {analysis.get('tokens_used', 0)} tokens")
                
            except Exception as e:
                logger.error(f"   ❌ Analysis failed: {e}")
        
        # Repository-wide analysis with actual Java content
        logger.info("🏗️ Performing repository-wide analysis...")
        
        # Build comprehensive context from Java files
        repo_context = """
        Java Enterprise Application Analysis
        
        This is a comprehensive Java enterprise application with the following structure:
        """
        
        # Add module information
        modules = list(set(f.module_name for f in java_files))
        repo_context += f"\nModules: {', '.join(modules)}\n"
        
        # Add package information
        packages = list(set(f.package_name for f in java_files if f.package_name != 'default'))
        repo_context += f"Packages: {', '.join(packages[:15])}\n"
        
        # Add sample code from most complex files
        repo_context += "\nSample Java Classes:\n"
        
        complex_files = sorted(java_files, key=lambda x: x.complexity, reverse=True)[:5]
        for i, file_info in enumerate(complex_files):
            repo_context += f"""
        {i+1}. File: {Path(file_info.file_path).name}
           Package: {file_info.package_name}
           Classes: {', '.join(file_info.class_names)}
           Methods: {', '.join(file_info.methods[:5])}
           Complexity: {file_info.complexity}
           
           Code Preview:
           {file_info.content_preview}
           
        """
        
        repo_context += """
        Please analyze this Java enterprise application and provide:
        1. Overall architecture assessment
        2. Technology stack identification
        3. Design patterns in use
        4. Business domain analysis
        5. Code quality evaluation
        6. Security considerations
        7. Performance implications
        8. Modernization recommendations
        9. Technical debt assessment
        10. Integration patterns
        """
        
        # Perform comprehensive analysis
        repo_analysis = await processor.ollama.analyze_code_repository(
            repository_context=repo_context,
            analysis_type="comprehensive_java_enterprise_analysis"
        )
        
        logger.info(f"✅ Repository analysis completed: {repo_analysis.tokens_used} tokens")
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results = {
            'java_files_analyzed': len(java_files),
            'detailed_analyses': len(analyses),
            'modules': modules,
            'packages': packages,
            'individual_analyses': analyses,
            'repository_analysis': {
                'content': repo_analysis.content,
                'tokens_used': repo_analysis.tokens_used,
                'processing_time': repo_analysis.processing_time,
                'context_utilization': repo_analysis.context_utilization
            }
        }
        
        os.makedirs("output", exist_ok=True)
        
        # Save JSON results
        import json
        with open(f"output/java_analysis_{timestamp}.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save repository analysis as markdown
        with open(f"output/java_repository_analysis_{timestamp}.md", 'w') as f:
            f.write(f"# Java Enterprise Application Analysis - {timestamp}\n\n")
            f.write(f"**Files Analyzed:** {len(java_files)} Java files\n")
            f.write(f"**Modules:** {', '.join(modules)}\n")
            f.write(f"**Total Packages:** {len(packages)}\n\n")
            f.write("## Repository Analysis\n\n")
            f.write(repo_analysis.content)
            
            f.write("\n\n## Individual File Analyses\n\n")
            for analysis in analyses:
                file_name = Path(analysis['file']).name
                f.write(f"### {file_name}\n\n")
                f.write(analysis['analysis'].get('analysis_content', 'Analysis failed'))
                f.write("\n\n---\n\n")
        
        # Display summary
        logger.info("=" * 60)
        logger.info("🎉 JAVA ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"📊 Java files discovered: {len(java_files)}")
        logger.info(f"🧠 Detailed analyses: {len(analyses)}")
        logger.info(f"🏢 Modules: {len(modules)} ({', '.join(modules)})")
        logger.info(f"📦 Packages: {len(packages)}")
        logger.info(f"🎯 Repository analysis: {repo_analysis.tokens_used} tokens")
        logger.info(f"📁 Results saved to output/java_analysis_{timestamp}.json")
        logger.info(f"📄 Report saved to output/java_repository_analysis_{timestamp}.md")
        logger.info("=" * 60)
        
        # Cleanup
        await processor.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)