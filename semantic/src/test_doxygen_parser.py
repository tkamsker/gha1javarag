import unittest
from pathlib import Path
import os
from doxygen_parser import DoxygenParser
import tempfile
import logging

# Set up logging to see debug output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestDoxygenParser(unittest.TestCase):
    def setUp(self):
        self.parser = DoxygenParser()
        # Get the absolute path to the test data directory
        current_dir = Path(__file__).parent
        self.test_xml_dir = str(current_dir.parent / "data" / "hotel_docs_doxygen2" / "xml")
        
        # Verify the directory exists
        if not os.path.exists(self.test_xml_dir):
            self.skipTest(f"Test data directory not found: {self.test_xml_dir}")

    def test_jsp_file_parsing(self):
        """Test parsing of JSP files with @ symbol removal."""
        artifacts = self.parser.parse_directory(self.test_xml_dir)
        
        # Find JSP artifacts
        jsp_artifacts = [a for a in artifacts if a["name"].endswith('.jsp')]
        
        # Verify that @ symbols are removed from JSP files
        for artifact in jsp_artifacts:
            if "source_code" in artifact:
                self.assertNotIn("@", artifact["source_code"], 
                               f"@ symbol found in JSP file {artifact['name']}")

    def test_location_information(self):
        """Test that location information is properly extracted."""
        artifacts = self.parser.parse_directory(self.test_xml_dir)
        
        # Check that location info is present in metadata
        for artifact in artifacts:
            self.assertIn("metadata", artifact)
            self.assertIn("location", artifact["metadata"])
            
            location = artifact["metadata"]["location"]
            # Verify location fields
            self.assertIn("file", location)
            self.assertIn("line", location)
            self.assertIn("bodyfile", location)
            self.assertIn("bodystart", location)
            self.assertIn("bodyend", location)

    def test_programlisting_extraction(self):
        """Test extraction of code from programlisting sections."""
        artifacts = self.parser.parse_directory(self.test_xml_dir)
        
        # Find programlisting artifacts
        programlisting_artifacts = [a for a in artifacts if a["id"].endswith('_programlisting')]
        
        # Verify programlisting artifacts have required fields
        for artifact in programlisting_artifacts:
            self.assertIn("source_code", artifact)
            self.assertIn("metadata", artifact)
            self.assertIn("location", artifact["metadata"])
            self.assertTrue(artifact["source_code"].strip())

    def test_problematic_at_symbol_xml(self):
        """Test parsing of XML with stray '@' symbols outside tags."""
        problematic_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<doxygen>
  <compounddef id="test_jsp" kind="file" language="Java">
    <compoundname>test.jsp</compoundname>
    <programlisting>
      <codeline><highlight class="normal">@page content</highlight></codeline>
    </programlisting>
  </compounddef>
</doxygen>
@'''  # stray @ at the end
        
        with tempfile.NamedTemporaryFile('w+', suffix='.xml', delete=False) as tmp:
            tmp.write(problematic_xml)
            tmp.flush()
            tmp_path = tmp.name
            
            # Log the original content
            logger.debug("Original XML content:")
            logger.debug(problematic_xml)
            
            parser = DoxygenParser()
            
            # Get the preprocessed content directly
            preprocessed_content = parser._preprocess_xml(Path(tmp_path))
            logger.debug("Preprocessed XML content:")
            logger.debug(preprocessed_content)
            
            # Check if @ symbol is still present
            self.assertNotIn("@", preprocessed_content, 
                           "Preprocessed content still contains @ symbol")
            
            artifacts = parser._parse_file(Path(tmp_path))
            
            # Should parse without error and extract the programlisting
            programlisting_artifacts = [a for a in artifacts if a["id"].endswith('_programlisting')]
            self.assertTrue(programlisting_artifacts, 
                          "No programlisting artifact extracted from problematic XML")
            
            for artifact in programlisting_artifacts:
                self.assertIn("source_code", artifact)
                self.assertIn("test.jsp", artifact["name"])
                
                # Log the extracted source code
                logger.debug("Extracted source code:")
                logger.debug(artifact["source_code"])
        
        os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main() 