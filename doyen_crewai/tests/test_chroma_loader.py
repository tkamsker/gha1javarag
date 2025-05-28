"""Tests for the ChromaDB loader component."""

import pytest
from src.preprocessing.chroma_loader import ChromaDBLoader

def test_chroma_loader_initialization(temp_dir):
    """Test ChromaDB loader initialization."""
    loader = ChromaDBLoader(persist_directory=str(temp_dir / "chroma_db"))
    assert loader.persist_directory == str(temp_dir / "chroma_db")
    assert loader.collection.name == "code_embeddings"

def test_load_embeddings(chroma_loader, sample_entities, sample_embeddings):
    """Test loading embeddings into ChromaDB."""
    result = chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    assert result["ids"] == list(sample_entities.keys())
    assert len(result["metadatas"]) == len(sample_entities)
    
    # Verify metadata fields
    for i, (name, entity) in enumerate(sample_entities.items()):
        metadata = result["metadatas"][i]
        assert metadata["name"] == entity.name
        assert metadata["kind"] == entity.kind
        assert metadata["description"] == entity.description
        assert metadata["file"] == entity.source_file
        assert metadata["calls"] == ",".join(entity.calls)
        assert metadata["document"] == entity.documentation

def test_get_entity_embedding(chroma_loader, sample_entities, sample_embeddings):
    """Test retrieving entity embeddings."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Test retrieving embedding
    name = "TestClass"
    embedding = sample_embeddings[name]
    retrieved = chroma_loader.get_entity_embedding(name)
    
    # Compare embeddings with tolerance for floating point differences
    assert len(retrieved) == len(embedding)
    for r, e in zip(retrieved, embedding):
        assert abs(r - e) < 1e-6

def test_find_similar_entities(chroma_loader, sample_entities, sample_embeddings):
    """Test finding similar entities."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Test finding similar entities
    name = "TestClass"
    similar = chroma_loader.find_similar_entities(name, n_results=2)
    
    assert len(similar) == 2
    assert all(isinstance(item, tuple) for item in similar)
    assert all(len(item) == 2 for item in similar)
    assert all(isinstance(item[0], str) for item in similar)
    assert all(isinstance(item[1], dict) for item in similar)

def test_clear_collection(chroma_loader, sample_entities, sample_embeddings):
    """Test clearing the collection."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Clear collection
    chroma_loader.clear_collection()
    
    # Verify collection is empty
    stats = chroma_loader.get_collection_stats()
    assert stats["total_entities"] == 0

def test_get_collection_stats(chroma_loader, sample_entities, sample_embeddings):
    """Test getting collection statistics."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Get stats
    stats = chroma_loader.get_collection_stats()
    
    assert isinstance(stats, dict)
    assert "total_entities" in stats
    assert stats["total_entities"] == len(sample_entities) 