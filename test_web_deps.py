#!/usr/bin/env python3

"""
Test script to verify web dependencies are available
"""

def check_module(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def main():
    print("🔍 Checking web dependencies...")
    
    flask_available = check_module('flask')
    fastapi_available = check_module('fastapi')
    uvicorn_available = check_module('uvicorn')
    
    print(f"Flask: {'✅ Available' if flask_available else '❌ Not available'}")
    print(f"FastAPI: {'✅ Available' if fastapi_available else '❌ Not available'}")
    print(f"Uvicorn: {'✅ Available' if uvicorn_available else '❌ Not available'}")
    
    if not flask_available and not (fastapi_available and uvicorn_available):
        print("\n⚠️  No web framework is available.")
        print("Please install with: pip install flask fastapi uvicorn[standard]")
        print("Or run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ At least one web framework is available!")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)