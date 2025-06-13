import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from pathlib import Path
import re
import os
import logging
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from collections import defaultdict
import openai

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_VERSION')
openai.api_type = os.getenv('OPENAI_API_TYPE')

@dataclass
class DoxygenArtifact:
    name: str
    kind: str  # class, method, file
    description: str
    source_file: str
    parent: Optional[str] = None
    parameters: List[Dict] = None
    return_value: Optional[str] = None

@dataclass
class ClusterRequirement:
    cluster_id: str
    cluster_name: str
    description: str
    functional_requirements: List[Dict]
    data_model_entities: List[str]
    business_rules: List[str]
    source_files: List[str]
    doxygen_artifacts: List[DoxygenArtifact]

class Iteration5Processor:
    def __init__(self, clusters_file: str, analysis_report_file: str, xml_input_dir: str):
        self.clusters_file = clusters_file
        self.analysis_report_file = analysis_report_file
        self.xml_input_dir = xml_input_dir
        self.clusters: Dict = {}
        self.analysis_report: Dict = {}
        self.doxygen_data: Dict[str, List[DoxygenArtifact]] = defaultdict(list)
        self.cluster_requirements: List[ClusterRequirement] = []
        
        # LLM Configuration
        self.llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-4')
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE', '0.7'))
        
        logger.debug(f"Initialized processor with clusters_file: {clusters_file}, analysis_report_file: {analysis_report_file}, xml_input_dir: {xml_input_dir}")
        logger.debug(f"LLM Configuration: provider={self.llm_provider}, model={self.llm_model}, temperature={self.llm_temperature}")

    def analyze_with_llm(self, prompt: str) -> str:
        """Use OpenAI to analyze text and extract insights."""
        try:
            response = openai.ChatCompletion.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a requirements analysis expert. Extract and structure requirements from the provided text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.llm_temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return ""

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
            
    def load_doxygen_data(self):
        """Load and parse Doxygen XML files."""
        try:
            xml_files = Path(self.xml_input_dir).glob('*.xml')
            for xml_file in xml_files:
                logger.debug(f"Processing XML file: {xml_file}")
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Process compound elements (classes, files)
                for compound in root.findall('.//compounddef'):
                    kind = compound.get('kind')
                    name = compound.find('compoundname').text if compound.find('compoundname') is not None else ''
                    description = compound.find('.//briefdescription/para').text if compound.find('.//briefdescription/para') is not None else ''
                    location = compound.find('.//location')
                    source_file = location.get('file') if location is not None else ''
                    
                    # Use LLM to enhance description if available
                    if description:
                        enhanced_description = self.analyze_with_llm(f"Analyze and enhance this class description: {description}")
                        description = enhanced_description if enhanced_description else description
                    
                    artifact = DoxygenArtifact(
                        name=name,
                        kind=kind,
                        description=description,
                        source_file=source_file
                    )
                    self.doxygen_data[name].append(artifact)
                    
                    # Process member elements (methods, properties)
                    for member in compound.findall('.//memberdef'):
                        member_kind = member.get('kind')
                        member_name = member.find('name').text if member.find('name') is not None else ''
                        member_desc = member.find('.//briefdescription/para').text if member.find('.//briefdescription/para') is not None else ''
                        
                        # Use LLM to enhance method description
                        if member_desc:
                            enhanced_desc = self.analyze_with_llm(f"Analyze and enhance this method description: {member_desc}")
                            member_desc = enhanced_desc if enhanced_desc else member_desc
                        
                        # Get parameters
                        params = []
                        for param in member.findall('.//param'):
                            param_name = param.find('declname').text if param.find('declname') is not None else ''
                            param_desc = param.find('.//parameterdescription/para').text if param.find('.//parameterdescription/para') is not None else ''
                            
                            # Use LLM to enhance parameter description
                            if param_desc:
                                enhanced_param = self.analyze_with_llm(f"Analyze and enhance this parameter description: {param_desc}")
                                param_desc = enhanced_param if enhanced_param else param_desc
                            
                            params.append({'name': param_name, 'description': param_desc})
                        
                        # Get return value
                        return_value = member.find('.//detaileddescription/para').text if member.find('.//detaileddescription/para') is not None else ''
                        
                        # Use LLM to enhance return value description
                        if return_value:
                            enhanced_return = self.analyze_with_llm(f"Analyze and enhance this return value description: {return_value}")
                            return_value = enhanced_return if enhanced_return else return_value
                        
                        member_artifact = DoxygenArtifact(
                            name=member_name,
                            kind=member_kind,
                            description=member_desc,
                            source_file=source_file,
                            parent=name,
                            parameters=params,
                            return_value=return_value
                        )
                        self.doxygen_data[name].append(member_artifact)
                        
            logger.debug(f"Loaded XML data for {len(self.doxygen_data)} artifacts")
        except Exception as e:
            logger.error(f"Error loading XML data: {e}")
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
        """Extract functional requirements from cluster data and XML artifacts."""
        requirements = []
        for class_name, artifacts in cluster_data.items():
            logger.debug(f"Processing class: {class_name}")
            
            # Get XML artifacts for this class
            xml_artifacts = self.doxygen_data.get(class_name, [])
            
            for artifact in artifacts:
                if 'source_code' not in artifact:
                    logger.debug(f"No source code found for artifact in {class_name}")
                    continue
                
                # Process methods from source code
                method_pattern = r'(public|protected|private)\s+\w+\s+(\w+)\s*\('
                methods = re.finditer(method_pattern, artifact['source_code'])
                
                for method in methods:
                    method_name = method.group(2)
                    if method_name.startswith('do'):  # Skip standard servlet methods
                        logger.debug(f"Skipping standard servlet method: {method_name}")
                        continue
                    
                    # Find corresponding XML artifact
                    xml_method = next((a for a in xml_artifacts if a.name == method_name), None)
                    
                    # Create requirement ID based on cluster and method
                    req_id = f"FR-{class_name.split('::')[0]}-{method_name.upper()}"
                    logger.debug(f"Extracted requirement ID: {req_id}")
                    
                    # Use XML description if available, otherwise extract from comments
                    if xml_method and xml_method.description:
                        description = xml_method.description
                    else:
                        comment_pattern = r'/\*\s*(.*?)\s*\*/'
                        comments = re.findall(comment_pattern, artifact['source_code'])
                        description = comments[0] if comments else f"Implements {method_name} functionality"
                    
                    # Use LLM to enhance the description
                    enhanced_description = self.analyze_with_llm(f"Analyze and enhance this requirement description: {description}")
                    description = enhanced_description if enhanced_description else description
                    
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
                    
                    # Add parameters from XML if available
                    parameters = []
                    if xml_method and xml_method.parameters:
                        parameters = xml_method.parameters
                    
                    requirements.append({
                        'id': req_id,
                        'description': description,
                        'source': artifact.get('source_file', ''),
                        'operations': sql_ops,
                        'table_name': table_name,
                        'parameters': parameters,
                        'return_value': xml_method.return_value if xml_method else None
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
        """Extract business rules from cluster data and XML artifacts."""
        rules = set()
        
        # Extract rules from XML descriptions
        for class_name, artifacts in cluster_data.items():
            xml_artifacts = self.doxygen_data.get(class_name, [])
            for artifact in xml_artifacts:
                if artifact.description:
                    # Use LLM to identify business rules
                    prompt = f"Extract business rules from this description: {artifact.description}"
                    rules_text = self.analyze_with_llm(prompt)
                    if rules_text:
                        rules.add(f"Business rule from {class_name}: {rules_text}")
        
        # Extract rules from source code
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
                    r'validate[A-Z]\w+',  # validation methods
                    r'check[A-Z]\w+',  # check methods
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
                        
                        # Use LLM to analyze the context and extract rules
                        prompt = f"Extract business rules from this code context: {context}"
                        rules_text = self.analyze_with_llm(prompt)
                        if rules_text:
                            rules.add(f"Business rule from {class_name}: {rules_text}")
        
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
            
            # Get XML artifacts for this cluster
            cluster_artifacts = []
            for class_name in cluster_data.keys():
                cluster_artifacts.extend(self.doxygen_data.get(class_name, []))
            
            requirement = ClusterRequirement(
                cluster_id=cluster_id,
                cluster_name=cluster_name,
                description=f"Cluster handling {cluster_name} functionality",
                functional_requirements=self.extract_functional_requirements(cluster_data),
                data_model_entities=self.extract_data_model_entities(cluster_data),
                business_rules=self.extract_business_rules(cluster_data),
                source_files=self.extract_source_files(cluster_data),
                doxygen_artifacts=cluster_artifacts
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
                        if fr['parameters']:
                            f.write("  Parameters:\n")
                            for param in fr['parameters']:
                                f.write(f"  - {param['name']}: {param['description']}\n")
                        if fr['return_value']:
                            f.write(f"  Returns: {fr['return_value']}\n")
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
    xml_input_dir = os.getenv('XML_INPUT_DIR')
    
    logger.debug(f"Starting processor with clusters_file: {clusters_file}, analysis_report_file: {analysis_report_file}")
    
    processor = Iteration5Processor(clusters_file, analysis_report_file, xml_input_dir)
    processor.load_data()
    processor.load_doxygen_data()
    processor.process_clusters()
    processor.generate_requirements_doc(requirements_doc)
    processor.generate_traceability_matrix(traceability_matrix)
    
    logger.debug("Processor completed successfully")

if __name__ == '__main__':
    main() 