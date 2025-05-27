"""Tests for the embedding generator component."""

import pytest
from unittest.mock import patch, MagicMock
from src.preprocessing.embedding_generator import OllamaEmbeddingGenerator
from src.preprocessing.xml_parser import CodeEntity

def test_embedding_generator_initialization():
    """Test embedding generator initialization."""
    generator = OllamaEmbeddingGenerator(
        api_url="http://localhost:11434",
        model="llama2"
    )
    assert generator.api_url == "http://localhost:11434"
    assert generator.model == "llama2"

def test_generate_embedding():
    """Test generating a single embedding."""
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        embedding = generator.generate_embedding("Test text")
        
        assert embedding == [0.1, 0.2, 0.3]
        mock_post.assert_called_once()

def test_generate_embeddings_batch():
    """Test generating embeddings in batch."""
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        texts = ["Text 1", "Text 2", "Text 3"]
        embeddings = generator.generate_embeddings_batch(texts, batch_size=2)
        
        assert len(embeddings) == 3
        assert all(emb == [0.1, 0.2, 0.3] for emb in embeddings)
        assert mock_post.call_count == 3  # One call per text

def test_generate_entity_embeddings():
    """Test generating embeddings for code entities."""
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        
        # Create sample entities
        entities = {
            "TestClass": CodeEntity(
                name="TestClass",
                kind="class",
                source_file="test.h",
                brief="Test class",
                detailed="Detailed description"
            ),
            "testMethod": CodeEntity(
                name="testMethod",
                kind="function",
                source_file="test.h",
                brief="Test method",
                detailed="Detailed description"
            )
        }
        
        embeddings = generator.generate_entity_embeddings(entities)
        
        assert len(embeddings) == 2
        assert "TestClass" in embeddings
        assert "testMethod" in embeddings
        assert all(emb == [0.1, 0.2, 0.3] for emb in embeddings.values())

def test_generate_embedding_api_error():
    """Test handling API errors during embedding generation."""
    with patch("requests.post") as mock_post:
        # Mock API error
        mock_post.side_effect = Exception("API Error")
        
        generator = OllamaEmbeddingGenerator()
        embedding = generator.generate_embedding("Test text")
        
        assert embedding is None

def test_generate_embeddings_batch_partial_failure():
    """Test handling partial failures in batch embedding generation."""
    with patch("requests.post") as mock_post:
        # Mock mixed success/failure responses
        def mock_post_side_effect(*args, **kwargs):
            if "Text 2" in args[1]["json"]["prompt"]:
                raise Exception("API Error")
            mock_response = MagicMock()
            mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
            return mock_response
        
        mock_post.side_effect = mock_post_side_effect
        
        generator = OllamaEmbeddingGenerator()
        texts = ["Text 1", "Text 2", "Text 3"]
        embeddings = generator.generate_embeddings_batch(texts)
        
        assert len(embeddings) == 3
        assert embeddings[0] == [0.1, 0.2, 0.3]  # Success
        assert embeddings[1] is None  # Failure
        assert embeddings[2] == [0.1, 0.2, 0.3]  # Success 