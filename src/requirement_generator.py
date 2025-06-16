import os
import yaml
from dotenv import load_dotenv
from chromadb_connector import ChromaDBConnector

def generate_requirements_spec(xml_dir, output_dir):
    """Generate a structured requirements specification document from the YAML output."""
    yaml_file = os.path.join(xml_dir, 'doxygen_output.yaml')
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file not found at {yaml_file}")
        return
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    spec = {
        'functional_requirements': [],
        'data_model': [],
        'traceability_matrix': [],
    }
    for entry in data:
        if entry['kind'] == 'class':
            # Generate functional requirements using AI
            feature_id = f"FR-{entry['name']}"
            description = entry.get('compound_name', '')
            source_class = entry['name']
            # Placeholder for AI-generated requirement
            ai_requirement = generate_ai_requirement(entry)
            spec['functional_requirements'].append({
                'feature_id': feature_id,
                'description': description,
                'source_class': source_class,
                'ai_generated': ai_requirement,
            })
            spec['data_model'].append({
                'entity': entry['name'],
                'attributes': [m['name'] for m in entry.get('members', []) if m['kind'] == 'variable'],
            })
            for member in entry.get('members', []):
                if member['kind'] == 'function':
                    spec['traceability_matrix'].append({
                        'requirement_id': feature_id,
                        'source_file': entry['name'],
                        'method': member['name'],
                        'type': 'Method',
                    })
    output_file = os.path.join(output_dir, 'requirements_spec.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(spec, f, sort_keys=False, allow_unicode=True)
    print(f"Requirements specification written to {output_file}")

def generate_ai_requirement(entry):
    """Placeholder function for AI-generated requirements."""
    # Replace this with actual AI logic
    return f"AI-generated requirement for {entry['name']}"

def query_chromadb_for_namespace(namespace):
    """Query ChromaDB for all files in a namespace."""
    db_connector = ChromaDBConnector()
    # Use the query method and filter by namespace if needed
    results = db_connector.query(namespace)
    return results

def generate_requirements_for_namespace(namespace, output_dir):
    """Generate requirements for a namespace using ChromaDB and LLM."""
    files = query_chromadb_for_namespace(namespace)
    if not files:
        print(f"No files found for namespace: {namespace}")
        return
    # Placeholder for LLM summarization
    summary = f"Summary for {namespace}: {files}"
    output_file = os.path.join(output_dir, f"{namespace}_requirements.yaml")
    with open(output_file, 'w') as f:
        yaml.dump({'namespace': namespace, 'summary': summary}, f, sort_keys=False, allow_unicode=True)
    print(f"Requirements for {namespace} written to {output_file}")

def identify_class_clusters(data):
    """Identify logical class clusters using AI."""
    # Placeholder for AI clustering logic
    clusters = {
        'OrderProcessing': ['Controller::AddDoctor', 'Controller::AddPatient'],
        'UserManagement': ['Controller::UserLogin', 'Controller::UserRegister'],
    }
    return clusters

def generate_markdown_requirements(clusters, output_dir):
    """Generate markdown requirements documents per cluster."""
    for cluster_name, classes in clusters.items():
        md_content = f"## Cluster: {cluster_name}\n\n"
        md_content += "**Description:** Handles all operations related to this cluster.\n\n"
        md_content += "### Functional Requirements\n"
        for class_name in classes:
            md_content += f"- **FR-{class_name}:** AI-generated requirement for {class_name}.\n"
        md_content += "\n### Data Model Entities\n"
        for class_name in classes:
            md_content += f"- **{class_name}**\n"
        md_content += "\n### Business Rules\n"
        md_content += "- Placeholder for business rules.\n"
        md_content += "\n### Source File References\n"
        for class_name in classes:
            md_content += f"- {class_name}.java\n"
        output_file = os.path.join(output_dir, f"{cluster_name}_requirements.md")
        with open(output_file, 'w') as f:
            f.write(md_content)
        print(f"Markdown requirements for {cluster_name} written to {output_file}")

if __name__ == "__main__":
    load_dotenv()
    xml_dir = os.getenv('XML_INPUT_DIR')
    output_dir = os.getenv('OUTPUT_DIR', './output')
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable not set.")
    else:
        generate_requirements_spec(xml_dir, output_dir)
        # Example: Generate requirements for the 'Controller' namespace
        generate_requirements_for_namespace('Controller', output_dir)
        # Identify class clusters and generate markdown requirements
        with open(os.path.join(xml_dir, 'doxygen_output.yaml'), 'r') as f:
            data = yaml.safe_load(f)
        clusters = identify_class_clusters(data)
        generate_markdown_requirements(clusters, output_dir) 