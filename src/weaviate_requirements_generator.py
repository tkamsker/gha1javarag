#!/usr/bin/env python3
"""
Weaviate Requirements Generator
Generates comprehensive requirements documentation using Weaviate vector database and data structure insights
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

class WeaviateRequirementsGenerator:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.requirements_dir = self.output_dir / "requirements_weaviate"
        
        # Initialize Weaviate client
        try:
            self.weaviate_client = weaviate.connect_to_local()
            logger.info("✅ Connected to Weaviate for requirements generation")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Weaviate: {e}")
            raise
        
        # Initialize Ollama client
        self.ollama_base_url = "http://localhost:11434"
        self.ollama_model = "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"

    async def generate_comprehensive_requirements(self, metadata: Dict[str, Any], data_structures: Dict[str, Any]):
        """Generate comprehensive requirements using Weaviate and data structure insights"""
        logger.info("📋 Generating comprehensive requirements with Weaviate and data structures...")
        
        # Create requirements directories
        os.makedirs(self.requirements_dir, exist_ok=True)
        os.makedirs(self.requirements_dir / "by_layer", exist_ok=True)
        os.makedirs(self.requirements_dir / "by_data_structure", exist_ok=True)
        os.makedirs(self.requirements_dir / "by_domain", exist_ok=True)
        os.makedirs(self.requirements_dir / "analysis", exist_ok=True)
        
        # Generate only basic requirements in Step 1 to avoid timeout
        await self._generate_data_driven_requirements(data_structures)
        
        logger.info("✅ Basic requirements generation completed")

    async def generate_full_requirements(self, metadata: Dict[str, Any], data_structures: Dict[str, Any]):
        """Generate full comprehensive requirements (for Step 2)"""
        logger.info("📋 Generating full comprehensive requirements...")
        
        # Generate all types of requirements
        await self._generate_layer_based_requirements(metadata)
        await self._generate_domain_based_requirements(data_structures)
        await self._generate_modernization_requirements(metadata, data_structures)
        await self._generate_integration_requirements(data_structures)
        
        # Generate master requirements document
        await self._generate_master_requirements_document(metadata, data_structures)
        
        logger.info("✅ Full comprehensive requirements generation completed")

    async def _generate_data_driven_requirements(self, data_structures: Dict[str, Any]):
        """Generate requirements based on discovered data structures - simplified for Step 1"""
        logger.info("🗃️ Generating data-driven requirements...")
        
        entities = data_structures.get('entities', [])
        dtos = data_structures.get('dtos', [])
        relationships = data_structures.get('relationships', [])
        
        # Generate simple summary requirements without AI calls
        summary_reqs = self._generate_simple_data_summary(entities, dtos, relationships)
        
        # Save basic data summary
        with open(self.requirements_dir / "by_data_structure" / "data_summary.md", 'w') as f:
            f.write(summary_reqs)
        
        logger.info(f"📊 Generated requirements for {len(entities)} entities and {len(dtos)} DTOs")

    def _generate_simple_data_summary(self, entities: List[Dict], dtos: List[Dict], relationships: List[Dict]) -> str:
        """Generate a simple data summary without AI calls"""
        summary = f"""# Data Structures Summary

## Overview
- **Entities Found**: {len(entities)}
- **DTOs Found**: {len(dtos)}
- **Relationships**: {len(relationships)}

## Entity Details
"""
        for entity in entities[:10]:  # Limit to first 10
            fields = entity.get('fields', [])
            summary += f"""
### {entity.get('name', 'Unknown')}
- **Package**: {entity.get('package_name', 'Unknown')}
- **Fields**: {len(fields)}
- **Business Domain**: {entity.get('business_domain', 'General')}
"""
            if fields:
                summary += "- **Key Fields**:\n"
                for field in fields[:5]:  # Top 5 fields
                    summary += f"  - {field.get('name', 'Unknown')}: {field.get('type', 'Unknown')}\n"

        summary += f"""
## DTO Details
"""
        for dto in dtos[:10]:  # Limit to first 10
            summary += f"""
### {dto.get('name', 'Unknown')}
- **Package**: {dto.get('package_name', 'Unknown')}
- **Fields**: {len(dto.get('fields', []))}
"""

        return summary

    async def _generate_entity_requirements(self, entity: Dict[str, Any]):
        """Generate requirements for a specific entity"""
        entity_name = entity.get('name', 'Unknown')
        
        context = f"""
# Entity Requirements Analysis: {entity_name}

## Entity Information
- **Name**: {entity_name}
- **Package**: {entity.get('package_name', 'Unknown')}
- **Business Domain**: {entity.get('business_domain', 'General')}
- **Fields Count**: {len(entity.get('fields', []))}
- **Complexity Score**: {entity.get('complexity_score', 0)}

## Fields Analysis
"""
        
        for field in entity.get('fields', []):
            context += f"""
### Field: {field.get('name', 'Unknown')}
- **Type**: {field.get('type', 'Unknown')}
- **Annotations**: {', '.join(field.get('annotations', []))}
- **Is Collection**: {field.get('is_collection', False)}
- **Is Relationship**: {field.get('is_relationship', False)}
"""
        
        context += f"""
## Relationships
{len(entity.get('relationships', []))} relationships identified.

## Requirements Generation Request
Based on this entity analysis, generate comprehensive functional requirements covering:

1. **Data Management Requirements**
   - CRUD operations for {entity_name}
   - Data validation rules
   - Field-specific constraints
   - Business rule enforcement

2. **Integration Requirements** 
   - API endpoints for {entity_name} operations
   - Data synchronization requirements
   - External system integration needs

3. **Security Requirements**
   - Access control for {entity_name} operations
   - Data privacy and protection requirements
   - Audit logging requirements

4. **Performance Requirements**
   - Query performance expectations
   - Caching requirements
   - Bulk operation handling

5. **User Interface Requirements**
   - Forms for {entity_name} creation/editing
   - List and search interfaces
   - Validation feedback mechanisms

Generate detailed, implementable requirements for this entity.
"""
        
        try:
            requirements_content = await self._call_ollama_for_requirements(context)
            
            with open(self.requirements_dir / "by_data_structure" / f"{entity_name.lower()}_requirements.md", 'w') as f:
                f.write(f"# {entity_name} Entity Requirements\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                f.write(requirements_content)
                
        except Exception as e:
            logger.error(f"Failed to generate requirements for entity {entity_name}: {e}")

    async def _generate_data_management_requirements(self, entities: List[Dict[str, Any]], 
                                                   relationships: List[Dict[str, Any]]) -> str:
        """Generate overall data management requirements"""
        
        context = f"""
# Data Management Requirements Analysis

## System Overview
Enterprise data management system with {len(entities)} primary entities and {len(relationships)} relationships.

## Entity Summary
"""
        
        for entity in entities[:10]:  # Top 10 entities
            context += f"""
### {entity.get('name', 'Unknown')}
- **Domain**: {entity.get('business_domain', 'General')}
- **Fields**: {len(entity.get('fields', []))}
- **Complexity**: {entity.get('complexity_score', 0)}
"""
        
        context += f"""
## Relationship Analysis
{len(relationships)} entity relationships identified, indicating complex data interdependencies.

## Requirements Generation Request
Generate comprehensive data management requirements covering:

1. **Data Architecture Requirements**
   - Entity relationship management
   - Data integrity constraints
   - Referential integrity rules
   - Cascade operation specifications

2. **Data Access Requirements**
   - Repository pattern implementation
   - Query optimization requirements
   - Caching strategy requirements
   - Transaction management

3. **Data Migration Requirements**
   - Legacy data migration specifications
   - Data transformation rules
   - Migration validation requirements
   - Rollback procedures

4. **Data Backup and Recovery Requirements**
   - Backup frequency and retention policies
   - Recovery time objectives (RTO)
   - Recovery point objectives (RPO)
   - Disaster recovery procedures

5. **Data Governance Requirements**
   - Data quality standards
   - Data lifecycle management
   - Data archiving policies
   - Compliance and audit requirements

6. **Performance Requirements**
   - Database query performance standards
   - Concurrent access requirements
   - Scalability requirements
   - Load balancing specifications

Generate detailed data management requirements suitable for enterprise implementation.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_data_validation_requirements(self, entities: List[Dict[str, Any]], 
                                                   dtos: List[Dict[str, Any]]) -> str:
        """Generate data validation requirements"""
        
        context = f"""
# Data Validation Requirements Analysis

## Validation Context
System with {len(entities)} entities and {len(dtos)} DTOs requiring comprehensive validation.

## Field Analysis Summary
"""
        
        validation_patterns = defaultdict(int)
        for entity in entities:
            for field in entity.get('fields', []):
                annotations = field.get('annotations', [])
                for annotation in annotations:
                    if any(val_ann in annotation.lower() for val_ann in ['valid', 'notnull', 'notempty', 'size', 'min', 'max', 'email', 'pattern']):
                        validation_patterns[annotation] += 1
        
        context += "Validation patterns found:\n"
        for pattern, count in validation_patterns.items():
            context += f"- {pattern}: {count} occurrences\n"
        
        context += f"""
## Requirements Generation Request
Generate comprehensive data validation requirements covering:

1. **Input Validation Requirements**
   - Field-level validation rules
   - Cross-field validation logic
   - Business rule validation
   - Format and pattern validation

2. **API Validation Requirements**
   - Request payload validation
   - Parameter validation
   - Response validation
   - Error handling and messaging

3. **Database Validation Requirements**
   - Constraint validation
   - Trigger-based validation
   - Referential integrity validation
   - Business rule enforcement

4. **User Interface Validation Requirements**
   - Real-time validation feedback
   - Form validation requirements
   - Error message display
   - Validation state management

5. **Integration Validation Requirements**
   - External data validation
   - Import/export validation
   - Data synchronization validation
   - Message queue validation

6. **Performance Requirements**
   - Validation performance standards
   - Bulk validation requirements
   - Asynchronous validation needs
   - Caching of validation rules

Generate detailed validation requirements with specific acceptance criteria.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_layer_based_requirements(self, metadata: Dict[str, Any]):
        """Generate requirements organized by architectural layers"""
        logger.info("🏗️ Generating layer-based requirements...")
        
        # Generate presentation layer requirements
        presentation_reqs = await self._generate_presentation_layer_requirements(metadata)
        with open(self.requirements_dir / "by_layer" / "presentation_layer_requirements.md", 'w') as f:
            f.write(presentation_reqs)
        
        # Generate business layer requirements
        business_reqs = await self._generate_business_layer_requirements(metadata)
        with open(self.requirements_dir / "by_layer" / "business_layer_requirements.md", 'w') as f:
            f.write(business_reqs)
        
        # Generate data layer requirements
        data_reqs = await self._generate_data_layer_requirements(metadata)
        with open(self.requirements_dir / "by_layer" / "data_layer_requirements.md", 'w') as f:
            f.write(data_reqs)

    async def _generate_presentation_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate presentation layer requirements"""
        
        context = f"""
# Presentation Layer Requirements Analysis

## Current Technology Assessment
Based on analysis of A1 Telekom Austria CuCo system with legacy GWT/ExtJS technology stack.

## System Context
- **Files Processed**: {metadata.get('files_processed', 0)}
- **Processing Time**: {metadata.get('processing_time', 0):.2f} seconds
- **Technology Stack**: Legacy GWT with ExtJS/GXT components

## Modernization Context
Legacy presentation layer requires modernization from GWT/ExtJS to contemporary web technologies.

## Requirements Generation Request
Generate comprehensive presentation layer requirements covering:

1. **User Interface Framework Requirements**
   - Modern JavaScript framework selection (React, Vue.js, Angular)
   - Component library requirements
   - State management requirements
   - Routing and navigation requirements

2. **User Experience Requirements**
   - Responsive design specifications
   - Accessibility compliance (WCAG 2.1 AA)
   - Browser compatibility requirements
   - Performance optimization requirements

3. **Customer Care Interface Requirements**
   - Agent dashboard specifications
   - Customer information display
   - Service request management interfaces
   - Real-time notification systems

4. **Administrative Interface Requirements**
   - System configuration interfaces
   - User management interfaces
   - Reporting and analytics dashboards
   - Bulk operation interfaces

5. **Mobile and Device Requirements**
   - Mobile-responsive design
   - Touch-friendly interactions
   - Offline capability requirements
   - Progressive Web App features

6. **Integration Requirements**
   - API integration patterns
   - Real-time data updates
   - WebSocket communication
   - Authentication integration

Generate detailed presentation layer requirements suitable for modern web application development.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_business_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate business layer requirements"""
        
        context = f"""
# Business Layer Requirements Analysis

## A1 Telekom Austria CuCo System Context
Customer Care operations requiring robust business logic implementation.

## System Analysis Results
- **Processing Time**: {metadata.get('processing_time', 0):.2f} seconds
- **Files Analyzed**: {metadata.get('files_processed', 0)}
- **Data Structures**: {metadata.get('data_structures_found', 0)} identified

## Requirements Generation Request
Generate comprehensive business layer requirements covering:

1. **Customer Care Business Logic**
   - Customer account management rules
   - Service provisioning workflows
   - Billing integration logic
   - Support ticket management

2. **Service Layer Architecture**
   - Business service specifications
   - Transaction management requirements
   - Business rule engine requirements
   - Workflow orchestration needs

3. **Integration Business Logic**
   - External system integration rules
   - Data synchronization logic
   - Message processing requirements
   - Event handling specifications

4. **Validation and Business Rules**
   - Business rule validation engine
   - Complex validation workflows
   - Approval process requirements
   - Audit trail specifications

5. **Performance and Scalability**
   - Business logic performance requirements
   - Caching strategies for business data
   - Asynchronous processing needs
   - Load balancing requirements

6. **Security and Compliance**
   - Business-level security requirements
   - Data privacy compliance
   - Regulatory compliance requirements
   - Audit and logging specifications

Generate detailed business layer requirements with clear implementation guidance.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_data_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate data layer requirements"""
        
        context = f"""
# Data Layer Requirements Analysis

## System Data Context
Enterprise data layer for A1 Telekom Austria Customer Care system.

## Analysis Results
- **Data Structures Found**: {metadata.get('data_structures_found', 0)}
- **Entity Relationships**: {metadata.get('entity_relationships', 0)}
- **Files Processed**: {metadata.get('files_processed', 0)}

## Requirements Generation Request
Generate comprehensive data layer requirements covering:

1. **Database Architecture Requirements**
   - Database technology selection
   - Schema design requirements
   - Indexing strategy requirements
   - Partitioning specifications

2. **Data Access Layer Requirements**
   - Repository pattern implementation
   - ORM configuration requirements
   - Query optimization specifications
   - Connection pooling requirements

3. **Data Migration Requirements**
   - Legacy data migration strategy
   - Data transformation specifications
   - Migration validation requirements
   - Incremental migration support

4. **Data Integrity Requirements**
   - Referential integrity constraints
   - Business rule constraints
   - Data validation at database level
   - Trigger specifications

5. **Performance Requirements**
   - Query performance standards
   - Bulk operation requirements
   - Caching layer specifications
   - Database monitoring requirements

6. **Backup and Recovery Requirements**
   - Backup strategy specifications
   - Recovery procedures
   - High availability requirements
   - Disaster recovery planning

Generate detailed data layer requirements with specific technical specifications.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_domain_based_requirements(self, data_structures: Dict[str, Any]):
        """Generate requirements organized by business domain"""
        logger.info("🏢 Generating domain-based requirements...")
        
        # Analyze business domains from data structures
        summary = data_structures.get('summary', {})
        business_domains = summary.get('business_domains', {})
        
        for domain, entities in business_domains.get('entities_by_domain', {}).items():
            if domain != 'general' and entities:
                domain_reqs = await self._generate_domain_requirements(domain, entities, data_structures)
                
                with open(self.requirements_dir / "by_domain" / f"{domain}_domain_requirements.md", 'w') as f:
                    f.write(domain_reqs)

    async def _generate_domain_requirements(self, domain: str, entities: List[str], 
                                          data_structures: Dict[str, Any]) -> str:
        """Generate requirements for a specific business domain"""
        
        context = f"""
# {domain.title()} Domain Requirements Analysis

## Domain Context
Business domain analysis for {domain} with {len(entities)} related entities.

## Domain Entities
"""
        
        for entity_name in entities[:5]:  # Limit to first 5 entities
            context += f"- {entity_name}\n"
        
        if len(entities) > 5:
            context += f"... and {len(entities) - 5} more entities\n"
        
        context += f"""
## Requirements Generation Request
Generate comprehensive requirements for the {domain} business domain covering:

1. **Domain-Specific Functional Requirements**
   - Core {domain} business processes
   - Domain-specific workflows
   - Business rule implementations
   - Integration requirements within domain

2. **Data Management Requirements**
   - {domain}-specific data models
   - Domain data validation rules
   - Data relationships within domain
   - Domain-specific reporting needs

3. **User Interface Requirements**
   - {domain}-focused user interfaces
   - Domain-specific dashboards
   - {domain} workflow interfaces
   - Domain reporting interfaces

4. **Integration Requirements**
   - External system integrations for {domain}
   - Cross-domain data synchronization
   - {domain}-specific API requirements
   - Message processing for {domain}

5. **Performance Requirements**
   - {domain}-specific performance needs
   - Scalability requirements for {domain}
   - Caching strategies for {domain} data
   - Load balancing for {domain} operations

6. **Security and Compliance**
   - {domain}-specific security requirements
   - Regulatory compliance for {domain}
   - Data privacy in {domain} context
   - Audit requirements for {domain}

Generate detailed domain-specific requirements with clear business context.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_modernization_requirements(self, metadata: Dict[str, Any], 
                                                 data_structures: Dict[str, Any]):
        """Generate modernization requirements"""
        logger.info("🔄 Generating modernization requirements...")
        
        modernization_reqs = await self._generate_comprehensive_modernization_requirements(metadata, data_structures)
        
        with open(self.requirements_dir / "analysis" / "modernization_requirements.md", 'w') as f:
            f.write(modernization_reqs)

    async def _generate_comprehensive_modernization_requirements(self, metadata: Dict[str, Any], 
                                                               data_structures: Dict[str, Any]) -> str:
        """Generate comprehensive modernization requirements"""
        
        context = f"""
# Modernization Requirements Analysis

## Legacy System Context
A1 Telekom Austria CuCo system modernization from GWT/ExtJS to contemporary architecture.

## Current System Analysis
- **Files Analyzed**: {metadata.get('files_processed', 0)}
- **Data Structures**: {metadata.get('data_structures_found', 0)} identified
- **Processing Time**: {metadata.get('processing_time', 0):.2f} seconds

## Legacy Technology Stack
- Frontend: GWT with ExtJS/GXT components
- Backend: Java Enterprise with Spring Framework
- Data Access: iBATIS/MyBatis
- Architecture: Monolithic multi-module structure

## Requirements Generation Request
Generate comprehensive modernization requirements covering:

1. **Frontend Modernization Requirements**
   - Migration from GWT to modern JavaScript framework
   - Component-based architecture implementation
   - State management modernization
   - Progressive Web App capabilities

2. **Backend Modernization Requirements**
   - Microservices architecture transition
   - API-first design implementation
   - Spring Boot modernization
   - Cloud-native architecture requirements

3. **Data Layer Modernization Requirements**
   - Modern ORM implementation (JPA/Hibernate)
   - Database modernization strategy
   - Data migration requirements
   - NoSQL integration where appropriate

4. **Architecture Modernization Requirements**
   - Containerization strategy (Docker/Kubernetes)
   - CI/CD pipeline implementation
   - Cloud deployment requirements
   - Monitoring and observability

5. **Integration Modernization Requirements**
   - REST API standardization
   - Message queue implementation
   - Event-driven architecture
   - External system integration modernization

6. **Security Modernization Requirements**
   - Modern authentication/authorization (OAuth2, JWT)
   - Security framework updates
   - Compliance requirements
   - Zero-trust architecture principles

7. **Performance and Scalability Requirements**
   - Horizontal scaling capabilities
   - Performance optimization requirements
   - Caching strategy modernization
   - Load balancing and failover

8. **Migration Strategy Requirements**
   - Phased migration approach
   - Parallel system operation
   - Data migration strategy
   - User training and change management

Generate detailed modernization requirements with clear implementation roadmap.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_integration_requirements(self, data_structures: Dict[str, Any]):
        """Generate integration requirements"""
        logger.info("🔗 Generating integration requirements...")
        
        integration_reqs = await self._generate_comprehensive_integration_requirements(data_structures)
        
        with open(self.requirements_dir / "analysis" / "integration_requirements.md", 'w') as f:
            f.write(integration_reqs)

    async def _generate_comprehensive_integration_requirements(self, data_structures: Dict[str, Any]) -> str:
        """Generate comprehensive integration requirements"""
        
        entities_count = len(data_structures.get('entities', []))
        relationships_count = len(data_structures.get('relationships', []))
        
        context = f"""
# Integration Requirements Analysis

## Integration Context
A1 Telekom Austria CuCo system requiring comprehensive integration capabilities.

## Data Integration Context
- **Entities**: {entities_count} business entities requiring integration
- **Relationships**: {relationships_count} data relationships affecting integration
- **Business Domains**: Multiple domains requiring cross-system integration

## Requirements Generation Request
Generate comprehensive integration requirements covering:

1. **Internal System Integration Requirements**
   - Customer database integration specifications
   - Billing system integration requirements
   - Network operations system integration
   - CRM system synchronization needs

2. **External Partner Integration Requirements**
   - Wholesale partner system interfaces
   - Third-party service provider APIs
   - Regulatory reporting system integration
   - Payment gateway integration needs

3. **API Integration Requirements**
   - RESTful API design standards
   - GraphQL implementation for complex queries
   - API versioning and lifecycle management
   - API security and authentication requirements

4. **Data Integration Requirements**
   - Real-time data synchronization specifications
   - Batch processing and ETL requirements
   - Data transformation and mapping needs
   - Master data management integration

5. **Message Integration Requirements**
   - Asynchronous messaging requirements
   - Event-driven integration patterns
   - Message queue specifications
   - Event streaming requirements

6. **Business Process Integration Requirements**
   - Workflow integration across systems
   - Business process orchestration
   - Human task integration
   - Exception handling and recovery

7. **Security and Governance Requirements**
   - Integration security standards
   - Data governance in integrations
   - Audit and compliance requirements
   - Integration monitoring and logging

8. **Performance and Reliability Requirements**
   - Integration performance standards
   - High availability requirements
   - Failover and recovery mechanisms
   - Load balancing for integrations

Generate detailed integration requirements with clear technical specifications.
"""
        
        return await self._call_ollama_for_requirements(context)

    async def _generate_master_requirements_document(self, metadata: Dict[str, Any], 
                                                   data_structures: Dict[str, Any]):
        """Generate master requirements document"""
        logger.info("📋 Generating master requirements document...")
        
        master_doc_content = f"""# A1 Telekom Austria CuCo - Master Requirements Document

**Generated**: {datetime.now().isoformat()}
**Analysis Scope**: {metadata.get('files_processed', 0)} files processed
**Data Structures**: {metadata.get('data_structures_found', 0)} discovered
**Processing Time**: {metadata.get('processing_time', 0):.2f} seconds

## Executive Summary

This master requirements document provides comprehensive specifications for the modernization and enhancement of the A1 Telekom Austria Customer Care (CuCo) enterprise system. The analysis has identified {metadata.get('data_structures_found', 0)} data structures across multiple business domains, indicating a sophisticated enterprise application requiring careful modernization planning.

## Requirements Organization

### 1. Data-Driven Requirements
Located in: `by_data_structure/`
- Entity-specific requirements for {len(data_structures.get('entities', []))} entities
- Data management requirements
- Data validation requirements
- Business rule specifications

### 2. Layer-Based Requirements
Located in: `by_layer/`
- Presentation layer modernization requirements
- Business layer architecture requirements  
- Data layer specifications
- Cross-layer integration requirements

### 3. Domain-Based Requirements
Located in: `by_domain/`
- Business domain-specific requirements
- Cross-domain integration specifications
- Domain-driven design requirements

### 4. Analysis and Modernization
Located in: `analysis/`
- Comprehensive modernization requirements
- Integration requirements
- Technology stack modernization
- Migration strategy specifications

## Key Findings

### Data Architecture
- **Entities**: {len(data_structures.get('entities', []))} business entities identified
- **DTOs**: {len(data_structures.get('dtos', []))} data transfer objects
- **Relationships**: {len(data_structures.get('relationships', []))} entity relationships
- **Enums**: {len(data_structures.get('enums', []))} enumeration types

### Business Domains
"""
        
        # Add business domain summary
        summary = data_structures.get('summary', {})
        business_domains = summary.get('business_domains', {})
        domain_distribution = business_domains.get('domain_distribution', {})
        
        for domain, count in domain_distribution.items():
            master_doc_content += f"- **{domain.title()}**: {count} entities\n"
        
        master_doc_content += f"""
### Technology Assessment
- **Current Stack**: GWT, ExtJS/GXT, Spring Framework, iBATIS
- **Modernization Target**: React/Vue.js, Spring Boot, JPA/Hibernate, Microservices
- **Integration Needs**: REST APIs, Message Queues, Event-Driven Architecture

## Implementation Priority

### Phase 1: Foundation (0-6 months)
1. Data layer modernization and migration
2. Core API development
3. Security framework implementation
4. Basic frontend modernization

### Phase 2: Core Features (6-12 months)  
1. Business logic migration
2. User interface modernization
3. Integration development
4. Testing and quality assurance

### Phase 3: Advanced Features (12-18 months)
1. Advanced analytics implementation
2. Mobile application development
3. Performance optimization
4. Scalability enhancements

### Phase 4: Optimization (18+ months)
1. AI/ML integration
2. Advanced automation
3. Cloud optimization
4. Continuous improvement

## Success Criteria

### Technical Criteria
- 100% functional parity with legacy system
- Improved performance (50% faster response times)
- Modern technology stack implementation
- Comprehensive test coverage (>90%)

### Business Criteria
- Seamless user transition
- Improved user experience metrics
- Reduced operational costs
- Enhanced scalability and maintainability

## Risk Mitigation

### Technical Risks
- Legacy system complexity → Phased migration approach
- Data migration challenges → Comprehensive testing strategy
- Integration complexities → API-first design approach

### Business Risks  
- User adoption challenges → Comprehensive training program
- Business continuity → Parallel system operation
- Timeline pressures → Agile development methodology

## Next Steps

1. **Requirements Review**: Stakeholder review and approval of all requirements
2. **Technical Planning**: Detailed technical design and architecture planning
3. **Resource Allocation**: Team assembly and resource planning
4. **Implementation Planning**: Detailed project plan and timeline development

## Documentation Structure

```
requirements_weaviate/
├── by_layer/
│   ├── presentation_layer_requirements.md
│   ├── business_layer_requirements.md
│   └── data_layer_requirements.md
├── by_data_structure/
│   ├── [entity]_requirements.md (for each entity)
│   ├── data_management_requirements.md
│   └── data_validation_requirements.md
├── by_domain/
│   └── [domain]_domain_requirements.md (for each domain)
└── analysis/
    ├── modernization_requirements.md
    └── integration_requirements.md
```

This comprehensive requirements documentation provides the foundation for successful modernization of the A1 Telekom Austria CuCo system, ensuring business continuity while enabling technological advancement and improved operational efficiency.
"""
        
        with open(self.requirements_dir / "master_requirements.md", 'w') as f:
            f.write(master_doc_content)

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
                        "num_predict": 2048,
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