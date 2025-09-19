#!/usr/bin/env python3
"""
Quick Requirements Generator
Generate comprehensive requirements based on existing analysis results
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

import re
import aiohttp
from typing import Dict, Any, List

class QuickRequirementsOllama:
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
    
    async def generate_requirements(self, context: str, requirement_type: str) -> Dict[str, Any]:
        """Generate requirements from context with optimized settings"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": context,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 2048,
                        "top_k": 40,
                        "top_p": 0.9
                    }
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=180)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'content': data.get('response', ''),
                            'requirement_type': requirement_type,
                            'processing_time': time.time() - start_time,
                            'success': True
                        }
                    else:
                        return {'error': f'HTTP {response.status}', 'success': False}
        except Exception as e:
            return {'error': str(e), 'success': False}

class QuickRequirementsGenerator:
    def __init__(self):
        self.ollama = QuickRequirementsOllama()
        self.output_dir = Path("output")
        
    async def generate_quick_requirements(self) -> Dict[str, Any]:
        """Generate requirements based on existing analysis"""
        start_time = time.time()
        
        # Check Ollama availability
        if not await self.ollama.health_check():
            raise RuntimeError("Ollama not available")
        
        logger.info("✅ Ollama ready for requirements generation")
        
        # Load existing analysis results
        existing_analysis = self._load_existing_analysis()
        
        if not existing_analysis:
            raise RuntimeError("No existing analysis found - run targeted analysis first")
        
        logger.info(f"📊 Loaded existing analysis: {len(existing_analysis.get('individual_analyses', []))} detailed analyses")
        
        # Generate requirements based on existing analysis
        requirements = {}
        
        # 1. Executive Summary
        logger.info("📋 Generating Executive Summary...")
        requirements['executive_summary'] = await self._generate_executive_summary(existing_analysis)
        
        # 2. Functional Requirements
        logger.info("⚙️ Generating Functional Requirements...")
        requirements['functional_requirements'] = await self._generate_functional_requirements(existing_analysis)
        
        # 3. Technical Requirements
        logger.info("🔧 Generating Technical Requirements...")
        requirements['technical_requirements'] = await self._generate_technical_requirements(existing_analysis)
        
        # 4. Security Requirements
        logger.info("🛡️ Generating Security Requirements...")
        requirements['security_requirements'] = await self._generate_security_requirements(existing_analysis)
        
        # 5. User Experience Requirements
        logger.info("👥 Generating User Experience Requirements...")
        requirements['ux_requirements'] = await self._generate_ux_requirements(existing_analysis)
        
        # 6. Integration Requirements
        logger.info("🔗 Generating Integration Requirements...")
        requirements['integration_requirements'] = await self._generate_integration_requirements(existing_analysis)
        
        # Compile final document
        final_doc = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'source_analysis': 'A1 Telekom Austria CuCo Targeted Analysis',
                'ai_model': 'Qwen3-Coder-30B',
                'processing_time': time.time() - start_time,
                'source_files_analyzed': len(existing_analysis.get('individual_analyses', []))
            },
            'requirements': requirements,
            'success': True
        }
        
        # Save results
        await self._save_quick_requirements(final_doc)
        
        return final_doc

    def _load_existing_analysis(self) -> Dict[str, Any]:
        """Load most recent targeted analysis"""
        try:
            # Look for the most recent targeted analysis
            analysis_files = list(self.output_dir.glob("targeted_java_analysis_*.json"))
            if not analysis_files:
                return {}
            
            # Get the most recent file
            latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Failed to load existing analysis: {e}")
            return {}

    async def _generate_executive_summary(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary from existing analysis"""
        
        context = f"""
# A1 Telekom Austria CuCo - Executive Requirements Summary

## PROJECT OVERVIEW
Based on comprehensive analysis of the A1 Telekom Austria Customer Care (CuCo) enterprise Java application.

## ANALYSIS SCOPE
- **Java Files Analyzed**: {analysis_data.get('java_files_found', 0)}
- **Detailed AI Analyses**: {analysis_data.get('files_analyzed', 0)}
- **Modules Identified**: {', '.join(analysis_data.get('modules', []))}
- **Technology Stack**: GWT, ExtJS, Spring Framework, iBATIS, Servlet API

## EXISTING ANALYSIS INSIGHTS
From detailed code analysis, the system demonstrates:
- Enterprise-level customer care operations
- Multi-module architecture with clear separation of concerns
- Legacy technology stack requiring modernization
- Complex business logic for telecom operations

## KEY COMPONENTS ANALYZED
"""
        
        # Add sample analysis insights
        for i, analysis in enumerate(analysis_data.get('individual_analyses', [])[:3]):
            file_name = Path(analysis['file']).name
            file_info = analysis.get('file_info', {})
            business_context = file_info.get('business_context', file_info.get('module_name', 'General'))
            context += f"- {file_name}: {business_context}\n"
        
        context += """
## EXECUTIVE SUMMARY REQUEST
Generate a comprehensive executive summary for C-level stakeholders covering:

### 1. BUSINESS VALUE PROPOSITION
- System's role in A1 Telekom Austria operations
- Customer care capabilities and business impact
- Operational efficiency and competitive advantages

### 2. STRATEGIC REQUIREMENTS OVERVIEW
- Critical business capabilities that must be maintained
- Key modernization priorities
- Integration requirements with enterprise systems

### 3. INVESTMENT REQUIREMENTS
- Technology modernization investment
- Infrastructure and operational costs
- Training and change management needs

### 4. RISK ASSESSMENT
- Technology obsolescence risks
- Business continuity considerations
- Security and compliance requirements

### 5. SUCCESS METRICS
- Key performance indicators for the modernized system
- Business outcome measurements
- User satisfaction and operational efficiency metrics

### 6. IMPLEMENTATION STRATEGY
- Phased modernization approach
- Priority areas for immediate attention
- Long-term strategic roadmap

Provide a professional, business-focused executive summary suitable for investment decisions and strategic planning.
"""
        
        return await self.ollama.generate_requirements(context, "executive_summary")

    async def _generate_functional_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate functional requirements from analysis"""
        
        context = f"""
# A1 Telekom Austria CuCo - Functional Requirements

## SYSTEM ANALYSIS CONTEXT
Based on detailed analysis of {analysis_data.get('files_analyzed', 0)} critical Java components from the enterprise customer care system.

## IDENTIFIED SYSTEM COMPONENTS
"""
        
        # Add component insights from analysis
        for analysis in analysis_data.get('individual_analyses', []):
            file_info = analysis.get('file_info', {})
            file_path = file_info.get('file_path', 'Unknown')
            context += f"""
### {Path(file_path).name}
- **Module**: {file_info.get('module_name', 'Unknown')}
- **Package**: {file_info.get('package_name', 'Unknown')}
- **Classes**: {', '.join(file_info.get('class_names', []))}
- **Key Methods**: {', '.join(file_info.get('methods', [])[:5])}
"""
        
        context += f"""
## TECHNOLOGY STACK ANALYSIS
Current implementation uses: GWT frontend, ExtJS/GXT UI, Spring Framework, iBATIS data access, Java Servlets.

## FUNCTIONAL REQUIREMENTS GENERATION REQUEST
Generate comprehensive functional requirements covering:

### 1. USER MANAGEMENT FUNCTIONS
- User authentication and authorization
- Role-based access control
- User profile management
- Session management

### 2. CUSTOMER CARE OPERATIONS  
- Customer information management
- Service request processing
- Issue tracking and resolution
- Customer communication

### 3. ADMINISTRATIVE FUNCTIONS
- System configuration management
- User and role administration
- Reporting and analytics
- Data export and import

### 4. DATA MANAGEMENT FUNCTIONS
- Data validation and integrity
- Search and filtering capabilities
- Data archiving and retention
- Backup and recovery

### 5. INTEGRATION FUNCTIONS
- External system integration
- API and web service capabilities
- Real-time data synchronization
- Batch processing operations

### 6. WORKFLOW MANAGEMENT
- Business process automation
- Task assignment and tracking
- Approval workflows
- Notification and alerting

For each functional area, provide:
- Detailed functional specifications
- User acceptance criteria
- Business rules and validations
- Priority and dependencies

Format as professional functional requirements suitable for development teams.
"""
        
        return await self.ollama.generate_requirements(context, "functional_requirements")

    async def _generate_technical_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Technical Requirements

## CURRENT ARCHITECTURE ANALYSIS
Based on analysis of {analysis_data.get('java_files_found', 0)} Java files across {len(analysis_data.get('modules', []))} modules.

## TECHNOLOGY STACK ASSESSMENT
Current implementation:
- **Frontend**: GWT (Google Web Toolkit) with ExtJS/GXT components
- **Backend**: Java Enterprise with Spring Framework
- **Data Access**: iBATIS SQL mapping
- **Web Layer**: Java Servlets and filters
- **Architecture**: Multi-module layered architecture

## CODE ANALYSIS INSIGHTS
From detailed component analysis:
"""
        
        # Add technical insights from analyses
        for analysis in analysis_data.get('individual_analyses', [])[:5]:
            analysis_result = analysis.get('analysis', {})
            if analysis_result.get('success', False):
                analysis_content = analysis_result.get('analysis_content', analysis_result.get('content', ''))[:200]
                if analysis_content:
                    context += f"- {Path(analysis['file']).name}: {analysis_content}...\n"
        
        context += """
## TECHNICAL REQUIREMENTS GENERATION REQUEST
Generate comprehensive technical requirements covering:

### 1. ARCHITECTURE REQUIREMENTS
- Target architecture pattern (microservices, modular monolith, etc.)
- Component interaction patterns
- Scalability and performance architecture
- Data architecture and management

### 2. TECHNOLOGY STACK REQUIREMENTS
- Modern frontend framework selection (React, Angular, Vue.js)
- Backend framework and runtime requirements
- Database technology and requirements
- Integration middleware and messaging

### 3. INFRASTRUCTURE REQUIREMENTS
- Cloud infrastructure requirements
- Container orchestration needs
- Load balancing and scaling requirements
- Monitoring and logging infrastructure

### 4. DEVELOPMENT REQUIREMENTS
- Development environment specifications
- Build and deployment pipeline requirements
- Testing framework and automation
- Code quality and security scanning

### 5. SECURITY TECHNICAL REQUIREMENTS
- Authentication and authorization implementation
- Data encryption and protection
- Network security requirements
- Compliance and audit technical controls

### 6. INTEGRATION TECHNICAL REQUIREMENTS
- API design standards and specifications
- Message format and protocol requirements
- Real-time integration capabilities
- Legacy system integration patterns

### 7. PERFORMANCE REQUIREMENTS
- Response time and throughput specifications
- Resource utilization limits
- Caching and optimization requirements
- Database performance requirements

### 8. OPERATIONAL REQUIREMENTS
- Deployment and configuration management
- Monitoring and alerting specifications
- Backup and disaster recovery technical requirements
- Capacity planning and scaling requirements

Provide specific, implementable technical requirements with clear acceptance criteria.
"""
        
        return await self.ollama.generate_requirements(context, "technical_requirements")

    async def _generate_security_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Security Requirements

## SECURITY CONTEXT
Enterprise customer care system for A1 Telekom Austria handling sensitive customer data and telecom operations.
System serves multiple user roles including customer service agents, administrators, and system operators.

## CURRENT SECURITY ANALYSIS
Based on analysis of enterprise Java application components:
- Servlet-based web security patterns identified
- Role-based access control mechanisms in use
- Data validation and input sanitization patterns
- Session management and authentication components

## CODE SECURITY INSIGHTS
"""
        
        # Add security-relevant insights from component analyses
        security_relevant_files = []
        for analysis in analysis_data.get('individual_analyses', []):
            file_info = analysis.get('file_info', {})
            file_path = file_info.get('file_path', '')
            package_name = file_info.get('package_name', '')
            if 'servlet' in file_path.lower() or 'security' in package_name.lower():
                security_relevant_files.append(f"- {Path(file_path).name}: {file_info.get('module_name', 'Security Component')}")
        
        if security_relevant_files:
            context += '\n'.join(security_relevant_files[:5])
        else:
            context += "- Multiple servlet-based security components identified\n- Role-based access control patterns found"
        
        context += """
## SECURITY REQUIREMENTS GENERATION REQUEST
Generate comprehensive security requirements for the telecom customer care system:

### 1. AUTHENTICATION REQUIREMENTS
- Multi-factor authentication implementation
- Single sign-on (SSO) integration
- Password policy and management
- Session security and timeout management

### 2. AUTHORIZATION REQUIREMENTS
- Role-based access control (RBAC) specifications
- Fine-grained permission management
- Administrative access controls
- Resource-level authorization

### 3. DATA PROTECTION REQUIREMENTS
- Customer data privacy protection (GDPR compliance)
- Data encryption at rest and in transit
- Data masking and anonymization
- Personal information handling

### 4. APPLICATION SECURITY REQUIREMENTS
- Input validation and sanitization
- SQL injection prevention
- Cross-site scripting (XSS) protection
- Cross-site request forgery (CSRF) protection

### 5. NETWORK SECURITY REQUIREMENTS
- Secure communication protocols (HTTPS/TLS)
- Network access controls and firewalls
- VPN and secure remote access
- API security and rate limiting

### 6. AUDIT AND COMPLIANCE REQUIREMENTS
- Comprehensive audit logging
- Regulatory compliance (telecom regulations)
- Data retention and deletion policies
- Compliance reporting and monitoring

### 7. INCIDENT RESPONSE REQUIREMENTS
- Security incident detection and monitoring
- Incident response procedures
- Vulnerability management
- Security awareness and training

### 8. OPERATIONAL SECURITY REQUIREMENTS
- Secure deployment and configuration
- Security monitoring and alerting
- Regular security assessments
- Disaster recovery security considerations

Provide specific, implementable security requirements with clear compliance mappings and risk mitigation strategies.
"""
        
        return await self.ollama.generate_requirements(context, "security_requirements")

    async def _generate_ux_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate user experience requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - User Experience Requirements

## USER CONTEXT ANALYSIS
Customer care system serving A1 Telekom Austria with current GWT/ExtJS frontend requiring modernization.

## CURRENT UI TECHNOLOGY ASSESSMENT
Based on code analysis:
- Legacy GWT (Google Web Toolkit) frontend
- ExtJS/GXT components for rich UI elements
- Servlet-based backend with traditional request/response patterns
- Multi-module architecture with role-based interfaces

## USER ROLES IDENTIFIED
From system analysis, key user types include:
- Customer Service Representatives
- System Administrators
- Supervisors and Managers
- Technical Support Staff

## UX MODERNIZATION REQUIREMENTS REQUEST
Generate comprehensive user experience requirements:

### 1. MODERN USER INTERFACE REQUIREMENTS
- Contemporary web interface design
- Responsive design for multiple device types
- Accessibility compliance (WCAG 2.1 AA)
- Cross-browser compatibility

### 2. USER INTERACTION REQUIREMENTS
- Intuitive navigation and information architecture
- Efficient task-oriented workflows
- Context-sensitive help and guidance
- Keyboard shortcuts and power-user features

### 3. PERFORMANCE UX REQUIREMENTS
- Fast page load times (< 3 seconds)
- Responsive user interactions
- Progressive loading for large datasets
- Offline capability where appropriate

### 4. PERSONALIZATION REQUIREMENTS
- Customizable dashboards and workspaces
- User preference management
- Role-based interface adaptation
- Personal productivity enhancements

### 5. DATA PRESENTATION REQUIREMENTS
- Clear, scannable data displays
- Effective use of visualizations and charts
- Advanced search and filtering capabilities
- Export and sharing functionality

### 6. WORKFLOW UX REQUIREMENTS
- Streamlined customer service workflows
- Multi-tasking and context switching support
- Progress indicators for complex operations
- Error prevention and recovery guidance

### 7. NOTIFICATION AND COMMUNICATION UX
- Real-time notifications and alerts
- In-app messaging and collaboration
- Status updates and progress tracking
- Customer communication integration

### 8. MOBILE AND ACCESSIBILITY REQUIREMENTS
- Mobile-optimized interfaces
- Touch-friendly interactions
- Screen reader compatibility
- High contrast and font scaling support

### 9. TRAINING AND ADOPTION REQUIREMENTS
- Onboarding and tutorial systems
- Contextual help and documentation
- Training mode for new users
- Change management support features

Provide specific, measurable UX requirements with clear user satisfaction and productivity metrics.
"""
        
        return await self.ollama.generate_requirements(context, "ux_requirements")

    async def _generate_integration_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integration requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Integration Requirements

## INTEGRATION CONTEXT
Enterprise customer care system requiring integration with A1 Telekom Austria's broader IT ecosystem and external partners.

## CURRENT INTEGRATION ANALYSIS
Based on analysis of {analysis_data.get('files_analyzed', 0)} system components:
- Servlet-based web services for external integration
- Database integration through iBATIS data access layer
- Multi-module architecture supporting service integration
- Legacy system integration patterns identified

## ENTERPRISE INTEGRATION REQUIREMENTS REQUEST
Generate comprehensive integration requirements:

### 1. INTERNAL SYSTEM INTEGRATIONS
- Customer Master Data Management (MDM) integration
- Billing and invoicing system integration
- Network operations and service provisioning systems
- CRM and sales system integration
- HR and workforce management system integration

### 2. EXTERNAL PARTNER INTEGRATIONS
- Third-party service provider APIs
- Wholesale partner system integration
- Regulatory reporting system interfaces
- Credit checking and verification services
- Payment processing and gateway integration

### 3. API AND WEB SERVICES REQUIREMENTS
- RESTful API design and implementation standards
- GraphQL API capabilities for flexible data querying
- SOAP web services for legacy system compatibility
- API versioning and lifecycle management
- API documentation and developer portal

### 4. DATA INTEGRATION REQUIREMENTS
- Real-time data synchronization capabilities
- Batch data processing and ETL operations
- Data transformation and mapping requirements
- Data quality validation and cleansing
- Master data management and governance

### 5. MESSAGE QUEUING AND EVENTS
- Asynchronous message processing capabilities
- Event-driven architecture implementation
- Message queue reliability and ordering
- Event sourcing and audit trail requirements
- Dead letter queue and error handling

### 6. SECURITY AND GOVERNANCE
- API security and authentication requirements
- Data privacy and protection in integrations
- Integration monitoring and logging
- Service level agreement (SLA) management
- Change management for integration endpoints

### 7. PERFORMANCE AND SCALABILITY
- High-throughput integration capabilities
- Load balancing and failover requirements
- Integration caching and optimization
- Bandwidth and latency optimization
- Scalable integration architecture

### 8. MONITORING AND MANAGEMENT
- Integration health monitoring and alerting
- Performance metrics and SLA tracking
- Integration testing and validation
- Error handling and retry mechanisms
- Business process monitoring

### 9. COMPLIANCE AND REGULATORY
- Regulatory compliance in data exchange
- Audit trail and logging requirements
- Data retention and archival policies
- Cross-border data transfer compliance
- Industry standard protocol adherence

Provide detailed, implementable integration requirements with clear technical specifications and governance policies.
"""
        
        return await self.ollama.generate_requirements(context, "integration_requirements")

    async def _save_quick_requirements(self, requirements_doc: Dict[str, Any]):
        """Save quick requirements documentation"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save complete requirements JSON
            with open(f"output/cuco_quick_requirements_{timestamp}.json", 'w') as f:
                json.dump(requirements_doc, f, indent=2, default=str)
            
            # Save consolidated markdown report
            with open(f"output/cuco_complete_requirements_{timestamp}.md", 'w') as f:
                f.write("# A1 Telekom Austria CuCo - Complete Enterprise Requirements\n\n")
                f.write(f"**Generated**: {requirements_doc['metadata']['generated_at']}\n")
                f.write(f"**Source Analysis**: {requirements_doc['metadata']['source_files_analyzed']} Java files analyzed\n")
                f.write(f"**AI Model**: {requirements_doc['metadata']['ai_model']}\n")
                f.write(f"**Processing Time**: {requirements_doc['metadata']['processing_time']:.2f} seconds\n\n")
                
                # Add all requirement sections
                for req_type, req_data in requirements_doc['requirements'].items():
                    if req_data.get('success', False):
                        f.write(f"## {req_type.replace('_', ' ').title()}\n\n")
                        f.write(req_data.get('content', 'Requirements generation failed'))
                        f.write("\n\n" + "="*80 + "\n\n")
            
            # Save individual requirement documents  
            for req_type, req_data in requirements_doc['requirements'].items():
                if req_data.get('success', False):
                    with open(f"output/cuco_{req_type}_{timestamp}.md", 'w') as f:
                        f.write(f"# A1 Telekom Austria CuCo - {req_type.replace('_', ' ').title()}\n\n")
                        f.write(f"Generated: {requirements_doc['metadata']['generated_at']}\n\n")
                        f.write(req_data.get('content', 'Requirements generation failed'))
            
            logger.info(f"📁 Quick requirements documentation saved:")
            logger.info(f"   • Complete JSON: output/cuco_quick_requirements_{timestamp}.json")
            logger.info(f"   • Consolidated report: output/cuco_complete_requirements_{timestamp}.md")
            logger.info(f"   • Individual sections: output/cuco_*_{timestamp}.md")
            
        except Exception as e:
            logger.error(f"Failed to save requirements: {e}")

async def main():
    """Main execution function"""
    logger.info("🚀 A1 Telekom Austria CuCo - Quick Requirements Generation")
    logger.info("=" * 70)
    logger.info("📋 Generating comprehensive requirements from existing analysis")
    logger.info("🧠 Using Qwen3-Coder-30B for AI-powered requirements extraction")
    logger.info("=" * 70)
    
    try:
        generator = QuickRequirementsGenerator()
        requirements_doc = await generator.generate_quick_requirements()
        
        # Display results summary
        logger.info("=" * 70)
        logger.info("🎉 QUICK REQUIREMENTS GENERATION COMPLETE")
        logger.info("=" * 70)
        
        metadata = requirements_doc['metadata']
        logger.info(f"📊 Processing time: {metadata['processing_time']:.2f} seconds")
        logger.info(f"🎯 Source files: {metadata['source_files_analyzed']} analyzed components")
        logger.info(f"🧠 AI Model: {metadata['ai_model']}")
        
        requirements = requirements_doc['requirements']
        logger.info(f"\n📋 Requirements Generated:")
        
        for req_type, req_data in requirements.items():
            status = "✅" if req_data.get('success', False) else "❌"
            proc_time = req_data.get('processing_time', 0)
            logger.info(f"   {status} {req_type.replace('_', ' ').title()} ({proc_time:.2f}s)")
        
        logger.info(f"\n📁 Complete requirements documentation available in output/ directory")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Quick requirements generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)