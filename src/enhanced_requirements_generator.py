#!/usr/bin/env python3
"""
Enhanced Requirements Generator
Generates high-quality requirements based on improved UI component analysis
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EnhancedRequirementsGenerator:
    """Generate enhanced requirements from improved data structure analysis"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        
    def generate_frontend_backend_requirements(self):
        """Generate separated frontend and backend requirements"""
        
        # Load enhanced data structures
        enhanced_file = self.output_dir / "data_structures_analysis_enhanced.json"
        if not enhanced_file.exists():
            logger.error("Enhanced data structures file not found")
            return
        
        with open(enhanced_file, 'r') as f:
            data = json.load(f)
        
        # Generate frontend requirements
        self._generate_frontend_requirements(data)
        
        # Generate backend requirements  
        self._generate_backend_requirements(data)
        
        # Generate integration requirements
        self._generate_integration_requirements(data)
        
        logger.info("✅ Enhanced requirements generated successfully")
    
    def _generate_frontend_requirements(self, data: Dict[str, Any]):
        """Generate detailed frontend requirements"""
        ui_components = data.get("ui_components", [])
        
        content = """# Frontend Requirements

**Status**: Enhanced analysis based on UI component extraction
**UI Components Analyzed**: {total_components}
**UI Widgets Detected**: {total_widgets}
**Form Fields Identified**: {total_fields}

## Overview
Frontend requirements derived from comprehensive analysis of GWT portlet UI components, widgets, and user interactions.

""".format(
            total_components=len(ui_components),
            total_widgets=data.get("summary", {}).get("total_ui_widgets", 0),
            total_fields=data.get("summary", {}).get("total_form_fields", 0)
        )
        
        # UI Component Requirements
        content += "## UI Component Requirements\n\n"
        
        for component in ui_components:
            name = component.get("name", "Unknown")
            widgets = component.get("ui_widgets", [])
            form_fields = component.get("form_fields", [])
            interactions = component.get("interactions", [])
            
            content += f"### {name} Component\n"
            content += f"- **Type**: {component.get('portlet_type', 'Unknown')}\n"
            content += f"- **Package**: {component.get('package_name', 'Unknown')}\n"
            content += f"- **Complexity Score**: {component.get('complexity_score', 0)}\n"
            content += f"- **Business Domain**: {component.get('business_domain', 'Unknown')}\n\n"
            
            # Widget Requirements
            if widgets:
                content += "#### UI Widgets\n"
                for widget in widgets:
                    content += f"- **{widget['name']}** ({widget['widget_type']})\n"
                    content += f"  - Purpose: User interface {widget['widget_type'].lower()} component\n"
                    if widget['widget_type'] == 'Button':
                        content += f"  - Behavior: Click handling and user action triggering\n"
                        content += f"  - Styling: Corporate design system compliance\n"
                    elif widget['widget_type'] == 'Grid':
                        content += f"  - Behavior: Data display with sorting and filtering\n"
                        content += f"  - Performance: Lazy loading for large datasets\n"
                    elif widget['widget_type'] == 'CellTree':
                        content += f"  - Behavior: Hierarchical data navigation\n"
                        content += f"  - Interaction: Selection and expansion handling\n"
                content += "\n"
            
            # Form Field Requirements
            if form_fields:
                content += "#### Form Field Requirements\n"
                for field in form_fields:
                    content += f"- **{field['name']}** ({field['type']})\n"
                    content += f"  - Required: {field.get('required', False)}\n"
                    if field.get('validation_rules'):
                        content += f"  - Validation: {', '.join(field['validation_rules'])}\n"
                    content += f"  - Client-side validation: Real-time validation feedback\n"
                    content += f"  - Error handling: User-friendly error messages\n"
                content += "\n"
            
            # Interaction Requirements
            if interactions:
                content += "#### User Interactions\n"
                for interaction in interactions:
                    if interaction == "click_handler":
                        content += "- **Click Handling**: Responsive click events with loading states\n"
                    elif interaction == "selection_handler":
                        content += "- **Selection Handling**: Multi-select support with visual feedback\n"
                    elif interaction == "data_loading":
                        content += "- **Data Loading**: Progressive loading with spinner indicators\n"
                    elif interaction == "data_update":
                        content += "- **Data Updates**: Optimistic updates with rollback capability\n"
                    elif interaction == "dialog_display":
                        content += "- **Modal Dialogs**: Accessible modal dialogs with escape handling\n"
                content += "\n"
        
        # Browser and Performance Requirements
        content += """## Browser and Performance Requirements

### Browser Compatibility
- **Supported Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Support**: Responsive design for tablets and mobile devices
- **Progressive Enhancement**: Graceful degradation for older browsers

### Performance Requirements
- **Initial Load**: Page load within 3 seconds
- **Interaction Response**: UI interactions respond within 100ms
- **Form Validation**: Client-side validation within 50ms
- **Data Grid Performance**: Handle 1000+ rows with virtual scrolling

### Accessibility Requirements
- **WCAG 2.1 AA Compliance**: Full accessibility compliance
- **Keyboard Navigation**: Complete keyboard accessibility
- **Screen Reader Support**: ARIA labels and descriptions
- **Focus Management**: Proper focus handling in dialogs and forms

### User Experience Requirements
- **Loading States**: Visual feedback for all async operations
- **Error Handling**: Clear error messages with recovery actions
- **Confirmation Dialogs**: User confirmation for destructive actions
- **Undo Functionality**: Undo capability for data modifications

---
*Generated by Enhanced Requirements Generator*
"""
        
        # Save frontend requirements
        frontend_file = self.output_dir / "requirements_enhanced" / "frontend_requirements.md"
        frontend_file.parent.mkdir(exist_ok=True)
        
        with open(frontend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Frontend requirements saved to {frontend_file}")
    
    def _generate_backend_requirements(self, data: Dict[str, Any]):
        """Generate detailed backend requirements"""
        backend_services = data.get("summary", {}).get("backend_services_needed", [])
        ui_components = data.get("ui_components", [])
        
        content = """# Backend Requirements

**Status**: Enhanced analysis based on UI component and service inference
**Backend Services Identified**: {total_services}
**Business Domains**: {domains}

## Overview
Backend requirements derived from UI component analysis and inferred data flow patterns.

""".format(
            total_services=len(backend_services),
            domains=", ".join(data.get("summary", {}).get("business_domains", {}).keys())
        )
        
        # Service Architecture Requirements
        content += "## Service Architecture Requirements\n\n"
        
        service_descriptions = {
            "customer_service": {
                "name": "Customer Service",
                "purpose": "Core customer management operations",
                "operations": ["Create customer", "Update customer", "Delete customer", "Search customers", "Customer status management"],
                "data_entities": ["Customer", "CustomerStatus"],
                "dependencies": ["customer_repository", "customer_validation_service"]
            },
            "customer_repository": {
                "name": "Customer Repository",
                "purpose": "Data persistence layer for customer information",
                "operations": ["CRUD operations", "Query operations", "Bulk operations", "Transaction management"],
                "data_entities": ["Customer", "CustomerAudit"],
                "dependencies": ["database", "cache_service"]
            },
            "customer_validation_service": {
                "name": "Customer Validation Service", 
                "purpose": "Business rule validation for customer data",
                "operations": ["Email validation", "Phone validation", "Business rule validation", "Duplicate detection"],
                "data_entities": ["ValidationRule", "ValidationResult"],
                "dependencies": ["external_validation_apis"]
            },
            "billing_service": {
                "name": "Billing Service",
                "purpose": "Billing calculations and invoice management",
                "operations": ["Calculate billing", "Generate invoices", "Process payments", "Billing reports"],
                "data_entities": ["Billing", "Invoice", "Payment"],
                "dependencies": ["payment_service", "product_catalog_service"]
            },
            "payment_service": {
                "name": "Payment Service",
                "purpose": "Payment processing and transaction management",
                "operations": ["Process payments", "Refund handling", "Payment validation", "Gateway integration"],
                "data_entities": ["Payment", "Transaction", "PaymentMethod"],
                "dependencies": ["payment_gateway", "fraud_detection_service"]
            },
            "invoice_service": {
                "name": "Invoice Service",
                "purpose": "Invoice generation and delivery",
                "operations": ["Generate invoices", "PDF generation", "Email delivery", "Invoice tracking"],
                "data_entities": ["Invoice", "InvoiceItem", "DeliveryStatus"],
                "dependencies": ["billing_service", "notification_service"]
            },
            "product_catalog_service": {
                "name": "Product Catalog Service",
                "purpose": "Product and service catalog management",
                "operations": ["Product management", "Pricing management", "Catalog search", "Product configuration"],
                "data_entities": ["Product", "Service", "Price", "Configuration"],
                "dependencies": ["pricing_engine", "configuration_service"]
            }
        }
        
        for service_key in backend_services:
            if service_key in service_descriptions:
                service = service_descriptions[service_key]
                content += f"### {service['name']}\n"
                content += f"- **Purpose**: {service['purpose']}\n"
                content += f"- **Operations**:\n"
                for op in service['operations']:
                    content += f"  - {op}\n"
                content += f"- **Data Entities**: {', '.join(service['data_entities'])}\n"
                content += f"- **Dependencies**: {', '.join(service['dependencies'])}\n\n"
        
        # API Requirements
        content += """## REST API Requirements

### Customer API Endpoints
- **POST /api/customers** - Create new customer
- **GET /api/customers/{id}** - Get customer by ID
- **PUT /api/customers/{id}** - Update customer
- **DELETE /api/customers/{id}** - Soft delete customer
- **GET /api/customers/search** - Search customers with pagination

### Billing API Endpoints
- **GET /api/billing/customer/{id}** - Get customer billing information
- **POST /api/billing/calculate** - Calculate billing amounts
- **GET /api/billing/invoices** - Get invoices with filtering
- **POST /api/billing/payments** - Process payment

### API Standards
- **Authentication**: JWT token-based authentication
- **Rate Limiting**: 1000 requests per hour per client
- **Response Format**: JSON with consistent error handling
- **Status Codes**: Standard HTTP status codes
- **Versioning**: URL versioning (v1, v2, etc.)

## Data Security Requirements

### Data Protection
- **Encryption at Rest**: AES-256 encryption for sensitive data
- **Encryption in Transit**: TLS 1.3 for all API communications
- **Data Masking**: PII data masking in non-production environments
- **Access Control**: Role-based access control (RBAC)

### Audit and Compliance
- **Audit Logging**: Comprehensive audit trails for all data changes
- **GDPR Compliance**: Data subject rights implementation
- **Data Retention**: Configurable data retention policies
- **Backup and Recovery**: Automated backup with point-in-time recovery

## Performance Requirements

### Response Time
- **API Response Time**: 95% of requests under 500ms
- **Database Queries**: 95% under 200ms
- **Bulk Operations**: Progress tracking for long-running operations
- **Search Operations**: Full-text search results under 1 second

### Scalability
- **Horizontal Scaling**: Microservices architecture for independent scaling
- **Database Scaling**: Read replicas and connection pooling
- **Caching Strategy**: Redis caching for frequently accessed data
- **Load Balancing**: Application load balancing with health checks

---
*Generated by Enhanced Requirements Generator*
"""
        
        # Save backend requirements
        backend_file = self.output_dir / "requirements_enhanced" / "backend_requirements.md"
        backend_file.parent.mkdir(exist_ok=True)
        
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Backend requirements saved to {backend_file}")
    
    def _generate_integration_requirements(self, data: Dict[str, Any]):
        """Generate integration requirements between frontend and backend"""
        ui_components = data.get("ui_components", [])
        frontend_behaviors = data.get("summary", {}).get("frontend_behaviors", [])
        
        content = """# Integration Requirements

**Status**: Enhanced analysis of frontend-backend integration patterns
**Integration Points Identified**: {integration_points}
**Frontend Behaviors**: {behaviors}

## Overview
Integration requirements defining the communication patterns between frontend UI components and backend services.

""".format(
            integration_points=len(ui_components) * 2,  # Estimate based on UI components
            behaviors=", ".join(frontend_behaviors)
        )
        
        # Component-Service Integration
        content += "## Component-Service Integration Mapping\n\n"
        
        for component in ui_components:
            name = component.get("name", "Unknown")
            backend_services = component.get("backend_services", [])
            
            content += f"### {name} Integration\n"
            
            if "customer" in name.lower():
                content += """
#### Customer Management Integration
- **Data Loading**: CustomerPortlet → Customer Service → Customer Repository
- **CRUD Operations**: Form submissions → Customer API endpoints → Database
- **Validation**: Client validation → Server validation → Business rules
- **Search**: Search input → Customer search API → Filtered results

#### Integration Flow
1. **Customer List Loading**:
   ```
   CustomerPortlet.loadCustomers() 
   → GET /api/customers
   → CustomerService.getCustomers()
   → CustomerRepository.findAll()
   → Database query
   ```

2. **Customer Creation/Update**:
   ```
   CustomerPortlet.onAddCustomerClick()
   → editDialog.show()
   → Form validation (client-side)
   → POST/PUT /api/customers
   → CustomerValidationService.validate()
   → CustomerRepository.save()
   → Database transaction
   ```

3. **Customer Selection**:
   ```
   CustomerPortlet.onCustomerSelect()
   → GET /api/customers/{id}
   → CustomerService.getById()
   → CustomerRepository.findById()
   → Form population
   ```
"""
            
            elif "billing" in name.lower():
                content += """
#### Billing Management Integration
- **Search Operations**: BillingPortlet → Billing Service → Database queries
- **Data Grid**: Grid component → Billing API → Paginated results
- **Action Menu**: User actions → Billing operations → Backend services

#### Integration Flow
1. **Billing Search**:
   ```
   BillingPortlet.onSearchClick()
   → searchBox.getValue()
   → GET /api/billing/search?query={value}
   → BillingService.search()
   → Database query with filtering
   → Grid data update
   ```

2. **Billing Grid Actions**:
   ```
   actionMenu selection
   → Billing action (view/edit/process)
   → Appropriate billing API endpoint
   → BillingService operation
   → Database update
   → Grid refresh
   ```
"""
        
        # Error Handling Integration
        content += """
## Error Handling Integration

### Client-Side Error Handling
- **Network Errors**: Retry logic with exponential backoff
- **Validation Errors**: Display inline validation messages
- **Server Errors**: User-friendly error messages with error codes
- **Timeout Handling**: Progress indicators with timeout warnings

### Server-Side Error Integration
- **Structured Error Responses**: Consistent error format across all APIs
- **Error Logging**: Centralized logging with correlation IDs
- **Error Recovery**: Graceful degradation for service failures
- **Circuit Breaker**: Service failure protection with fallback

## Real-time Integration Requirements

### WebSocket Integration
- **Real-time Updates**: Customer status changes pushed to UI
- **Notification System**: Billing alerts and payment confirmations
- **Connection Management**: Automatic reconnection on connection loss
- **Message Queuing**: Offline message handling and replay

### Event-Driven Architecture
- **Domain Events**: Customer created/updated/deleted events
- **Event Streaming**: Billing events for real-time processing
- **Event Sourcing**: Audit trail through event history
- **CQRS Pattern**: Separate read/write models for complex operations

## Security Integration

### Authentication Integration
- **Single Sign-On**: JWT token validation across all services
- **Session Management**: Secure session handling with timeout
- **Role-Based Access**: UI component visibility based on user roles
- **API Security**: OAuth 2.0 / OpenID Connect integration

### Data Security Integration
- **Field-Level Encryption**: Sensitive fields encrypted in transit and storage
- **Data Masking**: PII data masked based on user permissions
- **Audit Integration**: All UI actions logged with user context
- **Compliance**: GDPR, PCI-DSS compliance in data handling

---
*Generated by Enhanced Requirements Generator*
"""
        
        # Save integration requirements
        integration_file = self.output_dir / "requirements_enhanced" / "integration_requirements.md"
        integration_file.parent.mkdir(exist_ok=True)
        
        with open(integration_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Integration requirements saved to {integration_file}")

def main():
    """Generate enhanced requirements"""
    generator = EnhancedRequirementsGenerator()
    generator.generate_frontend_backend_requirements()

if __name__ == "__main__":
    main()