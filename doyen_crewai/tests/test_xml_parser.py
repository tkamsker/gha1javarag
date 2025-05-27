"""Tests for the XML parser component."""

import os
import pytest
from pathlib import Path
from src.preprocessing.xml_parser import DoxygenXMLParser, CodeEntity

def create_sample_xml(temp_dir: Path) -> Path:
    """Create a sample XML file for testing."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <doxygen>
        <compounddef id="class_test" kind="class">
            <compoundname>Test</compoundname>
            <includes>test.h</includes>
            <sectiondef kind="public-func">
                <memberdef kind="function" id="class_test_1a1" prot="public" static="no">
                    <name>testMethod1</name>
                    <param>
                        <type>int</type>
                        <declname>param1</declname>
                    </param>
                    <briefdescription>Test method 1</briefdescription>
                    <detaileddescription>Detailed description of test method 1</detaileddescription>
                </memberdef>
                <memberdef kind="function" id="class_test_1a2" prot="public" static="no">
                    <name>testMethod2</name>
                    <param>
                        <type>string</type>
                        <declname>param2</declname>
                    </param>
                    <briefdescription>Test method 2</briefdescription>
                    <detaileddescription>Detailed description of test method 2</detaileddescription>
                </memberdef>
            </sectiondef>
        </compounddef>
    </doxygen>"""
    
    xml_file = temp_dir / "test.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_xml_parser_initialization(temp_dir):
    """Test XML parser initialization."""
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    assert parser.xml_dir == str(temp_dir)

def test_parse_xml_file(temp_dir):
    """Test parsing a single XML file."""
    xml_file = create_sample_xml(temp_dir)
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    
    entities = parser.parse_xml_file(xml_file)
    assert len(entities) == 3  # One class and two methods
    
    # Verify class entity
    class_entity = next(e for e in entities if e.kind == "class")
    assert class_entity.name == "Test"
    assert class_entity.source_file == "test.h"
    
    # Verify method entities
    methods = [e for e in entities if e.kind == "function"]
    assert len(methods) == 2
    
    method1 = next(m for m in methods if m.name == "testMethod1")
    assert method1.brief == "Test method 1"
    assert method1.detailed == "Detailed description of test method 1"
    
    method2 = next(m for m in methods if m.name == "testMethod2")
    assert method2.brief == "Test method 2"
    assert method2.detailed == "Detailed description of test method 2"

def test_parse_all_xml_files(temp_dir):
    """Test parsing all XML files in a directory."""
    # Create multiple XML files
    xml_file1 = create_sample_xml(temp_dir)
    xml_file2 = create_sample_xml(temp_dir / "test2.xml")
    
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_all_xml_files()
    
    # Should have 6 entities (3 from each file)
    assert len(entities) == 6
    
    # Verify all entities have required attributes
    for entity in entities:
        assert isinstance(entity, CodeEntity)
        assert entity.name
        assert entity.kind
        assert entity.source_file
        assert entity.brief is not None
        assert entity.detailed is not None

def test_parse_xml_file_invalid(temp_dir):
    """Test parsing an invalid XML file."""
    invalid_xml = temp_dir / "invalid.xml"
    invalid_xml.write_text("This is not valid XML")
    
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_xml_file(invalid_xml)
    assert len(entities) == 0

def test_parse_xml_file_missing(temp_dir):
    """Test parsing a non-existent XML file."""
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_xml_file(temp_dir / "nonexistent.xml")
    assert len(entities) == 0

def test_parse_all_xml_files_empty_dir(temp_dir):
    """Test parsing XML files from an empty directory."""
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_all_xml_files()
    assert len(entities) == 0 