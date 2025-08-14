from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ArchitecturalLayer(str, Enum):
    """Architectural layer classification"""
    FRONTEND = "frontend"
    BACKEND_SERVICE = "backend_service"
    DATA_ACCESS = "data_access"
    PERSISTENCE = "persistence"
    BATCH_PROCESS = "batch_process"
    CONFIGURATION = "configuration"
    TEST = "test"
    UTILITY = "utility"
    SECURITY = "security"
    INTEGRATION = "integration"
    API_GATEWAY = "api_gateway"
    UNKNOWN = "unknown"

class ComponentType(str, Enum):
    """Component type classification"""
    # Backend Components
    REST_CONTROLLER = "rest_controller"
    SERVICE_LAYER = "service_layer"
    REPOSITORY = "repository"
    DAO = "dao"
    ENTITY = "entity"
    DTO = "dto"
    MAPPER = "mapper"
    CONFIGURATION = "configuration"
    
    # Frontend Components
    JSP_PAGE = "jsp_page"
    JAVASCRIPT = "javascript"
    CSS_STYLESHEET = "css_stylesheet"
    HTML_TEMPLATE = "html_template"
    SERVLET = "servlet"
    FILTER = "filter"
    
    # Infrastructure
    DATABASE_SCRIPT = "database_script"
    MIGRATION = "migration"
    BATCH_JOB = "batch_job"
    SCHEDULER = "scheduler"
    
    # Testing
    UNIT_TEST = "unit_test"
    INTEGRATION_TEST = "integration_test"
    E2E_TEST = "e2e_test"
    
    # Other
    UTILITY_CLASS = "utility_class"
    CONSTANT = "constant"
    ENUM = "enum"
    INTERFACE = "interface"
    ABSTRACT_CLASS = "abstract_class"
    UNKNOWN = "unknown"

class TechnologyStack(str, Enum):
    """Technology stack identification"""
    SPRING_FRAMEWORK = "spring_framework"
    SPRING_BOOT = "spring_boot"
    HIBERNATE = "hibernate"
    JPA = "jpa"
    MYBATIS = "mybatis"
    IBATIS = "ibatis"
    JSF = "jsf"
    STRUTS = "struts"
    SERVLET_API = "servlet_api"
    JSP = "jsp"
    JSTL = "jstl"
    JQUERY = "jquery"
    ANGULAR = "angular"
    REACT = "react"
    BOOTSTRAP = "bootstrap"
    # Generic/Core technologies
    JAVA = "java"
    JAVASCRIPT = "javascript"
    SQL = "sql"
    XML = "xml"
    UNKNOWN = "unknown"

class DesignPattern(str, Enum):
    """Design pattern identification"""
    MVC = "mvc"
    REPOSITORY = "repository"
    SERVICE_LAYER = "service_layer"
    DAO = "dao"
    FACTORY = "factory"
    SINGLETON = "singleton"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"
    FACADE = "facade"
    ADAPTER = "adapter"
    BUILDER = "builder"
    UNKNOWN = "unknown"

class EnhancedFileClassification(BaseModel):
    """Enhanced file classification with architectural insights"""
    # Core Classification
    architectural_layer: ArchitecturalLayer
    component_type: ComponentType
    confidence_score: float = Field(ge=0.0, le=1.0)
    
    # Technology Analysis
    technology_stack: List[TechnologyStack] = Field(default_factory=list)
    frameworks_detected: List[str] = Field(default_factory=list)
    design_patterns: List[DesignPattern] = Field(default_factory=list)
    
    # Functional Analysis
    primary_purpose: str
    secondary_purposes: List[str] = Field(default_factory=list)
    business_domain: Optional[str] = None
    
    # Architectural Analysis
    dependencies: List[str] = Field(default_factory=list)
    exposes_api: bool = False
    consumes_api: bool = False
    database_interactions: bool = False
    
    # Quality Metrics
    complexity_indicators: List[str] = Field(default_factory=list)
    potential_issues: List[str] = Field(default_factory=list)
    refactoring_suggestions: List[str] = Field(default_factory=list)

class EnhancedAIAnalysis(BaseModel):
    """Complete enhanced AI analysis"""
    # Original analysis (maintained for compatibility)
    purpose: str
    components: List[Dict[str, str]] = Field(default_factory=list)
    data_structures: List[Dict[str, Any]] = Field(default_factory=list)
    business_rules: List[Dict[str, str]] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    
    # Enhanced classification
    file_classification: EnhancedFileClassification
    
    # Additional insights
    integration_points: List[str] = Field(default_factory=list)
    security_considerations: List[str] = Field(default_factory=list)
    performance_considerations: List[str] = Field(default_factory=list)

def validate_and_fix_ai_response(data: dict) -> dict:
    """Validate and fix common AI response issues"""
    if not isinstance(data, dict):
        return data
    
    # Fix technology_stack values
    if 'file_classification' in data and isinstance(data['file_classification'], dict):
        file_class = data['file_classification']
        
        # Technology stack mapping
        tech_mapping = {
            'core_java': 'java',
            'plain_java': 'java',
            'standard_java': 'java',
            'jdbc': 'java',  # Map JDBC to Java
            'servlets': 'servlet_api',
            'spring': 'spring_framework',
            'springboot': 'spring_boot',
            'spring-boot': 'spring_boot',
            'js': 'javascript',
            'html': 'xml',  # Map HTML to XML as generic markup
            'css': 'unknown',  # No specific CSS enum yet
        }
        
        if 'technology_stack' in file_class:
            tech_stack = file_class['technology_stack']
            if isinstance(tech_stack, list):
                # Fix each technology stack item
                fixed_tech_stack = []
                for tech in tech_stack:
                    if isinstance(tech, str):
                        # Apply mapping if available
                        tech_lower = tech.lower().replace('_', '').replace('-', '')
                        mapped_tech = tech_mapping.get(tech_lower, tech.lower())
                        
                        # Validate against enum values
                        valid_values = [e.value for e in TechnologyStack]
                        if mapped_tech in valid_values:
                            fixed_tech_stack.append(mapped_tech)
                        else:
                            # Default to 'unknown' for unrecognized technologies
                            fixed_tech_stack.append('unknown')
                    else:
                        fixed_tech_stack.append('unknown')
                
                file_class['technology_stack'] = fixed_tech_stack
            elif isinstance(tech_stack, str):
                # Handle single string value
                tech_lower = tech_stack.lower().replace('_', '').replace('-', '')
                mapped_tech = tech_mapping.get(tech_lower, tech_stack.lower())
                
                valid_values = [e.value for e in TechnologyStack]
                if mapped_tech in valid_values:
                    file_class['technology_stack'] = [mapped_tech]
                else:
                    file_class['technology_stack'] = ['unknown']
        
        # Fix design_patterns values
        if 'design_patterns' in file_class:
            patterns = file_class['design_patterns']
            if isinstance(patterns, list):
                fixed_patterns = []
                valid_patterns = [e.value for e in DesignPattern]
                for pattern in patterns:
                    if isinstance(pattern, str) and pattern.lower() in valid_patterns:
                        fixed_patterns.append(pattern.lower())
                    else:
                        fixed_patterns.append('unknown')
                file_class['design_patterns'] = fixed_patterns
    
    return data