Guide: Clearing Weaviate & Running cuco-ui-admin Pipeline

  Part 1: How to Clear Weaviate

  You have two options to clear Weaviate data:

  Option 1: Using the clean command (Recommended)

  ./docker-weaviate.sh clean

  This will:
  - Stop the Weaviate container
  - Remove all data from weaviate-data/ directory
  - Ask for confirmation before proceeding

  Option 2: Manual cleanup

  # Stop Weaviate
  ./docker-weaviate.sh stop

  # Remove all data
  rm -rf weaviate-data/*

  # Restart Weaviate
  ./docker-weaviate.sh start


  ######
   Complete Guide Created! ✅

  I've created two files to help you run the pipeline for cuco-ui-admin:

  1. run-cuco.sh - Dedicated Pipeline Script

  A dedicated script specifically for the cuco-ui-admin project that you can run in a separate terminal.

  Features:
  - ✅ Pre-flight checks (Ollama and Weaviate running)
  - ✅ Confirmation before starting
  - ✅ Progress tracking with colored output
  - ✅ Duration timing
  - ✅ Clear next steps after completion

  Usage:
  # Using .env configuration
  ./run-cuco.sh

  # Or specify path directly
  ./run-cuco.sh /path/to/cuco-ui-admin

  2. CUCO-QUICKSTART.md - Complete Reference Guide

  A comprehensive guide with:
  - How to clear Weaviate data
  - Terminal setup recommendations
  - Step-by-step pipeline execution
  - Search and query examples
  - Troubleshooting tips
  - Performance optimization

  ---
  Quick Commands Summary

  Clear Weaviate (Start Fresh)

  ./docker-weaviate.sh clean

  Run Pipeline (3 Terminals)

  Terminal 1 - Ollama:
  ollama serve

  Terminal 2 - Weaviate:
  ./docker-weaviate.sh start

  Terminal 3 - Pipeline:
  source .venv/bin/activate
  ./run-cuco.sh /path/to/cuco-ui-admin
  ./run-cuco.sh /Users/thomaskamsker/Documents/Atom/vron.one/playground/java/cuco-ui-admin

  ---
  What to Expect

  For cuco-ui-admin (539 files):
  - Discovery: ~6 seconds
  - Extraction: ~15-30 minutes ⏱️ (AI analysis of each file)
  - Indexing: ~10-15 seconds
  - Total: ~2,167 artifacts indexed

  The extraction step takes time because each file is analyzed with AI to extract semantic information, GWT patterns, and relationships.

  You can monitor progress in real-time:
  tail -f data/extraction-cuco-ui-admin.jsonl | jq -r '.file_path'

  ---
  Both files are now in your repository and ready to use! 🎉

