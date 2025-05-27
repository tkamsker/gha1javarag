"""Tests for the parser agent component."""

import pytest
from unittest.mock import MagicMock, patch
from src.agents.parser_agent import ParserAgent
from src.preprocessing.xml_parser import CodeEntity

def create_mock_chroma_loader():
    """Create a mock ChromaDB loader for testing."""
    mock_loader = MagicMock()
    
    # Mock get_entity_embedding
    mock_loader.get_entity_embedding.return_value = [0.1, 0.2, 0.3]
    
    # Mock find_similar_entities
    mock_loader.find_similar_entities.return_value = [
        {
            "name": "SimilarEntity1",
            "similarity": 0.8,
            "metadata": {"kind": "class", "source_file": "test.h"},
            "document": "Test entity 1"
        },
        {
            "name": "SimilarEntity2",
            "similarity": 0.6,
            "metadata": {"kind": "function", "source_file": "test.h"},
            "document": "Test entity 2"
        }
    ]
    
    return mock_loader

def test_parser_agent_initialization():
    """Test parser agent initialization."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    assert agent.chroma_loader == mock_loader

def test_analyze_entity():
    """Test analyzing a single entity."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    entity = CodeEntity(
        name="TestClass",
        kind="class",
        source_file="test.h",
        brief="Test class",
        detailed="Detailed description"
    )
    
    analysis = agent._analyze_entity(entity)
    
    assert isinstance(analysis, dict)
    assert "name" in analysis
    assert "kind" in analysis
    assert "source_file" in analysis
    assert "brief" in analysis
    assert "detailed" in analysis
    assert "similar_entities" in analysis
    assert len(analysis["similar_entities"]) == 2

def test_find_related_entities():
    """Test finding related entities."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    entity = CodeEntity(
        name="TestClass",
        kind="class",
        source_file="test.h",
        brief="Test class",
        detailed="Detailed description"
    )
    
    related = agent._find_related_entities(entity)
    
    assert isinstance(related, list)
    assert len(related) == 2
    assert all(isinstance(item, dict) for item in related)
    assert all("name" in item for item in related)
    assert all("similarity" in item for item in related)

def test_find_similar_entities():
    """Test finding similar entities."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    similar = agent._find_similar_entities("TestClass", n_results=2)
    
    assert isinstance(similar, list)
    assert len(similar) == 2
    assert all(isinstance(item, dict) for item in similar)
    assert all("name" in item for item in similar)
    assert all("similarity" in item for item in similar)

def test_extract_requirements():
    """Test extracting requirements from entity description."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    description = """
    This class implements the following requirements:
    1. Must handle user authentication
    2. Should support multiple authentication methods
    3. Must validate input data
    """
    
    requirements = agent._extract_requirements(description)
    
    assert isinstance(requirements, list)
    assert len(requirements) == 3
    assert all(isinstance(req, str) for req in requirements)
    assert "user authentication" in requirements[0]
    assert "multiple authentication methods" in requirements[1]
    assert "validate input data" in requirements[2]

def test_analyze_codebase():
    """Test analyzing the entire codebase."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    # Mock the collection to return a list of entities
    mock_loader.collection.get.return_value = {
        "ids": ["TestClass", "testMethod"],
        "metadatas": [
            {
                "name": "TestClass",
                "kind": "class",
                "source_file": "test.h",
                "brief": "Test class",
                "detailed": "Detailed description"
            },
            {
                "name": "testMethod",
                "kind": "function",
                "source_file": "test.h",
                "brief": "Test method",
                "detailed": "Detailed description"
            }
        ],
        "documents": ["Test class", "Test method"]
    }
    
    results = agent.analyze_codebase()
    
    assert isinstance(results, dict)
    assert "entities" in results
    assert "relationships" in results
    assert "requirements" in results
    assert len(results["entities"]) == 2
    assert len(results["relationships"]) > 0
    assert len(results["requirements"]) > 0

def test_analyze_codebase_empty():
    """Test analyzing an empty codebase."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    # Mock empty collection
    mock_loader.collection.get.return_value = {
        "ids": [],
        "metadatas": [],
        "documents": []
    }
    
    results = agent.analyze_codebase()
    
    assert isinstance(results, dict)
    assert "entities" in results
    assert "relationships" in results
    assert "requirements" in results
    assert len(results["entities"]) == 0
    assert len(results["relationships"]) == 0
    assert len(results["requirements"]) == 0 