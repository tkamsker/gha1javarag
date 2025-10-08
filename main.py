#!/usr/bin/env python3
"""
Main entry point for the Java/JSP/GWT/JS → PRD pipeline.
"""
import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run CLI
from cli import cli

if __name__ == "__main__":
    cli()
