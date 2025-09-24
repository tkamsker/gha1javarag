import asyncio
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from dotenv import load_dotenv
from ai_providers import create_ai_provider
from rate_limiter import RateLimiter, RateLimitConfig
from logger_config import setup_logging

logger = logging.getLogger('java_analysis.step3_enhanced_test')

class EnhancedModernRequirementsProcessorTest:
    def __init__(self):
        load_dotenv()
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
        self.requirements_dir = self.output_dir / "requirements_enhanced_test"
        self.modern_requirements_file = self.output_dir / "enhanced_modern_requirements_test.md"
        self.cloud_architecture_file = self.output_dir / "cloud_architecture_blueprints_test.json"
        self.microservices_file = self.output_dir / "microservices_design_test.md"
        self.tech_stack_file = self.output_dir / "technology_stack_test.json"
        
        # Enhanced metadata files
        self.enhanced_metadata_file = self.output_dir / "enhanced_metadata.json"
        self.architecture_report_file = self.output_dir / "enhanced_architecture_report.json"
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"TEST MODE: Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Test mode rate limiting - very conservative
        rate_config = RateLimitConfig(
            requests_per_minute=8,
            requests_per_hour=400,
            delay_between_requests=10.0,
            exponential_backoff_base=2.0,
            max_retries=3
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Load enhanced data
        self.enhanced_metadata = self.load_enhanced_metadata()
        self.architecture_report = self.load_architecture_report()
        self.enhanced_requirements = self.load_enhanced_requirements()

    def load_enhanced_metadata(self) -> Dict[str, Any]:
        """Load enhanced metadata from Step1_Enhanced"""
        try:
            if not self.enhanced_metadata_file.exists():
                logger.warning(f"TEST MODE: Enhanced metadata file not found: {self.enhanced_metadata_file}")
                return {}
            
            with open(self.enhanced_metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"TEST MODE: Loaded enhanced metadata with {len(metadata)} entries")
            return metadata
            
        except Exception as e:
            logger.error(f"TEST MODE: Error loading enhanced metadata: {e}")
            return {}

    def load_architecture_report(self) -> Dict[str, Any]:
        """Load architecture report from Step1_Enhanced"""
        try:
            if not self.architecture_report_file.exists():
                logger.warning(f"TEST MODE: Architecture report file not found: {self.architecture_report_file}")
                return {}
            
            with open(self.architecture_report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            logger.info(f"TEST MODE: Loaded architecture report with {len(report.get('layers', {}))} layers")
            return report
            
        except Exception as e:
            logger.error(f"TEST MODE: Error loading architecture report: {e}")
            return {}

    def load_enhanced_requirements(self) -> Dict[str, Any]:
        """Load enhanced requirements from Step2_Enhanced (test or production)"""
        enhanced_requirements = {}
        
        # Try test directory first, then production directory
        test_dir = self.output_dir / "requirements_enhanced_test"
        prod_dir = self.output_dir / "requirements_enhanced"
        
        requirements_dir = test_dir if test_dir.exists() else prod_dir
        
        if not requirements_dir.exists():
            logger.warning(f"TEST MODE: Enhanced requirements directory not found: {requirements_dir}")
            return enhanced_requirements
        
        # Recursively find all markdown files
        for md_file in requirements_dir.rglob("*.md"):
            if md_file.name.startswith("step2_enhanced"):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract the relative path for organization
                relative_path = md_file.relative_to(requirements_dir)
                layer = relative_path.parts[0] if len(relative_path.parts) > 1 else "unknown"
                component = relative_path.parts[1] if len(relative_path.parts) > 2 else "unknown"
                
                enhanced_requirements[str(md_file)] = {
                    'content': content,
                    'layer': layer,
                    'component': component,
                    'file_path': str(md_file)
                }
                
            except Exception as e:
                logger.warning(f"TEST MODE: Error reading enhanced requirements file {md_file}: {e}")
        
        logger.info(f"TEST MODE: Loaded {len(enhanced_requirements)} enhanced requirements files")
        return enhanced_requirements

    async def generate_cloud_architecture_blueprint_test(self) -> Dict[str, Any]:
        """Test version - generate simplified cloud architecture blueprint"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare simplified architecture context for testing
        architecture_context = {
            'layers': list(self.architecture_report.get('layers', {}).keys())[:3],  # Limit to 3 layers
            'components': [],
            'technologies': []
        }
        
        # Extract limited components and technologies for testing
        for layer_name, layer_info in list(self.architecture_report.get('layers', {}).items())[:2]:  # Only first 2 layers
            components = layer_info.get('components', [])[:2]  # Limit components
            technologies = layer_info.get('technologies', [])[:2]  # Limit technologies
            
            architecture_context['components'].extend(components)
            architecture_context['technologies'].extend(technologies)
        
        prompt = f"""TEST MODE: Based on this simplified Java/JSP application analysis, create a basic cloud architecture blueprint:

Architecture Analysis:
{json.dumps(architecture_context, indent=2)}

Create a simplified cloud architecture blueprint with:

1. **Basic Microservices Design**: 2-3 core services
2. **Container Strategy**: Docker basics
3. **Cloud Infrastructure**: Key AWS/Azure services
4. **API Gateway**: Basic configuration

Keep the response concise for testing. Provide JSON format.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a cloud architect. Provide concise, practical recommendations for testing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000  # Reduced for testing
            )
            
            self.rate_limiter.record_request()
            
            # Try to parse as JSON
            try:
                blueprint = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("TEST MODE: AI response was not valid JSON, creating structured response")
                blueprint = {
                    "microservices_design": {"services": ["user-service", "business-service", "data-service"]},
                    "container_strategy": {"approach": "Docker containerization"},
                    "cloud_infrastructure": {"primary": "AWS", "services": ["ECS", "RDS", "API Gateway"]},
                    "api_gateway": {"type": "AWS API Gateway"},
                    "test_mode": True,
                    "raw_response": response
                }
            
            return blueprint
            
        except Exception as e:
            logger.error(f"TEST MODE: Error generating cloud architecture blueprint: {e}")
            return {"error": str(e), "test_mode": True}

    async def generate_microservices_design_test(self, cloud_blueprint: Dict[str, Any]) -> str:
        """Test version - generate simplified microservices design"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare simplified context for testing
        context = {
            'existing_layers': list(self.architecture_report.get('layers', {}).keys())[:2],
            'cloud_blueprint': cloud_blueprint.get('microservices_design', {}),
            'sample_count': len(self.enhanced_requirements)
        }
        
        prompt = f"""TEST MODE: Create a simplified microservices design document:

Context:
{json.dumps(context, indent=2)}

Create a basic microservices design with:
1. **Service Decomposition**: 2-3 main services
2. **API Contracts**: Basic REST endpoints
3. **Data Management**: Simple database strategy
4. **Communication**: Basic HTTP/REST

Keep it concise for testing purposes.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a microservices expert. Provide practical, concise designs for testing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000  # Reduced for testing
            )
            
            self.rate_limiter.record_request()
            return response
            
        except Exception as e:
            logger.error(f"TEST MODE: Error generating microservices design: {e}")
            return f"TEST MODE: Error generating microservices design: {str(e)}"

    async def generate_technology_stack_recommendations_test(self, cloud_blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Test version - generate simplified technology recommendations"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare simplified context
        current_technologies = []
        for layer_info in list(self.architecture_report.get('layers', {}).values())[:2]:  # Limit to 2 layers
            current_technologies.extend(layer_info.get('technologies', [])[:2])  # Limit technologies
        
        context = {
            'current_technologies': current_technologies,
            'cloud_blueprint': cloud_blueprint,
            'test_mode': True
        }
        
        prompt = f"""TEST MODE: Provide simplified technology recommendations:

Context:
{json.dumps(context, indent=2)}

Provide basic recommendations for:
1. **Frontend**: React basics
2. **Backend**: Node.js or Spring Boot
3. **Database**: PostgreSQL or MongoDB
4. **Cloud**: AWS basics

Keep it simple for testing. Provide JSON format.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a technology strategist. Provide practical recommendations for testing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000  # Reduced for testing
            )
            
            self.rate_limiter.record_request()
            
            # Try to parse as JSON
            try:
                tech_stack = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("TEST MODE: AI response was not valid JSON, creating structured response")
                tech_stack = {
                    "frontend_technologies": {"framework": "React", "testing": "Jest"},
                    "backend_technologies": {"runtime": "Node.js", "framework": "Express"},
                    "database_technologies": {"primary": "PostgreSQL", "cache": "Redis"},
                    "cloud_services": {"provider": "AWS", "compute": "ECS"},
                    "test_mode": True,
                    "raw_response": response
                }
            
            return tech_stack
            
        except Exception as e:
            logger.error(f"TEST MODE: Error generating technology stack recommendations: {e}")
            return {"error": str(e), "test_mode": True}

    async def generate_enhanced_modern_requirements_test(self, cloud_blueprint: Dict[str, Any], 
                                                        microservices_design: str, 
                                                        tech_stack: Dict[str, Any]) -> str:
        """Test version - generate simplified modern requirements"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare simplified context
        context = {
            'total_layers': len(self.architecture_report.get('layers', {})),
            'total_files': len(self.enhanced_metadata),
            'requirements_count': len(self.enhanced_requirements),
            'test_mode': True
        }
        
        prompt = f"""TEST MODE: Create a simplified modern requirements document:

Context:
{json.dumps(context, indent=2)}

Create a basic modern requirements document with:

1. **Executive Summary**: Current state and goals
2. **Architecture Overview**: Target microservices architecture
3. **Technology Plan**: Recommended tech stack
4. **Migration Strategy**: High-level approach

Keep it concise for testing purposes.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a solution architect. Create practical modernization documents for testing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2500  # Reduced for testing
            )
            
            self.rate_limiter.record_request()
            return response
            
        except Exception as e:
            logger.error(f"TEST MODE: Error generating enhanced modern requirements: {e}")
            return f"TEST MODE: Error generating enhanced modern requirements: {str(e)}"

    async def process_enhanced_modernization_test(self) -> None:
        """Test version of process enhanced modernization"""
        logger.info("TEST MODE: Starting enhanced modernization process...")
        
        # Generate cloud architecture blueprint
        logger.info("TEST MODE: Generating cloud architecture blueprint...")
        cloud_blueprint = await self.generate_cloud_architecture_blueprint_test()
        
        # Save cloud blueprint
        with open(self.cloud_architecture_file, 'w', encoding='utf-8') as f:
            json.dump(cloud_blueprint, f, indent=2)
        logger.info(f"TEST MODE: Cloud architecture blueprint saved to: {self.cloud_architecture_file}")
        
        # Generate microservices design
        logger.info("TEST MODE: Generating microservices design...")
        microservices_design = await self.generate_microservices_design_test(cloud_blueprint)
        
        # Save microservices design
        with open(self.microservices_file, 'w', encoding='utf-8') as f:
            f.write(f"# TEST MODE: Microservices Design Document\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode**: TEST\n\n")
            f.write(microservices_design)
        logger.info(f"TEST MODE: Microservices design saved to: {self.microservices_file}")
        
        # Generate technology stack recommendations
        logger.info("TEST MODE: Generating technology stack recommendations...")
        tech_stack = await self.generate_technology_stack_recommendations_test(cloud_blueprint)
        
        # Save technology stack
        with open(self.tech_stack_file, 'w', encoding='utf-8') as f:
            json.dump(tech_stack, f, indent=2)
        logger.info(f"TEST MODE: Technology stack recommendations saved to: {self.tech_stack_file}")
        
        # Generate comprehensive modern requirements
        logger.info("TEST MODE: Generating enhanced modern requirements document...")
        modern_requirements = await self.generate_enhanced_modern_requirements_test(
            cloud_blueprint, microservices_design, tech_stack
        )
        
        # Save modern requirements
        with open(self.modern_requirements_file, 'w', encoding='utf-8') as f:
            f.write(f"# TEST MODE: Enhanced Modern Requirements Document\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode**: TEST\n")
            f.write(f"**Source**: Enhanced analysis of Java/JSP application\n")
            f.write(f"**Architecture Layers**: {len(self.architecture_report.get('layers', {}))}\n")
            f.write(f"**Files Analyzed**: {len(self.enhanced_metadata)}\n")
            f.write(f"**Requirements Documents**: {len(self.enhanced_requirements)}\n\n")
            f.write("---\n\n")
            f.write(modern_requirements)
        
        logger.info(f"TEST MODE: Enhanced modern requirements document saved to: {self.modern_requirements_file}")

async def main():
    """Test version of main function"""
    logger = setup_logging(level=logging.INFO)
    logger.info("TEST MODE: Starting enhanced modernization requirements generation")
    
    try:
        processor = EnhancedModernRequirementsProcessorTest()
        await processor.process_enhanced_modernization_test()
        logger.info("TEST MODE: Enhanced modernization requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"TEST MODE: Error during enhanced modernization requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())