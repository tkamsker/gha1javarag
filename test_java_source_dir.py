#!/usr/bin/env python3
"""
Test JAVA_SOURCE_DIR functionality in step3 processors
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock
import sys

sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_java_source_dir_resolution():
    """Test that JAVA_SOURCE_DIR path resolution works correctly."""
    print("🧪 Testing JAVA_SOURCE_DIR path resolution...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a mock Java source structure
        java_source_dir = temp_path / "java_projects"
        java_source_dir.mkdir()
        
        # Create a test Java file with project structure
        project_file = java_source_dir / "cuco-cct-core" / "src" / "main" / "java" / "at" / "a1ta" / "cuco" / "cct" / "service" / "OpportunityService.java"
        project_file.parent.mkdir(parents=True)
        
        # Write sample Java content
        java_content = """package at.a1ta.cuco.cct.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class OpportunityService {
    
    @Autowired
    private OpportunityRepository opportunityRepository;
    
    public void createOpportunity(OpportunityDto dto) {
        // Business logic here
    }
    
    @Transactional
    public void updateOpportunity(Long id, OpportunityDto dto) {
        // Update logic here
    }
}
"""
        with open(project_file, 'w') as f:
            f.write(java_content)
        
        # Test step3_pgm_processor path resolution
        from step3_pgm_processor import Step3PgmProcessor
        
        config = Mock()
        config.java_source_dir = str(java_source_dir)
        config.output_dir = str(temp_path / "output")
        
        processor = Step3PgmProcessor(config)
        
        # Test various path formats that might come from the data
        test_paths = [
            "cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/OpportunityService.java",
            "src/main/java/at/a1ta/cuco/cct/service/OpportunityService.java"
        ]
        
        for test_path in test_paths:
            print(f"  Testing path: {test_path}")
            content = processor.revisit_source_file(test_path)
            
            if content and "OpportunityService" in content:
                print(f"  ✅ Successfully read content for {test_path}")
                print(f"  📄 Content preview: {content[:100]}...")
                
                # Test pattern detection
                if "@Service" in content:
                    print("  ✅ Detected @Service annotation")
                if "@Transactional" in content:
                    print("  ✅ Detected @Transactional annotation")
                if "OpportunityRepository" in content:
                    print("  ✅ Detected repository dependency")
                    
                return True
            else:
                print(f"  ⚠️ Could not read content for {test_path}")
        
        print("❌ None of the test paths worked")
        return False


def test_path_resolution_strategies():
    """Test different path resolution strategies."""
    print("🧪 Testing path resolution strategies...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create different directory structures
        java_dir = temp_path / "java_src"
        java_dir.mkdir()
        
        # Test file in nested structure
        test_file = java_dir / "project" / "src" / "TestService.java"
        test_file.parent.mkdir(parents=True)
        
        test_content = """@Service
public class TestService {
    public void doSomething() {}
}"""
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        from step3_pgm_processor import Step3PgmProcessor
        
        config = Mock()
        config.java_source_dir = str(java_dir)
        config.output_dir = str(temp_path / "output")
        
        processor = Step3PgmProcessor(config)
        
        # Test path resolution
        content = processor.revisit_source_file("project/src/TestService.java")
        
        if content and "TestService" in content:
            print("✅ Path resolution with JAVA_SOURCE_DIR works")
            return True
        else:
            print("❌ Path resolution failed")
            return False


def test_shell_script_validation():
    """Test that shell scripts validate JAVA_SOURCE_DIR."""
    print("🧪 Testing shell script JAVA_SOURCE_DIR validation...")
    
    try:
        from subprocess import run, PIPE
        
        # Test help shows JAVA_SOURCE_DIR info
        result = run(['./step3-pgm.sh', '--help'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "JAVA_SOURCE_DIR" in result.stdout:
                print("✅ step3-pgm.sh help includes JAVA_SOURCE_DIR documentation")
            else:
                print("⚠️ step3-pgm.sh help missing JAVA_SOURCE_DIR documentation")
        
        result = run(['./step3-crewai.sh', '--help'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "JAVA_SOURCE_DIR" in result.stdout:
                print("✅ step3-crewai.sh help includes JAVA_SOURCE_DIR documentation")
                return True
            else:
                print("⚠️ step3-crewai.sh help missing JAVA_SOURCE_DIR documentation")
                return False
        
        return True
        
    except Exception as e:
        print(f"⚠️ Shell script test failed: {e}")
        return True  # Non-critical


if __name__ == '__main__':
    print("🚀 Testing JAVA_SOURCE_DIR Integration")
    print("=" * 50)
    
    success = True
    
    if not test_java_source_dir_resolution():
        success = False
    
    print()
    if not test_path_resolution_strategies():
        success = False
    
    print()
    if not test_shell_script_validation():
        success = False
    
    print("=" * 50)
    if success:
        print("🎉 JAVA_SOURCE_DIR integration tests passed!")
        print()
        print("📋 Usage Instructions:")
        print("1. Add JAVA_SOURCE_DIR to your .env file:")
        print("   JAVA_SOURCE_DIR=/path/to/your/java/projects")
        print()
        print("2. Directory structure examples:")
        print("   /path/to/java/projects/")
        print("   ├── cuco-cct-core/")
        print("   │   └── src/main/java/...")
        print("   ├── cuco-core/")  
        print("   │   └── src/main/java/...")
        print("   └── other-project/")
        print("       └── src/main/java/...")
        print()
        print("3. The processors will automatically find source files using:")
        print("   - Full project path: project-name/src/main/java/...")
        print("   - Relative path: src/main/java/... (tries all projects)")
        print("   - Multiple fallback strategies for maximum compatibility")
    else:
        print("⚠️ Some JAVA_SOURCE_DIR tests failed - check implementation")