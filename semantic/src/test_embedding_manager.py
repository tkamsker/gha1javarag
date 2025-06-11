import unittest
from pathlib import Path
import shutil
import os
import tempfile
from embedding_manager import EmbeddingManager
from doxygen_parser import DoxygenParser

class TestEmbeddingManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Create a unique temporary directory for this test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db_dir = Path(self.temp_dir.name)
        
        # Initialize embedding manager with the temporary directory
        self.embedding_manager = EmbeddingManager(str(self.test_db_dir))
        
        # Sample artifacts for testing
        self.sample_artifacts = [
            {
                "id": "test1",
                "name": "TestFunction1",
                "description": "A test function that does something",
                "class": "TestClass",
                "kind": "function",
                "source_code": "def test_function():\n    return True",
                "metadata": {
                    "line_start": "1",
                    "line_end": "2"
                }
            },
            {
                "id": "test2",
                "name": "TestFunction2",
                "description": "Another test function with different functionality",
                "class": "TestClass",
                "kind": "function",
                "source_code": "def another_function():\n    return False",
                "metadata": {
                    "line_start": "3",
                    "line_end": "4"
                }
            }
        ]
    
    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'embedding_manager'):
            self.embedding_manager.close()
        # The temporary directory will be automatically cleaned up
        self.temp_dir.cleanup()
    
    def test_create_embeddings(self):
        """Test creating embeddings for artifacts."""
        # Create embeddings
        self.embedding_manager.create_embeddings(self.sample_artifacts)
        
        # Search for similar artifacts
        results = self.embedding_manager.search_similar("test function", n_results=2)
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertTrue(any("TestFunction1" in r["document"] for r in results))
        self.assertTrue(any("TestFunction2" in r["document"] for r in results))
    
    def test_search_similar(self):
        """Test searching for similar artifacts."""
        # Create embeddings
        self.embedding_manager.create_embeddings(self.sample_artifacts)
        
        # Search with different queries
        results1 = self.embedding_manager.search_similar("test function", n_results=1)
        results2 = self.embedding_manager.search_similar("another function", n_results=1)
        
        # Verify results
        self.assertEqual(len(results1), 1)
        self.assertEqual(len(results2), 1)
        self.assertTrue("TestFunction1" in results1[0]["document"])
        self.assertTrue("TestFunction2" in results2[0]["document"])
    
    def test_reset_collection(self):
        """Test resetting the ChromaDB collection."""
        # Create embeddings
        self.embedding_manager.create_embeddings(self.sample_artifacts)
        
        # Reset collection
        self.embedding_manager.reset_collection()
        
        # Verify collection is empty
        results = self.embedding_manager.search_similar("test", n_results=1)
        self.assertEqual(len(results), 0)
    
    def test_integration_with_doxygen_parser(self):
        """Test integration with DoxygenParser."""
        # Parse XML files
        parser = DoxygenParser()
        artifacts = parser.parse_directory("data/hotel_docs_doxygen2/xml")
        
        # Create embeddings
        self.embedding_manager.create_embeddings(artifacts)
        
        # Search for similar artifacts
        results = self.embedding_manager.search_similar("database connection", n_results=5)
        
        # Verify results
        self.assertTrue(len(results) > 0)
        self.assertTrue(all("document" in r for r in results))
        self.assertTrue(all("metadata" in r for r in results))

if __name__ == '__main__':
    unittest.main() 