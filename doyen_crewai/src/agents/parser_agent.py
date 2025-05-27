"""Parser agent for analyzing codebase structure and relationships."""

from typing import Dict, List

from crewai import Agent
from langchain.tools import Tool

from ..preprocessing.chroma_loader import ChromaDBLoader

class ParserAgent:
    """Agent responsible for parsing and analyzing codebase structure."""
    
    def __init__(self, chroma_loader: ChromaDBLoader):
        """Initialize the parser agent.
        
        Args:
            chroma_loader: ChromaDB loader instance for accessing embeddings and metadata
        """
        self.chroma_loader = chroma_loader
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with appropriate tools and configuration.
        
        Returns:
            Configured CrewAI agent
        """
        tools = [
            Tool(
                name="analyze_entity",
                func=self._analyze_entity,
                description="Analyze a specific code entity and its relationships"
            ),
            Tool(
                name="find_related_entities",
                func=self._find_related_entities,
                description="Find entities related to a given entity through calls or inheritance"
            ),
            Tool(
                name="find_similar_entities",
                func=self._find_similar_entities,
                description="Find semantically similar entities based on embeddings"
            ),
            Tool(
                name="extract_requirements",
                func=self._extract_requirements,
                description="Extract potential requirements from entity documentation"
            )
        ]
        
        return Agent(
            role="Code Parser",
            goal="Analyze codebase structure and extract meaningful relationships",
            backstory="""You are an expert code analyzer with deep knowledge of software architecture
            and design patterns. Your task is to understand the codebase structure and identify
            key relationships between components.""",
            tools=tools,
            verbose=True
        )
    
    def _analyze_entity(self, entity_name: str) -> Dict:
        """Analyze a specific code entity.
        
        Args:
            entity_name: Name of the entity to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Get entity data from ChromaDB
            result = self.chroma_loader.collection.get(
                ids=[entity_name],
                include=["metadatas", "documents"]
            )
            
            if not result["ids"]:
                return {"error": f"Entity not found: {entity_name}"}
            
            metadata = result["metadatas"][0]
            document = result["documents"][0]
            
            return {
                "name": metadata["name"],
                "kind": metadata["kind"],
                "source_file": metadata["source_file"],
                "calls": metadata["calls"].split(",") if metadata["calls"] else [],
                "documentation": document
            }
            
        except Exception as e:
            return {"error": f"Error analyzing entity {entity_name}: {str(e)}"}
    
    def _find_related_entities(self, entity_name: str) -> List[Dict]:
        """Find entities related to a given entity.
        
        Args:
            entity_name: Name of the entity to find relations for
            
        Returns:
            List of dictionaries containing related entity information
        """
        try:
            # Get entity data
            entity_data = self._analyze_entity(entity_name)
            if "error" in entity_data:
                return [entity_data]
            
            related = []
            
            # Find entities that this entity calls
            for call in entity_data["calls"]:
                if call:
                    call_data = self._analyze_entity(call)
                    if "error" not in call_data:
                        related.append({
                            "name": call,
                            "relationship": "called_by",
                            "entity": call_data
                        })
            
            # Find entities that call this entity
            # This requires a full collection scan, which might be expensive
            # Consider implementing a more efficient indexing strategy if needed
            all_entities = self.chroma_loader.collection.get(
                include=["metadatas", "documents"]
            )
            
            for i, metadata in enumerate(all_entities["metadatas"]):
                calls = metadata["calls"].split(",") if metadata["calls"] else []
                if entity_name in calls:
                    related.append({
                        "name": metadata["name"],
                        "relationship": "calls",
                        "entity": {
                            "name": metadata["name"],
                            "kind": metadata["kind"],
                            "source_file": metadata["source_file"],
                            "calls": calls,
                            "documentation": all_entities["documents"][i]
                        }
                    })
            
            return related
            
        except Exception as e:
            return [{"error": f"Error finding related entities for {entity_name}: {str(e)}"}]
    
    def _find_similar_entities(self, entity_name: str, n_results: int = 5) -> List[Dict]:
        """Find semantically similar entities based on embeddings.
        
        Args:
            entity_name: Name of the entity to find similar entities for
            n_results: Number of similar entities to return
            
        Returns:
            List of dictionaries containing similar entity information
        """
        return self.chroma_loader.find_similar_entities(entity_name, n_results)
    
    def _extract_requirements(self, entity_name: str) -> List[str]:
        """Extract potential requirements from entity documentation.
        
        Args:
            entity_name: Name of the entity to extract requirements from
            
        Returns:
            List of potential requirements
        """
        try:
            # Get entity data
            entity_data = self._analyze_entity(entity_name)
            if "error" in entity_data:
                return [entity_data["error"]]
            
            requirements = []
            doc = entity_data["documentation"].lower()
            
            # Look for requirement indicators
            indicators = [
                "must", "should", "shall", "will", "needs to",
                "required", "requirement", "needs", "requires"
            ]
            
            for line in doc.split("\n"):
                if any(indicator in line for indicator in indicators):
                    requirements.append(line.strip())
            
            return requirements
            
        except Exception as e:
            return [f"Error extracting requirements for {entity_name}: {str(e)}"]
    
    def analyze_codebase(self) -> Dict:
        """Analyze the entire codebase and return structured results.
        
        Returns:
            Dictionary containing codebase analysis results
        """
        try:
            # Get all entities from ChromaDB
            all_entities = self.chroma_loader.collection.get(
                include=["metadatas", "documents"]
            )
            
            results = {
                "entities": {},
                "relationships": {},
                "requirements": []
            }
            
            # Analyze each entity
            for i, metadata in enumerate(all_entities["metadatas"]):
                name = metadata["name"]
                results["entities"][name] = self._analyze_entity(name)
                results["relationships"][name] = self._find_related_entities(name)
                results["requirements"].extend(self._extract_requirements(name))
            
            return results
            
        except Exception as e:
            return {"error": f"Error analyzing codebase: {str(e)}"} 