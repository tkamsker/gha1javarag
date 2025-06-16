from typing import Dict, List, Any
import logging
from pathlib import Path
import json
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Requirement(BaseModel):
    """Pydantic model for requirements."""
    feature_id: str = Field(description="Unique identifier for the requirement")
    description: str = Field(description="Detailed description of the requirement")
    source_class: str = Field(description="Source class or file")
    type: str = Field(description="Type of requirement (e.g., Functional, Non-Functional)")
    priority: str = Field(description="Priority level (High, Medium, Low)")

class RequirementGenerator:
    def __init__(self):
        """Initialize the requirement generator."""
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="data/chromadb",
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="doxygen_docs",
            metadata={"description": "Doxygen documentation for requirements analysis"}
        )
        
        # Initialize LLM
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
                
            self.llm = ChatOpenAI(
                api_key=api_key,
                temperature=0,
                model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4')
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise
        
        # Initialize requirement template
        self.requirement_template = ChatPromptTemplate.from_messages([
            ("system", """You are a requirements engineer specializing in extracting clear, testable requirements from code documentation.
            Your task is to analyze code artifacts and generate well-structured requirements that capture both functional and non-functional aspects.
            
            Guidelines:
            1. Focus on user-centric requirements
            2. Make requirements specific and measurable
            3. Include both functional and non-functional aspects
            4. Consider security, performance, and usability
            5. Use clear, unambiguous language"""),
            ("human", """
            Code Artifact:
            Name: {name}
            Type: {type}
            Brief Description: {brief}
            Detailed Description: {detailed}
            Methods: {methods}
            
            Generate a requirement specification following this format:
            {format_instructions}
            """)
        ])
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def generate_requirements(self) -> List[Requirement]:
        """Generate requirements from stored documentation."""
        logger.info("Generating requirements from documentation...")
        requirements = []
        
        # Get all documents from ChromaDB
        results = self.collection.get()
        
        for doc, metadata in zip(results['documents'], results['metadatas']):
            try:
                class_info = json.loads(doc)
                
                # Prepare input for LLM
                input_data = {
                    "name": class_info['name'],
                    "type": class_info['type'],
                    "brief": class_info['brief'],
                    "detailed": class_info['detailed'],
                    "methods": json.dumps(class_info['methods']),
                    "format_instructions": Requirement.model_json_schema()
                }
                
                # Generate requirement using LLM
                response = self.llm.invoke(self.requirement_template.format_messages(**input_data))
                
                # Parse the response into a Requirement object
                requirement = Requirement.model_validate_json(response.content)
                requirements.append(requirement)
                
                logger.debug(f"Generated requirement for {class_info['name']}: {requirement.feature_id}")
                
            except Exception as e:
                logger.error(f"Error generating requirement for {metadata.get('name')}: {str(e)}")
                continue
        
        if not requirements:
            logger.warning("No requirements were generated")
        
        return requirements

    def generate_traceability_matrix(self, requirements: List[Requirement]) -> Dict[str, Any]:
        """Generate traceability matrix between requirements and code artifacts."""
        logger.info("Generating traceability matrix...")
        
        matrix = {
            "requirements": [],
            "artifacts": [],
            "mappings": []
        }
        
        try:
            # Get all documents from ChromaDB
            results = self.collection.get()
            
            # Add requirements
            for req in requirements:
                matrix["requirements"].append({
                    "id": req.feature_id,
                    "description": req.description,
                    "type": req.type,
                    "priority": req.priority
                })
            
            # Add artifacts
            for doc, metadata in zip(results['documents'], results['metadatas']):
                class_info = json.loads(doc)
                matrix["artifacts"].append({
                    "name": class_info['name'],
                    "type": class_info['type'],
                    "file": class_info['file']
                })
            
            # Generate mappings
            for req in requirements:
                for artifact in matrix["artifacts"]:
                    # Check for direct name match
                    if artifact['name'] in req.source_class:
                        matrix["mappings"].append({
                            "requirement_id": req.feature_id,
                            "artifact_name": artifact['name'],
                            "artifact_type": artifact['type'],
                            "match_type": "direct"
                        })
                    # Check for partial match in description
                    elif artifact['name'].lower() in req.description.lower():
                        matrix["mappings"].append({
                            "requirement_id": req.feature_id,
                            "artifact_name": artifact['name'],
                            "artifact_type": artifact['type'],
                            "match_type": "partial"
                        })
            
            logger.info(f"Generated traceability matrix with {len(matrix['mappings'])} mappings")
            
        except Exception as e:
            logger.error(f"Error generating traceability matrix: {str(e)}")
            raise
        
        return matrix

    def save_outputs(self, requirements: List[Requirement], matrix: Dict[str, Any]):
        """Save generated requirements and traceability matrix."""
        logger.info("Saving outputs...")
        
        try:
            # Save requirements
            requirements_file = self.output_dir / "requirements.json"
            with open(requirements_file, 'w', encoding='utf-8') as f:
                json.dump([req.model_dump() for req in requirements], f, indent=2, ensure_ascii=False)
            
            # Save traceability matrix
            matrix_file = self.output_dir / "traceability_matrix.json"
            with open(matrix_file, 'w', encoding='utf-8') as f:
                json.dump(matrix, f, indent=2, ensure_ascii=False)
            
            # Generate markdown report
            self._generate_markdown_report(requirements, matrix)
            
            logger.info(f"Outputs saved to {self.output_dir}")
            
        except Exception as e:
            logger.error(f"Error saving outputs: {str(e)}")
            raise

    def _generate_markdown_report(self, requirements: List[Requirement], matrix: Dict[str, Any]):
        """Generate a markdown report of the requirements and traceability."""
        report_file = self.output_dir / "requirements_report.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Requirements Specification Report\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Summary section
                f.write("## Summary\n\n")
                f.write(f"- Total Requirements: {len(requirements)}\n")
                f.write(f"- Total Artifacts: {len(matrix['artifacts'])}\n")
                f.write(f"- Total Mappings: {len(matrix['mappings'])}\n\n")
                
                # Requirements section
                f.write("## Requirements\n\n")
                f.write("| Feature ID | Description | Type | Priority | Source Class |\n")
                f.write("|------------|-------------|------|----------|--------------|\n")
                for req in requirements:
                    f.write(f"| {req.feature_id} | {req.description} | {req.type} | {req.priority} | {req.source_class} |\n")
                
                # Traceability section
                f.write("\n## Traceability Matrix\n\n")
                f.write("| Requirement ID | Artifact Name | Artifact Type | Match Type |\n")
                f.write("|----------------|---------------|---------------|------------|\n")
                for mapping in matrix["mappings"]:
                    f.write(f"| {mapping['requirement_id']} | {mapping['artifact_name']} | {mapping['artifact_type']} | {mapping['match_type']} |\n")
                
                # Statistics section
                f.write("\n## Statistics\n\n")
                f.write("### Requirements by Type\n")
                type_counts = {}
                for req in requirements:
                    type_counts[req.type] = type_counts.get(req.type, 0) + 1
                for req_type, count in type_counts.items():
                    f.write(f"- {req_type}: {count}\n")
                
                f.write("\n### Requirements by Priority\n")
                priority_counts = {}
                for req in requirements:
                    priority_counts[req.priority] = priority_counts.get(req.priority, 0) + 1
                for priority, count in priority_counts.items():
                    f.write(f"- {priority}: {count}\n")
            
            logger.info(f"Generated markdown report at {report_file}")
            
        except Exception as e:
            logger.error(f"Error generating markdown report: {str(e)}")
            raise

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize generator
        generator = RequirementGenerator()
        
        # Generate requirements
        requirements = generator.generate_requirements()
        logger.info(f"Generated {len(requirements)} requirements")
        
        if not requirements:
            logger.error("No requirements generated. Exiting.")
            return
        
        # Generate traceability matrix
        matrix = generator.generate_traceability_matrix(requirements)
        
        # Save outputs
        generator.save_outputs(requirements, matrix)
        
        logger.info("Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in pipeline execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 