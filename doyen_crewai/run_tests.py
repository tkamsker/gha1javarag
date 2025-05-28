#!/usr/bin/env python3

import os
import sys
import logging
import pytest
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_tests():
    """Run all tests in the tests directory."""
    try:
        # Get the directory containing this script
        script_dir = Path(__file__).parent.absolute()
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Add the src directory to Python path
        src_path = script_dir / 'src'
        sys.path.insert(0, str(src_path))
        
        logger.info("Starting test suite...")
        
        # Run pytest with verbosity and show local variables on failure
        result = pytest.main([
            'tests',
            '-v',
            '--tb=short',
            '--showlocals',
            '--capture=no'
        ])
        
        if result == 0:
            logger.info("All tests passed successfully!")
        else:
            logger.error(f"Tests failed with exit code {result}")
            sys.exit(result)
            
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_tests() 