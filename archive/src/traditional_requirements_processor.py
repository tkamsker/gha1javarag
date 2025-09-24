#!/usr/bin/env python3
"""
Traditional Requirements Processor with Weaviate and Data Structure Integration
Processes traditional requirements using Weaviate vector database and comprehensive data structure analysis
"""

import asyncio
import logging
import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import aiohttp
import weaviate

class TraditionalRequirementsProcessor:
    def __init__(self, weaviate_metadata_file: str, data_structures_file: str = None, 
                 architecture_file: str = None, debug_file: str = None, mode: str = "production"):
        self.weaviate_metadata_file = Path(weaviate_metadata_file)
        self.data_structures_file = Path(data_structures_file) if data_structures_file else None
        self.architecture_file = Path(architecture_file) if architecture_file else None
        self.debug_file = Path(debug_file) if debug_file else None
        self.mode = mode
        
        self.output_dir = Path("./output/requirements_traditional")
        
        # Initialize Weaviate client
        try:
            self.weaviate_client = weaviate.connect_to_local()
            logger.info("✅ Connected to Weaviate for traditional requirements")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Weaviate: {e}")
            raise
        
        # Initialize Ollama client
        self.ollama_base_url = "http://localhost:11434"
        self.ollama_model = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        
        # Load metadata and data structures
        self.metadata = self._load_metadata()
        self.data_structures = self._load_data_structures()
        self.architecture_data = self._load_architecture_data()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load Weaviate metadata"""
        try:
            with open(self.weaviate_metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Weaviate metadata: {e}")
            return {}

    def _load_data_structures(self) -> Dict[str, Any]:
        """Load data structures analysis"""
        if not self.data_structures_file or not self.data_structures_file.exists():
            logger.warning("Data structures file not found")
            return {}
        
        try:
            with open(self.data_structures_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load data structures: {e}")
            return {}

    def _load_architecture_data(self) -> Dict[str, Any]:
        """Load architecture data"""
        if not self.architecture_file or not self.architecture_file.exists():
            logger.warning("Architecture file not found")
            return {}
        
        try:
            with open(self.architecture_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load architecture data: {e}")
            return {}

    async def process_traditional_requirements(self) -> Dict[str, Any]:
        """Process traditional requirements with comprehensive analysis"""
        logger.info("📋 Processing traditional requirements with Weaviate and data structures...")
        
        start_time = datetime.now()
        
        # Create output directories
        self._create_output_directories()
        
        # Generate different categories of traditional requirements
        requirements_count = 0
        documents_generated = 0
        
        # 1. Functional Requirements
        logger.info("⚙️ Generating functional requirements...")
        functional_reqs = await self._generate_functional_requirements()
        requirements_count += await self._save_requirements("functional", "functional_requirements.md", functional_reqs)
        documents_generated += 1
        
        # 2. Non-Functional Requirements
        logger.info("📊 Generating non-functional requirements...")
        nonfunctional_reqs = await self._generate_non_functional_requirements()
        requirements_count += await self._save_requirements("non_functional", "non_functional_requirements.md", nonfunctional_reqs)
        documents_generated += 1
        
        # 3. Data Requirements
        logger.info("🗃️ Generating data requirements...")
        data_reqs = await self._generate_data_requirements()
        requirements_count += await self._save_requirements("data", "data_requirements.md", data_reqs)
        documents_generated += 1
        
        # 4. Integration Requirements
        logger.info("🔗 Generating integration requirements...")
        integration_reqs = await self._generate_integration_requirements()
        requirements_count += await self._save_requirements("integration", "integration_requirements.md", integration_reqs)
        documents_generated += 1
        
        # 5. Security Requirements
        logger.info("🛡️ Generating security requirements...")
        security_reqs = await self._generate_security_requirements()
        requirements_count += await self._save_requirements("security", "security_requirements.md", security_reqs)
        documents_generated += 1
        
        # 6. User Interface Requirements
        logger.info("👥 Generating user interface requirements...")
        ui_reqs = await self._generate_ui_requirements()
        requirements_count += await self._save_requirements("ui", "user_interface_requirements.md", ui_reqs)
        documents_generated += 1
        
        # 7. Performance Requirements
        logger.info("⚡ Generating performance requirements...")
        performance_reqs = await self._generate_performance_requirements()
        requirements_count += await self._save_requirements("performance", "performance_requirements.md", performance_reqs)
        documents_generated += 1
        
        # 8. Entity-Specific Requirements
        logger.info("🏗️ Generating entity-specific requirements...")
        entity_count = await self._generate_entity_specific_requirements()
        documents_generated += entity_count
        
        # 9. Business Rules Requirements
        logger.info("📝 Generating business rules requirements...")
        business_rules_reqs = await self._generate_business_rules_requirements()
        requirements_count += await self._save_requirements("business", "business_rules_requirements.md", business_rules_reqs)
        documents_generated += 1
        
        # 10. Compliance Requirements
        logger.info("📋 Generating compliance requirements...")
        compliance_reqs = await self._generate_compliance_requirements()
        requirements_count += await self._save_requirements("compliance", "compliance_requirements.md", compliance_reqs)
        documents_generated += 1
        
        # Generate master traditional requirements document
        await self._generate_master_traditional_document()
        documents_generated += 1
        
        # Generate requirements traceability matrix
        await self._generate_traceability_matrix()
        documents_generated += 1
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Compile results
        results = {
            'success': True,
            'processing_time': processing_time,
            'requirements_count': requirements_count,
            'documents_generated': documents_generated,
            'data_structures_analyzed': len(self.data_structures.get('entities', [])) + len(self.data_structures.get('dtos', [])),
            'entities_processed': len(self.data_structures.get('entities', [])),
            'relationships_analyzed': len(self.data_structures.get('relationships', [])),
            'mode': self.mode
        }
        
        # Save processing results
        with open(self.output_dir / "processing_results.json", 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"✅ Traditional requirements processing completed in {processing_time:.2f} seconds")
        logger.info(f"📊 Generated {requirements_count} requirements across {documents_generated} documents")
        
        return results

    def _create_output_directories(self):
        """Create output directory structure"""
        directories = [
            "functional",
            "non_functional", 
            "data",
            "integration",
            "security",
            "ui",
            "performance",
            "entities",
            "business",
            "compliance",
            "analysis"
        ]
        
        for directory in directories:
            os.makedirs(self.output_dir / directory, exist_ok=True)

    async def _generate_functional_requirements(self) -> str:
        """Generate comprehensive functional requirements"""
        
        entities = self.data_structures.get('entities', [])
        dtos = self.data_structures.get('dtos', [])
        
        context = f"""
# A1 Telekom Austria CuCo - Functional Requirements Analysis

## System Context
Customer Care (CuCo) enterprise system for A1 Telekom Austria with comprehensive data model analysis.

## Data Model Overview
- **Entities**: {len(entities)} business entities identified
- **DTOs**: {len(dtos)} data transfer objects
- **Processing Mode**: {self.mode}
- **Files Processed**: {self.metadata.get('files_processed', 0)}

## Key Business Entities
"""
        
        for entity in entities[:8]:
            context += f"""
### {entity.get('name', 'Unknown')}
- **Package**: {entity.get('package_name', 'Unknown')}
- **Domain**: {entity.get('business_domain', 'General')}
- **Fields**: {len(entity.get('fields', []))} fields
- **Complexity**: {entity.get('complexity_score', 0)}
"""
        
        context += f"""
## Functional Requirements Generation Request

Generate comprehensive traditional functional requirements for the A1 Telekom Austria CuCo system covering:

### 1. CUSTOMER MANAGEMENT FUNCTIONS
- Customer registration and profile management
- Customer information retrieval and updates
- Customer service history tracking
- Customer communication preferences
- Account status management

### 2. SERVICE MANAGEMENT FUNCTIONS
- Service catalog management
- Service provisioning and activation
- Service configuration and customization
- Service billing and pricing
- Service quality monitoring

### 3. ORDER MANAGEMENT FUNCTIONS
- Order creation and validation
- Order processing workflows
- Order fulfillment tracking
- Order modification and cancellation
- Order history and reporting

### 4. BILLING FUNCTIONS
- Invoice generation and delivery
- Payment processing and reconciliation
- Billing dispute management
- Pricing and discount application
- Revenue reporting and analytics

### 5. SUPPORT FUNCTIONS
- Ticket creation and assignment
- Issue tracking and resolution
- Escalation procedures
- Knowledge base management
- Support performance metrics

### 6. REPORTING AND ANALYTICS FUNCTIONS
- Operational reporting
- Performance dashboards
- Business intelligence
- Data export capabilities
- Scheduled report generation

### 7. SYSTEM ADMINISTRATION FUNCTIONS
- User management and access control
- System configuration management
- Audit logging and monitoring
- Data backup and recovery
- System maintenance procedures

### 8. INTEGRATION FUNCTIONS
- External system interfaces
- Data synchronization processes
- API management and security
- Message queue processing
- Event handling and notifications

For each functional area, provide:
- Detailed functional specifications
- User acceptance criteria
- Business rules and validations
- Error handling requirements
- Performance expectations

Format as traditional software requirements suitable for formal documentation and stakeholder approval.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_non_functional_requirements(self) -> str:
        """Generate non-functional requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Non-Functional Requirements Analysis

## System Scale and Context
Enterprise-grade customer care system serving A1 Telekom Austria operations.

## Architecture Overview
- **Data Structures**: {len(self.data_structures.get('entities', [])) + len(self.data_structures.get('dtos', []))} identified
- **Business Domains**: Multiple domains including customer, billing, service, support
- **Technology Stack**: Java Enterprise with Spring Framework, requiring modernization

## Non-Functional Requirements Generation Request

Generate comprehensive traditional non-functional requirements covering:

### 1. PERFORMANCE REQUIREMENTS
- **Response Time**: Web pages must load within 3 seconds under normal load
- **Throughput**: System must handle 1000 concurrent users
- **Transaction Volume**: Process 10,000 transactions per hour
- **Database Performance**: Query response time under 500ms for 95% of queries
- **API Performance**: REST API calls must respond within 2 seconds

### 2. SCALABILITY REQUIREMENTS  
- **User Scalability**: Support growth to 5000 concurrent users
- **Data Scalability**: Handle 100% data growth over 5 years
- **Geographic Scalability**: Support multiple data centers
- **Component Scalability**: Individual services must scale independently
- **Load Distribution**: Automatic load balancing across instances

### 3. AVAILABILITY REQUIREMENTS
- **System Uptime**: 99.9% availability (8.76 hours downtime per year)
- **Planned Maintenance**: Maximum 4 hours monthly maintenance window
- **Recovery Time**: System recovery within 1 hour of failure
- **Data Recovery**: Recovery Point Objective (RPO) of 15 minutes
- **Business Continuity**: Critical functions available during maintenance

### 4. RELIABILITY REQUIREMENTS
- **System Stability**: Mean Time Between Failures (MTBF) of 720 hours
- **Error Rates**: System error rate below 0.1% of transactions
- **Data Integrity**: 100% data consistency across all operations
- **Failover**: Automatic failover within 30 seconds
- **Backup Reliability**: 99.99% backup success rate

### 5. SECURITY REQUIREMENTS
- **Authentication**: Multi-factor authentication for administrative users
- **Authorization**: Role-based access control with principle of least privilege
- **Data Encryption**: AES-256 encryption for data at rest and in transit
- **Session Management**: Automatic session timeout after 30 minutes inactivity
- **Audit Logging**: Complete audit trail for all system activities

### 6. USABILITY REQUIREMENTS
- **User Interface**: Intuitive interface requiring minimal training
- **Accessibility**: WCAG 2.1 AA compliance for accessibility
- **Browser Support**: Compatible with latest versions of Chrome, Firefox, Safari, Edge
- **Mobile Support**: Responsive design for tablet and mobile devices
- **User Experience**: Task completion time reduction by 40% over legacy system

### 7. MAINTAINABILITY REQUIREMENTS
- **Code Quality**: Minimum 90% code coverage with automated tests
- **Documentation**: Comprehensive technical and user documentation
- **Deployment**: Zero-downtime deployment capability
- **Monitoring**: Real-time system health monitoring and alerting
- **Updates**: Ability to deploy updates within 2-hour maintenance windows

### 8. COMPATIBILITY REQUIREMENTS
- **Operating Systems**: Support for Linux and Windows server environments
- **Databases**: Compatible with PostgreSQL, Oracle, and SQL Server
- **Integration**: RESTful API compatibility with existing enterprise systems
- **Legacy Systems**: Seamless integration with existing A1 systems
- **Standards Compliance**: Adherence to relevant telecommunications standards

### 9. CAPACITY REQUIREMENTS
- **Storage**: Initial 10TB storage with 100% growth capacity over 5 years
- **Memory**: 32GB RAM minimum per application server
- **CPU**: Multi-core processors with 70% average utilization threshold
- **Network**: 1Gbps network connectivity with 99.9% availability
- **Concurrent Sessions**: Support for 1000 concurrent user sessions

### 10. DISASTER RECOVERY REQUIREMENTS
- **Backup Strategy**: Daily incremental backups with weekly full backups
- **Geographic Distribution**: Primary and secondary data centers in different regions  
- **Recovery Procedures**: Documented and tested disaster recovery procedures
- **Data Synchronization**: Real-time data replication between sites
- **Communication Plan**: Emergency communication procedures for stakeholders

Format as traditional non-functional requirements with specific, measurable criteria and acceptance standards.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_data_requirements(self) -> str:
        """Generate data requirements based on discovered data structures"""
        
        entities = self.data_structures.get('entities', [])
        relationships = self.data_structures.get('relationships', [])
        summary = self.data_structures.get('summary', {})
        
        context = f"""
# A1 Telekom Austria CuCo - Data Requirements Analysis

## Data Architecture Overview
Comprehensive data requirements based on discovered enterprise data structures.

## Data Structure Summary
- **Business Entities**: {len(entities)} entities identified
- **Entity Relationships**: {len(relationships)} relationships mapped
- **Business Domains**: {len(summary.get('business_domains', {}).get('domain_distribution', {}))} domains
- **Complexity Analysis**: Available for detailed requirements specification

## Key Business Entities Analysis
"""
        
        for entity in entities[:10]:
            fields = entity.get('fields', [])
            context += f"""
### Entity: {entity.get('name', 'Unknown')}
- **Business Domain**: {entity.get('business_domain', 'General')}
- **Package**: {entity.get('package_name', 'Unknown')}
- **Field Count**: {len(fields)}
- **Key Fields**: {', '.join([f.get('name', 'Unknown') for f in fields[:5]])}
- **Complexity Score**: {entity.get('complexity_score', 0)}
"""
        
        context += f"""
## Data Requirements Generation Request

Generate comprehensive traditional data requirements covering:

### 1. DATA MODEL REQUIREMENTS
- **Entity Definitions**: Complete specification of all business entities
- **Attribute Definitions**: Detailed field specifications with data types
- **Relationship Definitions**: Foreign key and referential integrity requirements
- **Domain Constraints**: Business rule constraints on data values
- **Data Dictionary**: Comprehensive data dictionary with metadata

### 2. DATA STORAGE REQUIREMENTS
- **Database Design**: Normalized database schema design
- **Table Structure**: Primary keys, foreign keys, and indexes
- **Data Types**: Specific data type requirements for each field
- **Storage Capacity**: Initial and projected storage requirements
- **Partitioning Strategy**: Data partitioning for performance optimization

### 3. DATA INTEGRITY REQUIREMENTS
- **Referential Integrity**: Foreign key constraints and cascade rules
- **Domain Integrity**: Check constraints and validation rules
- **Entity Integrity**: Primary key and unique constraints
- **Business Rules**: Complex business rule validation
- **Data Consistency**: Cross-table consistency requirements

### 4. DATA ACCESS REQUIREMENTS
- **Query Performance**: Indexing strategy for optimal query performance
- **Concurrent Access**: Multi-user data access patterns
- **Transaction Management**: ACID transaction requirements
- **Locking Strategy**: Optimistic vs pessimistic locking requirements
- **Connection Pooling**: Database connection management

### 5. DATA MIGRATION REQUIREMENTS
- **Legacy Data Mapping**: Source-to-target data mapping specifications
- **Data Transformation**: ETL processes for data cleansing and transformation
- **Migration Validation**: Data quality verification procedures
- **Incremental Migration**: Phased migration approach requirements
- **Rollback Procedures**: Data migration rollback and recovery procedures

### 6. DATA SECURITY REQUIREMENTS
- **Access Control**: Role-based data access permissions
- **Data Classification**: Sensitive data identification and handling
- **Encryption Requirements**: Field-level and database-level encryption
- **Data Masking**: Sensitive data masking for non-production environments
- **Audit Logging**: Data access and modification audit trails

### 7. DATA BACKUP AND RECOVERY REQUIREMENTS
- **Backup Strategy**: Full and incremental backup procedures
- **Recovery Procedures**: Point-in-time recovery capabilities
- **Backup Retention**: Data retention policies and archival requirements
- **Recovery Testing**: Regular backup and recovery testing procedures
- **Geographic Distribution**: Backup storage across multiple locations

### 8. DATA ARCHIVAL REQUIREMENTS
- **Archival Policies**: Data lifecycle management and archival rules
- **Archive Storage**: Long-term data storage solutions
- **Data Retrieval**: Archived data retrieval procedures
- **Compliance Requirements**: Regulatory compliance for data retention
- **Purge Procedures**: Secure data deletion and purging processes

### 9. DATA QUALITY REQUIREMENTS
- **Validation Rules**: Data quality validation at point of entry
- **Data Cleansing**: Automated data cleansing procedures
- **Quality Metrics**: Data quality measurement and reporting
- **Error Handling**: Invalid data detection and correction procedures
- **Data Profiling**: Regular data quality assessment procedures

### 10. REPORTING AND ANALYTICS DATA REQUIREMENTS
- **Data Warehouse**: Analytics data warehouse design requirements
- **ETL Processes**: Extract, Transform, Load processes for analytics
- **Data Marts**: Subject-specific data mart requirements
- **Historical Data**: Historical data retention for trend analysis
- **Real-time Analytics**: Operational analytics and reporting requirements

For each data requirement category, provide specific technical specifications, acceptance criteria, and implementation guidelines suitable for database administrators and developers.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_integration_requirements(self) -> str:
        """Generate integration requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Integration Requirements Analysis

## Integration Context
Enterprise customer care system requiring comprehensive integration with A1 Telekom Austria ecosystem.

## System Integration Scope
- **Internal Systems**: Customer databases, billing systems, network operations
- **External Partners**: Wholesale partners, regulatory systems, third-party services
- **Legacy Systems**: Existing A1 infrastructure and applications
- **Modern Systems**: Cloud services and contemporary enterprise applications

## Integration Requirements Generation Request

Generate comprehensive traditional integration requirements covering:

### 1. INTERNAL SYSTEM INTEGRATION REQUIREMENTS
- **Customer Database Integration**: Real-time customer data synchronization
- **Billing System Integration**: Invoice and payment processing integration
- **Network Operations Integration**: Service provisioning and network management
- **CRM Integration**: Customer relationship management data sharing
- **ERP Integration**: Enterprise resource planning system connectivity

### 2. EXTERNAL SYSTEM INTEGRATION REQUIREMENTS
- **Regulatory Systems**: Automated regulatory reporting and compliance
- **Wholesale Partners**: B2B partner system integration
- **Payment Gateways**: Multiple payment processor integration
- **Credit Checking Services**: Real-time creditworthiness validation
- **Third-party Services**: External service provider API integration

### 3. API INTEGRATION REQUIREMENTS
- **REST API Standards**: RESTful web service design and implementation
- **SOAP Web Services**: Legacy system SOAP interface support
- **GraphQL APIs**: Flexible data querying capabilities
- **API Security**: OAuth 2.0 and JWT token-based authentication
- **API Versioning**: Backward compatibility and version management

### 4. DATA INTEGRATION REQUIREMENTS
- **Real-time Synchronization**: Event-driven real-time data updates
- **Batch Processing**: Scheduled bulk data processing and transfer
- **ETL Processes**: Extract, Transform, Load operations
- **Data Transformation**: Format conversion and data mapping
- **Data Validation**: Integrated data quality verification

### 5. MESSAGE INTEGRATION REQUIREMENTS
- **Message Queuing**: Asynchronous message processing (Apache Kafka/RabbitMQ)
- **Event Streaming**: Real-time event processing and distribution
- **Message Routing**: Intelligent message routing and filtering
- **Error Handling**: Dead letter queues and retry mechanisms
- **Message Security**: Encrypted message transmission and validation

### 6. WORKFLOW INTEGRATION REQUIREMENTS
- **Business Process Integration**: Cross-system workflow orchestration
- **Human Task Integration**: Manual approval and intervention points
- **Process Monitoring**: Business process tracking and analytics
- **Exception Handling**: Process failure detection and recovery
- **SLA Management**: Service level agreement monitoring and enforcement

### 7. SECURITY INTEGRATION REQUIREMENTS
- **Single Sign-On**: Enterprise SSO integration (SAML, OAuth)
- **Identity Management**: Centralized user identity and access management
- **Security Token Service**: Token-based authentication and authorization
- **Certificate Management**: Digital certificate lifecycle management
- **Audit Integration**: Centralized security audit logging

### 8. MONITORING INTEGRATION REQUIREMENTS
- **System Monitoring**: Integrated health monitoring and alerting
- **Performance Monitoring**: End-to-end performance tracking
- **Log Aggregation**: Centralized log collection and analysis
- **Metrics Collection**: Business and technical metrics gathering
- **Dashboard Integration**: Unified monitoring dashboard

### 9. FILE INTEGRATION REQUIREMENTS
- **File Transfer**: Secure file transfer protocols (SFTP, FTPS)
- **Batch File Processing**: Automated file processing workflows
- **File Format Support**: Multiple file format processing (CSV, XML, JSON, EDI)
- **File Validation**: Automated file content and format validation
- **Archive Management**: Processed file archival and retention

### 10. CLOUD INTEGRATION REQUIREMENTS
- **Cloud Services**: Integration with AWS, Azure, or Google Cloud services
- **Hybrid Architecture**: On-premises to cloud connectivity
- **Container Integration**: Docker and Kubernetes integration
- **Serverless Integration**: Function-as-a-Service integration
- **Cloud Storage**: Cloud-based file and data storage integration

### 11. PERFORMANCE INTEGRATION REQUIREMENTS
- **Load Balancing**: Integrated load balancing across systems
- **Caching Integration**: Distributed caching for performance optimization
- **Connection Pooling**: Database and service connection management
- **Circuit Breaker**: Fault tolerance and system protection patterns
- **Rate Limiting**: API and service rate limiting implementation

### 12. TESTING INTEGRATION REQUIREMENTS
- **Integration Testing**: Automated integration test suites
- **Mock Services**: Test environment mock service implementation
- **Data Provisioning**: Test data management and provisioning
- **Environment Management**: Multi-environment integration testing
- **Continuous Testing**: CI/CD pipeline integration testing

Provide detailed technical specifications for each integration requirement with specific protocols, standards, and implementation guidelines suitable for enterprise integration architects and developers.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_security_requirements(self) -> str:
        """Generate security requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Security Requirements Analysis

## Security Context
Enterprise-grade security requirements for A1 Telekom Austria customer care system handling sensitive customer data.

## Compliance and Regulatory Context
- **GDPR Compliance**: European data protection regulations
- **Telecommunications Regulations**: Austrian and EU telecommunications law
- **Industry Standards**: ISO 27001, SOC 2, PCI DSS where applicable
- **Corporate Security Policies**: A1 Telekom Austria security standards

## Security Requirements Generation Request

Generate comprehensive traditional security requirements covering:

### 1. AUTHENTICATION REQUIREMENTS
- **Multi-Factor Authentication**: Mandatory MFA for all administrative users
- **Single Sign-On**: Enterprise SSO integration with Active Directory/LDAP
- **Password Policy**: Complex passwords with minimum 12 characters, special characters required
- **Account Lockout**: Automatic lockout after 5 failed login attempts
- **Session Management**: Secure session handling with 30-minute idle timeout

### 2. AUTHORIZATION REQUIREMENTS
- **Role-Based Access Control**: Granular RBAC with principle of least privilege
- **Permission Management**: Fine-grained permissions for all system functions
- **Administrative Access**: Segregated administrative access with approval workflows
- **Resource Access Control**: Object-level security for sensitive data access
- **Audit Trail**: Complete access logging for all authorization decisions

### 3. DATA PROTECTION REQUIREMENTS
- **Data Encryption**: AES-256 encryption for data at rest and in transit
- **Database Encryption**: Transparent database encryption with key management
- **Field-Level Encryption**: Encryption of personally identifiable information (PII)
- **Key Management**: Hardware Security Module (HSM) for cryptographic key storage
- **Data Classification**: Automated data classification and handling procedures

### 4. NETWORK SECURITY REQUIREMENTS
- **Firewall Protection**: Multi-layer firewall protection with DMZ architecture
- **Network Segmentation**: VLAN segmentation for security zones
- **VPN Access**: Secure VPN for remote access with certificate-based authentication
- **Intrusion Detection**: Network intrusion detection and prevention systems
- **DDoS Protection**: Distributed denial of service attack mitigation

### 5. APPLICATION SECURITY REQUIREMENTS
- **Secure Coding**: OWASP Top 10 vulnerability prevention
- **Input Validation**: Comprehensive input sanitization and validation
- **SQL Injection Prevention**: Parameterized queries and stored procedures
- **Cross-Site Scripting Protection**: XSS prevention through output encoding
- **Cross-Site Request Forgery Protection**: CSRF tokens for state-changing operations

### 6. API SECURITY REQUIREMENTS
- **API Authentication**: OAuth 2.0 and JWT token-based authentication
- **API Authorization**: Fine-grained API access control with scopes
- **Rate Limiting**: API rate limiting to prevent abuse and DoS attacks
- **API Gateway**: Centralized API gateway for security policy enforcement
- **API Monitoring**: Real-time API security monitoring and threat detection

### 7. AUDIT AND COMPLIANCE REQUIREMENTS
- **Comprehensive Logging**: Detailed audit logs for all system activities
- **Log Integrity**: Tamper-evident logging with cryptographic signatures
- **Log Retention**: 7-year log retention for compliance requirements
- **Compliance Reporting**: Automated compliance reporting and dashboards
- **External Auditing**: Support for external security audits and assessments

### 8. INCIDENT RESPONSE REQUIREMENTS
- **Security Incident Detection**: Automated security incident detection and alerting
- **Incident Response Plan**: Documented incident response procedures
- **Forensic Capabilities**: Digital forensic investigation capabilities
- **Incident Communication**: Secure communication channels for incident response
- **Recovery Procedures**: Security incident recovery and business continuity procedures

### 9. DATA PRIVACY REQUIREMENTS
- **GDPR Compliance**: Full compliance with European data protection regulations
- **Privacy by Design**: Privacy considerations integrated into system design
- **Data Subject Rights**: Right to access, portability, erasure, and correction
- **Consent Management**: Granular consent management and tracking
- **Data Processing Records**: Comprehensive records of data processing activities

### 10. VULNERABILITY MANAGEMENT REQUIREMENTS
- **Vulnerability Scanning**: Regular automated vulnerability assessments
- **Penetration Testing**: Annual third-party penetration testing
- **Security Patching**: Automated security patch management with rapid deployment
- **Configuration Management**: Secure baseline configuration management
- **Security Monitoring**: Continuous security monitoring and threat intelligence

### 11. BUSINESS CONTINUITY SECURITY REQUIREMENTS
- **Disaster Recovery Security**: Security controls for disaster recovery procedures
- **Backup Security**: Encrypted and verified backup procedures
- **Alternate Site Security**: Security controls for alternate processing sites
- **Supply Chain Security**: Third-party vendor security requirements
- **Crisis Management**: Security aspects of crisis management procedures

### 12. MOBILE AND REMOTE ACCESS SECURITY REQUIREMENTS
- **Mobile Device Management**: MDM for corporate mobile devices
- **Remote Access Security**: Secure remote access with endpoint protection
- **BYOD Security**: Bring-your-own-device security policies and controls
- **Cloud Access Security**: Secure access to cloud-based resources
- **Location-Based Access**: Geographic access restrictions where appropriate

### 13. THIRD-PARTY INTEGRATION SECURITY REQUIREMENTS
- **Partner Security**: Security requirements for business partner integrations
- **API Partner Security**: Secure API access for external partners
- **Data Sharing Security**: Secure data sharing agreements and controls
- **Vendor Risk Management**: Third-party vendor security risk assessment
- **Integration Security Testing**: Security testing of all external integrations

### 14. SECURITY TRAINING AND AWARENESS REQUIREMENTS
- **Security Awareness Training**: Mandatory annual security training for all users
- **Phishing Simulation**: Regular phishing simulation and training
- **Security Documentation**: Comprehensive security policies and procedures
- **Incident Reporting**: Clear procedures for security incident reporting
- **Security Culture**: Promotion of security-conscious organizational culture

Provide specific, measurable security requirements with clear acceptance criteria and compliance mappings suitable for security architects, compliance officers, and implementation teams.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_ui_requirements(self) -> str:
        """Generate user interface requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - User Interface Requirements Analysis

## UI Context
Modern user interface requirements for A1 Telekom Austria customer care system modernization.

## Current Technology Assessment
- **Legacy Technology**: GWT with ExtJS/GXT components requiring modernization
- **Target Technology**: Modern web frameworks with responsive design
- **User Base**: Customer service representatives, administrators, supervisors
- **Usage Patterns**: High-volume transaction processing, real-time operations

## User Interface Requirements Generation Request

Generate comprehensive traditional user interface requirements covering:

### 1. GENERAL UI REQUIREMENTS
- **Modern Design**: Contemporary, intuitive user interface design
- **Responsive Layout**: Adaptive layout for desktop, tablet, and mobile devices
- **Accessibility Compliance**: WCAG 2.1 AA accessibility standards compliance
- **Browser Compatibility**: Support for Chrome, Firefox, Safari, Edge latest versions
- **Performance**: Page load times under 3 seconds, smooth animations

### 2. NAVIGATION REQUIREMENTS
- **Consistent Navigation**: Uniform navigation structure across all modules
- **Breadcrumb Navigation**: Clear breadcrumb trails for complex workflows
- **Quick Access**: Configurable quick access toolbar for frequently used functions
- **Search Integration**: Global search functionality with auto-complete
- **Context-Sensitive Menus**: Right-click context menus for efficient operations

### 3. DASHBOARD REQUIREMENTS
- **Personalized Dashboards**: User-configurable dashboard layouts
- **Widget Library**: Extensible widget library for different data visualizations
- **Real-Time Updates**: Live data updates with WebSocket or polling mechanisms
- **Drill-Down Capabilities**: Interactive drill-down from summary to detail views
- **Export Functions**: Dashboard data export to PDF, Excel, and CSV formats

### 4. DATA PRESENTATION REQUIREMENTS
- **Data Grids**: Advanced data grids with sorting, filtering, and pagination
- **Form Layouts**: Intuitive form designs with logical field grouping
- **Data Visualization**: Charts, graphs, and statistical displays
- **Print Layouts**: Printer-friendly versions of reports and forms
- **Data Export**: Multiple export formats with formatting preservation

### 5. CUSTOMER CARE INTERFACE REQUIREMENTS
- **Customer Search**: Advanced customer search with multiple criteria
- **Customer Profile**: Comprehensive customer information display
- **Service History**: Chronological service interaction history
- **Quick Actions**: One-click actions for common customer service tasks
- **Case Management**: Visual case tracking and status management

### 6. WORKFLOW INTERFACE REQUIREMENTS
- **Process Visualization**: Visual workflow status and progress indicators
- **Task Management**: Personal and team task queues with prioritization
- **Approval Workflows**: Electronic approval interfaces with digital signatures
- **Notification Center**: Centralized notification and alert management
- **Collaboration Tools**: Built-in commenting and collaboration features

### 7. FORM INTERFACE REQUIREMENTS
- **Dynamic Forms**: Context-sensitive form fields based on business rules
- **Validation Feedback**: Real-time field validation with clear error messages
- **Auto-Complete**: Intelligent auto-completion for common field values
- **Field Dependencies**: Dynamic field enabling/disabling based on other fields
- **Save State Management**: Auto-save and draft functionality for long forms

### 8. REPORTING INTERFACE REQUIREMENTS
- **Report Builder**: Drag-and-drop report builder for business users
- **Parameter Interface**: Intuitive parameter selection for report generation
- **Schedule Management**: Report scheduling interface with flexible timing options
- **Report Preview**: Preview functionality before final report generation
- **Report Distribution**: Email and secure link distribution capabilities

### 9. ADMINISTRATIVE INTERFACE REQUIREMENTS
- **User Management**: Intuitive user creation, modification, and deletion interfaces
- **Role Management**: Visual role and permission management
- **System Configuration**: User-friendly system configuration interfaces
- **Monitoring Dashboards**: System health and performance monitoring displays
- **Audit Interfaces**: Audit log viewing and filtering capabilities

### 10. MOBILE INTERFACE REQUIREMENTS
- **Touch-Optimized**: Touch-friendly interface elements and gestures
- **Offline Capabilities**: Limited offline functionality for critical operations
- **Progressive Web App**: PWA features for app-like mobile experience
- **Location Services**: GPS integration for field service applications
- **Camera Integration**: Document capture and photo attachment capabilities

### 11. ACCESSIBILITY REQUIREMENTS
- **Screen Reader Support**: Full compatibility with JAWS, NVDA, and VoiceOver
- **Keyboard Navigation**: Complete keyboard-only navigation support
- **High Contrast**: High contrast mode for visually impaired users
- **Font Scaling**: Support for browser font scaling up to 200%
- **Color Blindness**: Color-blind friendly color schemes and indicators

### 12. PERFORMANCE UI REQUIREMENTS
- **Loading Indicators**: Clear loading states for all asynchronous operations
- **Progressive Loading**: Content prioritization and progressive enhancement
- **Lazy Loading**: On-demand loading of non-critical interface elements
- **Caching Strategy**: Client-side caching for frequently accessed data
- **Bandwidth Optimization**: Optimized assets and compressed resources

### 13. CUSTOMIZATION REQUIREMENTS
- **Theme Support**: Multiple visual themes with corporate branding
- **Layout Customization**: User-configurable interface layouts
- **Shortcut Keys**: Customizable keyboard shortcuts for power users
- **Default Preferences**: User-specific default values and preferences
- **Interface Density**: Adjustable interface density (compact, normal, comfortable)

### 14. INTEGRATION INTERFACE REQUIREMENTS
- **Embedded Widgets**: Integration with external systems through embedded widgets
- **Single Sign-On**: Seamless SSO experience across integrated applications
- **Context Passing**: Seamless context passing between integrated systems
- **Unified Search**: Cross-system search capabilities
- **Consistent Styling**: Visual consistency across integrated applications

### 15. ERROR HANDLING INTERFACE REQUIREMENTS
- **Error Prevention**: Interface design that prevents common user errors
- **Clear Error Messages**: User-friendly error messages with corrective guidance
- **Error Recovery**: Easy error recovery mechanisms and undo functionality
- **Help Integration**: Context-sensitive help and documentation access
- **Feedback Mechanisms**: User feedback collection and suggestion systems

Provide detailed UI specifications with wireframes, mockups, and implementation guidelines suitable for UX designers, front-end developers, and quality assurance teams.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_performance_requirements(self) -> str:
        """Generate performance requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Performance Requirements Analysis

## Performance Context
High-performance requirements for A1 Telekom Austria enterprise customer care system.

## System Scale and Load Expectations
- **Concurrent Users**: Up to 1,000 simultaneous customer service representatives
- **Daily Transactions**: 50,000+ customer interactions per day
- **Peak Load**: 150% of normal load during peak hours
- **Geographic Distribution**: Multiple data centers across Austria and Europe
- **24/7 Operations**: Continuous availability requirements

## Performance Requirements Generation Request

Generate comprehensive traditional performance requirements covering:

### 1. RESPONSE TIME REQUIREMENTS
- **Web Page Load**: Initial page load within 2 seconds under normal conditions
- **Subsequent Page Navigation**: Page transitions within 1 second
- **Form Submission**: Form processing and response within 3 seconds
- **Search Operations**: Customer search results within 2 seconds
- **Report Generation**: Standard reports within 30 seconds, complex reports within 2 minutes
- **API Response Times**: REST API calls respond within 500 milliseconds

### 2. THROUGHPUT REQUIREMENTS
- **Transaction Processing**: Minimum 100 transactions per second sustained
- **Concurrent User Support**: 1,000 concurrent users with less than 10% performance degradation
- **Database Throughput**: 500 database queries per second capability
- **File Processing**: Batch file processing at 10,000 records per minute
- **API Throughput**: 1,000 API calls per minute per endpoint

### 3. SCALABILITY REQUIREMENTS
- **Horizontal Scaling**: Linear performance scaling with additional servers
- **User Scaling**: Support 5,000 concurrent users with infrastructure expansion
- **Data Scaling**: Handle 100% annual data growth without performance degradation
- **Geographic Scaling**: Maintain performance across multiple data centers
- **Component Scaling**: Individual microservices scale independently

### 4. RESOURCE UTILIZATION REQUIREMENTS
- **CPU Utilization**: Average CPU utilization below 70% under normal load
- **Memory Usage**: RAM utilization below 80% with automatic garbage collection
- **Disk I/O**: Disk utilization below 80% with SSD storage for critical operations
- **Network Bandwidth**: Network utilization below 60% of available capacity
- **Database Connections**: Efficient connection pooling with maximum 100 concurrent connections

### 5. DATABASE PERFORMANCE REQUIREMENTS
- **Query Performance**: 95% of queries execute within 100 milliseconds
- **Complex Query Performance**: Reporting queries complete within 5 seconds
- **Index Performance**: Automatic index optimization and maintenance
- **Concurrent Access**: Support 200 concurrent database connections
- **Backup Performance**: Database backups complete within 2-hour window without performance impact

### 6. CACHING REQUIREMENTS
- **Application Caching**: 90% cache hit ratio for frequently accessed data
- **Database Query Caching**: Result caching for repeated queries
- **Static Content Caching**: CDN caching for static resources with 95% hit ratio
- **Session Caching**: Distributed session caching for user sessions
- **Cache Invalidation**: Intelligent cache invalidation within 30 seconds of data updates

### 7. NETWORK PERFORMANCE REQUIREMENTS
- **Bandwidth Requirements**: Minimum 100 Mbps per 100 concurrent users
- **Latency Requirements**: Network latency under 50ms within regional data centers
- **CDN Performance**: Content delivery network with 99.9% availability
- **Compression**: HTTP compression reducing payload size by minimum 60%
- **Connection Management**: HTTP/2 support with connection multiplexing

### 8. LOAD BALANCING REQUIREMENTS
- **Load Distribution**: Intelligent load balancing across multiple servers
- **Health Monitoring**: Automatic detection and routing around failed servers
- **Session Affinity**: Sticky sessions where required for application functionality
- **Failover Performance**: Automatic failover within 30 seconds
- **Geographic Load Balancing**: Traffic routing to nearest data center

### 9. BATCH PROCESSING PERFORMANCE REQUIREMENTS
- **ETL Performance**: Extract, Transform, Load processes complete within 4-hour window
- **File Processing**: Large file processing at minimum 1 GB per hour
- **Scheduled Jobs**: Batch job completion within allocated time windows
- **Parallel Processing**: Multi-threaded processing for large datasets
- **Resource Management**: Batch processing without impacting online performance

### 10. BACKUP AND RECOVERY PERFORMANCE REQUIREMENTS
- **Backup Performance**: Full system backup within 6-hour window
- **Incremental Backup**: Incremental backups within 1-hour window
- **Recovery Performance**: Database recovery within 2 hours for full restore
- **Point-in-Time Recovery**: Recovery to specific point within 1 hour
- **Backup Verification**: Backup integrity verification within 30 minutes

### 11. MONITORING AND ALERTING PERFORMANCE REQUIREMENTS
- **Real-Time Monitoring**: Performance metrics updated every 30 seconds
- **Alert Response**: Performance alerts triggered within 2 minutes of threshold breach
- **Metric Collection**: System metrics collection with minimal performance overhead
- **Dashboard Performance**: Monitoring dashboards load within 5 seconds
- **Historical Reporting**: Performance trend reports generate within 1 minute

### 12. INTEGRATION PERFORMANCE REQUIREMENTS
- **External API Performance**: Third-party API integration responses within 5 seconds
- **Message Queue Performance**: Message processing with 1000 messages per second throughput
- **File Transfer Performance**: Secure file transfers at minimum 10 MB per second
- **Synchronization Performance**: Data synchronization between systems within 5 minutes
- **Web Service Performance**: SOAP and REST web services respond within 2 seconds

### 13. MOBILE PERFORMANCE REQUIREMENTS
- **Mobile Response Time**: Mobile interface loads within 3 seconds on 4G networks
- **Offline Performance**: Cached operations perform within 1 second
- **Synchronization**: Mobile data sync completes within 30 seconds
- **Battery Optimization**: Mobile app optimized for minimal battery consumption
- **Data Usage**: Efficient data usage with compression and caching

### 14. STRESS TESTING REQUIREMENTS
- **Load Testing**: Regular load testing at 150% of expected capacity
- **Stress Testing**: System remains stable at 200% of normal load
- **Volume Testing**: Handle 10x normal data volumes without failure
- **Endurance Testing**: 72-hour continuous operation without performance degradation
- **Spike Testing**: Handle sudden load spikes of 300% for 15-minute periods

### 15. PERFORMANCE OPTIMIZATION REQUIREMENTS
- **Code Optimization**: Regular code profiling and optimization
- **Query Optimization**: Database query performance tuning
- **Resource Optimization**: Memory and CPU usage optimization
- **Network Optimization**: Payload minimization and compression
- **Continuous Improvement**: Regular performance analysis and enhancement

Provide specific, measurable performance requirements with baseline metrics, target goals, and monitoring procedures suitable for performance engineers, system administrators, and development teams.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_entity_specific_requirements(self) -> int:
        """Generate requirements for each discovered entity"""
        entities = self.data_structures.get('entities', [])
        entity_count = 0
        
        for entity in entities:
            entity_name = entity.get('name', 'Unknown')
            
            # Generate entity-specific requirements
            entity_reqs = await self._generate_single_entity_requirements(entity)
            
            # Save entity requirements
            filename = f"{entity_name.lower()}_entity_requirements.md"
            with open(self.output_dir / "entities" / filename, 'w') as f:
                f.write(f"# {entity_name} Entity Requirements\n\n")
                f.write(f"**Generated**: {datetime.now().isoformat()}\n")
                f.write(f"**Entity Type**: Business Entity\n")
                f.write(f"**Package**: {entity.get('package_name', 'Unknown')}\n")
                f.write(f"**Domain**: {entity.get('business_domain', 'General')}\n\n")
                f.write(entity_reqs)
            
            entity_count += 1
        
        logger.info(f"📊 Generated requirements for {entity_count} entities")
        return entity_count

    async def _generate_single_entity_requirements(self, entity: Dict[str, Any]) -> str:
        """Generate requirements for a single entity"""
        
        entity_name = entity.get('name', 'Unknown')
        fields = entity.get('fields', [])
        
        context = f"""
# {entity_name} Entity Requirements Analysis

## Entity Overview
- **Name**: {entity_name}
- **Package**: {entity.get('package_name', 'Unknown')}
- **Business Domain**: {entity.get('business_domain', 'General')}
- **Field Count**: {len(fields)}
- **Complexity Score**: {entity.get('complexity_score', 0)}

## Field Analysis
"""
        
        for field in fields:
            context += f"""
### Field: {field.get('name', 'Unknown')}
- **Type**: {field.get('type', 'Unknown')}
- **Annotations**: {', '.join(field.get('annotations', []))}
- **Collection**: {field.get('is_collection', False)}
- **Relationship**: {field.get('is_relationship', False)}
"""
        
        context += f"""
## Entity Requirements Generation Request

Generate comprehensive traditional requirements for the {entity_name} entity covering:

### 1. FUNCTIONAL REQUIREMENTS
- **CRUD Operations**: Create, Read, Update, Delete operations for {entity_name}
- **Business Logic**: Entity-specific business rules and validations
- **Lifecycle Management**: Entity state management and transitions
- **Relationship Management**: Foreign key relationships and constraints
- **Search Capabilities**: Entity search and filtering requirements

### 2. DATA REQUIREMENTS  
- **Data Model**: Complete data model specification with all fields
- **Validation Rules**: Field-level and entity-level validation requirements
- **Constraints**: Business rule constraints and referential integrity
- **Indexing**: Database indexing strategy for performance optimization
- **Archival**: Data archival and retention policies for {entity_name}

### 3. API REQUIREMENTS
- **REST Endpoints**: RESTful API endpoints for {entity_name} operations
- **Request/Response**: Detailed API request and response specifications
- **Error Handling**: API error handling and status codes
- **Pagination**: Large dataset pagination and filtering
- **Security**: API security and access control requirements

### 4. USER INTERFACE REQUIREMENTS
- **Forms**: {entity_name} creation and editing forms with validation
- **List Views**: {entity_name} listing with search and filter capabilities
- **Detail Views**: Comprehensive {entity_name} detail display
- **Relationship Views**: Related entity display and navigation
- **Bulk Operations**: Mass operations on multiple {entity_name} records

### 5. INTEGRATION REQUIREMENTS
- **External Systems**: Integration points with external systems
- **Data Synchronization**: Real-time and batch synchronization needs
- **Import/Export**: Data import and export capabilities
- **Message Processing**: Event-driven updates and notifications
- **Third-party APIs**: External service integration requirements

### 6. PERFORMANCE REQUIREMENTS
- **Query Performance**: Database query optimization for {entity_name}
- **Caching Strategy**: Entity caching for improved performance
- **Bulk Processing**: Efficient bulk operations and batch processing
- **Concurrent Access**: Multi-user concurrent access handling
- **Scalability**: Performance scaling with data volume growth

### 7. SECURITY REQUIREMENTS
- **Access Control**: Role-based access control for {entity_name} operations
- **Data Privacy**: Personal data protection and privacy compliance
- **Audit Trail**: Complete audit logging for all {entity_name} operations
- **Field-level Security**: Sensitive field access restrictions
- **Data Encryption**: Encryption requirements for sensitive {entity_name} data

### 8. REPORTING REQUIREMENTS
- **Standard Reports**: Common {entity_name} reports and analytics
- **Custom Reports**: Flexible reporting capabilities
- **Real-time Dashboards**: {entity_name} metrics and KPI displays
- **Data Export**: Export capabilities in multiple formats
- **Historical Analysis**: Trend analysis and historical reporting

Provide detailed, implementable requirements with specific acceptance criteria for each category.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_business_rules_requirements(self) -> str:
        """Generate business rules requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Business Rules Requirements Analysis

## Business Rules Context
Comprehensive business rules management for A1 Telekom Austria customer care operations.

## System Business Context
- **Industry**: Telecommunications services
- **Business Model**: B2C and B2B customer care services
- **Regulatory Environment**: Austrian and EU telecommunications regulations
- **Operational Scope**: Customer lifecycle management, service provisioning, billing, support

## Business Rules Requirements Generation Request

Generate comprehensive traditional business rules requirements covering:

### 1. CUSTOMER MANAGEMENT BUSINESS RULES
- **Customer Registration**: Rules for new customer registration and validation
- **Customer Classification**: Business and residential customer categorization rules
- **Customer Status Management**: Active, suspended, terminated customer status rules
- **Customer Hierarchy**: Corporate customer hierarchy and relationship rules
- **Credit Assessment**: Customer creditworthiness evaluation and limits

### 2. SERVICE PROVISIONING BUSINESS RULES
- **Service Eligibility**: Rules determining customer service eligibility
- **Service Configuration**: Valid service configuration combinations and constraints
- **Service Dependencies**: Rules for service interdependencies and prerequisites
- **Service Lifecycle**: Service activation, modification, and termination rules
- **Service Level Agreements**: SLA definition and compliance rules

### 3. PRICING AND BILLING BUSINESS RULES
- **Pricing Rules**: Dynamic pricing based on customer type, volume, and promotions
- **Discount Application**: Business rules for discount eligibility and calculation
- **Billing Cycle Management**: Billing frequency and cycle management rules
- **Payment Terms**: Payment due dates, grace periods, and penalty calculations
- **Revenue Recognition**: Revenue recognition rules for different service types

### 4. ORDER MANAGEMENT BUSINESS RULES
- **Order Validation**: Rules for order completeness and accuracy validation
- **Order Routing**: Automatic order routing based on service type and complexity
- **Order Priority**: Business rules for order prioritization and scheduling
- **Order Fulfillment**: Rules governing order fulfillment processes and timelines
- **Order Cancellation**: Cancellation policies and refund calculation rules

### 5. SUPPORT AND CASE MANAGEMENT BUSINESS RULES
- **Case Classification**: Automatic case classification and severity assignment
- **Escalation Rules**: Automatic escalation based on case age, type, and customer tier
- **Resolution Timeframes**: Service level commitments for different case types
- **Case Routing**: Intelligent case routing to appropriate support teams
- **Customer Communication**: Rules for customer notification and update frequencies

### 6. REGULATORY COMPLIANCE BUSINESS RULES
- **Data Protection**: GDPR compliance rules for personal data handling
- **Telecommunications Regulations**: Austrian telecommunications authority compliance
- **Number Portability**: Mobile number portability process rules
- **Universal Service**: Universal service obligation compliance rules
- **Consumer Protection**: Consumer rights and protection regulation compliance

### 7. QUALITY ASSURANCE BUSINESS RULES
- **Service Quality Monitoring**: Rules for service quality measurement and thresholds
- **Performance Benchmarks**: KPI targets and performance measurement rules
- **Customer Satisfaction**: Customer satisfaction measurement and improvement rules
- **Quality Incident Management**: Quality incident detection and response rules
- **Continuous Improvement**: Business rules for process improvement initiatives

### 8. RISK MANAGEMENT BUSINESS RULES
- **Credit Risk**: Rules for customer credit risk assessment and management
- **Operational Risk**: Business continuity and operational risk mitigation rules
- **Fraud Detection**: Automated fraud detection and prevention rules
- **Security Compliance**: Information security and access control rules
- **Vendor Risk**: Third-party vendor risk assessment and management rules

### 9. WORKFLOW AND APPROVAL BUSINESS RULES
- **Approval Hierarchies**: Rules for approval workflows based on transaction value and type
- **Authority Limits**: Employee authority limits for different business decisions
- **Workflow Routing**: Intelligent workflow routing based on business context
- **Exception Handling**: Rules for handling workflow exceptions and escalations
- **Audit Requirements**: Business rules requiring audit trail and documentation

### 10. INTEGRATION BUSINESS RULES
- **Data Synchronization**: Rules for maintaining data consistency across systems
- **System Integration**: Business rules governing inter-system communication
- **Partner Integration**: Rules for business partner data exchange and workflows
- **External Service Integration**: Rules for third-party service integration and failover
- **Legacy System Integration**: Rules for legacy system data migration and synchronization

### 11. PERFORMANCE AND CAPACITY BUSINESS RULES
- **Resource Allocation**: Rules for system resource allocation and prioritization
- **Capacity Planning**: Business rules for capacity planning and scaling decisions
- **Performance Monitoring**: Rules for performance threshold monitoring and alerting
- **Load Balancing**: Business rules for load distribution and traffic management
- **Disaster Recovery**: Rules for disaster recovery activation and procedures

### 12. BUSINESS RULE MANAGEMENT REQUIREMENTS
- **Rule Definition**: Structured approach to defining and documenting business rules
- **Rule Versioning**: Version control and change management for business rules
- **Rule Testing**: Comprehensive testing requirements for business rule changes
- **Rule Deployment**: Controlled deployment process for business rule updates
- **Rule Monitoring**: Monitoring and metrics for business rule effectiveness

### 13. EXCEPTION HANDLING BUSINESS RULES
- **Business Exception Classification**: Categorization of business exceptions and handling procedures
- **Override Procedures**: Rules for business rule overrides and manual interventions
- **Escalation Procedures**: Escalation rules for unresolved business exceptions
- **Compensation Procedures**: Rules for customer compensation and service credits
- **Communication Rules**: Customer and stakeholder communication for business exceptions

### 14. BUSINESS CONTINUITY BUSINESS RULES
- **Service Continuity**: Rules ensuring continuous service delivery during disruptions
- **Data Recovery**: Business rules for data recovery and system restoration
- **Alternative Procedures**: Manual procedures when automated systems are unavailable
- **Communication Protocols**: Rules for crisis communication and stakeholder notification
- **Recovery Priorities**: Business rules defining recovery priorities and sequences

Provide detailed business rules with specific conditions, actions, and exception handling suitable for business analysts, process owners, and system implementers.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_compliance_requirements(self) -> str:
        """Generate compliance requirements"""
        
        context = f"""
# A1 Telekom Austria CuCo - Compliance Requirements Analysis

## Compliance Context
Comprehensive regulatory and industry compliance requirements for A1 Telekom Austria customer care system.

## Regulatory Environment
- **Austrian Telecommunications Regulations**: RTR-GmbH regulatory compliance
- **European Union Regulations**: EU-wide telecommunications and data protection laws
- **Data Protection**: GDPR and Austrian data protection regulations
- **Industry Standards**: ISO, SOC, and telecommunications industry standards
- **Corporate Compliance**: A1 Telekom Austria internal compliance policies

## Compliance Requirements Generation Request

Generate comprehensive traditional compliance requirements covering:

### 1. GDPR DATA PROTECTION COMPLIANCE REQUIREMENTS
- **Lawful Basis**: Establish lawful basis for all personal data processing activities
- **Data Subject Rights**: Implement right to access, rectification, erasure, and portability
- **Consent Management**: Granular consent collection, storage, and withdrawal mechanisms
- **Data Protection Impact Assessment**: DPIA procedures for high-risk processing activities
- **Data Breach Notification**: 72-hour breach notification to supervisory authorities

### 2. TELECOMMUNICATIONS REGULATORY COMPLIANCE REQUIREMENTS
- **Number Portability**: Compliance with mobile number portability regulations
- **Universal Service**: Universal service obligation compliance and reporting
- **Emergency Services**: Emergency call (112) service requirements and location data
- **Consumer Protection**: Telecommunications consumer protection regulation compliance
- **Market Analysis**: Regulatory reporting for market analysis and competition monitoring

### 3. FINANCIAL COMPLIANCE REQUIREMENTS
- **Revenue Recognition**: Compliance with accounting standards for revenue recognition
- **Tax Compliance**: VAT calculation and reporting compliance across EU jurisdictions
- **Financial Reporting**: Regulatory financial reporting requirements
- **Anti-Money Laundering**: AML compliance for high-value transactions and customer verification
- **Payment Services**: PSD2 compliance for payment processing and customer authentication

### 4. AUDIT AND RECORD KEEPING COMPLIANCE REQUIREMENTS
- **Audit Trail**: Comprehensive audit trail for all system activities and data changes
- **Record Retention**: Regulatory record retention periods and secure storage requirements
- **Audit Access**: Regulatory authority audit access and data provision capabilities
- **Documentation Standards**: Regulatory documentation standards and maintenance procedures
- **Evidence Preservation**: Legal hold and evidence preservation capabilities

### 5. SECURITY AND PRIVACY COMPLIANCE REQUIREMENTS
- **Information Security**: ISO 27001 compliance for information security management
- **Access Control**: Regulatory access control requirements and identity management
- **Encryption Standards**: Regulatory encryption requirements for data protection
- **Security Incident Reporting**: Regulatory security incident notification requirements
- **Privacy by Design**: Privacy-by-design implementation throughout system architecture

### 6. CUSTOMER PROTECTION COMPLIANCE REQUIREMENTS
- **Fair Trading**: Fair trading practices and transparent pricing compliance
- **Contract Terms**: Regulatory requirements for customer contract terms and conditions
- **Complaint Handling**: Regulatory complaint handling procedures and timeframes
- **Service Quality**: Minimum service quality standards and performance monitoring
- **Accessibility**: Accessibility requirements for customers with disabilities

### 7. ENVIRONMENTAL COMPLIANCE REQUIREMENTS
- **Energy Efficiency**: Energy efficiency reporting and optimization requirements
- **Electronic Waste**: E-waste management and recycling compliance
- **Carbon Footprint**: Carbon footprint reporting and reduction initiatives
- **Sustainable Operations**: Environmental sustainability in business operations
- **Green IT**: Green IT practices and environmental impact minimization

### 8. EMPLOYMENT AND LABOR COMPLIANCE REQUIREMENTS
- **Data Protection for Employees**: Employee personal data protection and privacy rights
- **Working Time Regulations**: EU working time directive compliance for system access logs
- **Equal Opportunity**: Equal opportunity and non-discrimination in system access and usage
- **Health and Safety**: Occupational health and safety compliance for system users
- **Training Requirements**: Mandatory regulatory training and certification tracking

### 9. CROSS-BORDER COMPLIANCE REQUIREMENTS
- **Data Transfer**: International data transfer compliance and adequacy decisions
- **Multi-Jurisdictional Operations**: Compliance across multiple European jurisdictions
- **Treaty Obligations**: International treaty and agreement compliance
- **Customs and Trade**: Cross-border service delivery compliance requirements
- **Tax Treaties**: International tax treaty compliance for cross-border services

### 10. INDUSTRY STANDARDS COMPLIANCE REQUIREMENTS
- **ISO Standards**: ISO 9001, 27001, and 20000 compliance implementation
- **SOC Compliance**: SOC 2 Type II compliance for service organization controls
- **ITIL Standards**: ITIL framework compliance for IT service management
- **Telecommunications Standards**: ITU-T and ETSI telecommunications standards compliance
- **Quality Standards**: Quality management system compliance and certification

### 11. BUSINESS CONTINUITY COMPLIANCE REQUIREMENTS
- **Disaster Recovery**: Regulatory disaster recovery and business continuity requirements
- **Service Continuity**: Minimum service availability requirements and reporting
- **Crisis Management**: Crisis management and communication compliance requirements
- **Risk Management**: Enterprise risk management framework compliance
- **Insurance Requirements**: Regulatory insurance coverage and claims procedures

### 12. VENDOR AND PARTNER COMPLIANCE REQUIREMENTS
- **Third-Party Risk Management**: Due diligence and ongoing monitoring of vendors and partners
- **Contractual Compliance**: Regulatory requirements in vendor and partner contracts
- **Data Processing Agreements**: GDPR-compliant data processing agreements with partners
- **Supply Chain Compliance**: Supply chain transparency and compliance verification
- **Subcontractor Management**: Regulatory requirements for subcontractor oversight

### 13. REPORTING AND DISCLOSURE COMPLIANCE REQUIREMENTS
- **Regulatory Reporting**: Automated regulatory reporting to relevant authorities
- **Transparency Reporting**: Public transparency reports on government requests and compliance
- **Performance Reporting**: Service performance reporting to regulatory bodies
- **Incident Reporting**: Mandatory incident reporting to appropriate authorities
- **Statistical Reporting**: Market statistics and operational data reporting requirements

### 14. COMPLIANCE MONITORING AND MANAGEMENT REQUIREMENTS
- **Compliance Dashboard**: Real-time compliance monitoring and reporting dashboard
- **Policy Management**: Centralized policy management and version control
- **Training Management**: Compliance training tracking and certification management
- **Assessment Procedures**: Regular compliance assessment and gap analysis procedures
- **Remediation Tracking**: Compliance violation remediation and corrective action tracking

### 15. EMERGING COMPLIANCE REQUIREMENTS
- **Digital Services Act**: EU Digital Services Act compliance preparation
- **AI Regulation**: EU AI regulation compliance for artificial intelligence systems
- **Cybersecurity Directive**: NIS2 directive compliance for network and information security
- **Data Governance Act**: EU Data Governance Act compliance for data sharing and reuse
- **ePrivacy Regulation**: Preparation for EU ePrivacy regulation implementation

Provide specific compliance requirements with regulatory citations, implementation guidelines, and monitoring procedures suitable for compliance officers, legal teams, and system implementers.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_master_traditional_document(self):
        """Generate master traditional requirements document"""
        
        entities_count = len(self.data_structures.get('entities', []))
        relationships_count = len(self.data_structures.get('relationships', []))
        
        master_content = f"""# A1 Telekom Austria CuCo - Master Traditional Requirements Document

**Document Type**: Traditional Software Requirements Specification
**Generated**: {datetime.now().isoformat()}
**System**: A1 Telekom Austria Customer Care (CuCo) Enterprise System
**Analysis Scope**: {self.metadata.get('files_processed', 0)} files processed
**Data Structures**: {self.metadata.get('data_structures_found', 0)} identified
**Mode**: {self.mode}

## Document Overview

This master traditional requirements document provides comprehensive software requirements specifications for the A1 Telekom Austria Customer Care (CuCo) enterprise system. The document follows traditional software engineering practices and provides detailed functional and non-functional requirements suitable for enterprise software development.

## Executive Summary

The A1 Telekom Austria CuCo system modernization project requires comprehensive requirements documentation to guide the development of a modern, scalable, and compliant customer care solution. This document provides detailed requirements across all system domains, based on thorough analysis of the existing system architecture and business needs.

### Key Statistics
- **Business Entities**: {entities_count} entities requiring comprehensive management
- **Entity Relationships**: {relationships_count} complex relationships
- **Processing Mode**: {self.mode} configuration
- **Requirements Categories**: 10 major categories with detailed specifications

## Requirements Organization

### 1. Functional Requirements (`functional/`)
**Location**: `functional/functional_requirements.md`
- Complete functional specifications for all system capabilities
- User story definitions and acceptance criteria
- Business process requirements and workflows
- System behavior specifications

### 2. Non-Functional Requirements (`non_functional/`)
**Location**: `non_functional/non_functional_requirements.md`
- Performance, scalability, and reliability requirements
- Security and compliance specifications
- Usability and accessibility requirements
- Maintainability and supportability requirements

### 3. Data Requirements (`data/`)
**Location**: `data/data_requirements.md`
- Comprehensive data model specifications
- Database design requirements
- Data integrity and validation requirements
- Data migration and integration specifications

### 4. Integration Requirements (`integration/`)
**Location**: `integration/integration_requirements.md`
- External system integration specifications
- API design and implementation requirements
- Message processing and workflow integration
- Legacy system integration requirements

### 5. Security Requirements (`security/`)
**Location**: `security/security_requirements.md`
- Comprehensive security framework specifications
- Authentication and authorization requirements
- Data protection and privacy requirements
- Audit and compliance security measures

### 6. User Interface Requirements (`ui/`)
**Location**: `ui/user_interface_requirements.md`
- Modern web interface specifications
- User experience and accessibility requirements
- Mobile and responsive design requirements
- Interface integration specifications

### 7. Performance Requirements (`performance/`)
**Location**: `performance/performance_requirements.md`
- Detailed performance benchmarks and targets
- Scalability and capacity requirements
- Load balancing and failover specifications
- Performance monitoring requirements

### 8. Entity-Specific Requirements (`entities/`)
**Location**: `entities/[entity_name]_entity_requirements.md`
- Individual requirements for each of {entities_count} business entities
- Entity-specific CRUD operations and business rules
- Data validation and integrity requirements
- Entity lifecycle management specifications

### 9. Business Rules Requirements (`business/`)
**Location**: `business/business_rules_requirements.md`
- Comprehensive business rule specifications
- Workflow and approval process requirements
- Exception handling and escalation procedures
- Business continuity requirements

### 10. Compliance Requirements (`compliance/`)
**Location**: `compliance/compliance_requirements.md`
- GDPR and data protection compliance
- Telecommunications regulatory compliance
- Industry standards and certification requirements
- Audit and reporting compliance specifications

## Implementation Approach

### Phase 1: Foundation (Months 1-6)
**Priorities**:
1. Core data model implementation based on entity requirements
2. Basic security framework and authentication system
3. Primary user interface components
4. Essential integration interfaces

**Deliverables**:
- Database schema implementation
- User management and authentication system
- Core customer management interfaces
- Basic reporting capabilities

### Phase 2: Core Functionality (Months 7-12)
**Priorities**:
1. Complete functional requirements implementation
2. Advanced user interface features
3. Integration with external systems
4. Performance optimization and testing

**Deliverables**:
- Complete customer care functionality
- Advanced reporting and analytics
- External system integrations
- Performance-optimized system

### Phase 3: Advanced Features (Months 13-18)
**Priorities**:
1. Advanced analytics and business intelligence
2. Mobile application development
3. Advanced automation features
4. Compliance and audit capabilities

**Deliverables**:
- Business intelligence platform
- Mobile applications
- Automated workflow systems
- Comprehensive compliance framework

### Phase 4: Optimization and Enhancement (Months 19-24)
**Priorities**:
1. System optimization and performance tuning
2. Advanced security features
3. Integration optimization
4. Continuous improvement implementation

**Deliverables**:
- Optimized system performance
- Enhanced security measures
- Streamlined integrations
- Continuous improvement processes

## Quality Assurance and Testing

### Testing Requirements
- **Unit Testing**: Minimum 90% code coverage for all components
- **Integration Testing**: Comprehensive testing of all system integrations
- **Performance Testing**: Load testing at 150% of expected capacity
- **Security Testing**: Penetration testing and vulnerability assessment
- **User Acceptance Testing**: Comprehensive UAT with business stakeholders

### Quality Standards
- **Code Quality**: Adherence to established coding standards and best practices
- **Documentation**: Complete technical and user documentation
- **Compliance**: Full compliance with all regulatory and industry requirements
- **Performance**: Meeting all specified performance benchmarks
- **Security**: Implementation of comprehensive security measures

## Risk Management

### Technical Risks
- **Legacy System Complexity**: Mitigated through phased migration approach
- **Integration Challenges**: Addressed through comprehensive API design and testing
- **Performance Requirements**: Managed through performance testing and optimization
- **Security Compliance**: Ensured through comprehensive security framework

### Business Risks
- **User Adoption**: Mitigated through comprehensive training and change management
- **Business Continuity**: Addressed through parallel system operation during transition
- **Regulatory Compliance**: Managed through dedicated compliance framework
- **Timeline Pressures**: Controlled through agile methodology and regular stakeholder communication

## Success Criteria

### Technical Success Criteria
- 100% functional requirements implementation
- All performance benchmarks achieved
- Complete security and compliance framework
- Successful integration with all external systems

### Business Success Criteria
- Seamless user transition from legacy system
- Improved operational efficiency and productivity
- Enhanced customer service capabilities
- Full regulatory and compliance adherence

## Stakeholder Responsibilities

### Business Stakeholders
- Requirements review and approval
- User acceptance testing participation
- Change management and training support
- Business process validation

### Technical Teams
- Requirements implementation and development
- System testing and quality assurance
- Integration development and testing
- Performance optimization and tuning

### Compliance Teams
- Regulatory compliance validation
- Security framework implementation
- Audit preparation and support
- Policy and procedure development

## Document Control

### Version Management
- All requirements documents under version control
- Change management process for requirement updates
- Stakeholder approval required for major changes
- Traceability maintained throughout development lifecycle

### Review Process
- Regular requirements review sessions with stakeholders
- Technical review by development teams
- Compliance review by regulatory experts
- Final approval by project steering committee

## Next Steps

1. **Stakeholder Review**: Comprehensive review of all requirements documents
2. **Technical Architecture**: Detailed technical architecture design based on requirements
3. **Implementation Planning**: Detailed project planning and resource allocation
4. **Development Initiation**: Begin development based on approved requirements

This master document provides the foundation for successful implementation of the A1 Telekom Austria CuCo system modernization project, ensuring all requirements are clearly defined, traceable, and implementable.
"""
        
        with open(self.output_dir / "master_traditional_requirements.md", 'w') as f:
            f.write(master_content)

    async def _generate_traceability_matrix(self):
        """Generate requirements traceability matrix"""
        
        entities = self.data_structures.get('entities', [])
        
        traceability_content = f"""# A1 Telekom Austria CuCo - Requirements Traceability Matrix

**Generated**: {datetime.now().isoformat()}
**Purpose**: Track relationships between business requirements, system components, and implementation

## Traceability Matrix Overview

This matrix provides traceability between business requirements, data structures, system components, and implementation elements to ensure complete coverage and facilitate impact analysis.

## Business Entity to Requirement Traceability

| Entity Name | Package | Domain | Functional Req | Data Req | Security Req | UI Req | API Req |
|-------------|---------|--------|----------------|----------|--------------|--------|---------|
"""
        
        for entity in entities:
            entity_name = entity.get('name', 'Unknown')
            package = entity.get('package_name', 'Unknown')
            domain = entity.get('business_domain', 'General')
            
            traceability_content += f"| {entity_name} | {package} | {domain} | ✓ | ✓ | ✓ | ✓ | ✓ |\n"
        
        traceability_content += f"""
## Requirement Category Coverage

### Functional Requirements Coverage
- **Customer Management**: {len([e for e in entities if 'customer' in e.get('business_domain', '').lower()])} entities
- **Service Management**: {len([e for e in entities if 'product' in e.get('business_domain', '').lower()])} entities  
- **Billing Management**: {len([e for e in entities if 'billing' in e.get('business_domain', '').lower()])} entities
- **Order Management**: {len([e for e in entities if 'order' in e.get('business_domain', '').lower()])} entities
- **Support Management**: {len([e for e in entities if 'support' in e.get('business_domain', '').lower()])} entities

### Data Requirements Coverage
- **Total Entities**: {len(entities)} business entities
- **Entity Relationships**: {len(self.data_structures.get('relationships', []))} relationships
- **Data Validation Rules**: Comprehensive validation for all entities
- **Data Integration**: External system integration for all entities

### Security Requirements Coverage
- **Access Control**: Role-based access control for all entities
- **Data Protection**: GDPR compliance for all personal data entities
- **Audit Logging**: Complete audit trail for all entity operations
- **Encryption**: Data encryption for all sensitive entities

## Implementation Traceability

### Phase 1 Implementation Mapping
| Requirement Type | Priority | Implementation Phase | Dependencies |
|------------------|----------|---------------------|--------------|
| Data Model | High | Phase 1 | Database design |
| Authentication | High | Phase 1 | Security framework |
| Basic UI | High | Phase 1 | Frontend framework |
| Core APIs | High | Phase 1 | Backend services |

### Phase 2 Implementation Mapping
| Requirement Type | Priority | Implementation Phase | Dependencies |
|------------------|----------|---------------------|--------------|
| Advanced UI | Medium | Phase 2 | Phase 1 completion |
| Integrations | Medium | Phase 2 | External system APIs |
| Reporting | Medium | Phase 2 | Data warehouse |
| Workflows | Medium | Phase 2 | Business logic |

### Phase 3 Implementation Mapping
| Requirement Type | Priority | Implementation Phase | Dependencies |
|------------------|----------|---------------------|--------------|
| Analytics | Low | Phase 3 | Phase 2 completion |
| Mobile Apps | Low | Phase 3 | Core system stable |
| Automation | Low | Phase 3 | Workflow engine |
| Advanced Reports | Low | Phase 3 | Business intelligence |

## Test Coverage Traceability

### Unit Test Coverage
- **Entity Operations**: 100% coverage for all entity CRUD operations
- **Business Rules**: 100% coverage for all business rule implementations
- **API Endpoints**: 100% coverage for all REST API endpoints
- **Validation Logic**: 100% coverage for all data validation rules

### Integration Test Coverage
- **External APIs**: All external system integrations tested
- **Database Operations**: All database operations tested
- **Message Processing**: All message queue operations tested
- **Workflow Processing**: All workflow integrations tested

### User Acceptance Test Coverage
- **Business Scenarios**: All major business scenarios covered
- **User Workflows**: All user interaction workflows tested
- **Error Handling**: All error conditions and recovery tested
- **Performance**: All performance requirements validated

## Compliance Traceability

### GDPR Compliance Mapping
| Data Entity | Personal Data | Consent Required | Right to Erasure | Data Portability |
|-------------|---------------|------------------|-------------------|------------------|
"""
        
        for entity in entities:
            if 'customer' in entity.get('business_domain', '').lower():
                entity_name = entity.get('name', 'Unknown')
                traceability_content += f"| {entity_name} | ✓ | ✓ | ✓ | ✓ |\n"
        
        traceability_content += f"""
### Regulatory Compliance Mapping
- **Telecommunications Regulations**: All customer and service entities compliant
- **Data Protection**: All personal data entities GDPR compliant
- **Financial Regulations**: All billing entities compliant
- **Industry Standards**: ISO and SOC compliance implemented

## Change Impact Analysis

### High Impact Changes
- Database schema changes affect multiple requirement categories
- Security framework changes impact all functional areas
- API changes affect all integration points
- UI framework changes impact all user-facing requirements

### Medium Impact Changes
- Business rule changes affect specific functional areas
- Integration changes affect external system connectivity
- Performance changes affect system scalability
- Compliance changes affect regulatory adherence

### Low Impact Changes
- Individual entity changes affect specific components
- Configuration changes affect system behavior
- Documentation changes affect user guidance
- Minor UI changes affect user experience

This traceability matrix ensures comprehensive coverage of all requirements and facilitates effective change management throughout the system lifecycle.
"""
        
        with open(self.output_dir / "analysis" / "requirements_traceability_matrix.md", 'w') as f:
            f.write(traceability_content)

    async def _save_requirements(self, category: str, filename: str, content: str) -> int:
        """Save requirements content and return estimated requirement count"""
        
        category_dir = self.output_dir / category
        os.makedirs(category_dir, exist_ok=True)
        
        with open(category_dir / filename, 'w') as f:
            f.write(content)
        
        # Estimate requirement count based on content structure
        requirement_count = content.count('###') + content.count('**Requirement')
        return requirement_count

    async def _call_ollama_for_requirements(self, context: str) -> str:
        """Call Ollama API to generate requirements content"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.ollama_model,
                    "prompt": context,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 3072,
                        "top_k": 40,
                        "top_p": 0.9
                    }
                }
                
                async with session.post(f"{self.ollama_base_url}/api/generate", 
                                      json=payload,
                                      timeout=aiohttp.ClientTimeout(total=180)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'Requirements generation failed')
                    else:
                        return f"Error: HTTP {response.status}"
        except Exception as e:
            logger.error(f"Failed to call Ollama: {e}")
            return f"Error generating requirements: {e}"

    def __del__(self):
        """Cleanup Weaviate connection"""
        try:
            if hasattr(self, 'weaviate_client'):
                self.weaviate_client.close()
        except:
            pass