#!/bin/bash

# Quick diagnostic script to check package installation

echo "=== Package Installation Diagnostic ==="
echo ""

echo "1. Check if package is installed:"
pip list | grep codeindex
echo ""

echo "2. Show package installation details:"
pip show codeindex
echo ""

echo "3. Check Python sys.path:"
python -c "import sys; print('\n'.join(sys.path))"
echo ""

echo "4. Check if src/codeindex exists:"
ls -la src/codeindex/ 2>&1 | head -10
echo ""

echo "5. Check site-packages for codeindex:"
find .venv/lib/python*/site-packages -name "*codeindex*" 2>/dev/null
echo ""

echo "6. Try direct import:"
python -c "import codeindex; print(codeindex.__file__)"
echo ""

echo "7. Check if using the .pth file method:"
find .venv/lib/python*/site-packages -name "*.pth" -exec grep -l codeindex {} \; 2>/dev/null
cat $(find .venv/lib/python*/site-packages -name "*.pth" -exec grep -l codeindex {} \; 2>/dev/null) 2>/dev/null
echo ""

echo "8. Manually test the import that's failing:"
python -c "import sys; print('Python:', sys.executable); sys.path.insert(0, 'src'); from codeindex.services.weaviate_client import WeaviateManager; print('SUCCESS')"
