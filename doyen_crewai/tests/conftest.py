"""Pytest configuration and common fixtures."""

import os
import tempfile
from pathlib import Path
from typing import Dict, Generator

import pytest
from dotenv import load_dotenv

from src.preprocessing.xml_parser import CodeEntity
from src.preprocessing.chroma_loader import ChromaDBLoader

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def sample_entities() -> Dict[str, CodeEntity]:
    """Create sample code entities for testing."""
    return {
        "TestClass": CodeEntity(
            name="TestClass",
            kind="class",
            description="A test class",
            source_file="test/TestClass.java",
            calls=["testMethod1", "testMethod2"],
            documentation="Test class documentation"
        ),
        "testMethod1": CodeEntity(
            name="testMethod1",
            kind="function",
            description="First test method",
            source_file="test/TestClass.java",
            calls=["helperMethod"],
            documentation="Test method 1 documentation"
        ),
        "testMethod2": CodeEntity(
            name="testMethod2",
            kind="function",
            description="Second test method",
            source_file="test/TestClass.java",
            calls=[],
            documentation="Test method 2 documentation"
        )
    }

@pytest.fixture
def sample_embeddings() -> Dict[str, list]:
    """Create sample embeddings for testing."""
    return {
        "TestClass": [0.1, 0.2, 0.3],
        "testMethod1": [0.2, 0.3, 0.4],
        "testMethod2": [0.3, 0.4, 0.5]
    }

@pytest.fixture
def chroma_loader(temp_dir: Path) -> ChromaDBLoader:
    """Create a ChromaDB loader instance for testing."""
    return ChromaDBLoader(persist_directory=str(temp_dir / "chroma_db"))

@pytest.fixture(autouse=True)
def setup_env():
    """Set up test environment variables."""
    # Save original environment
    original_env = dict(os.environ)
    
    # Set test environment variables
    os.environ.update({
        "XML_INPUT_DIR": str(Path(__file__).parent / "test_data"),
        "OLLAMA_API_URL": "http://localhost:11434",
        "OLLAMA_MODEL": "all-minilm",
        "CHROMA_PERSIST_DIRECTORY": str(Path(__file__).parent / "test_data" / "chroma_db"),
        "LOG_LEVEL": "DEBUG"
    })
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env) 