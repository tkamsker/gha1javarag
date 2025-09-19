"""
Weaviate Schema Definitions Optimized for 1M Token Context Window
Enhanced for repository-scale analysis with Qwen3-Coder-30B integration
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger('java_analysis.weaviate_schemas')

class ChunkType(Enum):
    """Types of code chunks for hierarchical organization"""
    REPOSITORY = "repository"          # Root level - entire repository context
    MODULE = "module"                 # Package/module level
    FILE = "file"                     # Individual file level
    CLASS = "class"                   # Class/interface level
    METHOD = "method"                 # Method/function level
    DOCUMENTATION = "documentation"   # Comments and documentation
    CONFIGURATION = "configuration"   # Config files (XML, properties, etc.)
    INTEGRATION = "integration"       # Cross-service integration points

class ArchitecturalLayer(Enum):
    """Architectural layers for Java/JSP applications"""
    PRESENTATION = "presentation"     # JSP, servlets, controllers
    SERVICE = "service"              # Business logic layer
    DATA_ACCESS = "data_access"      # DAO, repositories
    MODEL = "model"                  # Entity classes, DTOs
    CONFIGURATION = "configuration"   # Spring config, XML configs
    UTILITY = "utility"              # Helper classes, utilities
    INTEGRATION = "integration"       # External service integration
    LEGACY = "legacy"                # Legacy JSP/servlet code

@dataclass
class VectorIndexConfig:
    """Configuration for vector indexing optimization"""
    distance_metric: str = "cosine"
    ef_construction: int = 512       # Increased for better quality
    ef: int = 256                    # Search parameter
    max_connections: int = 32        # HNSW parameter
    dynamic_ef_min: int = 100        # Dynamic search optimization
    dynamic_ef_max: int = 500
    dynamic_ef_factor: int = 8

class WeaviateSchemas:
    """Weaviate schema definitions for Java/JSP code analysis"""
    
    @staticmethod
    def get_java_code_chunks_schema(ollama_url: str = "http://localhost:11434") -> Dict[str, Any]:
        """
        Primary schema for Java code chunks with 1M token context optimization
        """
        return {
            "class": "JavaCodeChunk",
            "description": "Java/JSP code chunks with enhanced metadata and 1M token context support",
            "vectorizer": "text2vec-ollama",
            "moduleConfig": {
                "text2vec-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "nomic-embed-text"
                },
                "generative-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
                }
            },
            "vectorIndexConfig": {
                "distance": "cosine",
                "efConstruction": 512,
                "ef": 256,
                "maxConnections": 32,
                "dynamicEfMin": 100,
                "dynamicEfMax": 500,
                "dynamicEfFactor": 8
            },
            "properties": [
                # Core content and identification
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The actual code content or text"
                },
                {
                    "name": "file_path",
                    "dataType": ["string"],
                    "description": "Full path to the source file"
                },
                {
                    "name": "chunk_id",
                    "dataType": ["string"],
                    "description": "Unique identifier for this chunk"
                },
                {
                    "name": "chunk_type",
                    "dataType": ["string"],
                    "description": "Type of chunk (repository, module, file, class, method, etc.)"
                },
                {
                    "name": "language",
                    "dataType": ["string"],
                    "description": "Programming language (Java, JSP, XML, etc.)"
                },
                
                # Hierarchical relationships for 1M context
                {
                    "name": "parent_chunk_id",
                    "dataType": ["string"],
                    "description": "ID of parent chunk in hierarchy"
                },
                {
                    "name": "child_chunk_ids",
                    "dataType": ["string[]"],
                    "description": "IDs of child chunks in hierarchy"
                },
                {
                    "name": "sibling_chunk_ids",
                    "dataType": ["string[]"],
                    "description": "IDs of related sibling chunks"
                },
                {
                    "name": "repository_context",
                    "dataType": ["text"],
                    "description": "Extended repository context for 1M token window analysis"
                },
                
                # Code structure metadata
                {
                    "name": "class_name",
                    "dataType": ["string"],
                    "description": "Name of the containing class"
                },
                {
                    "name": "method_name",
                    "dataType": ["string"],
                    "description": "Name of the method/function"
                },
                {
                    "name": "package_name",
                    "dataType": ["string"],
                    "description": "Java package name"
                },
                {
                    "name": "imports",
                    "dataType": ["string[]"],
                    "description": "Import statements and dependencies"
                },
                {
                    "name": "annotations",
                    "dataType": ["string[]"],
                    "description": "Java annotations present"
                },
                
                # Architectural metadata
                {
                    "name": "architectural_layer",
                    "dataType": ["string"],
                    "description": "Architectural layer (presentation, service, data_access, etc.)"
                },
                {
                    "name": "business_domain",
                    "dataType": ["string"],
                    "description": "Business domain or module"
                },
                {
                    "name": "design_patterns",
                    "dataType": ["string[]"],
                    "description": "Detected design patterns"
                },
                {
                    "name": "integration_points",
                    "dataType": ["string[]"],
                    "description": "External integration points (APIs, databases, etc.)"
                },
                
                # Quality and complexity metrics
                {
                    "name": "complexity_score",
                    "dataType": ["number"],
                    "description": "Cyclomatic complexity score"
                },
                {
                    "name": "lines_of_code",
                    "dataType": ["int"],
                    "description": "Number of lines of code"
                },
                {
                    "name": "technical_debt_score",
                    "dataType": ["number"],
                    "description": "Estimated technical debt score"
                },
                {
                    "name": "maintainability_index",
                    "dataType": ["number"],
                    "description": "Maintainability index (0-100)"
                },
                
                # Qwen3-Coder specific analysis
                {
                    "name": "qwen_analysis_score",
                    "dataType": ["number"],
                    "description": "Qwen3-Coder specific analysis quality score"
                },
                {
                    "name": "modernization_opportunities",
                    "dataType": ["string[]"],
                    "description": "Identified modernization opportunities"
                },
                {
                    "name": "performance_insights",
                    "dataType": ["string[]"],
                    "description": "Performance optimization insights"
                },
                {
                    "name": "security_concerns",
                    "dataType": ["string[]"],
                    "description": "Identified security concerns"
                },
                
                # Legacy JSP specific metadata
                {
                    "name": "jsp_elements",
                    "dataType": ["string[]"],
                    "description": "JSP elements used (scriptlets, expressions, etc.)"
                },
                {
                    "name": "servlet_mappings",
                    "dataType": ["string[]"],
                    "description": "Servlet mappings and URL patterns"
                },
                {
                    "name": "legacy_patterns",
                    "dataType": ["string[]"],
                    "description": "Detected legacy patterns that need modernization"
                },
                
                # Context window optimization
                {
                    "name": "token_count",
                    "dataType": ["int"],
                    "description": "Estimated token count for content"
                },
                {
                    "name": "context_weight",
                    "dataType": ["number"],
                    "description": "Weight for context window prioritization"
                },
                {
                    "name": "semantic_importance",
                    "dataType": ["number"],
                    "description": "Semantic importance score for retrieval ranking"
                },
                
                # Metadata timestamps
                {
                    "name": "created_at",
                    "dataType": ["date"],
                    "description": "Chunk creation timestamp"
                },
                {
                    "name": "last_analyzed",
                    "dataType": ["date"],
                    "description": "Last analysis timestamp"
                },
                {
                    "name": "analysis_version",
                    "dataType": ["string"],
                    "description": "Version of analysis pipeline used"
                }
            ]
        }
    
    @staticmethod
    def get_architectural_patterns_schema(ollama_url: str = "http://localhost:11434") -> Dict[str, Any]:
        """Schema for architectural patterns and high-level insights"""
        return {
            "class": "ArchitecturalPattern",
            "description": "Repository-wide architectural patterns and design insights",
            "vectorizer": "text2vec-ollama",
            "moduleConfig": {
                "text2vec-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "nomic-embed-text"
                },
                "generative-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
                }
            },
            "properties": [
                {
                    "name": "pattern_name",
                    "dataType": ["string"],
                    "description": "Name of the architectural pattern"
                },
                {
                    "name": "pattern_type",
                    "dataType": ["string"],
                    "description": "Type of pattern (design, architectural, integration, etc.)"
                },
                {
                    "name": "description",
                    "dataType": ["text"],
                    "description": "Detailed description of the pattern implementation"
                },
                {
                    "name": "affected_files",
                    "dataType": ["string[]"],
                    "description": "Files involved in this pattern"
                },
                {
                    "name": "affected_classes",
                    "dataType": ["string[]"],
                    "description": "Classes involved in this pattern"
                },
                {
                    "name": "confidence_score",
                    "dataType": ["number"],
                    "description": "Confidence in pattern detection (0-1)"
                },
                {
                    "name": "impact_level",
                    "dataType": ["string"],
                    "description": "Impact level (low, medium, high, critical)"
                },
                {
                    "name": "recommendations",
                    "dataType": ["string[]"],
                    "description": "Recommended actions or improvements"
                },
                {
                    "name": "repository_context",
                    "dataType": ["text"],
                    "description": "Full repository context for this pattern"
                },
                {
                    "name": "created_at",
                    "dataType": ["date"],
                    "description": "Pattern detection timestamp"
                }
            ]
        }
    
    @staticmethod
    def get_business_rules_schema(ollama_url: str = "http://localhost:11434") -> Dict[str, Any]:
        """Schema for extracted business rules and domain logic"""
        return {
            "class": "BusinessRule",
            "description": "Extracted business rules and domain logic",
            "vectorizer": "text2vec-ollama",
            "moduleConfig": {
                "text2vec-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "nomic-embed-text"
                },
                "generative-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
                }
            },
            "properties": [
                {
                    "name": "rule_name",
                    "dataType": ["string"],
                    "description": "Business rule identifier"
                },
                {
                    "name": "rule_description",
                    "dataType": ["text"],
                    "description": "Description of the business rule"
                },
                {
                    "name": "business_domain",
                    "dataType": ["string"],
                    "description": "Business domain (finance, hr, inventory, etc.)"
                },
                {
                    "name": "rule_type",
                    "dataType": ["string"],
                    "description": "Type of rule (validation, calculation, workflow, etc.)"
                },
                {
                    "name": "implementation_files",
                    "dataType": ["string[]"],
                    "description": "Files where this rule is implemented"
                },
                {
                    "name": "related_entities",
                    "dataType": ["string[]"],
                    "description": "Domain entities affected by this rule"
                },
                {
                    "name": "validation_logic",
                    "dataType": ["text"],
                    "description": "Validation logic implementation"
                },
                {
                    "name": "business_context",
                    "dataType": ["text"],
                    "description": "Business context and justification"
                },
                {
                    "name": "complexity_level",
                    "dataType": ["string"],
                    "description": "Rule complexity (simple, moderate, complex, very_complex)"
                },
                {
                    "name": "modernization_priority",
                    "dataType": ["string"],
                    "description": "Priority for modernization (low, medium, high, critical)"
                },
                {
                    "name": "created_at",
                    "dataType": ["date"],
                    "description": "Rule extraction timestamp"
                }
            ]
        }
    
    @staticmethod
    def get_integration_points_schema(ollama_url: str = "http://localhost:11434") -> Dict[str, Any]:
        """Schema for integration points and external dependencies"""
        return {
            "class": "IntegrationPoint",
            "description": "External integration points and API connections",
            "vectorizer": "text2vec-ollama",
            "moduleConfig": {
                "text2vec-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "nomic-embed-text"
                },
                "generative-ollama": {
                    "endpoint": f"{ollama_url}",
                    "model": "danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
                }
            },
            "properties": [
                {
                    "name": "integration_name",
                    "dataType": ["string"],
                    "description": "Name of the integration point"
                },
                {
                    "name": "integration_type",
                    "dataType": ["string"],
                    "description": "Type (REST API, SOAP, Database, File, Queue, etc.)"
                },
                {
                    "name": "endpoint_url",
                    "dataType": ["string"],
                    "description": "Integration endpoint URL or connection string"
                },
                {
                    "name": "protocol",
                    "dataType": ["string"],
                    "description": "Communication protocol (HTTP, HTTPS, JDBC, JMS, etc.)"
                },
                {
                    "name": "authentication_method",
                    "dataType": ["string"],
                    "description": "Authentication method used"
                },
                {
                    "name": "data_format",
                    "dataType": ["string"],
                    "description": "Data format (JSON, XML, CSV, etc.)"
                },
                {
                    "name": "implementation_files",
                    "dataType": ["string[]"],
                    "description": "Files implementing this integration"
                },
                {
                    "name": "error_handling",
                    "dataType": ["text"],
                    "description": "Error handling implementation"
                },
                {
                    "name": "performance_characteristics",
                    "dataType": ["text"],
                    "description": "Performance and scalability characteristics"
                },
                {
                    "name": "security_considerations",
                    "dataType": ["string[]"],
                    "description": "Security considerations and implementations"
                },
                {
                    "name": "modernization_recommendations",
                    "dataType": ["string[]"],
                    "description": "Recommendations for modernization"
                },
                {
                    "name": "created_at",
                    "dataType": ["date"],
                    "description": "Integration point detection timestamp"
                }
            ]
        }

class SchemaManager:
    """Manages Weaviate schema operations"""
    
    def __init__(self, weaviate_client, ollama_url: str = "http://localhost:11434"):
        self.client = weaviate_client
        self.ollama_url = ollama_url
        self.schemas = WeaviateSchemas()
        
    def create_all_schemas(self) -> bool:
        """Create all schema classes in Weaviate"""
        try:
            schemas_to_create = [
                self.schemas.get_java_code_chunks_schema(self.ollama_url),
                self.schemas.get_architectural_patterns_schema(self.ollama_url),
                self.schemas.get_business_rules_schema(self.ollama_url),
                self.schemas.get_integration_points_schema(self.ollama_url)
            ]
            
            for schema in schemas_to_create:
                try:
                    # Check if class already exists
                    existing_classes = self.client.schema.get()
                    class_names = [cls['class'] for cls in existing_classes.get('classes', [])]
                    
                    if schema['class'] not in class_names:
                        self.client.schema.create_class(schema)
                        logger.info(f"Created schema class: {schema['class']}")
                    else:
                        logger.info(f"Schema class already exists: {schema['class']}")
                        
                except Exception as e:
                    logger.error(f"Failed to create schema {schema['class']}: {e}")
                    return False
            
            logger.info("All schemas created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create schemas: {e}")
            return False
    
    def delete_all_schemas(self) -> bool:
        """Delete all schema classes (use with caution)"""
        try:
            schema_classes = ["JavaCodeChunk", "ArchitecturalPattern", "BusinessRule", "IntegrationPoint"]
            
            for class_name in schema_classes:
                try:
                    self.client.schema.delete_class(class_name)
                    logger.info(f"Deleted schema class: {class_name}")
                except Exception as e:
                    logger.warning(f"Could not delete {class_name}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete schemas: {e}")
            return False
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get information about current schemas"""
        try:
            schema_info = self.client.schema.get()
            return {
                'classes': len(schema_info.get('classes', [])),
                'class_names': [cls['class'] for cls in schema_info.get('classes', [])],
                'full_schema': schema_info
            }
        except Exception as e:
            logger.error(f"Failed to get schema info: {e}")
            return {}