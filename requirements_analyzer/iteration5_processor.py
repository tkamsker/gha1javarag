import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import re
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ClusterRequirement:
    cluster_id: str
    cluster_name: str
    description: str
    functional_requirements: List[Dict]
    data_model_entities: List[str]
    business_rules: List[str]
    source_files: List[str]

class Iteration5Processor:
    def __init__(self, clusters_file: str, analysis_report_file: str):
        self.clusters_file = clusters_file
        self.analysis_report_file = analysis_report_file
        self.clusters: Dict = {}
        self.analysis_report: Dict = {}
        self.cluster_requirements: List[ClusterRequirement] = []
        logger.debug(f"Initialized processor with clusters_file: {clusters_file}, analysis_report_file: {analysis_report_file}")
        
    def load_data(self):
        """Load both clusters and analysis report data."""
        try:
            with open(self.clusters_file, 'r') as f:
                self.clusters = json.load(f)
            logger.debug(f"Loaded clusters from {self.clusters_file}")
        except Exception as e:
            logger.error(f"Error loading clusters: {e}")
            raise

        try:
            with open(self.analysis_report_file, 'r') as f:
                self.analysis_report = json.load(f)
            logger.debug(f"Loaded analysis report from {self.analysis_report_file}")
        except Exception as e:
            logger.error(f"Error loading analysis report: {e}")
            raise
            
    def extract_cluster_name(self, cluster_id: str, cluster_data: Dict) -> str:
        """Extract meaningful cluster name from cluster data."""
        # Look for common patterns in class names
        class_names = list(cluster_data.keys())
        if not class_names:
            logger.debug(f"No class names found for cluster {cluster_id}")
            return f"Cluster_{cluster_id}"
            
        # Try to find a common prefix or category
        prefixes = set()
        for class_name in class_names:
            if '::' in class_name:
                prefix = class_name.split('::')[0]
                prefixes.add(prefix)
                
        if prefixes:
            logger.debug(f"Found prefixes for cluster {cluster_id}: {prefixes}")
            return f"{list(prefixes)[0]}_Cluster"
        logger.debug(f"No prefixes found for cluster {cluster_id}")
        return f"Cluster_{cluster_id}"
        
    def extract_functional_requirements(self, cluster_data: Dict) -> List[Dict]:
        """Extract functional requirements from cluster data."""
        requirements = []
        for class_name, artifacts in cluster_data.items():
            logger.debug(f"Processing class: {class_name}")
            for artifact in artifacts:
                if 'source_code' not in artifact:
                    logger.debug(f"No source code found for artifact in {class_name}")
                    continue
                    
                # Extract method names and their purposes
                method_pattern = r'(public|protected|private)\s+\w+\s+(\w+)\s*\('
                methods = re.finditer(method_pattern, artifact['source_code'])
                
                for method in methods:
                    method_name = method.group(2)
                    if method_name.startswith('do'):  # Skip standard servlet methods
                        logger.debug(f"Skipping standard servlet method: {method_name}")
                        continue
                        
                    # Create requirement ID based on cluster and method
                    req_id = f"FR-{class_name.split('::')[0]}-{method_name.upper()}"
                    logger.debug(f"Extracted requirement ID: {req_id}")
                    
                    # Extract method description from comments
                    comment_pattern = r'/\*\s*(.*?)\s*\*/'
                    comments = re.findall(comment_pattern, artifact['source_code'])
                    description = comments[0] if comments else f"Implements {method_name} functionality"
                    logger.debug(f"Extracted description for {req_id}: {description}")
                    
                    # Extract SQL operations
                    sql_ops = []
                    if 'persistence_info' in artifact:
                        sql_ops = artifact['persistence_info'].get('operations', [])
                        logger.debug(f"Extracted SQL operations for {req_id}: {sql_ops}")
                    
                    # Extract table name if available
                    table_name = ""
                    if 'persistence_info' in artifact:
                        table_name = artifact['persistence_info'].get('table_name', '')
                        logger.debug(f"Extracted table name for {req_id}: {table_name}")
                    
                    requirements.append({
                        'id': req_id,
                        'description': description,
                        'source': artifact.get('source_file', ''),
                        'operations': sql_ops,
                        'table_name': table_name
                    })
                    
        return requirements
        
    def extract_data_model_entities(self, cluster_data: Dict) -> List[str]:
        """Extract data model entities from cluster data."""
        entities = set()
        for class_name, artifacts in cluster_data.items():
            for artifact in artifacts:
                if 'persistence_info' in artifact:
                    entities.add(artifact['persistence_info']['table_name'])
        return list(entities)
        
    def extract_business_rules(self, cluster_data: Dict) -> List[str]:
        """Extract business rules from cluster data."""
        rules = set()
        for class_name, artifacts in cluster_data.items():
            logger.debug(f"Processing business rules for class: {class_name}")
            for artifact in artifacts:
                if 'source_code' not in artifact:
                    logger.debug(f"No source code found for artifact in {class_name}")
                    continue
                    
                # Look for validation patterns
                validation_patterns = [
                    r'if\s*\([^)]*\)\s*{',  # if conditions
                    r'throw\s+new\s+\w+Exception',  # exception throwing
                    r'assert\s+',  # assertions
                ]
                
                for pattern in validation_patterns:
                    matches = re.finditer(pattern, artifact['source_code'])
                    for match in matches:
                        # Get more context around the match
                        start = max(0, match.start() - 100)
                        end = min(len(artifact['source_code']), match.end() + 100)
                        context = artifact['source_code'][start:end]
                        
                        # Clean up the context
                        context = re.sub(r'\s+', ' ', context).strip()
                        context = re.sub(r'[{};]', '', context)  # Remove braces and semicolons
                        
                        # Extract meaningful parts
                        if 'if' in context:
                            condition = re.search(r'if\s*\((.*?)\)', context)
                            if condition:
                                rule = f"Validation rule in {class_name}: {condition.group(1)}"
                                rules.add(rule)
                                logger.debug(f"Extracted validation rule: {rule}")
                        elif 'throw' in context:
                            exception = re.search(r'throw\s+new\s+(\w+Exception)', context)
                            if exception:
                                rule = f"Exception handling in {class_name}: {exception.group(1)}"
                                rules.add(rule)
                                logger.debug(f"Extracted exception rule: {rule}")
                        elif 'assert' in context:
                            assertion = re.search(r'assert\s+(.*?);', context)
                            if assertion:
                                rule = f"Assertion in {class_name}: {assertion.group(1)}"
                                rules.add(rule)
                                logger.debug(f"Extracted assertion rule: {rule}")
                        
        return list(rules)
        
    def extract_source_files(self, cluster_data: Dict) -> List[str]:
        """Extract unique source files from cluster data."""
        files = set()
        for class_name, artifacts in cluster_data.items():
            for artifact in artifacts:
                if 'source_file' in artifact and artifact['source_file']:
                    files.add(artifact['source_file'])
        return list(files)
        
    def process_clusters(self):
        """Process all clusters and generate requirements."""
        for cluster_id, cluster_data in self.clusters.items():
            cluster_name = self.extract_cluster_name(cluster_id, cluster_data)
            
            requirement = ClusterRequirement(
                cluster_id=cluster_id,
                cluster_name=cluster_name,
                description=f"Cluster handling {cluster_name} functionality",
                functional_requirements=self.extract_functional_requirements(cluster_data),
                data_model_entities=self.extract_data_model_entities(cluster_data),
                business_rules=self.extract_business_rules(cluster_data),
                source_files=self.extract_source_files(cluster_data)
            )
            
            self.cluster_requirements.append(requirement)
            
    def generate_requirements_doc(self, output_file: str):
        """Generate the requirements document in Markdown format."""
        with open(output_file, 'w') as f:
            f.write("# System Requirements by Cluster\n\n")
            
            for req in self.cluster_requirements:
                if not any([req.functional_requirements, req.data_model_entities, 
                          req.business_rules, req.source_files]):
                    continue
                    
                f.write(f"## Cluster: {req.cluster_name}\n\n")
                f.write(f"**Description:** {req.description}\n\n")
                
                if req.functional_requirements:
                    f.write("### Functional Requirements\n")
                    for fr in req.functional_requirements:
                        f.write(f"- **{fr['id']}:** {fr['description']}\n")
                        if fr['operations']:
                            f.write(f"  Operations: {', '.join(fr['operations'])}\n")
                        f.write(f"  _Source: {fr['source']}_\n")
                    f.write("\n")
                
                if req.data_model_entities:
                    f.write("### Data Model Entities\n")
                    for entity in req.data_model_entities:
                        f.write(f"- **{entity}**\n")
                    f.write("\n")
                
                if req.business_rules:
                    f.write("### Business Rules\n")
                    for rule in req.business_rules:
                        f.write(f"- {rule}\n")
                    f.write("\n")
                
                if req.source_files:
                    f.write("### Source Files\n")
                    for file in req.source_files:
                        f.write(f"- {file}\n")
                    f.write("\n")
                
    def generate_traceability_matrix(self, output_file: str):
        """Generate the traceability matrix in Markdown format."""
        try:
            with open(output_file, 'w') as f:
                f.write("# Requirements Traceability Matrix\n\n")
                f.write("| Requirement ID | Description | Source Files | Related Entities | Operations |\n")
                f.write("|---------------|-------------|--------------|------------------|------------|\n")
                
                for req in self.cluster_requirements:
                    for fr in req.functional_requirements:
                        # Get related entities from the requirement's table name
                        entities = fr.get('table_name', '')
                        if not entities and req.data_model_entities:
                            entities = ", ".join(req.data_model_entities)
                        
                        # Get source files
                        files = fr.get('source', '')
                        if not files and req.source_files:
                            files = ", ".join(req.source_files)
                        
                        # Get operations
                        operations = ", ".join(fr.get('operations', []))
                        
                        # Write the row
                        f.write(f"| {fr['id']} | {fr['description']} | {files} | {entities} | {operations} |\n")
            logger.debug(f"Generated traceability matrix: {output_file}")
        except Exception as e:
            logger.error(f"Error generating traceability matrix: {e}")
            raise
                    
def main():
    # Use environment variables for file paths
    clusters_file = os.getenv('CLUSTERS_FILE')
    analysis_report_file = os.getenv('ANALYSIS_REPORT_FILE')
    requirements_doc = os.getenv('REQUIREMENTS_DOC')
    traceability_matrix = os.getenv('TRACEABILITY_MATRIX')
    
    logger.debug(f"Starting processor with clusters_file: {clusters_file}, analysis_report_file: {analysis_report_file}")
    
    processor = Iteration5Processor(clusters_file, analysis_report_file)
    processor.load_data()
    processor.process_clusters()
    processor.generate_requirements_doc(requirements_doc)
    processor.generate_traceability_matrix(traceability_matrix)
    
    logger.debug("Processor completed successfully")

if __name__ == '__main__':
    main() 