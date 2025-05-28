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
    
    # Mock find_similar_entities to return tuples (id, metadata)
    mock_loader.find_similar_entities.return_value = [
        ("SimilarEntity1", {
            "name": "SimilarEntity1",
            "kind": "class",
            "description": "Entity 1",
            "file": "test.h",
            "calls": [],
            "document": "Test entity 1",
            "similarity": 0.8
        }),
        ("SimilarEntity2", {
            "name": "SimilarEntity2",
            "kind": "function",
            "description": "Entity 2",
            "file": "test.h",
            "calls": [],
            "document": "Test entity 2",
            "similarity": 0.6
        })
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
        description="Test class",
        source_file="test.h",
        calls=["testMethod1", "testMethod2"],
        documentation="Detailed description"
    )
    
    analysis = agent.analyze_entity("TestClass")
    
    assert isinstance(analysis, dict)
    assert "name" in analysis
    assert "kind" in analysis
    assert "description" in analysis
    assert "file" in analysis
    assert "calls" in analysis
    assert "document" in analysis

def test_find_related_entities():
    """Test finding related entities."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    # Mock get_entity to return an entity with calls
    mock_loader.get_entity.side_effect = lambda eid: {
        "TestClass": {
            "name": "TestClass",
            "kind": "class",
            "description": "Test class",
            "file": "test.h",
            "calls": ["testMethod1", "testMethod2"],
            "document": "Detailed description"
        },
        "testMethod1": {
            "name": "testMethod1",
            "kind": "function",
            "description": "First test method",
            "file": "test.h",
            "calls": [],
            "document": "Test method 1"
        },
        "testMethod2": {
            "name": "testMethod2",
            "kind": "function",
            "description": "Second test method",
            "file": "test.h",
            "calls": [],
            "document": "Test method 2"
        }
    }.get(eid, None)
    
    related = agent.find_related_entities("TestClass")
    
    assert isinstance(related, list)
    assert len(related) == 2
    assert all(isinstance(item, dict) for item in related)
    assert all("name" in item for item in related)
    assert all("kind" in item for item in related)
    assert all("description" in item for item in related)

def test_find_similar_entities():
    """Test finding similar entities."""
    mock_loader = create_mock_chroma_loader()
    agent = ParserAgent(chroma_loader=mock_loader)
    
    similar = agent.find_similar_entities("TestClass", n_results=2)
    
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
    
    requirements = agent.extract_requirements(description)
    
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
    
    # Mock get_all_entities to return two entities
    mock_loader.get_all_entities.return_value = {
        "TestClass": {
            "name": "TestClass",
            "kind": "class",
            "description": "Test class\n1. Must handle user authentication",
            "file": "test.h",
            "calls": ["testMethod1", "testMethod2"],
            "document": "Detailed description"
        },
        "testMethod": {
            "name": "testMethod",
            "kind": "function",
            "description": "Test method",
            "file": "test.h",
            "calls": [],
            "document": "Detailed description"
        }
    }
    # Mock get_entity to return the above entities
    mock_loader.get_entity.side_effect = lambda eid: mock_loader.get_all_entities.return_value.get(eid, None)
    
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