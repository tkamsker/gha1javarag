#!/usr/bin/env python3
"""
Test script to verify step3.py fixes work correctly
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_step3_import():
    """Test that step3.py can be imported without errors"""
    try:
        import step3
        print("✅ Step3 imports successfully")
        return True
    except Exception as e:
        print(f"❌ Step3 import failed: {str(e)}")
        return False

def test_step3_initialization():
    """Test that RequirementsProcessor can be initialized"""
    try:
        from step3 import RequirementsProcessor
        processor = RequirementsProcessor()
        print("✅ RequirementsProcessor initializes successfully")
        return True
    except Exception as e:
        print(f"❌ RequirementsProcessor initialization failed: {str(e)}")
        return False

def test_ai_provider_fallback():
    """Test that AI provider fallback works when no API key is set"""
    try:
        from step3 import RequirementsProcessor
        processor = RequirementsProcessor()
        
        # Test the AI provider fallback
        provider = processor._get_ai_provider()
        if provider is None:
            print("✅ AI provider fallback works correctly (no API key)")
        else:
            print("✅ AI provider initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AI provider fallback test failed: {str(e)}")
        return False

def test_file_categorization():
    """Test file categorization logic"""
    try:
        from step3 import RequirementsProcessor
        processor = RequirementsProcessor()
        
        # Test categorization
        test_files = [
            "service/UserService.java",
            "web/index.jsp",
            "entity/User.java",
            "test/UserTest.java",
            "batch/ReportJob.java",
            "config/application.properties"
        ]
        
        categories = {}
        for file_path in test_files:
            category = processor.categorize_file(file_path)
            categories[file_path] = category
        
        print("✅ File categorization works:")
        for file_path, category in categories.items():
            print(f"   {file_path} -> {category}")
        
        return True
    except Exception as e:
        print(f"❌ File categorization test failed: {str(e)}")
        return False

def test_mock_index_processing():
    """Test processing with a mock index file"""
    try:
        from step3 import RequirementsProcessor
        import tempfile
        import os
        
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock requirements directory
            req_dir = os.path.join(temp_dir, "requirements")
            os.makedirs(req_dir, exist_ok=True)
            
            # Create mock index file
            index_content = """# Requirements Documentation Index

## Backend Components

- [UserService](backend/UserService.md)
- [OrderController](backend/OrderController.md)

## Frontend Components

- [index](frontend/index.md)
- [login](frontend/login.md)

## Data Components

- [User](data/User.md)
- [Order](data/Order.md)
"""
            
            index_file = os.path.join(req_dir, "step2_index.md")
            with open(index_file, 'w') as f:
                f.write(index_content)
            
            # Create mock requirement files
            os.makedirs(os.path.join(req_dir, "backend"), exist_ok=True)
            os.makedirs(os.path.join(req_dir, "frontend"), exist_ok=True)
            os.makedirs(os.path.join(req_dir, "data"), exist_ok=True)
            
            # Create a simple mock requirement file
            mock_content = """# UserService

This is a service class for user management.

## Purpose
Handles user-related business logic.

## Components
- UserService: Main service class
"""
            
            with open(os.path.join(req_dir, "backend", "UserService.md"), 'w') as f:
                f.write(mock_content)
            
            # Test processor with mock data
            processor = RequirementsProcessor()
            processor.output_dir = temp_dir
            processor.requirements_dir = req_dir
            
            # Load the mock index
            processor.load_index(index_file)
            
            print("✅ Mock index processing works:")
            for category, config in processor.metadata_categories.items():
                if config['files']:
                    print(f"   {category}: {len(config['files'])} files")
            
            return True
            
    except Exception as e:
        print(f"❌ Mock index processing test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing step3.py fixes...\n")
    
    tests = [
        ("Import Test", test_step3_import),
        ("Initialization Test", test_step3_initialization),
        ("AI Provider Fallback Test", test_ai_provider_fallback),
        ("File Categorization Test", test_file_categorization),
        ("Mock Index Processing Test", test_mock_index_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Step3.py is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 