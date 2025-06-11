import unittest
import os
import numpy as np
from src.doxygen_parser import parse_doxygen_xml
from src.embedding_engine import EmbeddingEngine
from src.cluster_engine import ClusterEngine
from src.chroma_connector import ChromaConnector
from src.requirement_gen import RequirementGenerator
from tests.test_config import (
    TEST_XML_DIR, TEST_DB_DIR, SAMPLE_XML, SAMPLE_ARTIFACT,
    SAMPLE_CLUSTER, TEST_SETTINGS, setup_test_environment,
    cleanup_test_environment
)

class TestSemanticAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        setup_test_environment()

    def setUp(self):
        """Set up test cases"""
        self.embedding_engine = EmbeddingEngine()
        self.cluster_engine = ClusterEngine(n_clusters=TEST_SETTINGS['n_clusters'])
        self.chroma_connector = ChromaConnector(TEST_DB_DIR)
        self.requirement_gen = RequirementGenerator()

    def test_xml_parsing(self):
        """Test XML parsing functionality"""
        # Create test XML file
        xml_path = os.path.join(TEST_XML_DIR, "test.xml")
        with open(xml_path, "w") as f:
            f.write(SAMPLE_XML)

        # Parse XML
        artifacts = parse_doxygen_xml(TEST_XML_DIR)
        
        # Assertions
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0]['name'], SAMPLE_ARTIFACT['name'])
        self.assertEqual(artifacts[0]['class'], SAMPLE_ARTIFACT['class'])

    def test_embedding_generation(self):
        """Test embedding generation"""
        # Prepare text for embedding
        text = f"{SAMPLE_ARTIFACT['definition']} {SAMPLE_ARTIFACT['doc']}"
        
        # Generate embedding
        embedding = self.embedding_engine.generate_embedding(text)
        
        # Assertions
        self.assertEqual(len(embedding), TEST_SETTINGS['embedding_dim'])
        self.assertTrue(isinstance(embedding, np.ndarray))

    def test_clustering(self):
        """Test clustering functionality"""
        # Create test artifacts with embeddings
        artifacts = []
        for artifact in SAMPLE_CLUSTER:
            text = f"{artifact['definition']} {artifact['doc']}"
            embedding = self.embedding_engine.generate_embedding(text)
            artifacts.append({**artifact, 'embedding': embedding})

        # Perform clustering
        clustered_artifacts = self.cluster_engine.cluster_artifacts(artifacts)
        
        # Assertions
        self.assertEqual(len(clustered_artifacts), len(SAMPLE_CLUSTER))
        self.assertTrue(all('cluster' in a for a in clustered_artifacts))

    def test_chroma_storage(self):
        """Test ChromaDB storage"""
        # Create test artifact with embedding
        text = f"{SAMPLE_ARTIFACT['definition']} {SAMPLE_ARTIFACT['doc']}"
        embedding = self.embedding_engine.generate_embedding(text)
        artifact = {
            **SAMPLE_ARTIFACT,
            'embedding': embedding
        }

        # Store in ChromaDB
        self.chroma_connector.store_artifacts([artifact])
        
        # Query from ChromaDB
        results = self.chroma_connector.search_artifacts(SAMPLE_ARTIFACT['doc'])
        
        # Assertions
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['name'], SAMPLE_ARTIFACT['name'])

    def test_requirement_generation(self):
        """Test requirement generation"""
        # Generate requirement
        requirement = self.requirement_gen.generate_cluster_requirements(SAMPLE_CLUSTER)
        
        # Assertions
        self.assertTrue(isinstance(requirement, str))
        self.assertTrue(len(requirement) > 0)
        self.assertTrue('calculate' in requirement.lower())

    def tearDown(self):
        """Clean up after tests"""
        # Clear ChromaDB
        self.chroma_connector.clear_collection()

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        cleanup_test_environment()

if __name__ == '__main__':
    unittest.main() 