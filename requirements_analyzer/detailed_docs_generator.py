import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
import logging
from dataclasses import dataclass
from collections import defaultdict
from config import (
    CLUSTERS_FILE, ANALYSIS_REPORT_FILE, OUTPUT_DIR,
    SERVLET_ANALYSIS_FILE, DATA_MODEL_FILE, BUSINESS_RULES_FILE,
    DOC_TEMPLATES, CODE_PATTERNS, LOG_CONFIG
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG["level"]),
    format=LOG_CONFIG["format"],
    filename=LOG_CONFIG["file"]
)
logger = logging.getLogger(__name__)

@dataclass
class ServletAnalysis:
    name: str
    input_params: List[Dict[str, str]]
    output_destinations: List[Dict[str, str]]
    error_handling: List[Dict[str, str]]
    dependencies: List[str] = None
    complexity: int = 0

@dataclass
class DataModelEntity:
    name: str
    attributes: List[Dict[str, str]]
    relationships: List[Dict[str, str]]
    constraints: List[str]
    table_name: Optional[str] = None
    primary_key: Optional[str] = None

@dataclass
class BusinessRule:
    id: str
    description: str
    source_files: List[str]
    affected_entities: List[str]
    validation_logic: str
    priority: int = 0
    category: str = "General"

class CodeAnalyzer:
    """Static code analysis utilities."""
    
    @staticmethod
    def calculate_complexity(source_code: str) -> int:
        """Calculate cyclomatic complexity of the code."""
        complexity = 1  # Base complexity
        
        # Count control structures
        control_patterns = [
            r'if\s*\(',
            r'else\s*{',
            r'for\s*\(',
            r'while\s*\(',
            r'switch\s*\(',
            r'case\s+',
            r'catch\s*\(',
            r'\|\|',
            r'&&'
        ]
        
        for pattern in control_patterns:
            complexity += len(re.findall(pattern, source_code))
        
        return complexity

    @staticmethod
    def extract_dependencies(source_code: str) -> List[str]:
        """Extract dependencies from import statements and annotations."""
        dependencies = set()
        
        # Extract imports
        import_pattern = r'import\s+([\w\.]+)'
        dependencies.update(re.findall(import_pattern, source_code))
        
        # Extract annotations
        annotation_pattern = r'@(\w+)'
        dependencies.update(re.findall(annotation_pattern, source_code))
        
        return sorted(list(dependencies))

class DetailedDocsGenerator:
    def __init__(self):
        self.clusters = self._load_json(CLUSTERS_FILE)
        self.analysis_report = self._load_json(ANALYSIS_REPORT_FILE)
        
        # Initialize collections
        self.servlets: Dict[str, ServletAnalysis] = {}
        self.data_model: Dict[str, DataModelEntity] = {}
        self.business_rules: List[BusinessRule] = []
        
        # Initialize analyzer
        self.analyzer = CodeAnalyzer()

    def _load_json(self, file_path: str) -> dict:
        """Load and validate JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded {file_path}")
                return data
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            return {}

    def _extract_servlet_info(self, source_code: str, name: str) -> ServletAnalysis:
        """Extract servlet information with enhanced analysis."""
        # Extract input parameters
        input_params = []
        for match in re.finditer(CODE_PATTERNS["param"], source_code, re.DOTALL):
            param_name = match.group(1)
            param_desc = match.group(2).strip()
            input_params.append({
                "name": param_name,
                "type": "String",
                "description": param_desc
            })

        # Extract output destinations
        output_destinations = []
        for match in re.finditer(CODE_PATTERNS["db_operation"], source_code):
            output_destinations.append({
                "type": "Database",
                "destination": match.group(1),
                "description": "Database operation"
            })

        # Extract error handling
        error_handling = []
        for match in re.finditer(CODE_PATTERNS["error_handling"], source_code, re.DOTALL):
            error_type = match.group(2).strip()
            handling = match.group(3).strip()
            error_handling.append({
                "pattern": error_type,
                "handling": handling,
                "description": f"Error handling for {error_type}"
            })

        # Calculate complexity and dependencies
        complexity = self.analyzer.calculate_complexity(source_code)
        dependencies = self.analyzer.extract_dependencies(source_code)

        return ServletAnalysis(
            name=name,
            input_params=input_params,
            output_destinations=output_destinations,
            error_handling=error_handling,
            dependencies=dependencies,
            complexity=complexity
        )

    def _extract_data_model(self, source_code: str) -> List[DataModelEntity]:
        """Extract data model information with enhanced analysis."""
        entities = []
        for match in re.finditer(CODE_PATTERNS["class"], source_code, re.DOTALL):
            class_name = match.group(1)
            class_body = match.group(2)
            
            # Extract attributes
            attributes = []
            for attr_match in re.finditer(CODE_PATTERNS["attribute"], class_body):
                attr_type = attr_match.group(1)
                attr_name = attr_match.group(2)
                attributes.append({
                    "name": attr_name,
                    "type": attr_type,
                    "description": ""
                })

            # Extract relationships
            relationships = []
            for rel_match in re.finditer(CODE_PATTERNS["attribute"], class_body):
                rel_type = rel_match.group(1)
                rel_name = rel_match.group(2)
                relationships.append({
                    "entity": rel_name,
                    "type": rel_type,
                    "description": ""
                })

            # Try to identify table name and primary key
            table_name = None
            primary_key = None
            table_pattern = r'@Table\s*\(\s*name\s*=\s*["\']([^"\']+)["\']'
            pk_pattern = r'@Id\s+.*?private\s+\w+\s+(\w+)\s*;'
            
            table_match = re.search(table_pattern, class_body)
            if table_match:
                table_name = table_match.group(1)
            
            pk_match = re.search(pk_pattern, class_body)
            if pk_match:
                primary_key = pk_match.group(1)

            entities.append(DataModelEntity(
                name=class_name,
                attributes=attributes,
                relationships=relationships,
                constraints=[],
                table_name=table_name,
                primary_key=primary_key
            ))

        return entities

    def _extract_business_rules(self, source_code: str, file_name: str) -> List[BusinessRule]:
        """Extract business rules with enhanced analysis."""
        rules = []
        for match in re.finditer(CODE_PATTERNS["validation"], source_code, re.DOTALL):
            validation_logic = match.group(1).strip()
            
            # Determine rule category based on method name
            category = "General"
            if "validate" in validation_logic.lower():
                category = "Validation"
            elif "check" in validation_logic.lower():
                category = "Check"
            
            # Calculate priority based on complexity
            priority = self.analyzer.calculate_complexity(validation_logic)
            
            rules.append(BusinessRule(
                id=f"BR_{len(rules) + 1}",
                description=f"Validation rule: {validation_logic[:100]}...",
                source_files=[file_name],
                affected_entities=[],
                validation_logic=validation_logic,
                priority=priority,
                category=category
            ))
        return rules

    def process_clusters(self):
        """Process all clusters with enhanced analysis."""
        for cluster_id, cluster_data in self.clusters.items():
            logger.info(f"Processing cluster {cluster_id}")
            for artifact in cluster_data.get('artifacts', []):
                source_code = artifact.get('source_code', '')
                if not source_code:
                    continue

                file_name = artifact.get('name', '')
                
                # Process servlets
                if file_name.endswith(('.jsp', '.java')):
                    servlet_info = self._extract_servlet_info(source_code, file_name)
                    self.servlets[servlet_info.name] = servlet_info
                    logger.debug(f"Processed servlet: {file_name}")

                # Process data model
                if file_name.endswith('.java'):
                    entities = self._extract_data_model(source_code)
                    for entity in entities:
                        self.data_model[entity.name] = entity
                    logger.debug(f"Processed data model from: {file_name}")

                # Process business rules
                if file_name.endswith('.java'):
                    rules = self._extract_business_rules(source_code, file_name)
                    self.business_rules.extend(rules)
                    logger.debug(f"Processed business rules from: {file_name}")

    def generate_documentation(self):
        """Generate all documentation files with enhanced formatting."""
        self.process_clusters()
        
        # Generate servlet documentation
        self._generate_servlet_docs()
        
        # Generate data model documentation
        self._generate_data_model_docs()
        
        # Generate business rules documentation
        self._generate_business_rules_docs()
        
        logger.info("Documentation generation completed")

    def _generate_servlet_docs(self):
        """Generate enhanced servlet documentation."""
        with open(SERVLET_ANALYSIS_FILE, 'w', encoding='utf-8') as f:
            f.write(DOC_TEMPLATES["servlet"]["header"])
            
            for servlet_name, analysis in sorted(self.servlets.items()):
                f.write(DOC_TEMPLATES["servlet"]["section"].format(name=servlet_name))
                
                # Add complexity and dependencies
                f.write(f"**Complexity**: {analysis.complexity}\n\n")
                f.write("**Dependencies**:\n")
                for dep in analysis.dependencies:
                    f.write(f"- {dep}\n")
                f.write("\n")
                
                # Input Parameters
                f.write(DOC_TEMPLATES["servlet"]["input_params"])
                for param in analysis.input_params:
                    f.write(f"- **{param['name']}** ({param['type']}): {param['description']}\n")
                f.write("\n")
                
                # Output Destinations
                f.write(DOC_TEMPLATES["servlet"]["output_dest"])
                for dest in analysis.output_destinations:
                    f.write(f"- **{dest['type']}**: {dest['destination']}\n")
                    f.write(f"  - {dest['description']}\n")
                f.write("\n")
                
                # Error Handling
                f.write(DOC_TEMPLATES["servlet"]["error_handling"])
                for error in analysis.error_handling:
                    f.write(f"- **{error['pattern']}**\n")
                    f.write(f"  - Handling: {error['handling']}\n")
                    f.write(f"  - Description: {error['description']}\n")
                f.write("\n")

    def _generate_data_model_docs(self):
        """Generate enhanced data model documentation."""
        with open(DATA_MODEL_FILE, 'w', encoding='utf-8') as f:
            f.write(DOC_TEMPLATES["data_model"]["header"])
            
            for entity_name, entity in sorted(self.data_model.items()):
                f.write(DOC_TEMPLATES["data_model"]["section"].format(name=entity_name))
                
                # Add table information if available
                if entity.table_name:
                    f.write(f"**Table**: {entity.table_name}\n")
                if entity.primary_key:
                    f.write(f"**Primary Key**: {entity.primary_key}\n")
                f.write("\n")
                
                # Attributes
                f.write(DOC_TEMPLATES["data_model"]["attributes"])
                for attr in entity.attributes:
                    f.write(f"- **{attr['name']}** ({attr['type']}): {attr['description']}\n")
                f.write("\n")
                
                # Relationships
                f.write(DOC_TEMPLATES["data_model"]["relationships"])
                for rel in entity.relationships:
                    f.write(f"- **{rel['entity']}** ({rel['type']}): {rel['description']}\n")
                f.write("\n")
                
                # Constraints
                if entity.constraints:
                    f.write(DOC_TEMPLATES["data_model"]["constraints"])
                    for constraint in entity.constraints:
                        f.write(f"- {constraint}\n")
                    f.write("\n")

    def _generate_business_rules_docs(self):
        """Generate enhanced business rules documentation."""
        with open(BUSINESS_RULES_FILE, 'w', encoding='utf-8') as f:
            f.write(DOC_TEMPLATES["business_rules"]["header"])
            
            # Group rules by category
            rules_by_category = defaultdict(list)
            for rule in self.business_rules:
                rules_by_category[rule.category].append(rule)
            
            # Write rules by category
            for category, rules in sorted(rules_by_category.items()):
                f.write(f"## {category} Rules\n\n")
                
                # Sort rules by priority
                for rule in sorted(rules, key=lambda x: x.priority, reverse=True):
                    f.write(DOC_TEMPLATES["business_rules"]["section"].format(id=rule.id))
                    f.write(DOC_TEMPLATES["business_rules"]["description"].format(description=rule.description))
                    
                    f.write(DOC_TEMPLATES["business_rules"]["source_files"])
                    for file in rule.source_files:
                        f.write(f"- {file}\n")
                    f.write("\n")
                    
                    f.write(DOC_TEMPLATES["business_rules"]["affected_entities"])
                    for entity in rule.affected_entities:
                        f.write(f"- {entity}\n")
                    f.write("\n")
                    
                    f.write(DOC_TEMPLATES["business_rules"]["validation_logic"])
                    f.write(f"```java\n{rule.validation_logic}\n```\n\n")

def main():
    generator = DetailedDocsGenerator()
    generator.generate_documentation()
    logger.info("Documentation generation completed. Check the 'detailed_docs' directory for output files.")

if __name__ == "__main__":
    main() 