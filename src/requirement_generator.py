import os
import yaml
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
from chromadb_connector import ChromaDBConnector
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_requirements_spec(xml_dir: str, output_dir: str) -> None:
    """
    Generate a structured requirements specification document using reverse engineering.
    """
    yaml_file = os.path.join(xml_dir, 'doxygen_output.yaml')
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file not found at {yaml_file}")
        return

    # Load and process the YAML data
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    # Extract code artifacts
    artifacts = extract_code_artifacts(data)
    
    # Analyze dependencies
    dependencies = analyze_dependencies(artifacts)
    
    # Identify business rules
    business_rules = identify_business_rules(artifacts)
    
    # Generate requirements
    requirements = generate_requirements(artifacts, dependencies, business_rules)
    
    # Write the requirements to file
    output_file = os.path.join(output_dir, 'requirements_spec.yaml')
    with open(output_file, 'w') as f:
        yaml.dump(requirements, f, sort_keys=False, allow_unicode=True)
    print(f"Requirements specification written to {output_file}")

def generate_ai_requirement(entry):
    """Placeholder function for AI-generated requirements."""
    # Replace this with actual AI logic
    return f"AI-generated requirement for {entry['name']}"

def query_chromadb_for_namespace(namespace: str) -> List[Dict[str, Any]]:
    """
    Query ChromaDB for all files in a namespace and extract relevant information.
    """
    db_connector = ChromaDBConnector()
    results = db_connector.query(namespace)
    
    # Process and structure the results
    processed_results = []
    for result in results:
        if isinstance(result, dict):
            processed_results.append({
                'content': result.get('content', ''),
                'metadata': result.get('metadata', {}),
                'similarity': result.get('similarity', 0.0)
            })
    return processed_results

def generate_requirements_for_namespace(namespace: str, output_dir: str) -> None:
    """
    Generate requirements for a namespace using reverse engineering approach.
    """
    # Query ChromaDB for namespace information
    files = query_chromadb_for_namespace(namespace)
    if not files:
        print(f"No files found for namespace: {namespace}")
        return

    # Extract artifacts from the files
    artifacts = extract_code_artifacts(str(files))
    
    # Analyze dependencies
    dependencies = analyze_dependencies(artifacts)
    
    # Identify business rules
    business_rules = identify_business_rules(artifacts)
    
    # Generate requirements
    requirements = generate_requirements(artifacts, dependencies, business_rules)
    
    # Write the requirements to file
    output_file = os.path.join(output_dir, f"{namespace}_requirements.yaml")
    with open(output_file, 'w') as f:
        yaml.dump(requirements, f, sort_keys=False, allow_unicode=True)
    print(f"Requirements for {namespace} written to {output_file}")

def identify_class_clusters(data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Identify logical class clusters using dependency analysis.
    """
    artifacts = extract_code_artifacts(str(data))
    dependencies = analyze_dependencies(artifacts)
    
    # Group classes based on their dependencies
    clusters = {}
    for component, deps in dependencies.items():
        cluster_name = component.split('::')[0]
        if cluster_name not in clusters:
            clusters[cluster_name] = []
        clusters[cluster_name].append(component)
    
    return clusters

def generate_markdown_requirements(clusters: Dict[str, List[str]], output_dir: str) -> None:
    """
    Generate markdown requirements documents per cluster using reverse engineering.
    """
    for cluster_name, classes in clusters.items():
        # Extract artifacts for the cluster
        cluster_data = {'classes': classes}
        artifacts = extract_code_artifacts(str(cluster_data))
        
        # Analyze dependencies
        dependencies = analyze_dependencies(artifacts)
        
        # Identify business rules
        business_rules = identify_business_rules(artifacts)
        
        # Generate markdown content
        md_content = f"# Requirements Specification for {cluster_name}\n\n"
        
        # Add functional requirements
        md_content += "## Functional Requirements\n\n"
        for class_name in classes:
            md_content += f"### {class_name}\n"
            md_content += f"- **FR-{class_name}:** Derived from code analysis\n"
            if class_name in dependencies:
                md_content += "- **Dependencies:**\n"
                for dep in dependencies[class_name]:
                    md_content += f"  - {dep}\n"
        
        # Add business rules
        md_content += "\n## Business Rules\n\n"
        for rule in business_rules:
            md_content += f"- {rule}\n"
        
        # Add technical details
        md_content += "\n## Technical Details\n\n"
        md_content += "### Class Dependencies\n"
        for class_name, deps in dependencies.items():
            if class_name in classes:
                md_content += f"- **{class_name}** depends on:\n"
                for dep in deps:
                    md_content += f"  - {dep}\n"
        
        # Write to file
        output_file = os.path.join(output_dir, f"{cluster_name}_requirements.md")
        with open(output_file, 'w') as f:
            f.write(md_content)
        print(f"Markdown requirements for {cluster_name} written to {output_file}")

def generate_ai_description(text: str) -> str:
    """Generate AI description using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical writer creating software requirements documentation."},
                {"role": "user", "content": f"Generate a clear and concise description for this code element: {text}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating AI description: {str(e)}")
        return ""

def generate_data_model(attribute_info: dict) -> dict:
    """Generate data model description using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical writer creating data model documentation."},
                {"role": "user", "content": f"Generate a data model description for this attribute: {attribute_info}"}
            ],
            max_tokens=150
        )
        return {
            "description": response.choices[0].message.content.strip(),
            "type": attribute_info.get("type", "Unknown"),
            "constraints": attribute_info.get("constraints", [])
        }
    except Exception as e:
        print(f"Error generating data model for attribute {attribute_info.get('name', 'Unknown')}: {str(e)}")
        return {
            "description": "",
            "type": attribute_info.get("type", "Unknown"),
            "constraints": attribute_info.get("constraints", [])
        }

def extract_code_artifacts(source_code: str) -> Dict[str, Any]:
    """
    Extract key code artifacts from source code.
    Returns a dictionary containing classes, methods, and their relationships.
    """
    try:
        data = yaml.safe_load(source_code) if isinstance(source_code, str) else source_code
    except yaml.YAMLError:
        data = source_code

    artifacts = {
        'classes': [],
        'methods': [],
        'relationships': [],
        'attributes': [],
        'files': [],
        'namespaces': []
    }

    if isinstance(data, list):
        for entry in data:
            kind = entry.get('kind', '')
            
            # Handle different types of entries
            if kind == 'class':
                class_info = {
                    'name': entry.get('name', ''),
                    'compound_name': entry.get('compound_name', ''),
                    'description': entry.get('description', '') or generate_ai_description(entry.get('name', ''))
                }
                artifacts['classes'].append(class_info)

                # Extract methods
                for member in entry.get('members', []):
                    if member.get('kind') == 'function':
                        method_info = {
                            'name': member.get('name', ''),
                            'class': class_info['name'],
                            'description': member.get('description', '') or generate_ai_description(f"{class_info['name']}.{member.get('name', '')}"),
                            'parameters': member.get('parameters', []),
                            'return_type': member.get('return_type', '')
                        }
                        artifacts['methods'].append(method_info)

                # Extract attributes
                for member in entry.get('members', []):
                    if member.get('kind') == 'variable':
                        attribute_info = {
                            'name': member.get('name', ''),
                            'class': class_info['name'],
                            'type': member.get('type', ''),
                            'description': member.get('description', '') or generate_ai_description(f"{class_info['name']}.{member.get('name', '')}")
                        }
                        artifacts['attributes'].append(attribute_info)
            
            elif kind == 'file':
                file_info = {
                    'name': entry.get('name', ''),
                    'description': entry.get('description', '') or generate_ai_description(entry.get('name', '')),
                    'path': entry.get('path', '')
                }
                artifacts['files'].append(file_info)
            
            elif kind == 'namespace':
                namespace_info = {
                    'name': entry.get('name', ''),
                    'description': entry.get('description', '') or generate_ai_description(entry.get('name', '')),
                    'members': entry.get('members', [])
                }
                artifacts['namespaces'].append(namespace_info)

    return artifacts

def analyze_dependencies(artifacts: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Analyze dependencies between code artifacts.
    Returns a dictionary mapping components to their dependencies.
    """
    dependencies = {}
    
    # Analyze method dependencies
    for method in artifacts['methods']:
        class_name = method['class']
        if class_name not in dependencies:
            dependencies[class_name] = []
        
        # Check for parameter dependencies
        for param in method.get('parameters', []):
            param_type = param.get('type', '')
            if param_type and param_type not in dependencies[class_name]:
                dependencies[class_name].append(param_type)
        
        # Check for attribute dependencies
        for attr in artifacts['attributes']:
            if attr['class'] == class_name:
                attr_type = attr.get('type', '')
                if attr_type and attr_type not in dependencies[class_name]:
                    dependencies[class_name].append(attr_type)

    return dependencies

def identify_business_rules(artifacts: Dict[str, Any]) -> List[str]:
    """
    Identify business rules from code artifacts using AI analysis.
    """
    business_rules = []
    
    # Extract rules from class descriptions
    for class_info in artifacts['classes']:
        description = class_info.get('description', '')
        if description:
            try:
                # Use AI to extract business rules from class description
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a business analyst. Extract business rules from the following description."},
                        {"role": "user", "content": f"Extract business rules from: {description}"}
                    ],
                    max_tokens=200
                )
                rules = response.choices[0].message.content.strip().split('\n')
                business_rules.extend([f"Class {class_info['name']}: {rule}" for rule in rules if rule])
            except Exception as e:
                print(f"Error extracting business rules from class {class_info['name']}: {e}")
    
    # Extract rules from method descriptions
    for method in artifacts['methods']:
        description = method.get('description', '')
        if description:
            try:
                # Use AI to extract business rules from method description
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a business analyst. Extract business rules from the following method description."},
                        {"role": "user", "content": f"Extract business rules from: {description}"}
                    ],
                    max_tokens=200
                )
                rules = response.choices[0].message.content.strip().split('\n')
                business_rules.extend([f"Method {method['class']}.{method['name']}: {rule}" for rule in rules if rule])
            except Exception as e:
                print(f"Error extracting business rules from method {method['class']}.{method['name']}: {e}")
    
    # Extract rules from attribute descriptions
    for attr in artifacts['attributes']:
        description = attr.get('description', '')
        if description:
            try:
                # Use AI to extract business rules from attribute description
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a business analyst. Extract business rules from the following attribute description."},
                        {"role": "user", "content": f"Extract business rules from: {description}"}
                    ],
                    max_tokens=200
                )
                rules = response.choices[0].message.content.strip().split('\n')
                business_rules.extend([f"Attribute {attr['class']}.{attr['name']}: {rule}" for rule in rules if rule])
            except Exception as e:
                print(f"Error extracting business rules from attribute {attr['class']}.{attr['name']}: {e}")
    
    return business_rules

def generate_requirements(artifacts: Dict[str, Any], 
                         dependencies: Dict[str, List[str]], 
                         business_rules: List[str]) -> Dict[str, Any]:
    """
    Generate requirements from analyzed artifacts using AI enhancement.
    """
    requirements = {
        'functional_requirements': [],
        'non_functional_requirements': [],
        'business_rules': business_rules,
        'dependencies': dependencies,
        'data_model': []
    }
    
    # Generate functional requirements from methods
    for method in artifacts['methods']:
        try:
            # Use AI to enhance method description into a requirement
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a requirements engineer. Convert the following method description into a functional requirement."},
                    {"role": "user", "content": f"Convert to requirement: {method['description']}"}
                ],
                max_tokens=200
            )
            enhanced_description = response.choices[0].message.content.strip()
            
            req = {
                'id': f"FR-{method['class']}-{method['name']}",
                'description': enhanced_description,
                'source': f"{method['class']}.{method['name']}",
                'dependencies': [dep for dep in dependencies.get(method['class'], [])],
                'parameters': method.get('parameters', []),
                'return_type': method.get('return_type', '')
            }
            requirements['functional_requirements'].append(req)
        except Exception as e:
            print(f"Error generating requirement for method {method['class']}.{method['name']}: {e}")
    
    # Generate data model from attributes
    for attr in artifacts['attributes']:
        try:
            # Use AI to enhance attribute description
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data modeler. Enhance the following attribute description."},
                    {"role": "user", "content": f"Enhance description: {attr['description']}"}
                ],
                max_tokens=150
            )
            enhanced_description = response.choices[0].message.content.strip()
            
            entity = {
                'name': attr['class'],
                'attributes': [{
                    'name': attr['name'],
                    'type': attr['type'],
                    'description': enhanced_description
                }]
            }
            requirements['data_model'].append(entity)
        except Exception as e:
            print(f"Error generating data model for attribute {attr['class']}.{attr['name']}: {e}")
    
    # Add non-functional requirements based on dependencies and system characteristics
    for class_name, deps in dependencies.items():
        if deps:
            try:
                # Use AI to generate non-functional requirements
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a requirements engineer. Generate non-functional requirements based on the following dependencies."},
                        {"role": "user", "content": f"Generate NFRs for class {class_name} with dependencies: {', '.join(deps)}"}
                    ],
                    max_tokens=200
                )
                nfr_description = response.choices[0].message.content.strip()
                
                req = {
                    'id': f"NFR-{class_name}-Dependencies",
                    'description': nfr_description,
                    'source': class_name,
                    'dependencies': deps
                }
                requirements['non_functional_requirements'].append(req)
            except Exception as e:
                print(f"Error generating NFR for class {class_name}: {e}")
    
    return requirements

if __name__ == "__main__":
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not set. AI-generated descriptions will be limited.")
    
    xml_dir = os.getenv('XML_INPUT_DIR')
    output_dir = os.getenv('OUTPUT_DIR', './output')
    
    if not xml_dir:
        print("Error: XML_INPUT_DIR environment variable not set.")
    else:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate main requirements specification
        generate_requirements_spec(xml_dir, output_dir)
        
        # Generate requirements for the 'Controller' namespace
        generate_requirements_for_namespace('Controller', output_dir)
        
        # Identify class clusters and generate markdown requirements
        with open(os.path.join(xml_dir, 'doxygen_output.yaml'), 'r') as f:
            data = yaml.safe_load(f)
        clusters = identify_class_clusters(data)
        generate_markdown_requirements(clusters, output_dir) 