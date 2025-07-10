#!/bin/bash

# Next Steps Helper Script
# Shows you what to do after implementing the enhanced classification system

echo "🎯 Enhanced AI Classification System - Next Steps"
echo "==============================================="

# Check if enhanced system has been run
if [ -f "output/enhanced_metadata.json" ]; then
    echo "✅ Enhanced Step1 has been completed!"
    echo ""
    echo "📊 Available Results:"
    
    if [ -f "output/enhanced_architecture_report.json" ]; then
        echo "  ✅ Architecture Report: output/enhanced_architecture_report.json"
    fi
    
    if [ -d "output/requirements_enhanced" ]; then
        echo "  ✅ Enhanced Requirements: output/requirements_enhanced/"
        echo "     - By Layer: output/requirements_enhanced/by_layer/"
        echo "     - By Component: output/requirements_enhanced/by_component/"
        echo "     - Analysis: output/requirements_enhanced/analysis/"
    fi
    
    echo ""
    echo "🔍 What you can do next:"
    echo ""
    echo "1. 📋 EXPLORE RESULTS:"
    echo "   ./start_web.sh                    # Start web interface for interactive exploration"
    echo "   cat output/enhanced_architecture_report.json | jq '.'  # View architecture summary"
    echo "   ls output/requirements_enhanced/by_layer/              # Browse layer requirements"
    echo ""
    echo "2. 🔧 OPTIONAL - RUN TRADITIONAL STEPS:"
    echo "   ./Step2.sh production             # Generate traditional requirements (StrictDoc)"
    echo "   ./Step3.sh production             # Generate modern requirements documentation"
    echo ""
    echo "3. 📈 ADVANCED ANALYSIS:"
    echo "   python test_chromadb_functionality.py  # Test ChromaDB semantic search"
    echo "   cd strictdoc && ./Web.sh              # View StrictDoc documentation"
    echo ""
    echo "4. 🎯 FOCUSED ANALYSIS (Debug Mode):"
    echo "   echo 'path/to/specific/file.java' > debug_files.txt"
    echo "   DEBUGFILE=debug_files.txt ./Step1_Enhanced.sh test"
    echo ""
    
else
    echo "⚠️  Enhanced Step1 has not been run yet!"
    echo ""
    echo "🚀 GETTING STARTED:"
    echo ""
    echo "1. 🔧 SETUP ENVIRONMENT:"
    echo "   # Copy and edit environment file"
    echo "   cp env.example .env"
    echo "   # Edit .env with your settings (AI provider, paths, etc.)"
    echo ""
    echo "2. 🧪 TEST THE SYSTEM:"
    echo "   python test_enhanced_classification.py  # Validate all components"
    echo ""
    echo "3. 🎯 RUN ENHANCED ANALYSIS:"
    echo "   ./Step1_Enhanced.sh production          # Full analysis (recommended)"
    echo "   ./Step1_Enhanced.sh test                # Fast test mode"
    echo "   ./Step1_Enhanced.sh emergency           # Conservative mode (slow but safe)"
    echo ""
    echo "4. 🎛️  AI PROVIDER OPTIONS:"
    echo "   # For OpenAI (requires API key):"
    echo "   export AI_PROVIDER=openai && export OPENAI_API_KEY=your-key"
    echo ""
    echo "   # For Anthropic (requires API key):"
    echo "   export AI_PROVIDER=anthropic && export ANTHROPIC_API_KEY=your-key"
    echo ""
    echo "   # For Ollama (local, free):"
    echo "   export AI_PROVIDER=ollama && export OLLAMA_MODEL_NAME=deepseek-r1:32b"
    echo "   # Make sure Ollama is running: ollama serve"
    echo ""
fi

echo ""
echo "📚 HELPFUL RESOURCES:"
echo "  - ENHANCED_WORKFLOW_GUIDE.md     # Comprehensive workflow guide"
echo "  - CLAUDE.md                      # Project documentation and commands"
echo "  - metadataimprove.md            # Implementation plan details"
echo "  - README.md                     # Basic usage instructions"
echo ""

# Check system status
echo "🔍 SYSTEM STATUS:"

# Check if required directories exist
if [ -d "src" ]; then
    echo "  ✅ Source code directory exists"
else
    echo "  ❌ Source code directory missing"
fi

# Check if AI providers are configured
if [ -n "$OPENAI_API_KEY" ]; then
    echo "  ✅ OpenAI API key configured"
elif [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "  ✅ Anthropic API key configured"
elif command -v ollama &> /dev/null; then
    echo "  ✅ Ollama available (local AI)"
else
    echo "  ⚠️  No AI provider configured"
fi

# Check if ChromaDB data exists
if [ -d "data/chromadb" ] && [ "$(ls -A data/chromadb 2>/dev/null)" ]; then
    echo "  ✅ ChromaDB data exists"
else
    echo "  ⚠️  No ChromaDB data found"
fi

echo ""
echo "💡 QUICK START:"
echo "   If this is your first time, run: ./Step1_Enhanced.sh test"
echo "   For production analysis, run: ./Step1_Enhanced.sh production"
echo ""