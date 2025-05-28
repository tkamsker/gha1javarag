"""Tests for the XML parser component."""

import os
import pytest
from pathlib import Path
from src.preprocessing.xml_parser import DoxygenXMLParser, CodeEntity

def create_sample_xml(temp_dir: Path, prefix: str = "") -> Path:
    """Create a sample XML file for testing with unique names."""
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
    <doxygen>
        <compounddef id="class_{prefix}test" kind="class">
            <compoundname>{prefix}Test</compoundname>
            <includes>test.h</includes>
            <briefdescription>Test class</briefdescription>
            <detaileddescription>Detailed description</detaileddescription>
            <sectiondef kind="public-func">
                <memberdef kind="function" id="class_{prefix}test_1a1" prot="public" static="no">
                    <name>{prefix}testMethod1</name>
                    <param>
                        <type>int</type>
                        <declname>param1</declname>
                    </param>
                    <briefdescription>Test method 1</briefdescription>
                    <detaileddescription>Detailed description of test method 1</detaileddescription>
                </memberdef>
                <memberdef kind="function" id="class_{prefix}test_1a2" prot="public" static="no">
                    <name>{prefix}testMethod2</name>
                    <param>
                        <type>string</type>
                        <declname>param2</declname>
                    </param>
                    <briefdescription>Test method 2</briefdescription>
                    <detaileddescription>Detailed description of test method 2</detaileddescription>
                </memberdef>
            </sectiondef>
        </compounddef>
    </doxygen>'''
    
    xml_file = temp_dir / "test.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_xml_parser_initialization(temp_dir):
    """Test XML parser initialization."""
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    assert parser.xml_dir == temp_dir

def test_parse_xml_file(temp_dir):
    """Test parsing a single XML file."""
    xml_file = create_sample_xml(temp_dir)
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_xml_file(xml_file)
    
    # Should have 3 entities (1 class, 2 methods)
    assert len(entities) == 3
    
    # Verify class entity
    class_entity = entities["Test"]
    assert isinstance(class_entity, CodeEntity)
    assert class_entity.name == "Test"
    assert class_entity.kind == "class"
    assert class_entity.description == "Test class"
    assert class_entity.source_file == "test.h"
    assert class_entity.calls == ["testMethod1", "testMethod2"]
    assert class_entity.documentation == "Detailed description"
    
    # Verify method entities
    method1 = entities["testMethod1"]
    assert isinstance(method1, CodeEntity)
    assert method1.name == "testMethod1"
    assert method1.kind == "function"
    assert method1.description == "Test method 1"
    assert method1.source_file == "test.h"
    assert method1.calls == []
    assert method1.documentation == "Detailed description of test method 1"
    
    method2 = entities["testMethod2"]
    assert isinstance(method2, CodeEntity)
    assert method2.name == "testMethod2"
    assert method2.kind == "function"
    assert method2.description == "Test method 2"
    assert method2.source_file == "test.h"
    assert method2.calls == []
    assert method2.documentation == "Detailed description of test method 2"

def test_parse_all_xml_files(temp_dir):
    """Test parsing all XML files in a directory."""
    # Create multiple XML files with unique names
    xml_file1 = create_sample_xml(temp_dir, prefix="A")
    subdir = temp_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)
    xml_file2 = create_sample_xml(subdir, prefix="B")
    
    parser = DoxygenXMLParser(xml_dir=str(temp_dir))
    entities = parser.parse_all_xml_files()
    
    # Should have 6 entities (3 from each file)
    assert len(entities) == 6
    
    # Verify all entities have required attributes
    for entity in entities.values():
        assert isinstance(entity, CodeEntity)
        assert entity.name
        assert entity.kind
        assert entity.description is not None
        assert entity.source_file
        assert isinstance(entity.calls, list)
        assert entity.documentation is not None

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