import os
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging

try:
    from ai_analyzer import AIAnalyzer
    from classification_prompts import ClassificationPromptBuilder
    from metadata_schemas import EnhancedAIAnalysis, EnhancedFileClassification, validate_and_fix_ai_response
except ImportError:
    from .ai_analyzer import AIAnalyzer
    from .classification_prompts import ClassificationPromptBuilder
    from .metadata_schemas import EnhancedAIAnalysis, EnhancedFileClassification, validate_and_fix_ai_response

logger = logging.getLogger('java_analysis.enhanced_ai_analyzer')

class EnhancedAIAnalyzer(AIAnalyzer):
    """Enhanced AI analyzer with architectural classification"""
    
    def __init__(self):
        super().__init__()
        self.prompt_builder = ClassificationPromptBuilder()
        logger.info("Enhanced AI analyzer initialized with classification capabilities")
    
    def create_enhanced_file_prompt(self, file_type: str, content: str, file_path: str) -> str:
        """Create enhanced classification prompt"""
        return self.prompt_builder.create_classification_prompt(file_path, content, file_type)
    
    async def analyze_file_with_classification(self, file_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file with enhanced classification"""
        file_path = file_metadata.get('file_path', '')
        file_type = file_metadata.get('file_type', 'Unknown')
        content = file_metadata.get('content', '')
        
        logger.info(f"Enhanced analysis for: {file_path}")
        
        # Check if we should continue making requests (only for OpenAI)
        if self.ai_provider.get_provider_name() == "OpenAI":
            if not self.rate_limiter.should_continue_requests():
                stats = self.rate_limiter.get_stats()
                if stats.get('quota_exceeded'):
                    logger.error("Cannot continue analysis due to quota exceeded")
                    file_metadata.update({
                        'analysis_status': 'failed',
                        'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                    })
                    return file_metadata
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create enhanced prompt
        prompt = self.create_enhanced_file_prompt(file_type, content, file_path)
        
        # Get AI analysis
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Check if we should continue before each attempt (only for OpenAI)
                if self.ai_provider.get_provider_name() == "OpenAI":
                    if not self.rate_limiter.should_continue_requests():
                        stats = self.rate_limiter.get_stats()
                        if stats.get('quota_exceeded'):
                            logger.error("Cannot continue analysis due to quota exceeded")
                            file_metadata.update({
                                'analysis_status': 'failed',
                                'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                            })
                            return file_metadata
                
                messages = [
                    {"role": "system", "content": "You are an expert software architect specializing in code analysis and architectural classification. Provide accurate, detailed analysis."},
                    {"role": "user", "content": prompt}
                ]
                
                analysis_text = await self.ai_provider.create_chat_completion(
                    messages=messages,
                    temperature=0.1,  # Lower temperature for more consistent classification
                    max_tokens=2500
                )
                
                logger.debug(f"Successfully received enhanced analysis from {self.ai_provider.get_provider_name()}")
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Parse enhanced analysis
                enhanced_analysis = self.parse_enhanced_analysis(analysis_text, file_path)
                
                # Update file metadata
                file_metadata.update({
                    'enhanced_ai_analysis': enhanced_analysis,
                    'analysis_status': 'completed_enhanced',
                    'ai_provider': self.ai_provider.get_provider_name(),
                    'ai_model': self.ai_provider.get_model_name()
                })
                
                logger.info(f"Enhanced analysis completed for: {file_path}")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.debug(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"Enhanced analysis failed (attempt {attempt + 1}) for {file_path}: {str(e)}")
                self.rate_limiter.record_failure(e)
                
                # Check if this is a quota exceeded error (only for OpenAI)
                if self.ai_provider.get_provider_name() == "OpenAI":
                    if 'insufficient_quota' in str(e).lower() or 'quota' in str(e).lower():
                        logger.error("QUOTA EXCEEDED: Stopping analysis")
                        file_metadata.update({
                            'analysis_status': 'failed',
                            'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                        })
                        return file_metadata
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    file_metadata.update({
                        'analysis_status': 'failed',
                        'error': str(e)
                    })
        
        return file_metadata
    
    def parse_enhanced_analysis(self, analysis_text: str, file_path: str) -> Dict[str, Any]:
        """Parse enhanced analysis response with validation and fixing"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_dict = json.loads(json_match.group())
                
                # Validate and fix AI response before Pydantic validation
                analysis_dict = validate_and_fix_ai_response(analysis_dict)
                
                # Validate using Pydantic model
                enhanced_analysis = EnhancedAIAnalysis.model_validate(analysis_dict)
                return enhanced_analysis.model_dump()
            else:
                logger.warning(f"Could not extract JSON from analysis for {file_path}")
                return self.create_fallback_analysis(analysis_text, file_path)
                
        except Exception as e:
            logger.error(f"Failed to parse enhanced analysis for {file_path}: {e}")
            logger.debug(f"Raw analysis text: {analysis_text[:500]}...")
            return self.create_fallback_analysis(analysis_text, file_path)
    
    def create_fallback_analysis(self, analysis_text: str, file_path: str) -> Dict[str, Any]:
        """Create fallback analysis when parsing fails"""
        # Basic classification based on file path and extension
        architectural_layer = self.guess_layer_from_path(file_path)
        component_type = self.guess_component_from_path(file_path)
        
        return {
            "purpose": analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text,
            "components": [],
            "data_structures": [],
            "business_rules": [],
            "dependencies": [],
            "file_classification": {
                "architectural_layer": architectural_layer,
                "component_type": component_type,
                "confidence_score": 0.3,  # Low confidence for fallback
                "technology_stack": [],
                "frameworks_detected": [],
                "design_patterns": [],
                "primary_purpose": "Analysis parsing failed",
                "secondary_purposes": [],
                "business_domain": None,
                "dependencies": [],
                "exposes_api": False,
                "consumes_api": False,
                "database_interactions": False,
                "complexity_indicators": ["parsing_failed"],
                "potential_issues": ["analysis_parsing_failed"],
                "refactoring_suggestions": []
            },
            "integration_points": [],
            "security_considerations": [],
            "performance_considerations": []
        }
    
    def guess_layer_from_path(self, file_path: str) -> str:
        """Guess architectural layer from file path"""
        path_lower = file_path.lower()
        
        if any(x in path_lower for x in ['test', 'spec']):
            return "test"
        elif any(x in path_lower for x in ['controller', 'rest', 'api']):
            return "backend_service"
        elif any(x in path_lower for x in ['service', 'business']):
            return "backend_service"
        elif any(x in path_lower for x in ['dao', 'repository']):
            return "data_access"
        elif any(x in path_lower for x in ['entity', 'model', 'domain']):
            return "persistence"
        elif any(x in path_lower for x in ['jsp', 'html', 'css', 'js']):
            return "frontend"
        elif any(x in path_lower for x in ['config', 'properties', 'xml']):
            return "configuration"
        elif any(x in path_lower for x in ['batch', 'job', 'scheduler']):
            return "batch_process"
        elif any(x in path_lower for x in ['util', 'helper', 'common']):
            return "utility"
        else:
            return "unknown"
    
    def guess_component_from_path(self, file_path: str) -> str:
        """Guess component type from file path and extension"""
        path_lower = file_path.lower()
        
        if file_path.endswith('.jsp'):
            return "jsp_page"
        elif file_path.endswith('.js'):
            return "javascript"
        elif file_path.endswith('.css'):
            return "css_stylesheet"
        elif file_path.endswith('.html'):
            return "html_template"
        elif file_path.endswith('.sql'):
            return "database_script"
        elif 'test' in path_lower:
            return "unit_test"
        elif 'controller' in path_lower:
            return "rest_controller"
        elif 'service' in path_lower:
            return "service_layer"
        elif 'repository' in path_lower:
            return "repository"
        elif 'dao' in path_lower:
            return "dao"
        elif 'entity' in path_lower:
            return "entity"
        elif 'dto' in path_lower:
            return "dto"
        else:
            return "unknown"
    
    async def analyze_files_with_classification(self, metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple files with enhanced classification"""
        logger.info(f"Starting enhanced analysis of {len(metadata_list)} files using {self.ai_provider.get_provider_name()}")
        analyzed_metadata = []
        
        for idx, metadata in enumerate(metadata_list, 1):
            logger.info(f"Processing file {idx}/{len(metadata_list)}")
            analyzed = await self.analyze_file_with_classification(metadata)
            analyzed_metadata.append(analyzed)
        
        logger.info("Completed enhanced analysis of all files")
        return analyzed_metadata