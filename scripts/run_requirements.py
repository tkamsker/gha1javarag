#!/usr/bin/env python3
"""
Script to run the requirements generation process.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.cli import cli

if __name__ == '__main__':
    cli(['requirements'])
