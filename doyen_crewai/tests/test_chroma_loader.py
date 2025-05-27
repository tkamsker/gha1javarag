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
    # Load embeddings
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Verify collection stats
    stats = chroma_loader.get_collection_stats()
    assert stats["total_entities"] == len(sample_entities)
    
    # Verify each entity was loaded correctly
    for name, entity in sample_entities.items():
        result = chroma_loader.collection.get(
            ids=[name],
            include=["metadatas", "documents", "embeddings"]
        )
        
        assert len(result["ids"]) == 1
        assert result["ids"][0] == name
        assert result["metadatas"][0]["name"] == entity.name
        assert result["metadatas"][0]["kind"] == entity.kind
        assert result["metadatas"][0]["source_file"] == entity.source_file
        assert result["embeddings"][0] == sample_embeddings[name]

def test_get_entity_embedding(chroma_loader, sample_entities, sample_embeddings):
    """Test retrieving entity embeddings."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Test retrieving embeddings
    for name, embedding in sample_embeddings.items():
        retrieved = chroma_loader.get_entity_embedding(name)
        assert retrieved == embedding
    
    # Test non-existent entity
    assert chroma_loader.get_entity_embedding("NonExistentEntity") is None

def test_find_similar_entities(chroma_loader, sample_entities, sample_embeddings):
    """Test finding similar entities."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Test finding similar entities
    similar = chroma_loader.find_similar_entities("TestClass", n_results=2)
    assert len(similar) == 2
    assert all("name" in entity for entity in similar)
    assert all("similarity" in entity for entity in similar)
    assert all("metadata" in entity for entity in similar)
    assert all("document" in entity for entity in similar)

def test_clear_collection(chroma_loader, sample_entities, sample_embeddings):
    """Test clearing the collection."""
    # Load embeddings first
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Verify data was loaded
    stats_before = chroma_loader.get_collection_stats()
    assert stats_before["total_entities"] > 0
    
    # Clear collection
    chroma_loader.clear_collection()
    
    # Verify collection is empty
    stats_after = chroma_loader.get_collection_stats()
    assert stats_after["total_entities"] == 0

def test_get_collection_stats(chroma_loader, sample_entities, sample_embeddings):
    """Test getting collection statistics."""
    # Test empty collection
    stats_empty = chroma_loader.get_collection_stats()
    assert stats_empty["total_entities"] == 0
    assert "persist_directory" in stats_empty
    
    # Load embeddings
    chroma_loader.load_embeddings(sample_entities, sample_embeddings)
    
    # Test populated collection
    stats_populated = chroma_loader.get_collection_stats()
    assert stats_populated["total_entities"] == len(sample_entities)
    assert stats_populated["persist_directory"] == chroma_loader.persist_directory 