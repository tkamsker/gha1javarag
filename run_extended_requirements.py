#!/usr/bin/env python3
"""
Extended Requirements Generation Script
Focused on extracting and documenting enterprise requirements from Java codebase
"""

import asyncio
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import re
import aiohttp
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Set, Tuple

@dataclass
class RequirementComponent:
    component_id: str
    component_name: str
    component_type: str  # 'functional', 'non_functional', 'technical', 'business'
    description: str
    source_files: List[str]
    priority: str  # 'high', 'medium', 'low'
    business_value: str
    technical_complexity: str
    dependencies: List[str]

@dataclass
class BusinessProcess:
    process_name: str
    description: str
    actors: List[str]
    steps: List[str]
    supporting_components: List[str]
    business_rules: List[str]
    data_entities: List[str]

class RequirementsOllama:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        
    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    return response.status == 200
        except:
            return False
    
    async def extract_requirements(self, context: str, requirement_type: str) -> Dict[str, Any]:
        """Extract specific type of requirements from context"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": context,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 3072,
                        "num_ctx": 1024000,  # 1M context window
                        "top_k": 40,
                        "top_p": 0.9
                    }
                }
                
                start_time = time.time()
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=300)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'requirements_content': data.get('response', ''),
                            'requirement_type': requirement_type,
                            'tokens_used': len(context) // 3,
                            'processing_time': time.time() - start_time,
                            'success': True
                        }
                    else:
                        return {'error': f'HTTP {response.status}', 'success': False}
        except Exception as e:
            return {'error': str(e), 'success': False}

class ExtendedRequirementsGenerator:
    def __init__(self, java_root_path: str):
        self.java_root_path = Path(java_root_path)
        self.ollama = RequirementsOllama()
        self.business_processes = []
        self.requirement_components = []
        
        # Enhanced patterns for requirements extraction
        self.requirements_patterns = {
            'business_rules': re.compile(r'// Business Rule:|/\* Business Rule:|// BR:|/\* BR:', re.IGNORECASE),
            'validation': re.compile(r'validate|validation|check|verify|ensure', re.IGNORECASE),
            'permissions': re.compile(r'permission|authority|role|access|authorize|authenticate', re.IGNORECASE),
            'workflow': re.compile(r'workflow|process|step|stage|phase', re.IGNORECASE),
            'integration': re.compile(r'integrate|connect|sync|api|service|endpoint', re.IGNORECASE),
            'data_rules': re.compile(r'constraint|foreign key|unique|required|mandatory', re.IGNORECASE),
            'user_roles': re.compile(r'admin|user|customer|agent|operator|manager', re.IGNORECASE),
            'operations': re.compile(r'create|read|update|delete|save|load|export|import', re.IGNORECASE)
        }

    async def generate_extended_requirements(self) -> Dict[str, Any]:
        """Generate comprehensive requirements documentation"""
        start_time = time.time()
        
        # Check Ollama availability
        if not await self.ollama.health_check():
            raise RuntimeError("Ollama not available")
        
        logger.info("✅ Ollama ready for requirements extraction")
        
        # Phase 1: Code Analysis and Pattern Extraction
        logger.info("🔍 Phase 1: Extracting requirements patterns from code...")
        code_patterns = await self._extract_code_patterns()
        
        # Phase 2: Business Process Discovery
        logger.info("💼 Phase 2: Discovering business processes...")
        business_processes = await self._discover_business_processes(code_patterns)
        
        # Phase 3: Functional Requirements Generation
        logger.info("⚙️ Phase 3: Generating functional requirements...")
        functional_reqs = await self._generate_functional_requirements(business_processes, code_patterns)
        
        # Phase 4: Non-Functional Requirements
        logger.info("🎯 Phase 4: Extracting non-functional requirements...")
        non_functional_reqs = await self._generate_non_functional_requirements(code_patterns)
        
        # Phase 5: Technical Requirements
        logger.info("🔧 Phase 5: Documenting technical requirements...")
        technical_reqs = await self._generate_technical_requirements(code_patterns)
        
        # Phase 6: Compliance and Security Requirements
        logger.info("🛡️ Phase 6: Analyzing security and compliance requirements...")
        security_reqs = await self._generate_security_requirements(code_patterns)
        
        # Phase 7: Integration Requirements
        logger.info("🔗 Phase 7: Mapping integration requirements...")
        integration_reqs = await self._generate_integration_requirements(code_patterns)
        
        # Phase 8: User Experience Requirements
        logger.info("👥 Phase 8: Extracting user experience requirements...")
        ux_reqs = await self._generate_ux_requirements(code_patterns)
        
        # Compile comprehensive requirements document
        requirements_doc = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'source_system': 'A1 Telekom Austria CuCo',
                'analysis_scope': 'Complete Java Enterprise Application',
                'methodology': 'AI-Powered Code Analysis with Qwen3-Coder-30B',
                'processing_time': time.time() - start_time
            },
            'executive_summary': await self._generate_executive_summary(code_patterns),
            'business_context': {
                'discovered_processes': business_processes,
                'business_rules_count': len(code_patterns.get('business_rules', [])),
                'user_roles_identified': code_patterns.get('user_roles', []),
                'key_operations': code_patterns.get('operations', [])
            },
            'functional_requirements': functional_reqs,
            'non_functional_requirements': non_functional_reqs,
            'technical_requirements': technical_reqs,
            'security_requirements': security_reqs,
            'integration_requirements': integration_reqs,
            'user_experience_requirements': ux_reqs,
            'implementation_roadmap': await self._generate_implementation_roadmap(),
            'traceability_matrix': await self._generate_traceability_matrix(code_patterns)
        }
        
        # Save comprehensive requirements
        await self._save_requirements_documentation(requirements_doc)
        
        return requirements_doc

    async def _extract_code_patterns(self) -> Dict[str, Any]:
        """Extract patterns from codebase that indicate requirements"""
        patterns = {
            'business_rules': [],
            'validations': [],
            'permissions': [],
            'workflows': [],
            'integrations': [],
            'data_rules': [],
            'user_roles': set(),
            'operations': set(),
            'components': [],
            'services': [],
            'controllers': [],
            'entities': []
        }
        
        file_count = 0
        logger.info("📂 Scanning Java files for requirements patterns...")
        
        for file_path in self.java_root_path.rglob("*.java"):
            file_count += 1
            if file_count % 200 == 0:
                logger.info(f"   ... processed {file_count} files")
                
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Extract various patterns
                    self._extract_file_patterns(file_path, content, patterns)
                    
                except Exception as e:
                    logger.warning(f"Could not process {file_path}: {e}")
        
        # Convert sets to lists for JSON serialization
        patterns['user_roles'] = list(patterns['user_roles'])
        patterns['operations'] = list(patterns['operations'])
        
        logger.info(f"📊 Pattern extraction complete: {file_count} files processed")
        logger.info(f"   • Business rules: {len(patterns['business_rules'])}")
        logger.info(f"   • Validations: {len(patterns['validations'])}")
        logger.info(f"   • User roles: {len(patterns['user_roles'])}")
        logger.info(f"   • Operations: {len(patterns['operations'])}")
        
        return patterns

    def _extract_file_patterns(self, file_path: Path, content: str, patterns: Dict[str, Any]):
        """Extract requirements patterns from a single file"""
        
        # Extract business rules from comments
        business_rule_matches = self.requirements_patterns['business_rules'].findall(content)
        for match in business_rule_matches:
            patterns['business_rules'].append({
                'file': str(file_path),
                'context': match,
                'line_context': self._get_line_context(content, match)
            })
        
        # Extract validation patterns
        validation_matches = self.requirements_patterns['validation'].findall(content)
        for match in validation_matches:
            patterns['validations'].append({
                'file': str(file_path),
                'validation_type': match,
                'context': self._get_line_context(content, match)
            })
        
        # Extract permission/security patterns
        permission_matches = self.requirements_patterns['permissions'].findall(content)
        for match in permission_matches:
            patterns['permissions'].append({
                'file': str(file_path),
                'permission_type': match,
                'context': self._get_line_context(content, match)
            })
        
        # Extract workflow patterns
        workflow_matches = self.requirements_patterns['workflow'].findall(content)
        for match in workflow_matches:
            patterns['workflows'].append({
                'file': str(file_path),
                'workflow_element': match,
                'context': self._get_line_context(content, match)
            })
        
        # Extract integration patterns
        integration_matches = self.requirements_patterns['integration'].findall(content)
        for match in integration_matches:
            patterns['integrations'].append({
                'file': str(file_path),
                'integration_type': match,
                'context': self._get_line_context(content, match)
            })
        
        # Extract user roles
        user_role_matches = self.requirements_patterns['user_roles'].findall(content)
        patterns['user_roles'].update(match.lower() for match in user_role_matches)
        
        # Extract operations
        operation_matches = self.requirements_patterns['operations'].findall(content)
        patterns['operations'].update(match.lower() for match in operation_matches)
        
        # Classify file type and extract components
        file_name = file_path.name.lower()
        if 'service' in file_name:
            patterns['services'].append(str(file_path))
        elif 'controller' in file_name or 'servlet' in file_name:
            patterns['controllers'].append(str(file_path))
        elif 'entity' in file_name or 'model' in file_name or 'dto' in file_name:
            patterns['entities'].append(str(file_path))
        else:
            patterns['components'].append(str(file_path))

    def _get_line_context(self, content: str, match: str, context_lines: int = 2) -> str:
        """Get context lines around a match"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if match.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                return '\n'.join(lines[start:end])
        return match

    async def _discover_business_processes(self, code_patterns: Dict[str, Any]) -> List[BusinessProcess]:
        """Discover business processes from code patterns"""
        
        # Create context for business process discovery
        context = f"""
# A1 Telekom Austria CuCo - Business Process Discovery

Based on analysis of enterprise Java application code, discover business processes from these patterns:

## CODE ANALYSIS RESULTS
- Services found: {len(code_patterns.get('services', []))}
- Controllers/Servlets: {len(code_patterns.get('controllers', []))}
- User roles identified: {', '.join(code_patterns.get('user_roles', [])[:10])}
- Key operations: {', '.join(code_patterns.get('operations', [])[:15])}
- Workflow patterns: {len(code_patterns.get('workflows', []))}
- Permission patterns: {len(code_patterns.get('permissions', []))}

## SAMPLE WORKFLOW PATTERNS
"""
        
        for workflow in code_patterns.get('workflows', [])[:5]:
            context += f"File: {Path(workflow['file']).name}\n"
            context += f"Context: {workflow['context']}\n\n"
        
        context += """
## SAMPLE PERMISSION PATTERNS
"""
        
        for permission in code_patterns.get('permissions', [])[:5]:
            context += f"File: {Path(permission['file']).name}\n"
            context += f"Context: {permission['context']}\n\n"
        
        context += """
## BUSINESS PROCESS DISCOVERY REQUEST
Based on this code analysis, identify the key business processes in the A1 Telekom Austria Customer Care (CuCo) system.

For each business process, provide:
1. **Process Name**: Clear, business-focused name
2. **Description**: What the process accomplishes
3. **Actors**: Who participates (users, systems, roles)
4. **Key Steps**: High-level process steps
5. **Supporting Systems**: Technical components involved
6. **Business Rules**: Key business rules governing the process
7. **Data Entities**: Main data objects used

Focus on customer care, administration, user management, and operational processes typical for a telecom customer care system.

Format the response as structured business process descriptions suitable for business analysts and stakeholders.
"""
        
        result = await self.ollama.extract_requirements(context, "business_process_discovery")
        
        # For now, return a placeholder - in production, you'd parse the AI response
        return [
            BusinessProcess(
                process_name="Customer Care Management",
                description="Comprehensive customer service and support operations",
                actors=["Customer Service Agent", "Customer", "System Administrator"],
                steps=["Authentication", "Issue Identification", "Resolution", "Documentation"],
                supporting_components=code_patterns.get('services', [])[:5],
                business_rules=["User authorization required", "Data validation mandatory"],
                data_entities=["Customer", "Service Request", "Resolution"]
            )
        ]

    async def _generate_functional_requirements(self, business_processes: List[BusinessProcess], 
                                              code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate functional requirements from business processes and code patterns"""
        
        context = f"""
# A1 Telekom Austria CuCo - Functional Requirements Generation

## BUSINESS CONTEXT
Customer Care (CuCo) system for A1 Telekom Austria serving telecom operations.

## DISCOVERED BUSINESS PROCESSES
{len(business_processes)} business processes identified including customer care management, user administration, and operational workflows.

## CODE ANALYSIS INSIGHTS
- User Operations: {', '.join(code_patterns.get('operations', [])[:20])}
- User Roles: {', '.join(code_patterns.get('user_roles', []))}
- Validation Patterns: {len(code_patterns.get('validations', []))} validation rules found
- Services: {len(code_patterns.get('services', []))} business services
- Controllers: {len(code_patterns.get('controllers', []))} web controllers

## SAMPLE VALIDATION PATTERNS
"""
        
        for validation in code_patterns.get('validations', [])[:8]:
            context += f"- {validation['validation_type']}: {validation['file']}\n"
        
        context += f"""
## FUNCTIONAL REQUIREMENTS GENERATION REQUEST
Generate comprehensive functional requirements for the CuCo system covering:

### 1. USER MANAGEMENT REQUIREMENTS
- User registration and authentication
- Role-based access control
- User profile management
- Password and security management

### 2. CUSTOMER CARE REQUIREMENTS
- Customer information management
- Service request handling
- Issue tracking and resolution
- Communication management

### 3. ADMINISTRATIVE REQUIREMENTS
- System configuration
- User administration
- Reporting and analytics
- Data export/import capabilities

### 4. OPERATIONAL REQUIREMENTS
- Workflow management
- Task assignment and tracking
- Notification and alerting
- Audit and logging

### 5. DATA MANAGEMENT REQUIREMENTS
- Data validation and integrity
- Data backup and recovery
- Data archiving and retention
- Data privacy and compliance

For each requirement category, provide:
- Detailed functional specifications
- User stories or use cases
- Acceptance criteria
- Business value and priority
- Dependencies and constraints

Format as professional functional requirements suitable for development teams and business stakeholders.
"""
        
        functional_reqs = await self.ollama.extract_requirements(context, "functional_requirements")
        return functional_reqs

    async def _generate_non_functional_requirements(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate non-functional requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Non-Functional Requirements Analysis

## SYSTEM CONTEXT
Enterprise Java application serving A1 Telekom Austria customer care operations.
Technology stack: GWT, ExtJS/GXT, Spring Framework, iBATIS, Servlet API.

## CODE ANALYSIS INSIGHTS
- Total Components: {len(code_patterns.get('components', []))} 
- Services: {len(code_patterns.get('services', []))}
- Web Controllers: {len(code_patterns.get('controllers', []))}
- Integration Points: {len(code_patterns.get('integrations', []))}
- Security Patterns: {len(code_patterns.get('permissions', []))}

## NON-FUNCTIONAL REQUIREMENTS GENERATION REQUEST
Generate comprehensive non-functional requirements covering:

### 1. PERFORMANCE REQUIREMENTS
- Response time expectations for web interfaces
- Throughput requirements for customer care operations
- Database query performance standards
- Resource utilization limits

### 2. SCALABILITY REQUIREMENTS
- User concurrency requirements
- Data growth projections
- System expansion capabilities
- Load distribution requirements

### 3. AVAILABILITY REQUIREMENTS
- System uptime requirements (99.9%, 99.99%, etc.)
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
- Maintenance window requirements

### 4. SECURITY REQUIREMENTS
- Authentication and authorization standards
- Data encryption requirements
- Audit logging requirements
- Compliance requirements (GDPR, telecom regulations)

### 5. USABILITY REQUIREMENTS
- User interface responsiveness
- Accessibility standards
- Multi-language support
- Browser compatibility

### 6. MAINTAINABILITY REQUIREMENTS
- Code quality standards
- Documentation requirements
- Testing coverage requirements
- Deployment and release requirements

### 7. COMPATIBILITY REQUIREMENTS
- Operating system compatibility
- Browser compatibility
- Integration compatibility
- Data format compatibility

### 8. RELIABILITY REQUIREMENTS
- Error handling requirements
- Data integrity requirements
- System monitoring requirements
- Backup and recovery requirements

For each category, provide specific, measurable requirements with clear acceptance criteria and business justification.
"""
        
        non_functional_reqs = await self.ollama.extract_requirements(context, "non_functional_requirements")
        return non_functional_reqs

    async def _generate_technical_requirements(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical requirements and architecture specifications"""
        
        context = f"""
# A1 Telekom Austria CuCo - Technical Requirements Analysis

## CURRENT TECHNOLOGY ASSESSMENT
Based on code analysis of the enterprise Java application:

### Current Technology Stack
- Frontend: GWT (Google Web Toolkit) with ExtJS/GXT
- Backend: Java Enterprise with Spring Framework
- Data Access: iBATIS SQL mapping framework
- Web Layer: Servlet API with custom servlets
- Application Server: Likely Apache Tomcat or similar

### Architecture Patterns Identified
- Services: {len(code_patterns.get('services', []))} business services
- Controllers: {len(code_patterns.get('controllers', []))} web controllers  
- Components: {len(code_patterns.get('components', []))} general components
- Integration Points: {len(code_patterns.get('integrations', []))} external integrations

## TECHNICAL REQUIREMENTS GENERATION REQUEST
Generate comprehensive technical requirements covering:

### 1. ARCHITECTURE REQUIREMENTS
- Overall system architecture (layered, microservices, etc.)
- Component interaction patterns
- Data flow architecture
- Integration architecture

### 2. TECHNOLOGY STACK REQUIREMENTS
- Programming languages and frameworks
- Database technologies and requirements
- Web server and application server requirements
- Development and deployment tools

### 3. INFRASTRUCTURE REQUIREMENTS
- Server hardware specifications
- Network requirements and topology
- Storage requirements
- Backup and disaster recovery infrastructure

### 4. DEVELOPMENT REQUIREMENTS
- Development environment setup
- Version control requirements
- Build and deployment pipeline
- Testing framework requirements

### 5. INTEGRATION REQUIREMENTS
- API design standards
- Message format specifications
- Protocol requirements (HTTP, HTTPS, etc.)
- Third-party integration requirements

### 6. DATA REQUIREMENTS
- Database design standards
- Data modeling requirements
- Data migration requirements
- Data synchronization requirements

### 7. SECURITY TECHNICAL REQUIREMENTS
- Network security requirements
- Application security requirements
- Data security and encryption
- Identity and access management technical specs

### 8. MONITORING AND LOGGING REQUIREMENTS
- Application monitoring requirements
- System logging standards
- Performance monitoring requirements
- Error tracking and reporting

Provide specific, implementable technical requirements with clear specifications and rationale for each requirement.
"""
        
        technical_reqs = await self.ollama.extract_requirements(context, "technical_requirements")
        return technical_reqs

    async def _generate_security_requirements(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security and compliance requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Security and Compliance Requirements

## SECURITY CONTEXT ANALYSIS
Enterprise customer care system for A1 Telekom Austria handling sensitive customer data and telecom operations.

## CODE SECURITY PATTERNS IDENTIFIED
- Permission/Authorization patterns: {len(code_patterns.get('permissions', []))}
- User role patterns: {', '.join(code_patterns.get('user_roles', []))}
- Validation patterns: {len(code_patterns.get('validations', []))} validation checks

## SAMPLE SECURITY PATTERNS FROM CODE
"""
        
        for permission in code_patterns.get('permissions', [])[:8]:
            context += f"- File: {Path(permission['file']).name}\n"
            context += f"  Pattern: {permission['permission_type']}\n"
            context += f"  Context: {permission['context'][:100]}...\n\n"
        
        context += """
## SECURITY REQUIREMENTS GENERATION REQUEST
Generate comprehensive security requirements for the telecom customer care system:

### 1. AUTHENTICATION REQUIREMENTS
- User authentication methods and standards
- Multi-factor authentication requirements
- Password policy requirements
- Session management requirements

### 2. AUTHORIZATION REQUIREMENTS
- Role-based access control (RBAC) specifications
- Permission granularity requirements
- Administrative access controls
- Resource-level access controls

### 3. DATA PROTECTION REQUIREMENTS
- Data encryption requirements (at rest and in transit)
- Personal data protection (GDPR compliance)
- Customer data privacy requirements
- Data masking and anonymization

### 4. NETWORK SECURITY REQUIREMENTS
- Network access controls
- Firewall requirements
- VPN and secure communication
- DDoS protection requirements

### 5. APPLICATION SECURITY REQUIREMENTS
- Input validation and sanitization
- SQL injection prevention
- Cross-site scripting (XSS) prevention
- Cross-site request forgery (CSRF) protection

### 6. AUDIT AND COMPLIANCE REQUIREMENTS
- Audit logging requirements
- Compliance with telecom regulations
- GDPR compliance requirements
- Data retention and deletion policies

### 7. INCIDENT RESPONSE REQUIREMENTS
- Security incident detection
- Incident response procedures
- Security monitoring requirements
- Vulnerability management

### 8. BUSINESS CONTINUITY REQUIREMENTS
- Disaster recovery security requirements
- Backup security requirements
- Business continuity planning
- Crisis management procedures

Provide specific, implementable security requirements with clear compliance mappings and risk mitigation strategies.
"""
        
        security_reqs = await self.ollama.extract_requirements(context, "security_requirements")
        return security_reqs

    async def _generate_integration_requirements(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integration requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Integration Requirements Analysis

## INTEGRATION CONTEXT
Customer care system requiring integration with various A1 Telekom Austria systems and external partners.

## INTEGRATION PATTERNS IDENTIFIED
{len(code_patterns.get('integrations', []))} integration patterns found in code analysis.

## SAMPLE INTEGRATION PATTERNS
"""
        
        for integration in code_patterns.get('integrations', [])[:10]:
            context += f"- {integration['integration_type']}: {Path(integration['file']).name}\n"
        
        context += """
## INTEGRATION REQUIREMENTS GENERATION REQUEST
Generate comprehensive integration requirements:

### 1. INTERNAL SYSTEM INTEGRATIONS
- Customer database integration
- Billing system integration  
- Network management system integration
- CRM system integration

### 2. EXTERNAL PARTNER INTEGRATIONS
- Third-party service provider APIs
- Payment gateway integrations
- External verification services
- Regulatory reporting systems

### 3. API REQUIREMENTS
- RESTful API design standards
- API versioning and lifecycle management
- API security and authentication
- API documentation requirements

### 4. DATA EXCHANGE REQUIREMENTS
- Data format specifications (JSON, XML, etc.)
- Data transformation requirements
- Real-time vs batch processing requirements
- Data validation and error handling

### 5. MESSAGE QUEUING REQUIREMENTS
- Asynchronous message processing
- Message queue reliability requirements
- Message ordering and delivery guarantees
- Dead letter queue handling

### 6. SYNCHRONIZATION REQUIREMENTS
- Data synchronization patterns
- Conflict resolution strategies
- Eventual consistency requirements
- Master data management

### 7. MONITORING AND ERROR HANDLING
- Integration monitoring requirements
- Error detection and alerting
- Retry and fallback mechanisms
- Integration performance monitoring

### 8. COMPLIANCE AND GOVERNANCE
- Data sharing agreements
- Compliance with data protection regulations
- Integration security requirements
- Change management for integrations

Provide detailed, implementable integration requirements with clear technical specifications and governance policies.
"""
        
        integration_reqs = await self.ollama.extract_requirements(context, "integration_requirements")
        return integration_reqs

    async def _generate_ux_requirements(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate user experience requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - User Experience Requirements

## UX CONTEXT ANALYSIS
Customer care system serving A1 Telekom Austria agents and administrators with GWT/ExtJS frontend.

## USER ROLES IDENTIFIED
{', '.join(code_patterns.get('user_roles', []))}

## USER OPERATIONS IDENTIFIED  
{', '.join(code_patterns.get('operations', [])[:20])}

## UX REQUIREMENTS GENERATION REQUEST
Generate comprehensive user experience requirements:

### 1. USER INTERFACE REQUIREMENTS
- Modern, intuitive interface design
- Responsive design for various screen sizes
- Consistent visual design language
- Accessibility compliance (WCAG 2.1)

### 2. NAVIGATION REQUIREMENTS
- Clear navigation hierarchy
- Search and filtering capabilities
- Quick access to frequently used functions
- Contextual navigation aids

### 3. WORKFLOW REQUIREMENTS
- Streamlined customer care workflows
- Task-based user interfaces
- Progress indicators for long operations
- Undo/redo capabilities where appropriate

### 4. PERFORMANCE REQUIREMENTS
- Fast page load times (< 3 seconds)
- Responsive user interactions
- Efficient data loading and display
- Minimal bandwidth usage

### 5. PERSONALIZATION REQUIREMENTS
- User preference settings
- Customizable dashboards
- Role-based interface adaptation
- Personal productivity features

### 6. NOTIFICATION REQUIREMENTS
- Real-time notifications for urgent items
- Configurable alert preferences
- Visual and audio notification options
- Notification history and management

### 7. DATA PRESENTATION REQUIREMENTS
- Clear, readable data displays
- Effective use of charts and graphs
- Sortable and filterable data tables
- Export capabilities for reports

### 8. MOBILE AND DEVICE REQUIREMENTS
- Mobile-friendly interfaces
- Cross-browser compatibility
- Tablet optimization
- Offline capability where applicable

### 9. HELP AND SUPPORT REQUIREMENTS
- Context-sensitive help
- User documentation and tutorials
- Training mode for new users
- Support contact integration

Provide specific, measurable UX requirements with clear acceptance criteria and user satisfaction metrics.
"""
        
        ux_reqs = await self.ollama.extract_requirements(context, "ux_requirements")
        return ux_reqs

    async def _generate_executive_summary(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Executive Requirements Summary

## PROJECT CONTEXT
Comprehensive requirements analysis of A1 Telekom Austria Customer Care (CuCo) enterprise application.

## ANALYSIS SCOPE
- Technology: Java Enterprise Application with GWT frontend
- Business Domain: Telecom Customer Care Operations  
- Components Analyzed: {len(code_patterns.get('components', []))} + {len(code_patterns.get('services', []))} services
- User Roles: {', '.join(code_patterns.get('user_roles', []))}
- Core Operations: {', '.join(code_patterns.get('operations', [])[:15])}

## EXECUTIVE SUMMARY GENERATION REQUEST
Create a comprehensive executive summary suitable for C-level stakeholders covering:

### 1. BUSINESS OVERVIEW
- System purpose and business value
- Key stakeholders and users
- Critical business processes supported
- ROI and business impact

### 2. STRATEGIC REQUIREMENTS SUMMARY  
- High-level functional capabilities
- Critical non-functional requirements
- Security and compliance imperatives
- Integration and modernization needs

### 3. IMPLEMENTATION PRIORITIES
- High-priority requirements for immediate attention
- Medium-term development objectives
- Long-term strategic goals
- Risk mitigation priorities

### 4. INVESTMENT REQUIREMENTS
- Development effort estimates
- Infrastructure requirements
- Training and change management needs
- Ongoing operational costs

### 5. SUCCESS METRICS
- Key performance indicators
- User satisfaction metrics
- Business outcome measurements
- Technical performance targets

### 6. RISKS AND MITIGATION
- Technical risks and mitigation strategies
- Business continuity considerations
- Compliance and regulatory risks
- Resource and timeline risks

Provide a professional executive summary focused on business value, strategic alignment, and investment decision-making.
"""
        
        executive_summary = await self.ollama.extract_requirements(context, "executive_summary")
        return executive_summary

    async def _generate_implementation_roadmap(self) -> Dict[str, Any]:
        """Generate implementation roadmap"""
        
        context = """
# A1 Telekom Austria CuCo - Implementation Roadmap

## MODERNIZATION CONTEXT
Legacy GWT/ExtJS enterprise application requiring modernization while maintaining business continuity.

## ROADMAP GENERATION REQUEST
Create a phased implementation roadmap covering:

### PHASE 1: FOUNDATION (0-6 months)
- Infrastructure modernization
- Security enhancements
- Critical bug fixes
- Performance optimizations

### PHASE 2: CORE MODERNIZATION (6-18 months)  
- Frontend framework migration
- API modernization
- Database optimization
- User experience improvements

### PHASE 3: ADVANCED FEATURES (18-30 months)
- Advanced analytics
- Mobile capabilities
- AI/ML integration
- Advanced automation

### PHASE 4: STRATEGIC EXPANSION (30+ months)
- Cloud migration
- Microservices architecture
- Advanced integration capabilities
- Next-generation features

For each phase, provide:
- Key deliverables and milestones
- Resource requirements
- Dependencies and prerequisites
- Success criteria
- Risk mitigation strategies
"""
        
        roadmap = await self.ollama.extract_requirements(context, "implementation_roadmap")
        return roadmap

    async def _generate_traceability_matrix(self, code_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate requirements traceability matrix"""
        
        # This would map requirements to source code files, tests, and business processes
        # For now, return a structured mapping based on code patterns
        
        return {
            'business_to_code_mapping': {
                'user_management': code_patterns.get('services', [])[:5],
                'customer_care': code_patterns.get('controllers', [])[:5],
                'administration': code_patterns.get('components', [])[:5]
            },
            'requirement_to_test_mapping': {
                'functional_requirements': [],  # Would be populated with test mappings
                'non_functional_requirements': [],
                'security_requirements': []
            },
            'code_to_business_mapping': {
                file: "business_process_mapping" for file in code_patterns.get('services', [])[:10]
            }
        }

    async def _save_requirements_documentation(self, requirements_doc: Dict[str, Any]):
        """Save comprehensive requirements documentation"""
        try:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save complete requirements JSON
            with open(f"output/cuco_comprehensive_requirements_{timestamp}.json", 'w') as f:
                json.dump(requirements_doc, f, indent=2, default=str)
            
            # Save individual requirement documents
            for req_type in ['functional_requirements', 'non_functional_requirements', 
                           'technical_requirements', 'security_requirements',
                           'integration_requirements', 'user_experience_requirements']:
                
                req_data = requirements_doc.get(req_type, {})
                if req_data.get('success', False):
                    with open(f"output/cuco_{req_type}_{timestamp}.md", 'w') as f:
                        f.write(f"# A1 Telekom Austria CuCo - {req_type.replace('_', ' ').title()}\n")
                        f.write(f"Generated: {requirements_doc['metadata']['generated_at']}\n\n")
                        f.write(req_data.get('requirements_content', 'Requirements generation failed'))
            
            # Save executive summary  
            exec_summary = requirements_doc.get('executive_summary', {})
            if exec_summary.get('success', False):
                with open(f"output/cuco_executive_summary_{timestamp}.md", 'w') as f:
                    f.write("# A1 Telekom Austria CuCo - Executive Requirements Summary\n")
                    f.write(f"Generated: {requirements_doc['metadata']['generated_at']}\n\n")
                    f.write(exec_summary.get('requirements_content', 'Executive summary generation failed'))
            
            # Save implementation roadmap
            roadmap = requirements_doc.get('implementation_roadmap', {})  
            if roadmap.get('success', False):
                with open(f"output/cuco_implementation_roadmap_{timestamp}.md", 'w') as f:
                    f.write("# A1 Telekom Austria CuCo - Implementation Roadmap\n")
                    f.write(f"Generated: {requirements_doc['metadata']['generated_at']}\n\n")
                    f.write(roadmap.get('requirements_content', 'Roadmap generation failed'))
            
            logger.info(f"📁 Requirements documentation saved:")
            logger.info(f"   • Comprehensive: output/cuco_comprehensive_requirements_{timestamp}.json")
            logger.info(f"   • Individual requirement types: output/cuco_*_requirements_{timestamp}.md")
            logger.info(f"   • Executive summary: output/cuco_executive_summary_{timestamp}.md") 
            logger.info(f"   • Implementation roadmap: output/cuco_implementation_roadmap_{timestamp}.md")
            
        except Exception as e:
            logger.error(f"Failed to save requirements documentation: {e}")

async def main():
    """Main execution function"""
    logger.info("📋 A1 Telekom Austria CuCo - Extended Requirements Generation")
    logger.info("=" * 80)
    logger.info("🎯 Comprehensive requirements extraction from Java enterprise application")
    logger.info("🧠 AI-powered analysis with Qwen3-Coder-30B (1M context window)")
    logger.info("=" * 80)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        generator = ExtendedRequirementsGenerator(java_root_path)
        requirements_doc = await generator.generate_extended_requirements()
        
        # Display results summary
        logger.info("=" * 80)
        logger.info("🎉 EXTENDED REQUIREMENTS GENERATION COMPLETE")
        logger.info("=" * 80)
        
        metadata = requirements_doc['metadata']
        logger.info(f"📊 Analysis completed in {metadata['processing_time']:.2f} seconds")
        logger.info(f"🎯 System: {metadata['source_system']}")
        logger.info(f"🧠 AI Model: {metadata['methodology']}")
        
        business_context = requirements_doc['business_context']
        logger.info(f"\n📈 Business Analysis:")
        logger.info(f"   • Business processes: {len(business_context['discovered_processes'])}")
        logger.info(f"   • Business rules: {business_context['business_rules_count']}")
        logger.info(f"   • User roles: {len(business_context['user_roles_identified'])}")
        logger.info(f"   • Operations: {len(business_context['key_operations'])}")
        
        logger.info(f"\n📋 Requirements Generated:")
        req_types = ['functional_requirements', 'non_functional_requirements', 
                    'technical_requirements', 'security_requirements',
                    'integration_requirements', 'user_experience_requirements']
        
        for req_type in req_types:
            req_data = requirements_doc.get(req_type, {})
            status = "✅" if req_data.get('success', False) else "❌"
            logger.info(f"   {status} {req_type.replace('_', ' ').title()}")
        
        logger.info(f"\n📁 Complete documentation available in output/ directory")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Extended requirements generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)