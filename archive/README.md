# Archive Directory

This directory contains non-enhanced Weaviate scripts and legacy components that have been replaced by the enhanced Weaviate implementation.

## Structure

- **scripts/**: Legacy shell scripts using ChromaDB-based processing
  - Original Step1.sh, Step2.sh, Step3.sh (ChromaDB-based)
  - Step1_Enhanced.sh, Step2_Enhanced.sh, Step3_Enhanced.sh (ChromaDB-enhanced)
  - Legacy web interface scripts (fastapi_app.py, flask_app.py)
  - Utility scripts (kill_all_stepps_enhanced.sh, etc.)

- **src/**: Legacy Python processors and connectors
  - ChromaDB-based processors (main.py, enhanced_main.py, etc.)
  - ChromaDB connector (chromadb_connector.py)
  - Legacy requirement processors
  - Test and debug variants

- **docs/**: Legacy documentation
  - ChromaDB system analysis and workflow guides

- **tests/**: Legacy test files
  - ChromaDB functionality tests
  - Enhanced chunking and classification tests

## Current Focus

The main codebase now focuses on **Enhanced Weaviate** implementation:
- `Step1_Enhanced_Weaviate.sh`
- `Step2_Enhanced_Weaviate.sh` 
- `Step3_Enhanced_Weaviate.sh`
- `src/enhanced_weaviate_processor.py`
- `src/weaviate_connector.py`
- `src/weaviate_schemas.py`
- `src/weaviate_requirements_generator.py`

## Migration Notes

Files in this archive were moved on 2025-09-24 as part of the transition to focus exclusively on the enhanced Weaviate implementation. These files may still contain useful patterns or code that could be referenced if needed.