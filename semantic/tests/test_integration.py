import pytest
import os
from pathlib import Path
from src.doxygen_parser import parse_doxygen_xml
from src.embedder import CodeEmbedder
from src.cluster_engine import ClusterEngine
from src.requirement_gen import RequirementGenerator
from src.embedding_manager import EmbeddingManager
from src.get_persistence import get_persistence

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_XML_DIR = TEST_DATA_DIR / "doxygen_xml"
TEST_CHROMA_DIR = TEST_DATA_DIR / "chroma_db"

@pytest.fixture(scope="session")
def setup_test_environment():
    """Create test directories and sample XML files"""
    os.makedirs(TEST_XML_DIR, exist_ok=True)
    os.makedirs(TEST_CHROMA_DIR, exist_ok=True)
    
    # Create a sample XML file for testing
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <doxygen>
        <compounddef id="class_1" kind="class">
            <compoundname>TestClass</compoundname>
            <memberdef kind="function" id="method_1">
                <name>testMethod</name>
                <definition>public void testMethod()</definition>
                <argsstring>()</argsstring>
                <detaileddescription>This is a test method</detaileddescription>
            </memberdef>
        </compounddef>
    </doxygen>"""
    
    with open(TEST_XML_DIR / "test.xml", "w") as f:
        f.write(sample_xml)
    
    yield
    
    # Cleanup
    import shutil
    shutil.rmtree(TEST_DATA_DIR)

@pytest.fixture
def embedder():
    """Create a CodeEmbedder instance for testing"""
    return CodeEmbedder()

def test_doxygen_parsing(setup_test_environment):
    """Test parsing of Doxygen XML files"""
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    assert len(artifacts) > 0
    assert artifacts[0]['name'] == 'testMethod'
    assert artifacts[0]['class'] == 'TestClass'

def test_embedding_generation(setup_test_environment, embedder):
    """Test embedding generation for artifacts"""
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    artifacts = embedder.embed_artifacts(artifacts)
    assert 'embedding' in artifacts[0]
    assert len(artifacts[0]['embedding']) > 0

def test_clustering(setup_test_environment, embedder):
    """Test clustering of artifacts"""
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    artifacts = embedder.embed_artifacts(artifacts)
    cluster_engine = ClusterEngine(n_clusters=1)
    artifacts = cluster_engine.cluster_artifacts(artifacts)
    assert 'cluster' in artifacts[0]
    assert isinstance(artifacts[0]['cluster'], int)

def test_requirement_generation(setup_test_environment, monkeypatch):
    """Test requirement generation"""
    import os
    os.environ['TEST_MODE'] = 'true'
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    generator = RequirementGenerator()
    requirement = generator.generate_artifact_requirement(artifacts[0])
    assert isinstance(requirement, str)
    assert len(requirement) > 0

def test_embedding_manager(setup_test_environment, embedder):
    """Test the embedding manager functionality"""
    manager = EmbeddingManager()
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    artifacts = embedder.embed_artifacts(artifacts)
    
    # Test embedding storage and retrieval
    manager.create_embeddings(artifacts)
    retrieved = manager.get_embeddings([artifacts[0]['id']])
    assert len(retrieved) > 0

def test_persistence(setup_test_environment, embedder):
    """Test persistence layer functionality"""
    persistence = get_persistence("test_chroma_db")
    artifacts = parse_doxygen_xml(TEST_XML_DIR)
    artifacts = embedder.embed_artifacts(artifacts)
    
    # Test storing and retrieving artifacts
    persistence.store_artifacts(artifacts)
    retrieved = persistence.get_artifact_by_id(artifacts[0]['id'])
    assert retrieved is not None 