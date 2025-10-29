#!/usr/bin/env python3
"""Validate setup and prerequisites before running the pipeline"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def check_imports():
    """Check if all required packages are installed"""
    print("Checking imports...")
    missing = []
    
    try:
        import crewai
        print("✓ crewai")
    except ImportError:
        missing.append("crewai")
        print("✗ crewai - missing")
    
    try:
        import ollama
        print("✓ ollama")
    except ImportError:
        missing.append("ollama")
        print("✗ ollama - missing")
    
    try:
        import weaviate
        print("✓ weaviate-client")
    except ImportError:
        missing.append("weaviate-client")
        print("✗ weaviate-client - missing")
    
    try:
        import dotenv
        print("✓ python-dotenv")
    except ImportError:
        missing.append("python-dotenv")
        print("✗ python-dotenv - missing")
    
    try:
        import httpx
        print("✓ httpx")
    except ImportError:
        missing.append("httpx")
        print("✗ httpx - missing")
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_config():
    """Check configuration"""
    print("\nChecking configuration...")
    try:
        from src.config import Config
        
        # Check source directory
        if not Config.JAVA_SOURCE_DIR.exists():
            print(f"⚠ Source directory does not exist: {Config.JAVA_SOURCE_DIR}")
            print("   Please update JAVA_SOURCE_DIR in .env file")
        else:
            print(f"✓ Source directory: {Config.JAVA_SOURCE_DIR}")
        
        # Check output directories
        Config.ensure_output_dirs()
        if Config.OUTPUT_DIR.exists():
            print(f"✓ Output directory: {Config.OUTPUT_DIR}")
        
        # Check Ollama config
        print(f"✓ Ollama model: {Config.OLLAMA_MODEL_NAME}")
        print(f"✓ Ollama URL: {Config.OLLAMA_BASE_URL}")
        
        # Check Weaviate config
        print(f"✓ Weaviate URL: {Config.WEAVIATE_URL}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_services():
    """Check if external services are accessible"""
    print("\nChecking external services...")
    from src.config import Config
    import httpx
    
    # Check Ollama
    try:
        ollama_url = f"{Config.OLLAMA_BASE_URL}/api/tags"
        response = httpx.get(ollama_url, timeout=5.0)
        if response.status_code == 200:
            print("✓ Ollama is accessible")
        else:
            print(f"⚠ Ollama returned status {response.status_code}")
    except Exception as e:
        print(f"⚠ Cannot connect to Ollama: {e}")
        print("   Make sure Ollama is running: ollama serve")
    
    # Check Weaviate
    try:
        weaviate_url = f"{Config.WEAVIATE_URL}/v1/.well-known/ready"
        response = httpx.get(weaviate_url, timeout=5.0)
        if response.status_code == 200:
            print("✓ Weaviate is accessible")
        else:
            print(f"⚠ Weaviate returned status {response.status_code}")
    except Exception as e:
        print(f"⚠ Cannot connect to Weaviate: {e}")
        print("   Make sure Weaviate is running via Docker")
    
    from src.config import Config
    return True

def check_code_structure():
    """Check if code structure is correct"""
    print("\nChecking code structure...")
    checks = [
        ("src/config.py", "Configuration module"),
        ("src/utils/logger.py", "Logger module"),
        ("src/utils/ollama_client.py", "Ollama client"),
        ("src/utils/weaviate_client.py", "Weaviate client"),
        ("src/agents/step1_agents.py", "Step 1 agents"),
        ("src/agents/step2_agents.py", "Step 2 agents"),
        ("src/agents/step3_agents.py", "Step 3 agents"),
        ("src/pipeline.py", "Pipeline orchestrator"),
        ("main.py", "Main entry point"),
    ]
    
    all_ok = True
    for path_str, name in checks:
        path = Path(path_str)
        if path.exists():
            print(f"✓ {name} ({path_str})")
        else:
            print(f"✗ {name} missing ({path_str})")
            all_ok = False
    
    return all_ok

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("Requirements Extraction Pipeline - Setup Validation")
    print("=" * 60)
    
    checks = [
        ("Code Structure", check_code_structure),
        ("Imports", check_imports),
        ("Configuration", check_config),
        ("External Services", check_services),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed! Ready to run the pipeline.")
        print("   Run: python main.py")
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    from src.config import Config
    sys.exit(main())

