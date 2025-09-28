#!/usr/bin/env python3
"""
Fallback Requirements Generator

When AI models fail or produce corrupted output, this module generates 
professional requirements documentation based on structured analysis data.
"""

import json
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FallbackRequirementsGenerator:
    """Generates requirements documentation without relying on AI models"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_data_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate data layer requirements from structured data"""
        
        data_structures = metadata.get('data_structures', {})
        classes = data_structures.get('classes', [])
        ui_components = data_structures.get('ui_components', [])
        
        # Extract form fields for database schema
        form_fields = []
        for component in ui_components:
            form_fields.extend(component.get('form_fields', []))
        
        content = []
        content.append("# Data Layer Requirements")
        content.append("")
        content.append("**Status**: Generated from structural analysis")
        content.append(f"**Generated**: Based on analysis of {len(classes)} classes and {len(ui_components)} UI components")
        content.append("")
        
        # Database Technology Stack
        content.append("## 1. Database Technology Stack")
        content.append("")
        content.append("### Primary Database")
        content.append("- **Database Engine**: PostgreSQL 15+")
        content.append("- **Connection Pool**: HikariCP with 10-50 connections")
        content.append("- **Transaction Management**: Spring Transaction Management")
        content.append("- **ORM Framework**: JPA/Hibernate 5.6+")
        content.append("")
        
        # Database Schema Design
        content.append("## 2. Database Schema Design")
        content.append("")
        
        if classes:
            content.append("### Core Tables")
            content.append("")
            
            for cls in classes:
                table_name = cls.get('name', '').lower()
                if table_name.endswith('portlet'):
                    table_name = table_name.replace('portlet', '')
                
                content.append(f"#### {table_name} Table")
                content.append("")
                content.append(f"```sql")
                content.append(f"CREATE TABLE {table_name} (")
                
                # Generate fields based on class analysis
                fields = cls.get('fields', [])
                sql_fields = []
                
                # Always include ID
                sql_fields.append(f"  {table_name}_id UUID PRIMARY KEY DEFAULT gen_random_uuid()")
                
                for field in fields:
                    field_name = field.get('name', '')
                    field_type = field.get('type', 'String')
                    
                    # Skip UI-specific fields
                    if field_name in ['uiBinder', 'mainPanel', 'customerTree', 'addCustomerBtn', 
                                     'editDialog', 'billingGrid', 'searchBox', 'searchBtn', 'actionMenu']:
                        continue
                    
                    # Map Java types to SQL types
                    if field_type == 'String':
                        sql_type = 'VARCHAR(255)'
                    elif field_type == 'Integer':
                        sql_type = 'INTEGER'
                    elif field_type == 'Long':
                        sql_type = 'BIGINT'
                    elif field_type == 'Date':
                        sql_type = 'TIMESTAMP'
                    elif field_type == 'Boolean':
                        sql_type = 'BOOLEAN'
                    else:
                        sql_type = 'VARCHAR(255)'  # Default
                    
                    # Add constraints based on field analysis
                    constraints = []
                    if field_name in ['email']:
                        constraints.append('UNIQUE')
                        sql_type = 'VARCHAR(320)'  # Email standard
                    if field_name in ['name', 'customerId', 'email']:
                        constraints.append('NOT NULL')
                    
                    constraint_str = ' '.join(constraints)
                    if constraint_str:
                        constraint_str = ' ' + constraint_str
                        
                    sql_fields.append(f"  {field_name} {sql_type}{constraint_str}")
                
                # Add audit fields
                sql_fields.append("  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                sql_fields.append("  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                sql_fields.append("  deleted_at TIMESTAMP NULL")
                
                content.append(',\n'.join(sql_fields))
                content.append(");")
                content.append("```")
                content.append("")
        
        # Add form field analysis
        if form_fields:
            content.append("### Form Field Mappings")
            content.append("")
            content.append("Based on UI form analysis:")
            content.append("")
            
            for field in form_fields:
                field_name = field.get('name', '')
                field_type = field.get('type', 'String')
                validation_rules = field.get('validation_rules', [])
                required = field.get('required', False)
                
                content.append(f"#### {field_name}")
                content.append(f"- **Database Type**: {self._get_sql_type(field_type, validation_rules)}")
                content.append(f"- **Required**: {'Yes' if required else 'No'}")
                if validation_rules:
                    content.append(f"- **Validation**: {', '.join(validation_rules)}")
                content.append("")
        
        # Data Relationships
        content.append("## 3. Data Relationships")
        content.append("")
        content.append("### Entity Relationships")
        
        if len(classes) > 1:
            content.append("- Customer-to-Billing relationship via customer_id foreign key")
            content.append("- Audit trail relationships for all entities")
        else:
            content.append("- Standard parent-child relationships where applicable")
            content.append("- Foreign key constraints for referential integrity")
        
        content.append("")
        
        # Performance and Optimization
        content.append("## 4. Performance and Optimization")
        content.append("")
        content.append("### Indexing Strategy")
        content.append("```sql")
        
        if form_fields:
            for field in form_fields:
                field_name = field.get('name', '')
                if 'email' in field_name or 'id' in field_name:
                    table_name = 'customer'  # Infer from context
                    content.append(f"CREATE INDEX idx_{table_name}_{field_name} ON {table_name}({field_name});")
        
        content.append("CREATE INDEX idx_created_at ON customer(created_at);")
        content.append("CREATE INDEX idx_updated_at ON customer(updated_at);")
        content.append("```")
        content.append("")
        
        # Backup and Recovery
        content.append("## 5. Backup and Recovery")
        content.append("")
        content.append("### Backup Strategy")
        content.append("- Daily full backups with 30-day retention")
        content.append("- Continuous WAL archiving for point-in-time recovery")
        content.append("- Weekly backup verification and restore testing")
        content.append("")
        
        content.append("### High Availability")
        content.append("- Primary-replica setup for read scaling")
        content.append("- Automatic failover with connection pooling")
        content.append("- Health check monitoring every 30 seconds")
        content.append("")
        
        return '\n'.join(content)
    
    def generate_business_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate business layer requirements from structured data"""
        
        data_structures = metadata.get('data_structures', {})
        ui_components = data_structures.get('ui_components', [])
        backend_services = data_structures.get('summary', {}).get('backend_services_needed', [])
        
        content = []
        content.append("# Business Layer Requirements")
        content.append("")
        content.append("**Status**: Generated from service inference analysis")
        content.append(f"**Services Identified**: {len(backend_services)}")
        content.append("")
        
        # Service Architecture
        content.append("## 1. Service Architecture")
        content.append("")
        
        if backend_services:
            content.append("### Core Business Services")
            content.append("")
            
            for service in backend_services:
                service_name = service.replace('_', ' ').title()
                content.append(f"#### {service_name}")
                content.append("")
                
                # Service-specific requirements
                if 'customer' in service:
                    content.append("**Purpose**: Customer management and lifecycle operations")
                    content.append("")
                    content.append("**Core Operations**:")
                    content.append("- Customer registration and onboarding")
                    content.append("- Customer profile management")
                    content.append("- Customer search and retrieval")
                    content.append("- Customer status management")
                    content.append("")
                elif 'billing' in service:
                    content.append("**Purpose**: Billing calculations and invoice generation")
                    content.append("")
                    content.append("**Core Operations**:")
                    content.append("- Billing calculation engine")
                    content.append("- Invoice generation and delivery")
                    content.append("- Payment processing integration")
                    content.append("- Billing dispute handling")
                    content.append("")
                elif 'validation' in service:
                    content.append("**Purpose**: Data validation and business rule enforcement")
                    content.append("")
                    content.append("**Core Operations**:")
                    content.append("- Input data validation")
                    content.append("- Business rule enforcement")
                    content.append("- Constraint checking")
                    content.append("- Data integrity validation")
                    content.append("")
                else:
                    content.append(f"**Purpose**: {service_name} operations and management")
                    content.append("")
                    content.append("**Core Operations**:")
                    content.append(f"- {service_name} creation and modification")
                    content.append(f"- {service_name} retrieval and search")
                    content.append(f"- {service_name} validation and processing")
                    content.append("")
        
        # Transaction Management
        content.append("## 2. Transaction Management")
        content.append("")
        content.append("### Transaction Strategy")
        content.append("- **Isolation Level**: READ_COMMITTED for most operations")
        content.append("- **Rollback Strategy**: Automatic rollback on business rule violations")
        content.append("- **Distributed Transactions**: Two-phase commit for cross-service operations")
        content.append("")
        
        # Business Rules
        content.append("## 3. Business Rules and Validation")
        content.append("")
        
        # Extract validation rules from form fields
        validation_rules = []
        for component in ui_components:
            form_fields = component.get('form_fields', [])
            for field in form_fields:
                rules = field.get('validation_rules', [])
                for rule in rules:
                    if rule not in validation_rules:
                        validation_rules.append(rule)
        
        if validation_rules:
            content.append("### Form Validation Rules")
            for rule in validation_rules:
                if rule == 'required':
                    content.append("- **Required Field Validation**: Ensure mandatory fields are populated")
                elif rule == 'email_format':
                    content.append("- **Email Format Validation**: RFC 5322 compliant email validation")
                elif rule == 'phone_format':
                    content.append("- **Phone Number Validation**: International phone number format validation")
                elif rule == 'unique':
                    content.append("- **Uniqueness Validation**: Ensure unique constraints are enforced")
                else:
                    content.append(f"- **{rule.title()} Validation**: Custom business rule implementation")
            content.append("")
        
        # Performance Requirements
        content.append("## 4. Performance Requirements")
        content.append("")
        content.append("### Response Time Targets")
        content.append("- **Service Calls**: 95% under 500ms")
        content.append("- **Database Operations**: 95% under 200ms") 
        content.append("- **Validation Operations**: 95% under 100ms")
        content.append("")
        
        content.append("### Scalability")
        content.append("- **Horizontal Scaling**: Services designed for horizontal scaling")
        content.append("- **Load Balancing**: Round-robin load balancing between service instances")
        content.append("- **Caching**: Redis caching for frequently accessed business data")
        content.append("")
        
        return '\n'.join(content)
    
    def generate_presentation_layer_requirements(self, metadata: Dict[str, Any]) -> str:
        """Generate presentation layer requirements from UI analysis"""
        
        data_structures = metadata.get('data_structures', {})
        ui_components = data_structures.get('ui_components', [])
        
        content = []
        content.append("# Presentation Layer Requirements")
        content.append("")
        content.append("**Status**: Generated from GWT UI component analysis")
        content.append(f"**UI Components**: {len(ui_components)}")
        content.append("")
        
        # Technology Stack
        content.append("## 1. Technology Stack Modernization")
        content.append("")
        content.append("### Current State")
        content.append("- **Framework**: Google Web Toolkit (GWT)")
        content.append("- **Component Library**: GWT widgets and custom portlets")
        content.append("- **Architecture**: Monolithic portlet-based architecture")
        content.append("")
        
        content.append("### Target State")
        content.append("- **Framework**: React 18+ with TypeScript")
        content.append("- **Component Library**: Material-UI (MUI) v5+")
        content.append("- **State Management**: Redux Toolkit + RTK Query")
        content.append("- **Build System**: Vite with modern ESBuild")
        content.append("")
        
        # UI Component Analysis
        if ui_components:
            content.append("## 2. UI Component Migration Strategy")
            content.append("")
            
            for component in ui_components:
                component_name = component.get('name', '')
                ui_widgets = component.get('ui_widgets', [])
                form_fields = component.get('form_fields', [])
                
                content.append(f"### {component_name} Migration")
                content.append("")
                content.append(f"**Current GWT Implementation**: {component_name}")
                content.append(f"**Target React Component**: {component_name}Component")
                content.append("")
                
                if ui_widgets:
                    content.append("**Widget Migration Map**:")
                    for widget in ui_widgets:
                        widget_type = widget.get('widget_type', '')
                        widget_name = widget.get('name', '')
                        
                        react_equivalent = self._get_react_equivalent(widget_type)
                        content.append(f"- `{widget_name}` ({widget_type}) → {react_equivalent}")
                    content.append("")
                
                if form_fields:
                    content.append("**Form Fields**:")
                    for field in form_fields:
                        field_name = field.get('name', '')
                        validation_rules = field.get('validation_rules', [])
                        content.append(f"- `{field_name}`: {', '.join(validation_rules) if validation_rules else 'No validation'}")
                    content.append("")
        
        # User Experience Requirements
        content.append("## 3. User Experience Requirements")
        content.append("")
        content.append("### Accessibility")
        content.append("- **WCAG 2.1 AA Compliance**: Full accessibility compliance")
        content.append("- **Keyboard Navigation**: Complete keyboard accessibility")
        content.append("- **Screen Reader Support**: ARIA labels and semantic HTML")
        content.append("- **Focus Management**: Proper focus handling and visual indicators")
        content.append("")
        
        content.append("### Browser Support")
        content.append("- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+")
        content.append("- **Mobile Support**: Responsive design for tablets (768px+)")
        content.append("- **Progressive Enhancement**: Core functionality without JavaScript")
        content.append("")
        
        # Performance Requirements
        content.append("## 4. Performance Requirements")
        content.append("")
        content.append("### Loading Performance")
        content.append("- **Initial Load**: First Contentful Paint < 2 seconds")
        content.append("- **Time to Interactive**: < 3 seconds on 3G networks")
        content.append("- **Bundle Size**: Main bundle < 250KB gzipped")
        content.append("")
        
        content.append("### Runtime Performance")
        content.append("- **UI Interactions**: Response time < 100ms")
        content.append("- **Form Validation**: Client-side validation < 50ms")
        content.append("- **Data Grid Performance**: Handle 1000+ rows with virtual scrolling")
        content.append("")
        
        return '\n'.join(content)
    
    def _get_sql_type(self, java_type: str, validation_rules: List[str]) -> str:
        """Map Java types and validation rules to SQL types"""
        if 'email' in validation_rules:
            return 'VARCHAR(320)'
        elif 'phone' in validation_rules:
            return 'VARCHAR(20)'
        elif java_type == 'Integer':
            return 'INTEGER'
        elif java_type == 'Long':
            return 'BIGINT'
        elif java_type == 'Date':
            return 'TIMESTAMP'
        elif java_type == 'Boolean':
            return 'BOOLEAN'
        else:
            return 'VARCHAR(255)'
    
    def _get_react_equivalent(self, gwt_widget: str) -> str:
        """Map GWT widgets to React/MUI equivalents"""
        mapping = {
            'Button': 'MUI Button',
            'TextBox': 'MUI TextField',
            'Grid': 'MUI DataGrid',
            'DialogBox': 'MUI Dialog',
            'ScrollPanel': 'Box with overflow:auto',
            'CellTree': 'MUI TreeView',
            'MenuBar': 'MUI MenuList'
        }
        return mapping.get(gwt_widget, f'Custom React component for {gwt_widget}')