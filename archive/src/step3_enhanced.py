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

logger = logging.getLogger('java_analysis.step3_enhanced')

class EnhancedModernRequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
        self.requirements_dir = self.output_dir / "requirements_enhanced"
        self.modern_requirements_file = self.output_dir / "enhanced_modern_requirements.md"
        self.cloud_architecture_file = self.output_dir / "cloud_architecture_blueprints.json"
        self.microservices_file = self.output_dir / "microservices_design.md"
        self.tech_stack_file = self.output_dir / "technology_stack.json"
        
        # Enhanced metadata files
        self.enhanced_metadata_file = self.output_dir / "enhanced_metadata.json"
        self.architecture_report_file = self.output_dir / "enhanced_architecture_report.json"
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Enhanced rate limiting
        rate_config = RateLimitConfig(
            requests_per_minute=12,
            requests_per_hour=600,
            delay_between_requests=6.0,
            exponential_backoff_base=2.0,
            max_retries=5
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
                logger.warning(f"Enhanced metadata file not found: {self.enhanced_metadata_file}")
                return {}
            
            with open(self.enhanced_metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            logger.info(f"Loaded enhanced metadata with {len(metadata)} entries")
            return metadata
            
        except Exception as e:
            logger.error(f"Error loading enhanced metadata: {e}")
            return {}

    def load_architecture_report(self) -> Dict[str, Any]:
        """Load architecture report from Step1_Enhanced"""
        try:
            if not self.architecture_report_file.exists():
                logger.warning(f"Architecture report file not found: {self.architecture_report_file}")
                return {}
            
            with open(self.architecture_report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            logger.info(f"Loaded architecture report with {len(report.get('layers', {}))} layers")
            return report
            
        except Exception as e:
            logger.error(f"Error loading architecture report: {e}")
            return {}

    def load_enhanced_requirements(self) -> Dict[str, Any]:
        """Load enhanced requirements from Step2_Enhanced"""
        enhanced_requirements = {}
        
        if not self.requirements_dir.exists():
            logger.warning(f"Enhanced requirements directory not found: {self.requirements_dir}")
            return enhanced_requirements
        
        # Recursively find all markdown files
        for md_file in self.requirements_dir.rglob("*.md"):
            if md_file.name.startswith("step2_enhanced_index"):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract the relative path for organization
                relative_path = md_file.relative_to(self.requirements_dir)
                layer = relative_path.parts[0] if len(relative_path.parts) > 1 else "unknown"
                component = relative_path.parts[1] if len(relative_path.parts) > 2 else "unknown"
                
                enhanced_requirements[str(md_file)] = {
                    'content': content,
                    'layer': layer,
                    'component': component,
                    'file_path': str(md_file)
                }
                
            except Exception as e:
                logger.warning(f"Error reading enhanced requirements file {md_file}: {e}")
        
        logger.info(f"Loaded {len(enhanced_requirements)} enhanced requirements files")
        return enhanced_requirements

    async def generate_cloud_architecture_blueprint(self) -> Dict[str, Any]:
        """Generate cloud architecture blueprint based on enhanced analysis"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare architecture context
        architecture_context = {
            'layers': self.architecture_report.get('layers', {}),
            'components': [],
            'technologies': set()
        }
        
        # Extract components and technologies
        for layer_name, layer_info in architecture_context['layers'].items():
            components = layer_info.get('components', [])
            technologies = layer_info.get('technologies', [])
            
            architecture_context['components'].extend(components)
            architecture_context['technologies'].update(technologies)
        
        architecture_context['technologies'] = list(architecture_context['technologies'])
        
        prompt = f"""Based on the following Java/JSP application architecture analysis, design a comprehensive cloud-native architecture blueprint:

Architecture Analysis:
{json.dumps(architecture_context, indent=2)}

Create a detailed cloud architecture blueprint that includes:

1. **Microservices Design**:
   - Break down the existing layers into microservices
   - Define service boundaries and responsibilities
   - Identify shared services and utilities

2. **Container Strategy**:
   - Docker containerization approach
   - Kubernetes deployment strategy
   - Service mesh considerations

3. **Cloud Infrastructure**:
   - AWS/Azure/GCP service recommendations
   - Serverless opportunities
   - Database migration strategy

4. **API Gateway and Communication**:
   - API Gateway configuration
   - Service-to-service communication patterns
   - Event-driven architecture opportunities

5. **Data Strategy**:
   - Database per service pattern
   - Data consistency patterns
   - Caching strategy

6. **Security Architecture**:
   - Identity and access management
   - Security between services
   - Compliance considerations

7. **Monitoring and Observability**:
   - Logging strategy
   - Metrics and monitoring
   - Distributed tracing

8. **DevOps and CI/CD**:
   - Pipeline design
   - Infrastructure as code
   - Testing strategy

Please provide a structured JSON response with these sections.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a cloud architecture expert specializing in modernizing legacy applications. Provide comprehensive, actionable cloud architecture blueprints."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            self.rate_limiter.record_request()
            
            # Try to parse as JSON
            try:
                blueprint = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("AI response was not valid JSON, creating structured response")
                blueprint = {
                    "microservices_design": {"raw_response": response},
                    "container_strategy": {"raw_response": response},
                    "cloud_infrastructure": {"raw_response": response},
                    "api_gateway": {"raw_response": response},
                    "data_strategy": {"raw_response": response},
                    "security_architecture": {"raw_response": response},
                    "monitoring": {"raw_response": response},
                    "devops": {"raw_response": response}
                }
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error generating cloud architecture blueprint: {e}")
            return {"error": str(e)}

    async def generate_microservices_design(self, cloud_blueprint: Dict[str, Any]) -> str:
        """Generate detailed microservices design document"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare microservices context
        microservices_context = {
            'existing_layers': list(self.architecture_report.get('layers', {}).keys()),
            'components': [],
            'cloud_blueprint': cloud_blueprint.get('microservices_design', {}),
            'sample_requirements': []
        }
        
        # Get sample requirements from each layer
        for req_file, req_data in list(self.enhanced_requirements.items())[:5]:  # Limit to 5 samples
            microservices_context['sample_requirements'].append({
                'layer': req_data['layer'],
                'component': req_data['component'],
                'content_preview': req_data['content'][:300] + "..."
            })
        
        prompt = f"""Based on the following architecture analysis and cloud blueprint, create a comprehensive microservices design document:

Context:
{json.dumps(microservices_context, indent=2)}

Create a detailed microservices design document that includes:

1. **Service Decomposition Strategy**
2. **Individual Service Specifications**
3. **Data Management Strategy**
4. **Inter-Service Communication**
5. **Service Discovery and Registry**
6. **API Contracts and Documentation**
7. **Distributed Transaction Management**
8. **Error Handling and Resilience**
9. **Security and Authorization**
10. **Monitoring and Health Checks**

Format the response as a comprehensive markdown document with proper sections and subsections.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a microservices architecture expert. Create detailed, practical microservices design documents with specific implementation guidance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            self.rate_limiter.record_request()
            return response
            
        except Exception as e:
            logger.error(f"Error generating microservices design: {e}")
            return f"Error generating microservices design: {str(e)}"

    async def generate_technology_stack_recommendations(self, cloud_blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technology stack recommendations"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare technology context
        current_technologies = set()
        for layer_info in self.architecture_report.get('layers', {}).values():
            current_technologies.update(layer_info.get('technologies', []))
        
        tech_context = {
            'current_technologies': list(current_technologies),
            'cloud_blueprint': cloud_blueprint,
            'architecture_layers': list(self.architecture_report.get('layers', {}).keys())
        }
        
        prompt = f"""Based on the following current technology stack and cloud architecture blueprint, provide comprehensive technology stack recommendations for modernization:

Current Context:
{json.dumps(tech_context, indent=2)}

Provide technology recommendations organized by:

1. **Frontend Technologies**:
   - UI Framework (React, Vue, Angular)
   - State Management
   - Build Tools
   - Testing Frameworks

2. **Backend Technologies**:
   - Runtime Environment (Node.js, Python, Java Spring Boot)
   - Web Frameworks
   - Authentication/Authorization
   - Caching Solutions

3. **Database Technologies**:
   - Primary Database Options
   - Caching Layer
   - Search Solutions
   - Data Pipeline Tools

4. **Cloud Services**:
   - Compute Services
   - Storage Solutions
   - Messaging Services
   - Monitoring Tools

5. **DevOps Tools**:
   - CI/CD Pipeline
   - Infrastructure as Code
   - Monitoring and Logging
   - Security Tools

6. **Migration Strategy**:
   - Phase-wise migration plan
   - Risk mitigation strategies
   - Testing approach

Please provide a structured JSON response with detailed explanations for each recommendation.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a technology strategist specializing in application modernization. Provide practical, well-reasoned technology recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            self.rate_limiter.record_request()
            
            # Try to parse as JSON
            try:
                tech_stack = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("AI response was not valid JSON, creating structured response")
                tech_stack = {
                    "frontend_technologies": {"raw_response": response},
                    "backend_technologies": {"raw_response": response},
                    "database_technologies": {"raw_response": response},
                    "cloud_services": {"raw_response": response},
                    "devops_tools": {"raw_response": response},
                    "migration_strategy": {"raw_response": response}
                }
            
            return tech_stack
            
        except Exception as e:
            logger.error(f"Error generating technology stack recommendations: {e}")
            return {"error": str(e)}

    async def generate_enhanced_modern_requirements(self, cloud_blueprint: Dict[str, Any], 
                                                   microservices_design: str, 
                                                   tech_stack: Dict[str, Any]) -> str:
        """Generate comprehensive modern requirements document"""
        await self.rate_limiter.wait_if_needed()
        
        # Prepare comprehensive context
        context = {
            'architecture_summary': {
                'total_layers': len(self.architecture_report.get('layers', {})),
                'total_files': len(self.enhanced_metadata),
                'layers': list(self.architecture_report.get('layers', {}).keys())
            },
            'cloud_blueprint_summary': {
                'microservices_count': len(cloud_blueprint.get('microservices_design', {}).get('services', [])),
                'key_technologies': list(tech_stack.get('backend_technologies', {}).keys())[:5]
            },
            'sample_requirements': []
        }
        
        # Get representative samples from each layer
        layer_samples = {}
        for req_file, req_data in self.enhanced_requirements.items():
            layer = req_data['layer']
            if layer not in layer_samples:
                layer_samples[layer] = []
            if len(layer_samples[layer]) < 2:  # Max 2 samples per layer
                layer_samples[layer].append({
                    'component': req_data['component'],
                    'content_preview': req_data['content'][:400] + "..."
                })
        
        context['sample_requirements'] = layer_samples
        
        prompt = f"""Based on the comprehensive analysis of this Java/JSP application, create a modern requirements document for cloud migration:

Analysis Context:
{json.dumps(context, indent=2)}

Create a comprehensive modern requirements document that includes:

1. **Executive Summary**
   - Current state assessment
   - Modernization goals and benefits
   - High-level migration strategy

2. **Architecture Modernization**
   - Current vs. target architecture
   - Microservices decomposition
   - Cloud-native patterns to adopt

3. **Technology Migration Plan**
   - Current technology assessment
   - Recommended technology stack
   - Migration path and timeline

4. **Functional Requirements**
   - Core business functionality preservation
   - New cloud-native capabilities
   - User experience improvements

5. **Non-Functional Requirements**
   - Performance and scalability
   - Security and compliance
   - Reliability and availability

6. **Data Migration Strategy**
   - Data architecture modernization
   - Migration approach and tools
   - Data validation and testing

7. **Security and Compliance**
   - Modern security patterns
   - Compliance requirements
   - Identity and access management

8. **Development and Operations**
   - Modern development practices
   - CI/CD pipeline requirements
   - Monitoring and observability

9. **Migration Roadmap**
   - Phase-wise migration plan
   - Risk mitigation strategies
   - Success criteria and KPIs

10. **Cost Analysis and ROI**
    - Migration costs estimation
    - Operational cost comparison
    - Expected return on investment

Format as a comprehensive markdown document with proper sections and technical details.
"""
        
        try:
            response = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a senior solution architect specializing in enterprise application modernization. Create comprehensive, executive-ready modernization requirements documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            self.rate_limiter.record_request()
            return response
            
        except Exception as e:
            logger.error(f"Error generating enhanced modern requirements: {e}")
            return f"Error generating enhanced modern requirements: {str(e)}"

    async def process_enhanced_modernization(self) -> None:
        """Process enhanced modernization requirements"""
        logger.info("Starting enhanced modernization process...")
        
        # Generate cloud architecture blueprint
        logger.info("Generating cloud architecture blueprint...")
        cloud_blueprint = await self.generate_cloud_architecture_blueprint()
        
        # Save cloud blueprint
        with open(self.cloud_architecture_file, 'w', encoding='utf-8') as f:
            json.dump(cloud_blueprint, f, indent=2)
        logger.info(f"Cloud architecture blueprint saved to: {self.cloud_architecture_file}")
        
        # Generate microservices design
        logger.info("Generating microservices design...")
        microservices_design = await self.generate_microservices_design(cloud_blueprint)
        
        # Save microservices design
        with open(self.microservices_file, 'w', encoding='utf-8') as f:
            f.write(f"# Microservices Design Document\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(microservices_design)
        logger.info(f"Microservices design saved to: {self.microservices_file}")
        
        # Generate technology stack recommendations
        logger.info("Generating technology stack recommendations...")
        tech_stack = await self.generate_technology_stack_recommendations(cloud_blueprint)
        
        # Save technology stack
        with open(self.tech_stack_file, 'w', encoding='utf-8') as f:
            json.dump(tech_stack, f, indent=2)
        logger.info(f"Technology stack recommendations saved to: {self.tech_stack_file}")
        
        # Generate comprehensive modern requirements
        logger.info("Generating enhanced modern requirements document...")
        modern_requirements = await self.generate_enhanced_modern_requirements(
            cloud_blueprint, microservices_design, tech_stack
        )
        
        # Save modern requirements
        with open(self.modern_requirements_file, 'w', encoding='utf-8') as f:
            f.write(f"# Enhanced Modern Requirements Document\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Source**: Enhanced analysis of Java/JSP application\n")
            f.write(f"**Architecture Layers**: {len(self.architecture_report.get('layers', {}))}\n")
            f.write(f"**Files Analyzed**: {len(self.enhanced_metadata)}\n")
            f.write(f"**Requirements Documents**: {len(self.enhanced_requirements)}\n\n")
            f.write("---\n\n")
            f.write(modern_requirements)
        
        logger.info(f"Enhanced modern requirements document saved to: {self.modern_requirements_file}")

async def main():
    """Main function to process enhanced modernization requirements"""
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting enhanced modernization requirements generation")
    
    try:
        processor = EnhancedModernRequirementsProcessor()
        await processor.process_enhanced_modernization()
        logger.info("Enhanced modernization requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during enhanced modernization requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())