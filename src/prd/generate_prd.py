from typing import List
import os
from src.common.models import CodeArtifact
import ollama
import logging

logger = logging.getLogger(__name__)

def generate_prd(project_name: str, artifacts: List[CodeArtifact], output_file: str, frontend: bool, include_frontend: bool):
    """
    Generates a PRD document from a list of CodeArtifacts using Ollama.
    """
    try:
        # Filter artifacts based on frontend/include_frontend flags
        filtered_artifacts = []
        if frontend: # Only frontend
            for artifact in artifacts:
                if "jsp" in artifact.language or "js" in artifact.language or "gwt" in artifact.framework.lower():
                    filtered_artifacts.append(artifact)
        elif include_frontend: # Both backend and frontend
            filtered_artifacts = artifacts
        else: # Only backend
            for artifact in artifacts:
                if not ("jsp" in artifact.language or "js" in artifact.language or "gwt" in artifact.framework.lower()):
                    filtered_artifacts.append(artifact)
        
        if not filtered_artifacts:
            logger.warning(f"No artifacts found for PRD generation for project {project_name} with specified filters.")
            with open(output_file, "w") as f:
                f.write(f"# PRD for {project_name}\n\nNo artifacts to generate PRD.")
            return

        # Prepare prompt for Ollama
        prompt_artifacts = "\n".join([
            f"### {art.artifact_type}: {art.artifact_id}\nFile: {art.file_path}\nDetails: {art.details}\nContent Summary: {art.content_for_embedding[:200]}..." 
            for art in filtered_artifacts
        ])
        
        prompt = f"""
        Based on the following code artifacts from project '{project_name}', generate a Product Requirements Document (PRD) in Markdown format.
        The PRD should include:
        - A high-level overview
        - Key features derived from the artifacts
        - User stories
        - Technical details (briefly, based on artifact types)
        - Potential areas for further development

        Code Artifacts:
        {prompt_artifacts}

        Please make sure the output is well-structured Markdown.
        """

        response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt}])
        prd_content = response['message']['content']

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            f.write(prd_content)
        logger.info(f"Generated PRD for project {project_name} at {output_file}")

    except Exception as e:
        logger.error(f"Error generating PRD: {e}")
