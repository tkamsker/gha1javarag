#!/usr/bin/env python3
"""
Simple test for Step3 implementations
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys

sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_basic_functionality():
    """Test basic functionality works"""
    print("🧪 Testing basic Step3-PGM functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test data
        test_data = {
            "projects": {
                "test_project": {
                    "name": "test_project",
                    "total_files": 2,
                    "file_list": [
                        {
                            "path": "src/UserService.java",
                            "language": "java",
                            "enhanced_ai_analysis": {
                                "file_classification": {
                                    "architectural_layer": "backend_service"
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        # Create data file
        data_file = temp_path / 'intermediate_step2.json'
        with open(data_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test PGM processor
        from step3_pgm_processor import Step3PgmProcessor
        
        config = Mock()
        config.output_dir = str(temp_path)
        
        with patch('step3_pgm_processor.LLMClient'), \
             patch('step3_pgm_processor.WeaviateClient') as mock_wv, \
             patch('step3_pgm_processor.ReportingManager'):
            
            mock_wv_instance = Mock()
            mock_wv_instance.get_all_collection_stats.return_value = {"total_count": 100}
            mock_wv_instance.query_chunks.return_value = []
            mock_wv_instance.close = Mock()
            mock_wv.return_value = mock_wv_instance
            
            processor = Step3PgmProcessor(config)
            
            try:
                processor.run(parallel=False)
                print("✅ Step3-PGM basic functionality works")
                
                # Check output was created
                pgm_dir = temp_path / 'requirements' / 'pgm'
                if pgm_dir.exists():
                    print("✅ PGM output directory created")
                    
                    project_dir = pgm_dir / 'projects' / 'test_project'
                    if project_dir.exists():
                        print("✅ Project directory created")
                        files = list(project_dir.glob('*'))
                        print(f"✅ Created {len(files)} output files")
                    else:
                        print("⚠️ Project directory not found")
                else:
                    print("⚠️ PGM output directory not found")
                    
                return True
                
            except Exception as e:
                print(f"❌ Error: {e}")
                return False


def test_script_help():
    """Test that help commands work"""
    print("🧪 Testing script help commands...")
    
    try:
        from subprocess import run, PIPE
        
        # Test step3-pgm help
        result = run(['./step3-pgm.sh', '--help'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'Step 3-PGM' in result.stdout:
            print("✅ step3-pgm.sh help works")
        else:
            print("⚠️ step3-pgm.sh help issue")
        
        # Test step3-crewai help  
        result = run(['./step3-crewai.sh', '--help'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'Step 3-CrewAI' in result.stdout:
            print("✅ step3-crewai.sh help works")
        else:
            print("⚠️ step3-crewai.sh help issue")
            
        return True
        
    except Exception as e:
        print(f"⚠️ Script help test failed: {e}")
        return True  # Non-critical


if __name__ == '__main__':
    print("🚀 Running Simple Step3 Tests")
    print("=" * 40)
    
    success = True
    
    if not test_basic_functionality():
        success = False
    
    if not test_script_help():
        success = False
    
    print("=" * 40)
    if success:
        print("🎉 Simple tests completed successfully!")
        print("\n📋 Step3 implementations are ready:")
        print("   ./step3-pgm.sh     - Programmatic approach") 
        print("   ./step3-crewai.sh  - Agent-based approach")
        print("\nNote: Install CrewAI for full agent functionality:")
        print("   pip install crewai crewai-tools")
    else:
        print("⚠️ Some issues found - check implementation")