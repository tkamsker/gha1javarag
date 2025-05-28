"""Parser agent for analyzing codebase structure."""

import logging
import re
from typing import Dict, Any, List
from crewai import Agent, Task
from ..preprocessing.chroma_loader import ChromaDBLoader
from .parser_tools import (
    GLOBAL_CHROMA_LOADER,
    analyze_entity_tool,
    find_related_entities_tool,
    find_similar_entities_tool,
    extract_requirements_tool
)

logger = logging.getLogger(__name__)

class ParserAgent:
    """Agent for parsing and analyzing code entities."""
    def __init__(self, chroma_loader: ChromaDBLoader):
        global GLOBAL_CHROMA_LOADER
        GLOBAL_CHROMA_LOADER = chroma_loader
        self.chroma_loader = chroma_loader
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        tools = [
            analyze_entity_tool,
            find_related_entities_tool,
            find_similar_entities_tool,
            extract_requirements_tool
        ]
        return Agent(
            role="Codebase Parser",
            goal="Analyze code entities and their relationships",
            backstory="You are an expert codebase parser.",
            tools=tools,
            verbose=True
        )

    def analyze_entity(self, entity_id: str) -> Dict[str, Any]:
        """Analyze a single entity.
        
        Args:
            entity_id: ID of the entity to analyze
            
        Returns:
            Dictionary containing entity analysis
        """
        try:
            entity = self.chroma_loader.get_entity(entity_id)
            if not entity:
                return {"error": f"Entity {entity_id} not found"}
            
            return {
                "id": entity_id,
                "name": entity.get("name", ""),
                "kind": entity.get("kind", ""),
                "description": entity.get("description", ""),
                "file": entity.get("file", ""),
                "calls": entity.get("calls", []),
                "document": entity.get("document", "")
            }
        except Exception as e:
            logger.error(f"Error analyzing entity {entity_id}: {str(e)}")
            return {"error": str(e)}

    def find_related_entities(self, entity_id: str) -> List[Dict[str, Any]]:
        """Find entities related to the given entity.
        
        Args:
            entity_id: ID of the entity to find related ones for
            
        Returns:
            List of related entities with their metadata
        """
        try:
            entity = self.chroma_loader.get_entity(entity_id)
            if not entity:
                return []
            
            related = []
            for call in entity.get("calls", []):
                called_entity = self.chroma_loader.get_entity(call)
                if called_entity:
                    related.append({
                        "id": call,
                        "name": called_entity.get("name", ""),
                        "kind": called_entity.get("kind", ""),
                        "description": called_entity.get("description", ""),
                        "file": called_entity.get("file", ""),
                        "calls": called_entity.get("calls", []),
                        "document": called_entity.get("document", "")
                    })
            return related
        except Exception as e:
            logger.error(f"Error finding related entities: {str(e)}")
            return []

    def find_similar_entities(self, entity_id: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Find semantically similar entities (public for testing)."""
        try:
            similar = self.chroma_loader.find_similar_entities(entity_id, n_results)
            return [{"id": id, **metadata} for id, metadata in similar]
        except Exception as e:
            logger.error(f"Error finding similar entities: {str(e)}")
            return []

    def extract_requirements(self, description: str) -> List[str]:
        """Extract requirements from a description (public for testing)."""
        try:
            requirements = []
            lines = description.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith(("- ", "* ", "• ")) or re.match(r"^\d+\.\s", line):
                    requirements.append(line.lstrip("- *•1234567890. "))
            return requirements
        except Exception as e:
            logger.error(f"Error extracting requirements: {str(e)}")
            return []

    def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the entire codebase.
        
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Get all entities
            entities = self.chroma_loader.get_all_entities()
            if not entities:
                return {
                    "total_entities": 0,
                    "entities": [],
                    "relationships": [],
                    "requirements": []
                }
            
            # Analyze each entity
            results = []
            relationships = []
            requirements = []
            for entity_id, entity in entities.items():
                # Get entity details
                details = self.analyze_entity(entity_id)
                if details:
                    results.append(details)
                
                # Find related entities
                related = self.find_related_entities(entity_id)
                for rel in related:
                    relationships.append({
                        "source": entity_id,
                        "target": rel["id"],
                        "type": "calls"
                    })
                
                # Find similar entities
                similar = self.find_similar_entities(entity_id)
                for sim in similar:
                    if sim["id"] != entity_id:  # Avoid self-similarity
                        relationships.append({
                            "source": entity_id,
                            "target": sim["id"],
                            "type": "similar",
                            "similarity": sim["similarity"]
                        })
                
                # Extract requirements
                if entity.get("description"):
                    reqs = self.extract_requirements(entity["description"])
                    requirements.extend(reqs)
            
            return {
                "total_entities": len(entities),
                "entities": results,
                "relationships": relationships,
                "requirements": list(set(requirements))  # Remove duplicates
            }
            
        except Exception as e:
            logger.error(f"Error analyzing codebase: {str(e)}")
            return {
                "total_entities": 0,
                "entities": [],
                "relationships": [],
                "requirements": []
            } 