"""
Demonstration of Iteration 13 Implementation
Practical test using existing codebase to showcase:
- Weaviate integration with local Ollama
- 1M token context window utilization
- Repository-scale analysis with Qwen3-Coder
"""

import asyncio
import logging
import json
import sys
import time
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class Iteration13Demo:
    """Demonstration of Iteration 13 capabilities"""
    
    def __init__(self):
        self.ollama = None
        self.demo_results = {}
        
    async def run_demo(self):
        """Run the complete demonstration"""
        logger.info("🚀 Starting Iteration 13 Demonstration")
        logger.info("=" * 70)
        
        demos = [
            ("1. Initialize Ollama Integration", self.demo_ollama_init),
            ("2. Repository Context Assembly", self.demo_repository_context),
            ("3. 1M Token Context Analysis", self.demo_1m_context_analysis),
            ("4. Architecture Pattern Analysis", self.demo_architecture_analysis),
            ("5. Legacy Code Modernization", self.demo_modernization_analysis),
            ("6. Performance Insights", self.demo_performance_insights)
        ]
        
        for demo_name, demo_func in demos:
            logger.info(f"\n{demo_name}")
            logger.info("-" * 50)
            try:
                result = await demo_func()
                self.demo_results[demo_name] = result
                if result.get('success', False):
                    logger.info(f"✅ {demo_name} completed successfully")
                else:
                    logger.warning(f"⚠️ {demo_name} completed with warnings")
            except Exception as e:
                logger.error(f"❌ {demo_name} failed: {e}")
                self.demo_results[demo_name] = {'success': False, 'error': str(e)}
        
        await self.save_demo_results()
        return self.demo_results

    async def demo_ollama_init(self):
        """Demo 1: Initialize Ollama with Qwen3-Coder"""
        try:
            from src.ollama_integration import OllamaIntegration, ContextWindowConfig
            
            # Initialize with optimized config for 1M token context
            context_config = ContextWindowConfig(
                max_tokens=1_048_576,
                target_utilization=0.95,
                moe_optimization=True
            )
            
            self.ollama = OllamaIntegration()
            self.ollama.context_config = context_config
            
            # Health check and model verification
            health = await self.ollama.health_check()
            if not health:
                return {'success': False, 'message': 'Ollama health check failed'}
            
            # Get model information
            models = await self.ollama.list_models()
            qwen_model = next((m for m in models if 'qwen' in m.name.lower()), None)
            
            result = {
                'success': True,
                'message': 'Ollama initialized successfully',
                'model_count': len(models),
                'qwen_model': qwen_model.name if qwen_model else 'Not found',
                'context_window': context_config.max_tokens,
                'moe_optimization': context_config.moe_optimization
            }
            
            logger.info(f"   📋 Found {len(models)} models")
            logger.info(f"   🤖 Qwen Model: {qwen_model.name if qwen_model else 'Not found'}")
            logger.info(f"   🔍 Context Window: {context_config.max_tokens:,} tokens")
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def demo_repository_context(self):
        """Demo 2: Assemble repository-wide context from existing codebase"""
        try:
            # Collect Python files from src directory as a proxy for Java analysis
            src_dir = Path("src")
            python_files = list(src_dir.glob("*.py"))[:10]  # Limit to first 10 files
            
            repository_context = []
            total_size = 0
            max_size = 500_000  # ~500KB limit for demo
            
            for file_path in python_files:
                if total_size >= max_size:
                    break
                    
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if total_size + len(content) <= max_size:
                        repository_context.append(f"# File: {file_path}\n{content}\n")
                        total_size += len(content)
                        
                except Exception as e:
                    logger.warning(f"Could not read {file_path}: {e}")
            
            full_context = "\n".join(repository_context)
            
            result = {
                'success': True,
                'message': 'Repository context assembled',
                'files_included': len(repository_context),
                'total_characters': len(full_context),
                'estimated_tokens': len(full_context) // 3,
                'context_sample': full_context[:300] + '...' if len(full_context) > 300 else full_context
            }
            
            logger.info(f"   📁 Included {len(repository_context)} files")
            logger.info(f"   📊 Total characters: {len(full_context):,}")
            logger.info(f"   🎯 Estimated tokens: {len(full_context) // 3:,}")
            
            # Store context for next demo
            self.repository_context = full_context
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def demo_1m_context_analysis(self):
        """Demo 3: Analyze repository using 1M token context window"""
        if not hasattr(self, 'repository_context'):
            return {'success': False, 'message': 'Repository context not available'}
            
        try:
            logger.info("   🧠 Analyzing repository with Qwen3-Coder...")
            
            analysis_prompt = f"""
            You are analyzing a Java JSP Application Reverse Engineering Tool codebase.
            This is a sophisticated system that uses AI to analyze legacy Java/JSP applications.
            
            Please provide a comprehensive analysis including:
            1. **Overall Architecture**: High-level system design and patterns
            2. **Core Components**: Main modules and their responsibilities  
            3. **AI Integration**: How the system uses AI providers (OpenAI, Anthropic, Ollama)
            4. **Database Integration**: ChromaDB and vector storage patterns
            5. **Processing Pipeline**: How code is analyzed and processed
            6. **Modernization Insights**: Opportunities for improvement
            7. **Technical Debt**: Areas needing refactoring
            8. **Performance Optimizations**: Potential improvements
            
            Repository Context:
            {self.repository_context}
            """
            
            start_time = time.time()
            result = await self.ollama.analyze_code_repository(
                repository_context=analysis_prompt,
                analysis_type="comprehensive_repository_analysis"
            )
            analysis_time = time.time() - start_time
            
            # Extract key insights
            analysis_content = result.content
            insights = {
                'architecture_mentioned': 'architecture' in analysis_content.lower(),
                'ai_integration_mentioned': any(term in analysis_content.lower() for term in ['openai', 'anthropic', 'ollama', 'ai provider']),
                'database_mentioned': any(term in analysis_content.lower() for term in ['chromadb', 'vector', 'database']),
                'modernization_mentioned': any(term in analysis_content.lower() for term in ['modernization', 'legacy', 'improvement', 'refactor'])
            }
            
            demo_result = {
                'success': True,
                'message': '1M token context analysis completed',
                'analysis_time': analysis_time,
                'tokens_used': result.tokens_used,
                'context_utilization': result.context_utilization,
                'confidence_score': result.confidence_score,
                'processing_time': result.processing_time,
                'insights_detected': insights,
                'analysis_length': len(analysis_content),
                'analysis_preview': analysis_content[:500] + '...' if len(analysis_content) > 500 else analysis_content
            }
            
            logger.info(f"   ⏱️  Analysis time: {analysis_time:.2f}s")
            logger.info(f"   🎯 Tokens used: {result.tokens_used:,}")
            logger.info(f"   📊 Context utilization: {result.context_utilization:.1%}")
            logger.info(f"   💡 Insights detected: {sum(insights.values())}/4")
            
            # Store full analysis for next demos
            self.full_analysis = analysis_content
            
            return demo_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def demo_architecture_analysis(self):
        """Demo 4: Extract architectural patterns and design insights"""
        if not hasattr(self, 'full_analysis'):
            return {'success': False, 'message': 'Full analysis not available'}
            
        try:
            architecture_prompt = f"""
            Based on the following system analysis, extract and categorize architectural patterns:
            
            Previous Analysis:
            {self.full_analysis}
            
            Please identify:
            1. **Design Patterns**: Which patterns are used (Factory, Strategy, Observer, etc.)
            2. **Architectural Patterns**: System-level patterns (MVC, Layered, etc.)
            3. **Integration Patterns**: How components communicate
            4. **Data Patterns**: How data is stored and accessed
            5. **AI Patterns**: How AI is integrated into the system
            
            Format as structured analysis with confidence scores.
            """
            
            result = await self.ollama.analyze_code_repository(
                repository_context=architecture_prompt,
                analysis_type="architectural_pattern_extraction"
            )
            
            # Parse patterns (simplified)
            patterns_found = []
            content_lower = result.content.lower()
            
            common_patterns = [
                'factory pattern', 'strategy pattern', 'observer pattern',
                'mvc pattern', 'repository pattern', 'singleton pattern',
                'adapter pattern', 'facade pattern', 'decorator pattern'
            ]
            
            for pattern in common_patterns:
                if pattern in content_lower:
                    patterns_found.append(pattern)
            
            demo_result = {
                'success': True,
                'message': 'Architectural analysis completed',
                'patterns_identified': patterns_found,
                'pattern_count': len(patterns_found),
                'analysis_length': len(result.content),
                'tokens_used': result.tokens_used,
                'architecture_analysis': result.content[:400] + '...' if len(result.content) > 400 else result.content
            }
            
            logger.info(f"   🏗️  Patterns identified: {len(patterns_found)}")
            for pattern in patterns_found[:5]:  # Show first 5
                logger.info(f"      - {pattern}")
            
            return demo_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def demo_modernization_analysis(self):
        """Demo 5: Identify legacy code modernization opportunities"""
        try:
            modernization_prompt = f"""
            Analyze this Java JSP Application Reverse Engineering Tool for modernization opportunities.
            
            Context: {self.repository_context[:10000]}
            
            Focus on:
            1. **Legacy Dependencies**: Outdated libraries or frameworks
            2. **Code Patterns**: Old-style Java patterns that could be modernized
            3. **Architecture Updates**: Migration to microservices, containerization
            4. **Performance Improvements**: Database optimization, caching strategies
            5. **Security Enhancements**: Modern security practices
            6. **Cloud Migration**: Opportunities for cloud deployment
            7. **API Modernization**: REST API improvements
            8. **Testing Improvements**: Modern testing approaches
            
            Prioritize recommendations by impact and effort required.
            """
            
            result = await self.ollama.analyze_code_repository(
                repository_context=modernization_prompt,
                analysis_type="legacy_modernization_analysis"
            )
            
            # Extract modernization themes
            modernization_areas = []
            content_lower = result.content.lower()
            
            modernization_keywords = [
                'microservices', 'containerization', 'docker', 'kubernetes',
                'rest api', 'graphql', 'spring boot', 'reactive programming',
                'cloud migration', 'aws', 'azure', 'gcp',
                'security', 'authentication', 'jwt', 'oauth',
                'caching', 'redis', 'elasticsearch', 'mongodb'
            ]
            
            for keyword in modernization_keywords:
                if keyword in content_lower:
                    modernization_areas.append(keyword)
            
            demo_result = {
                'success': True,
                'message': 'Modernization analysis completed',
                'modernization_areas': modernization_areas,
                'recommendations_count': len(modernization_areas),
                'tokens_used': result.tokens_used,
                'modernization_analysis': result.content[:500] + '...' if len(result.content) > 500 else result.content
            }
            
            logger.info(f"   🔄 Modernization areas identified: {len(modernization_areas)}")
            for area in modernization_areas[:5]:
                logger.info(f"      - {area}")
            
            return demo_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def demo_performance_insights(self):
        """Demo 6: Generate performance optimization insights"""
        try:
            performance_prompt = f"""
            Analyze this codebase for performance optimization opportunities:
            
            System Context: {self.repository_context[:8000]}
            
            Identify:
            1. **Database Performance**: Query optimization, indexing strategies
            2. **Memory Usage**: Memory leaks, optimization opportunities  
            3. **Processing Efficiency**: Algorithm improvements, caching
            4. **I/O Operations**: File handling, network operations
            5. **Concurrency**: Threading, async processing opportunities
            6. **Resource Management**: Connection pooling, resource cleanup
            7. **Monitoring**: Performance metrics and monitoring strategies
            
            Provide specific, actionable recommendations with estimated impact.
            """
            
            result = await self.ollama.analyze_code_repository(
                repository_context=performance_prompt,
                analysis_type="performance_optimization_analysis"
            )
            
            # Get performance statistics from Ollama
            perf_stats = self.ollama.get_performance_stats()
            
            demo_result = {
                'success': True,
                'message': 'Performance analysis completed',
                'ollama_performance_stats': perf_stats,
                'tokens_used': result.tokens_used,
                'analysis_length': len(result.content),
                'performance_insights': result.content[:400] + '...' if len(result.content) > 400 else result.content
            }
            
            logger.info(f"   ⚡ Performance analysis completed")
            logger.info(f"   📊 Ollama total requests: {perf_stats.get('total_requests', 0)}")
            logger.info(f"   ⏱️  Average response time: {perf_stats.get('average_response_time', 0):.2f}s")
            logger.info(f"   🎯 Average context utilization: {perf_stats.get('context_utilization_avg', 0):.1%}")
            
            return demo_result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def save_demo_results(self):
        """Save demonstration results to file"""
        try:
            timestamp = int(time.time())
            filename = f"iteration13_demo_results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.demo_results, f, indent=2, default=str)
            
            logger.info(f"📁 Demo results saved to: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save demo results: {e}")

async def main():
    """Run the Iteration 13 demonstration"""
    demo = Iteration13Demo()
    
    try:
        results = await demo.run_demo()
        
        logger.info("\n" + "=" * 70)
        logger.info("🎯 ITERATION 13 DEMONSTRATION SUMMARY")
        logger.info("=" * 70)
        
        successful_demos = sum(1 for result in results.values() if result.get('success', False))
        total_demos = len(results)
        
        logger.info(f"✅ Successful demonstrations: {successful_demos}/{total_demos}")
        
        if successful_demos == total_demos:
            logger.info("🚀 All demonstrations completed successfully!")
            logger.info("🎉 Iteration 13 implementation is working as expected!")
        else:
            logger.warning("⚠️  Some demonstrations had issues - check logs for details")
        
        logger.info("=" * 70)
        
        # Cleanup
        if demo.ollama:
            await demo.ollama.cleanup()
        
        return successful_demos == total_demos
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)