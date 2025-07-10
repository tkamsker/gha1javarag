from typing import List, Dict, Any

class ClassificationPromptBuilder:
    """Builds intelligent prompts for file classification"""
    
    @staticmethod
    def create_classification_prompt(file_path: str, content: str, file_type: str) -> str:
        """Create comprehensive classification prompt"""
        
        # Limit content for token efficiency
        limited_content = content[:2500] if len(content) > 2500 else content
        
        return f"""
TASK: Analyze this {file_type} file and provide comprehensive architectural classification.

FILE: {file_path}
CONTENT:
{limited_content}

ANALYSIS REQUIREMENTS:
Provide a JSON response with the following structure:

{{
    "purpose": "Brief description of main purpose",
    "components": [
        {{
            "name": "component name",
            "type": "component type",
            "description": "what it does"
        }}
    ],
    "data_structures": [
        {{
            "name": "structure name",
            "fields": ["field1", "field2"],
            "relationships": ["related entities"]
        }}
    ],
    "business_rules": [
        {{
            "description": "business rule description",
            "location": "where implemented"
        }}
    ],
    "dependencies": ["list of dependencies"],
    
    "file_classification": {{
        "architectural_layer": "one of: frontend, backend_service, data_access, persistence, batch_process, configuration, test, utility, security, integration, api_gateway, unknown",
        "component_type": "specific component type like rest_controller, service_layer, repository, dao, entity, dto, jsp_page, etc.",
        "confidence_score": 0.95,
        "technology_stack": ["spring_framework", "hibernate", "jsp"],
        "frameworks_detected": ["Spring Boot 2.x", "Hibernate 5.x"],
        "design_patterns": ["mvc", "repository", "service_layer"],
        "primary_purpose": "main functionality",
        "secondary_purposes": ["additional functions"],
        "business_domain": "domain area if identifiable",
        "dependencies": ["external dependencies"],
        "exposes_api": true/false,
        "consumes_api": true/false,
        "database_interactions": true/false,
        "complexity_indicators": ["high cyclomatic complexity", "multiple responsibilities"],
        "potential_issues": ["code smells", "anti-patterns"],
        "refactoring_suggestions": ["split large methods", "extract service"]
    }},
    
    "integration_points": ["database", "external APIs", "message queues"],
    "security_considerations": ["authentication", "authorization", "input validation"],
    "performance_considerations": ["database queries", "caching", "async processing"]
}}

CLASSIFICATION GUIDELINES:

ARCHITECTURAL LAYERS:
- frontend: JSP pages, HTML, CSS, JavaScript, client-side components
- backend_service: REST controllers, service classes, business logic
- data_access: DAO, Repository classes, data access logic
- persistence: Entity classes, database mappings, ORM configurations
- batch_process: Scheduled jobs, batch processors, ETL processes
- configuration: XML configs, properties files, application settings
- test: Unit tests, integration tests, test utilities
- utility: Helper classes, utility functions, common libraries
- security: Authentication, authorization, security filters
- integration: External API clients, message handlers, adapters
- api_gateway: API routing, gateway configurations

TECHNOLOGY DETECTION:
Look for imports, annotations, and patterns indicating:
- Spring Framework (@Controller, @Service, @Repository, @Component)
- Hibernate/JPA (@Entity, @Table, EntityManager)
- JSP/Servlet (HttpServlet, JSP directives)
- Testing frameworks (JUnit, TestNG, Mockito)

DESIGN PATTERNS:
- MVC: Controllers, Models, Views separation
- Repository: Data access abstraction
- Service Layer: Business logic encapsulation
- DAO: Data Access Object pattern
- Factory: Object creation patterns

ANALYZE THE CODE STRUCTURE, IMPORTS, ANNOTATIONS, AND NAMING CONVENTIONS TO MAKE ACCURATE CLASSIFICATIONS.
"""

    @staticmethod
    def create_batch_classification_prompt(files_batch: List[Dict[str, Any]]) -> str:
        """Create batch classification prompt for multiple files"""
        
        files_content = []
        for file_meta in files_batch:
            file_path = file_meta.get('file_path', '')
            file_type = file_meta.get('file_type', 'Unknown')
            content = file_meta.get('content', '')[:1500]  # Smaller chunks for batch
            
            files_content.append(f"""
=== FILE: {file_path} ===
TYPE: {file_type}
CONTENT: {content}
""")
        
        combined_content = "\n".join(files_content)
        
        return f"""
TASK: Analyze these files and provide architectural classification for each.

{combined_content}

For each file, provide the enhanced analysis structure shown above.
Format as:

## FILE: [filename]
{{
    "purpose": "...",
    "file_classification": {{ ... }},
    ...
}}

## FILE: [filename]
{{
    "purpose": "...",
    "file_classification": {{ ... }},
    ...
}}
"""