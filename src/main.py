import os
from dotenv import load_dotenv
from source_loader import SourceLoader
from chromadb_connector import ChromaDBConnector
from ast_processor import ASTProcessor
import logging
import sys
from validate_doxygen_xml import validate_doxygen_xml
from doxygen_to_yaml import parse_doxygen_xml
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_doxygen_pipeline(xml_dir):
    """Run the Doxygen validation and YAML extraction pipeline."""
    # Validate Doxygen XML
    report = validate_doxygen_xml(xml_dir)
    print("Validation Report:")
    print(f"Total compounds: {report['total_compounds']}")
    print("Found kinds:")
    for kind, count in report['found_kinds'].items():
        print(f"  {kind}: {count}")
    if report['missing_kinds']:
        print("Missing kinds:")
        for kind in report['missing_kinds']:
            print(f"  {kind}")
        print("Pipeline halted due to missing expected kinds.")
        return False
    else:
        print("All expected kinds found.")
    
    # Extract YAML
    data = parse_doxygen_xml(xml_dir)
    output_file = os.path.join(xml_dir, 'doxygen_output.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    print(f"YAML output written to {output_file}")
    return True

def generate_requirements_spec(xml_dir):
    """Generate a structured requirements specification document from the YAML output."""
    yaml_file = os.path.join(xml_dir, 'doxygen_output.yaml')
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file not found at {yaml_file}")
        return
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    spec = {
        'classes': [],
        'namespaces': [],
    }
    for entry in data:
        if entry['kind'] == 'class':
            spec['classes'].append({
                'name': entry['name'],
                'compound_name': entry.get('compound_name'),
                'base_classes': entry.get('base_classes', []),
                'members': entry.get('members', []),
            })
        elif entry['kind'] == 'namespace':
            spec['namespaces'].append({
                'name': entry['name'],
                'compound_name': entry.get('compound_name'),
            })
    output_file = os.path.join(xml_dir, 'requirements_spec.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(spec, f, sort_keys=False, allow_unicode=True)
    print(f"Requirements specification written to {output_file}")

def main():
    # Load environment variables
    load_dotenv()
    xml_dir = os.getenv('XML_INPUT_DIR')
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable not set.")
        return
    if run_doxygen_pipeline(xml_dir):
        generate_requirements_spec(xml_dir)

if __name__ == "__main__":
    main() 