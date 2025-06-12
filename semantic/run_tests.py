#!/usr/bin/env python3
import pytest
import sys
import os

def main():
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Run tests with coverage
    pytest_args = [
        "--verbose",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "tests/"
    ]
    
    return pytest.main(pytest_args)

if __name__ == "__main__":
    sys.exit(main()) 