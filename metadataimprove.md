# AI-Enhanced Metadata Classification Improvement Plan

## Executive Summary

This plan focuses on enhancing the existing AI analysis system to intelligently classify and categorize files based on their architectural purpose and functionality. The goal is to automatically identify whether files are backend services, frontend components, data access objects, persistence layers, batch processes, etc., for better organization and grouping.

## Current State Analysis

### Existing AI Analysis Structure
**Location**: `src/ai_analyzer.py` and `src/main.py` (BatchAIAnalyzer)

**Current AI Analysis Schema**:
```json
{
    "purpose": "string",
    "components": [{"name": "string", "type": "string", "description": "string"}],
    "data_structures": [{"name": "string", "fields": ["string"], "relationships": ["string"]}],
    "business_rules": [{"description": "string", "location": "string"}],
    "dependencies": ["string"]
}
```

**Current Limitations**:
- ❌ No architectural layer classification
- ❌ No file purpose categorization
- ❌ Limited component type identification
- ❌ No technology stack detection
- ❌ No design pattern recognition

## Enhanced Metadata Classification Plan

### Phase 1: Enhanced AI Analysis Schema (Priority: HIGH)

#### Step 1.1: Create Comprehensive Classification Schema
**Files to modify**: `src/metadata_schemas.py` (new file)

**Implementation**:
```python
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
    JSF = "jsf"
    STRUTS = "struts"
    SERVLET_API = "servlet_api"
    JSP = "jsp"
    JSTL = "jstl"
    JQUERY = "jquery"
    ANGULAR = "angular"
    REACT = "react"
    BOOTSTRAP = "bootstrap"
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
```

#### Step 1.2: Create Intelligent Classification Prompts
**Files to modify**: `src/classification_prompts.py` (new file)

**Implementation**:
```python
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
```

### Phase 2: Enhanced AI Analysis Engine (Priority: HIGH)

#### Step 2.1: Update AI Analyzer with Classification
**Files to modify**: `src/ai_analyzer.py`

**Key changes**:
```python
from .classification_prompts import ClassificationPromptBuilder
from .metadata_schemas import EnhancedAIAnalysis, EnhancedFileClassification

class EnhancedAIAnalyzer(AIAnalyzer):
    """Enhanced AI analyzer with architectural classification"""
    
    def __init__(self):
        super().__init__()
        self.prompt_builder = ClassificationPromptBuilder()
    
    def create_enhanced_file_prompt(self, file_type: str, content: str, file_path: str) -> str:
        """Create enhanced classification prompt"""
        return self.prompt_builder.create_classification_prompt(file_path, content, file_type)
    
    async def analyze_file_with_classification(self, file_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file with enhanced classification"""
        file_path = file_metadata.get('file_path', '')
        file_type = file_metadata.get('file_type', 'Unknown')
        content = file_metadata.get('content', '')
        
        # Create enhanced prompt
        prompt = self.create_enhanced_file_prompt(file_type, content, file_path)
        
        # Get AI analysis
        try:
            messages = [
                {"role": "system", "content": "You are an expert software architect specializing in code analysis and architectural classification. Provide accurate, detailed analysis."},
                {"role": "user", "content": prompt}
            ]
            
            analysis_text = await self.ai_provider.create_chat_completion(
                messages=messages,
                temperature=0.1,  # Lower temperature for more consistent classification
                max_tokens=2500
            )
            
            # Parse enhanced analysis
            enhanced_analysis = self.parse_enhanced_analysis(analysis_text, file_path)
            
            # Update file metadata
            file_metadata.update({
                'enhanced_ai_analysis': enhanced_analysis,
                'analysis_status': 'completed_enhanced',
                'ai_provider': self.ai_provider.get_provider_name(),
                'ai_model': self.ai_provider.get_model_name()
            })
            
        except Exception as e:
            logger.error(f"Enhanced analysis failed for {file_path}: {e}")
            file_metadata.update({
                'analysis_status': 'failed',
                'error': str(e)
            })
        
        return file_metadata
    
    def parse_enhanced_analysis(self, analysis_text: str, file_path: str) -> Dict[str, Any]:
        """Parse enhanced analysis response"""
        try:
            # Extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_dict = json.loads(json_match.group())
                
                # Validate using Pydantic model
                enhanced_analysis = EnhancedAIAnalysis.model_validate(analysis_dict)
                return enhanced_analysis.model_dump()
            else:
                logger.warning(f"Could not extract JSON from analysis for {file_path}")
                return self.create_fallback_analysis(analysis_text, file_path)
                
        except Exception as e:
            logger.error(f"Failed to parse enhanced analysis for {file_path}: {e}")
            return self.create_fallback_analysis(analysis_text, file_path)
    
    def create_fallback_analysis(self, analysis_text: str, file_path: str) -> Dict[str, Any]:
        """Create fallback analysis when parsing fails"""
        # Basic classification based on file path and extension
        architectural_layer = self.guess_layer_from_path(file_path)
        component_type = self.guess_component_from_path(file_path)
        
        return {
            "purpose": analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text,
            "components": [],
            "data_structures": [],
            "business_rules": [],
            "dependencies": [],
            "file_classification": {
                "architectural_layer": architectural_layer,
                "component_type": component_type,
                "confidence_score": 0.3,  # Low confidence for fallback
                "technology_stack": [],
                "frameworks_detected": [],
                "design_patterns": [],
                "primary_purpose": "Analysis parsing failed",
                "secondary_purposes": [],
                "business_domain": None,
                "dependencies": [],
                "exposes_api": False,
                "consumes_api": False,
                "database_interactions": False,
                "complexity_indicators": ["parsing_failed"],
                "potential_issues": ["analysis_parsing_failed"],
                "refactoring_suggestions": []
            },
            "integration_points": [],
            "security_considerations": [],
            "performance_considerations": []
        }
    
    def guess_layer_from_path(self, file_path: str) -> str:
        """Guess architectural layer from file path"""
        path_lower = file_path.lower()
        
        if any(x in path_lower for x in ['test', 'spec']):
            return "test"
        elif any(x in path_lower for x in ['controller', 'rest', 'api']):
            return "backend_service"
        elif any(x in path_lower for x in ['service', 'business']):
            return "backend_service"
        elif any(x in path_lower for x in ['dao', 'repository']):
            return "data_access"
        elif any(x in path_lower for x in ['entity', 'model', 'domain']):
            return "persistence"
        elif any(x in path_lower for x in ['jsp', 'html', 'css', 'js']):
            return "frontend"
        elif any(x in path_lower for x in ['config', 'properties', 'xml']):
            return "configuration"
        elif any(x in path_lower for x in ['batch', 'job', 'scheduler']):
            return "batch_process"
        elif any(x in path_lower for x in ['util', 'helper', 'common']):
            return "utility"
        else:
            return "unknown"
    
    def guess_component_from_path(self, file_path: str) -> str:
        """Guess component type from file path and extension"""
        path_lower = file_path.lower()
        
        if file_path.endswith('.jsp'):
            return "jsp_page"
        elif file_path.endswith('.js'):
            return "javascript"
        elif file_path.endswith('.css'):
            return "css_stylesheet"
        elif file_path.endswith('.html'):
            return "html_template"
        elif file_path.endswith('.sql'):
            return "database_script"
        elif 'test' in path_lower:
            return "unit_test"
        elif 'controller' in path_lower:
            return "rest_controller"
        elif 'service' in path_lower:
            return "service_layer"
        elif 'repository' in path_lower:
            return "repository"
        elif 'dao' in path_lower:
            return "dao"
        elif 'entity' in path_lower:
            return "entity"
        elif 'dto' in path_lower:
            return "dto"
        else:
            return "unknown"
```

### Phase 3: Metadata Storage and Grouping (Priority: HIGH)

#### Step 3.1: Update ChromaDB Connector for Enhanced Metadata
**Files to modify**: `src/chromadb_connector.py`

**Key changes**:
```python
def store_enhanced_metadata(self, file_path: str, content: str, enhanced_analysis: Dict[str, Any]):
    """Store enhanced metadata with classification"""
    chunks = self.chunker.chunk_code(file_path, content)
    
    for chunk in chunks:
        # Extract enhanced classification
        file_classification = enhanced_analysis.get('file_classification', {})
        
        # Enhanced metadata for ChromaDB
        enhanced_metadata = {
            # Original metadata
            'file_path': chunk.file_path,
            'language': chunk.language,
            'chunk_type': chunk.chunk_type,
            'start_line': str(chunk.start_line),
            'end_line': str(chunk.end_line),
            'complexity_score': str(chunk.complexity_score),
            'function_name': chunk.function_name or '',
            'class_name': chunk.class_name or '',
            'parent_context': chunk.parent_context or '',
            
            # Enhanced classification metadata
            'architectural_layer': file_classification.get('architectural_layer', 'unknown'),
            'component_type': file_classification.get('component_type', 'unknown'),
            'confidence_score': str(file_classification.get('confidence_score', 0.0)),
            'technology_stack': json.dumps(file_classification.get('technology_stack', [])),
            'design_patterns': json.dumps(file_classification.get('design_patterns', [])),
            'primary_purpose': file_classification.get('primary_purpose', ''),
            'business_domain': file_classification.get('business_domain', ''),
            'exposes_api': str(file_classification.get('exposes_api', False)),
            'consumes_api': str(file_classification.get('consumes_api', False)),
            'database_interactions': str(file_classification.get('database_interactions', False)),
            
            # Full AI analysis (JSON encoded)
            'enhanced_ai_analysis': json.dumps(enhanced_analysis)
        }
        
        # Store in ChromaDB with enhanced metadata
        self.collection.add(
            documents=[chunk.content],
            metadatas=[enhanced_metadata],
            ids=[chunk.chunk_id]
        )
```

#### Step 3.2: Create Grouping and Filtering Utilities
**Files to create**: `src/metadata_grouping.py`

**Implementation**:
```python
from typing import Dict, List, Any
from collections import defaultdict
from .metadata_schemas import ArchitecturalLayer, ComponentType

class MetadataGrouper:
    """Groups and filters files based on enhanced classification"""
    
    @staticmethod
    def group_by_architectural_layer(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by architectural layer"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            layer = classification.get('architectural_layer', 'unknown')
            groups[layer].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def group_by_component_type(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by component type"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            component_type = classification.get('component_type', 'unknown')
            groups[component_type].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def group_by_business_domain(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by business domain"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            domain = classification.get('business_domain') or 'unspecified'
            groups[domain].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def filter_by_technology_stack(metadata_list: List[Dict[str, Any]], 
                                  technology: str) -> List[Dict[str, Any]]:
        """Filter files by technology stack"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            tech_stack = classification.get('technology_stack', [])
            
            if technology.lower() in [tech.lower() for tech in tech_stack]:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_high_complexity(metadata_list: List[Dict[str, Any]], 
                              min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """Filter files with complexity indicators"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            confidence = classification.get('confidence_score', 0.0)
            complexity_indicators = classification.get('complexity_indicators', [])
            
            if confidence >= min_confidence and complexity_indicators:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def generate_architecture_report(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive architecture report"""
        layer_groups = MetadataGrouper.group_by_architectural_layer(metadata_list)
        component_groups = MetadataGrouper.group_by_component_type(metadata_list)
        domain_groups = MetadataGrouper.group_by_business_domain(metadata_list)
        
        # Technology analysis
        tech_usage = defaultdict(int)
        pattern_usage = defaultdict(int)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            for tech in classification.get('technology_stack', []):
                tech_usage[tech] += 1
            
            for pattern in classification.get('design_patterns', []):
                pattern_usage[pattern] += 1
        
        return {
            'total_files': len(metadata_list),
            'architectural_layers': {layer: len(files) for layer, files in layer_groups.items()},
            'component_types': {comp: len(files) for comp, files in component_groups.items()},
            'business_domains': {domain: len(files) for domain, files in domain_groups.items()},
            'technology_usage': dict(tech_usage),
            'design_pattern_usage': dict(pattern_usage),
            'files_with_api_exposure': len([f for f in metadata_list 
                                          if f.get('enhanced_ai_analysis', {}).get('file_classification', {}).get('exposes_api', False)]),
            'files_with_db_interaction': len([f for f in metadata_list 
                                            if f.get('enhanced_ai_analysis', {}).get('file_classification', {}).get('database_interactions', False)])
        }
```

### Phase 4: Integration and Output Enhancement (Priority: MEDIUM)

#### Step 4.1: Update Main Processing Pipeline
**Files to modify**: `src/main.py`

**Key changes**:
```python
# Replace BatchAIAnalyzer with EnhancedBatchAIAnalyzer
from .ai_analyzer import EnhancedAIAnalyzer
from .metadata_grouping import MetadataGrouper

class EnhancedBatchAIAnalyzer(BatchAIAnalyzer):
    """Enhanced batch analyzer with classification"""
    
    def __init__(self):
        super().__init__()
        self.enhanced_analyzer = EnhancedAIAnalyzer()
        self.grouper = MetadataGrouper()
    
    async def analyze_files_with_classification(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze files with enhanced classification"""
        
        # Use enhanced analysis
        for file_meta in files_metadata:
            await self.enhanced_analyzer.analyze_file_with_classification(file_meta)
        
        # Generate architecture report
        architecture_report = self.grouper.generate_architecture_report(files_metadata)
        
        # Save architecture report
        report_file = os.path.join(self.output_dir, 'architecture_report.json')
        with open(report_file, 'w') as f:
            json.dump(architecture_report, f, indent=2)
        
        logger.info(f"Generated architecture report: {report_file}")
        
        return files_metadata
```

#### Step 4.2: Create Enhanced Requirements Generator
**Files to create**: `src/enhanced_requirements_generator.py`

**Implementation**:
```python
class EnhancedRequirementsGenerator:
    """Generate requirements grouped by architectural classification"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.grouper = MetadataGrouper()
    
    def generate_grouped_requirements(self, metadata_list: List[Dict[str, Any]]):
        """Generate requirements documents grouped by classification"""
        
        # Group by architectural layer
        layer_groups = self.grouper.group_by_architectural_layer(metadata_list)
        
        for layer, files in layer_groups.items():
            self.generate_layer_requirements(layer, files)
        
        # Group by component type
        component_groups = self.grouper.group_by_component_type(metadata_list)
        
        for component_type, files in component_groups.items():
            self.generate_component_requirements(component_type, files)
        
        # Generate cross-cutting concerns
        self.generate_integration_analysis(metadata_list)
        self.generate_security_analysis(metadata_list)
        self.generate_performance_analysis(metadata_list)
    
    def generate_layer_requirements(self, layer: str, files: List[Dict[str, Any]]):
        """Generate requirements document for architectural layer"""
        layer_dir = os.path.join(self.output_dir, 'requirements', 'by_layer')
        os.makedirs(layer_dir, exist_ok=True)
        
        md_content = f"# {layer.title()} Layer Requirements\n\n"
        md_content += f"Total files in this layer: {len(files)}\n\n"
        
        for file_meta in files:
            file_path = file_meta.get('file_path', '')
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            md_content += f"## {file_path}\n\n"
            md_content += f"**Component Type**: {classification.get('component_type', 'unknown')}\n\n"
            md_content += f"**Primary Purpose**: {classification.get('primary_purpose', 'Not specified')}\n\n"
            md_content += f"**Technology Stack**: {', '.join(classification.get('technology_stack', []))}\n\n"
            md_content += f"**Design Patterns**: {', '.join(classification.get('design_patterns', []))}\n\n"
            
            if classification.get('business_domain'):
                md_content += f"**Business Domain**: {classification.get('business_domain')}\n\n"
            
            if enhanced_analysis.get('purpose'):
                md_content += f"**Detailed Purpose**: {enhanced_analysis.get('purpose')}\n\n"
        
        # Write markdown file
        filename = f"{layer}_requirements.md"
        filepath = os.path.join(layer_dir, filename)
        with open(filepath, 'w') as f:
            f.write(md_content)
```

## Implementation Timeline

### Week 1: Foundation
- [ ] Create enhanced metadata schemas
- [ ] Implement classification prompt builder
- [ ] Set up enhanced AI analysis structure

### Week 2: Core Analysis Enhancement
- [ ] Update AI analyzer with classification logic
- [ ] Implement enhanced prompts
- [ ] Add fallback classification mechanisms

### Week 3: Storage and Grouping
- [ ] Update ChromaDB connector for enhanced metadata
- [ ] Implement metadata grouping utilities
- [ ] Create filtering and search capabilities

### Week 4: Integration and Testing
- [ ] Update main processing pipeline
- [ ] Create enhanced requirements generator
- [ ] Implement architecture reporting

### Week 5: Validation and Optimization
- [ ] Test classification accuracy
- [ ] Optimize AI prompts based on results
- [ ] Add confidence scoring improvements

## Expected Outcomes

### Improved Organization
- Files automatically grouped by architectural layer
- Components classified by technical purpose
- Technology stack detection and grouping
- Business domain identification

### Enhanced Analysis
- Design pattern recognition
- Integration point identification
- Security and performance considerations
- Complexity and quality indicators

### Better Documentation
- Layer-specific requirements documents
- Component-type grouped analysis
- Cross-cutting concern documentation
- Architecture overview reports

### Quality Metrics
- Classification confidence scores
- Coverage analysis by layer
- Technology usage statistics
- Pattern compliance reporting

## Success Criteria

1. **Classification Accuracy**: >85% confidence on core files
2. **Layer Distribution**: Clear separation of architectural concerns
3. **Technology Detection**: Accurate framework and library identification
4. **Pattern Recognition**: Identification of common design patterns
5. **Documentation Quality**: Well-organized, actionable requirements documents

This plan transforms the existing AI analysis into an intelligent architectural classification system that provides deep insights into codebase structure and organization.