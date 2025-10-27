#!/usr/bin/env python3
"""
Test script for CrewAI requirements generation.
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from synth.crewai_requirements import CrewAIRequirementsGenerator
from config.settings import settings
import json

def test_crewai_requirements():
    """Test CrewAI requirements generation."""
    print("Testing CrewAI requirements generation...")
    
    # Load artifact context from build directory
    build_dir = settings.build_dir
    artifact_context = {}
    
    # Load some test artifacts
    mappings = {
        'dao_calls': ('java_calls', 'all_dao_calls.json'),
        'jsp_forms': ('jsp_forms', 'all_forms.json'),
        'backend_docs': ('backend_docs', 'all_backend_docs.json'),
        'gwt_uibinder': ('gwt_uibinder', 'all_uibinder.json'),
    }
    
    for key, (subdir, fname) in mappings.items():
        p = build_dir / subdir / fname
        if p.exists():
            with p.open('r', encoding='utf-8') as f:
                data = json.load(f)
                artifact_context[key] = data[:5]  # Just take first 5 for testing
                print(f"Loaded {len(artifact_context[key])} {key} artifacts")
        else:
            artifact_context[key] = []
    
    # Create generator
    generator = CrewAIRequirementsGenerator()
    
    # Generate requirements
    print(f"\nGenerating requirements for project 'test-project'...")
    output_files = generator.generate_requirements('test-project', artifact_context)
    
    print(f"\nGenerated {len(output_files)} files:")
    for file_path in output_files:
        print(f"  - {file_path}")
    
    return output_files

if __name__ == '__main__':
    try:
        files = test_crewai_requirements()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

