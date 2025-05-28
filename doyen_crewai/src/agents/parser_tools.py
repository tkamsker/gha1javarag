import logging
from typing import Type
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from ..preprocessing.chroma_loader import ChromaDBLoader

logger = logging.getLogger(__name__)

# Global loader for stateless tools
global GLOBAL_CHROMA_LOADER
GLOBAL_CHROMA_LOADER: ChromaDBLoader = None

class EntityInput(BaseModel):
    entity_id: str = Field(description="The ID of the entity to analyze")

class AnalyzeEntityTool(BaseTool):
    name: str = Field(default="analyze_entity", description="Analyzes a code entity and its relationships")
    description: str = Field(default="Analyzes a code entity and its relationships")
    args_schema: Type[BaseModel] = EntityInput

    def _run(self, entity_id: str) -> str:
        """Analyzes a code entity and its relationships."""
        try:
            entity = GLOBAL_CHROMA_LOADER.get_entity(entity_id)
            if not entity:
                return f"Entity {entity_id} not found"
            analysis = f"Analyzing entity: {entity_id}\n"
            analysis += f"Type: {entity.get('type', 'Unknown')}\n"
            analysis += f"Description: {entity.get('description', 'No description')}\n"
            if 'calls' in entity:
                analysis += f"Calls: {', '.join(entity['calls'])}\n"
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing entity {entity_id}: {str(e)}")
            return f"Error analyzing entity: {str(e)}"

class FindRelatedEntitiesTool(BaseTool):
    name: str = Field(default="find_related_entities", description="Finds entities related to a given entity")
    description: str = Field(default="Finds entities related to a given entity")
    args_schema: Type[BaseModel] = EntityInput

    def _run(self, entity_id: str) -> str:
        """Finds entities related to a given entity."""
        try:
            entity = GLOBAL_CHROMA_LOADER.get_entity(entity_id)
            if not entity:
                return f"Entity {entity_id} not found"
            related = []
            if 'calls' in entity:
                for call in entity['calls']:
                    related_entity = GLOBAL_CHROMA_LOADER.get_entity(call)
                    if related_entity:
                        related.append(f"{call} ({related_entity.get('type', 'Unknown')})")
            return f"Related entities for {entity_id}:\n" + "\n".join(related) if related else "No related entities found"
        except Exception as e:
            logger.error(f"Error finding related entities for {entity_id}: {str(e)}")
            return f"Error finding related entities: {str(e)}"

class FindSimilarEntitiesTool(BaseTool):
    name: str = Field(default="find_similar_entities", description="Finds semantically similar entities")
    description: str = Field(default="Finds semantically similar entities")
    args_schema: Type[BaseModel] = EntityInput

    def _run(self, entity_id: str) -> str:
        """Finds semantically similar entities."""
        try:
            similar = GLOBAL_CHROMA_LOADER.find_similar_entities(entity_id)
            if not similar:
                return f"No similar entities found for {entity_id}"
            return f"Similar entities for {entity_id}:\n" + "\n".join(
                f"{entity_id} ({entity.get('type', 'Unknown')})" for entity_id, entity in similar
            )
        except Exception as e:
            logger.error(f"Error finding similar entities for {entity_id}: {str(e)}")
            return f"Error finding similar entities: {str(e)}"

class ExtractRequirementsTool(BaseTool):
    name: str = Field(default="extract_requirements", description="Extracts requirements from code entities")
    description: str = Field(default="Extracts requirements from code entities")
    args_schema: Type[BaseModel] = EntityInput

    def _run(self, entity_id: str) -> str:
        """Extracts requirements from code entities."""
        try:
            entity = GLOBAL_CHROMA_LOADER.get_entity(entity_id)
            if not entity:
                return f"Entity {entity_id} not found"
            requirements = []
            if 'description' in entity:
                requirements.append(f"Description: {entity['description']}")
            if 'type' in entity:
                requirements.append(f"Type: {entity['type']}")
            if 'calls' in entity:
                requirements.append(f"Dependencies: {', '.join(entity['calls'])}")
            return f"Requirements for {entity_id}:\n" + "\n".join(requirements)
        except Exception as e:
            logger.error(f"Error extracting requirements for {entity_id}: {str(e)}")
            return f"Error extracting requirements: {str(e)}"

# Instantiate tools at module level
analyze_entity_tool = AnalyzeEntityTool()
find_related_entities_tool = FindRelatedEntitiesTool()
find_similar_entities_tool = FindSimilarEntitiesTool()
extract_requirements_tool = ExtractRequirementsTool() 