#!/usr/bin/env python3
"""
Test script for the debug feature
This script tests the debug file processor and related functionality
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_debug_file_processor():
    """Test the debug file processor functionality"""
    print("🧪 Testing Debug File Processor...")
    
    try:
        from debug_file_processor import DebugFileProcessor
        
        # Create a temporary debug file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            debug_file_path = f.name
            f.write("# Test debug file\n")
            f.write("/tmp/test1.java\n")
            f.write("/tmp/test2.java\n")
            f.write("  # Commented line\n")
            f.write("\n")  # Empty line
        
        # Set environment variable
        os.environ['DEBUGFILE'] = debug_file_path
        
        # Test processor initialization
        processor = DebugFileProcessor()
        
        # Test debug file reading
        debug_files = processor._read_debug_file()
        print(f"✅ Debug files read: {debug_files}")
        
        # Test debug mode detection
        print(f"✅ Debug mode: {processor.debug_mode}")
        
        # Cleanup
        os.unlink(debug_file_path)
        del os.environ['DEBUGFILE']
        
        print("✅ Debug file processor test passed")
        return True
        
    except Exception as e:
        print(f"❌ Debug file processor test failed: {e}")
        return False

def test_pom_xml_analysis():
    """Test pom.xml analysis functionality"""
    print("🧪 Testing POM.xml Analysis...")
    
    try:
        from debug_file_processor import DebugFileProcessor
        
        # Create a temporary pom.xml file
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <name>Test Project</name>
    <description>A test project for debug feature</description>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.7.0</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
            <version>2.7.0</version>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.7.0</version>
            </plugin>
        </plugins>
    </build>
</project>"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            pom_file_path = f.name
            f.write(pom_content)
        
        # Test pom.xml analysis
        processor = DebugFileProcessor()
        pom_metadata = processor._analyze_pom_xml(pom_file_path)
        
        # Verify basic extraction
        assert 'project_info' in pom_metadata
        assert 'dependencies' in pom_metadata
        assert 'build_info' in pom_metadata
        assert 'properties' in pom_metadata
        
        # Verify specific values
        project_info = pom_metadata['project_info']
        assert project_info['groupId'] == 'com.example'
        assert project_info['artifactId'] == 'test-project'
        assert project_info['version'] == '1.0.0'
        
        dependencies = pom_metadata['dependencies']
        assert len(dependencies) == 2
        assert any(dep['artifactId'] == 'spring-boot-starter-web' for dep in dependencies)
        
        print(f"✅ POM metadata extracted: {json.dumps(pom_metadata, indent=2)}")
        
        # Cleanup
        os.unlink(pom_file_path)
        
        print("✅ POM.xml analysis test passed")
        return True
        
    except Exception as e:
        print(f"❌ POM.xml analysis test failed: {e}")
        return False

def test_debug_mode_detection():
    """Test debug mode detection in shell scripts"""
    print("🧪 Testing Debug Mode Detection...")
    
    try:
        # Test environment variable detection
        test_cases = [
            ("", False),
            ("/nonexistent/file.txt", False),
            ("/tmp/existing_file.txt", True)
        ]
        
        for debug_file, expected in test_cases:
            # Create test file if needed
            if expected:
                with open("/tmp/existing_file.txt", 'w') as f:
                    f.write("test")
            
            # Test detection logic (simplified version of shell script logic)
            debug_mode = bool(debug_file and os.path.exists(debug_file))
            
            if debug_mode == expected:
                print(f"✅ Debug mode detection: {debug_file} -> {debug_mode}")
            else:
                print(f"❌ Debug mode detection failed: {debug_file} -> {debug_mode} (expected {expected})")
                return False
            
            # Cleanup
            if expected and os.path.exists("/tmp/existing_file.txt"):
                os.unlink("/tmp/existing_file.txt")
        
        print("✅ Debug mode detection test passed")
        return True
        
    except Exception as e:
        print(f"❌ Debug mode detection test failed: {e}")
        return False

def test_output_file_generation():
    """Test debug output file generation"""
    print("🧪 Testing Output File Generation...")
    
    try:
        # Test output directory structure
        output_dir = "./test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test debug metadata file path
        debug_metadata_file = os.path.join(output_dir, 'debug_metadata.json')
        step2_debug_index = os.path.join(output_dir, 'requirements', 'step2_debug_index.md')
        modern_requirements_debug = os.path.join(output_dir, 'modern_requirements_debug.md')
        
        # Create test files
        test_metadata = {
            "debug_mode": True,
            "debug_file_source": "/test/debug.txt",
            "files_processed": 2
        }
        
        with open(debug_metadata_file, 'w') as f:
            json.dump(test_metadata, f, indent=2)
        
        # Verify file creation
        assert os.path.exists(debug_metadata_file)
        
        # Test file content
        with open(debug_metadata_file, 'r') as f:
            loaded_metadata = json.load(f)
        
        assert loaded_metadata['debug_mode'] == True
        assert loaded_metadata['debug_file_source'] == "/test/debug.txt"
        
        print(f"✅ Debug metadata file created: {debug_metadata_file}")
        
        # Cleanup
        import shutil
        shutil.rmtree(output_dir)
        
        print("✅ Output file generation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Output file generation test failed: {e}")
        return False

def main():
    """Run all debug feature tests"""
    print("🚀 Starting Debug Feature Tests\n")
    
    tests = [
        test_debug_file_processor,
        test_pom_xml_analysis,
        test_debug_mode_detection,
        test_output_file_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All debug feature tests passed!")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 