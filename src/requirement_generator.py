import os
import yaml
from dotenv import load_dotenv

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

if __name__ == "__main__":
    load_dotenv()
    xml_dir = os.getenv('XML_INPUT_DIR')
    output_dir = os.getenv('OUTPUT_DIR', './output')
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable not set.")
    else:
        generate_requirements_spec(xml_dir, output_dir) 