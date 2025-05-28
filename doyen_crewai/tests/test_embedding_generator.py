"""Tests for the embedding generator component."""

import pytest
import time
from unittest.mock import patch, MagicMock
import requests
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

def test_generate_embedding_success():
    """Test successful embedding generation."""
    with patch("requests.post") as mock_post:
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        embedding = generator.generate_embedding("test text")
        
        assert embedding == [0.1, 0.2, 0.3]
        mock_post.assert_called_once()

def test_generate_embedding_timeout():
    """Test handling of timeout error."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout()
        
        generator = OllamaEmbeddingGenerator()
        embedding = generator.generate_embedding("test text")
        
        assert embedding is None

def test_generate_embedding_rate_limit():
    """Test handling of rate limit error."""
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=429))
        mock_response.status_code = 429
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        embedding = generator.generate_embedding("test text")
        
        assert embedding is None

def test_generate_embeddings_batch_with_retries():
    """Test batch embedding generation with retries."""
    with patch("requests.post") as mock_post:
        # Mock responses: first two attempts fail, third succeeds
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        timeout_response = MagicMock()
        timeout_response.raise_for_status.side_effect = requests.exceptions.Timeout()
        rate_limit_response = MagicMock()
        rate_limit_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=MagicMock(status_code=429))
        rate_limit_response.status_code = 429
        # Each text will go through 3 attempts, so 2 texts * 3 = 6 calls
        mock_post.side_effect = [timeout_response, rate_limit_response, mock_response, timeout_response, rate_limit_response, mock_response]
        
        generator = OllamaEmbeddingGenerator()
        texts = ["test1", "test2"]
        embeddings = generator.generate_embeddings_batch(texts)
        
        assert len(embeddings) == 2  # Both texts should succeed after retries
        assert all(emb == [0.1, 0.2, 0.3] for emb in embeddings.values())
        assert mock_post.call_count == 6  # 2 texts * 3 attempts each

def test_generate_entity_embeddings():
    """Test generating embeddings for code entities."""
    with patch("requests.post") as mock_post:
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        
        # Create sample entities
        entities = {
            "TestClass": CodeEntity(
                name="TestClass",
                kind="class",
                description="Test class",
                source_file="test.h",
                calls=["testMethod1", "testMethod2"],
                documentation="Detailed description"
            ),
            "testMethod": CodeEntity(
                name="testMethod",
                kind="function",
                description="Test method",
                source_file="test.h",
                calls=[],
                documentation="Detailed description"
            )
        }
        
        embeddings = generator.generate_entity_embeddings(entities)
        
        assert len(embeddings) == 2
        assert all(emb == [0.1, 0.2, 0.3] for emb in embeddings.values())
        assert mock_post.call_count == 2  # One call per entity

def test_batch_generate_embeddings():
    """Test batch generation of embeddings."""
    with patch("requests.post") as mock_post:
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        mock_post.return_value = mock_response
        
        generator = OllamaEmbeddingGenerator()
        
        # Create sample entities
        entities = {
            "TestClass": CodeEntity(
                name="TestClass",
                kind="class",
                description="Test class",
                source_file="test.h",
                calls=["testMethod1", "testMethod2"],
                documentation="Detailed description"
            ),
            "testMethod": CodeEntity(
                name="testMethod",
                kind="function",
                description="Test method",
                source_file="test.h",
                calls=[],
                documentation="Detailed description"
            )
        }
        
        embeddings = generator.batch_generate_embeddings(entities)
        
        assert len(embeddings) == 2
        assert all(emb == [0.1, 0.2, 0.3] for emb in embeddings.values())
        assert mock_post.call_count == 2  # One call per entity 