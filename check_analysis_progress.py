#!/usr/bin/env python3
"""
Check Analysis Progress
View current status and partial results
"""

import asyncio
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def check_ollama_status():
    """Check if Ollama is responding"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    logger.info("✅ Ollama Status: Running")
                    logger.info(f"📊 Available models: {len(models)}")
                    for model in models:
                        if 'qwen' in model.lower():
                            logger.info(f"   🤖 {model} (READY)")
                        else:
                            logger.info(f"   📦 {model}")
                    return True
    except Exception as e:
        logger.error(f"❌ Ollama Status: Not responding ({e})")
        return False

def check_analysis_progress():
    """Check current analysis progress"""
    logger.info("🔍 Checking Analysis Progress...")
    
    # Check output directory
    output_dir = Path("output")
    if not output_dir.exists():
        logger.info("📁 No output directory found - analysis hasn't started yet")
        return
    
    # List recent files
    output_files = list(output_dir.glob("*.json")) + list(output_dir.glob("*.md"))
    
    if not output_files:
        logger.info("📄 No result files found yet")
        return
    
    # Show recent files
    recent_files = sorted(output_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    logger.info(f"📊 Found {len(recent_files)} result files:")
    for i, file_path in enumerate(recent_files[:5]):
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        size_kb = file_path.stat().st_size / 1024
        logger.info(f"   {i+1}. {file_path.name} ({size_kb:.1f}KB, {mtime.strftime('%H:%M:%S')})")
    
    # Show latest results preview
    latest_file = recent_files[0]
    logger.info(f"\n📋 Latest Result Preview: {latest_file.name}")
    logger.info("-" * 50)
    
    try:
        if latest_file.suffix == '.json':
            with open(latest_file, 'r') as f:
                data = json.load(f)
            
            if 'processing_stats' in data:
                stats = data['processing_stats']
                logger.info(f"📊 Files processed: {stats.get('processed_files', 0)}/{stats.get('total_files', 0)}")
                logger.info(f"⏱️ Processing time: {stats.get('processing_time', 0):.2f}s")
                
            if 'java_files_found' in data:
                logger.info(f"☕ Java files found: {data['java_files_found']}")
                logger.info(f"🧠 Files analyzed: {data.get('files_analyzed', 0)}")
                
        elif latest_file.suffix == '.md':
            with open(latest_file, 'r') as f:
                content = f.read()
            
            # Show first 500 characters
            preview = content[:500]
            logger.info(preview + "...")
            
    except Exception as e:
        logger.error(f"Could not read {latest_file}: {e}")

def show_java_files_discovered():
    """Show what Java files were discovered"""
    java_root_path = Path("/Users/thomaskamsker/Documents/Atom/vron.one/playground/java")
    
    if not java_root_path.exists():
        logger.error(f"❌ Java root path not found: {java_root_path}")
        return
    
    logger.info(f"\n🔍 Java Files in Repository: {java_root_path}")
    logger.info("-" * 60)
    
    java_files = list(java_root_path.rglob("*.java"))
    
    if not java_files:
        logger.info("❌ No Java files found!")
        return
    
    logger.info(f"📊 Total Java files discovered: {len(java_files)}")
    
    # Group by module
    modules = {}
    for java_file in java_files:
        for part in java_file.parts:
            if any(keyword in part for keyword in ['cuco', 'administration', 'framework']):
                if part not in modules:
                    modules[part] = []
                modules[part].append(java_file)
                break
    
    logger.info(f"📦 Modules found: {len(modules)}")
    
    for module, files in modules.items():
        logger.info(f"\n   🏢 {module}: {len(files)} files")
        for file_path in sorted(files)[:3]:  # Show first 3 files per module
            rel_path = file_path.relative_to(java_root_path)
            logger.info(f"      - {rel_path}")
        if len(files) > 3:
            logger.info(f"      ... and {len(files) - 3} more files")

def show_quick_stats():
    """Show quick statistics"""
    logger.info("\n📊 Quick Repository Statistics:")
    logger.info("-" * 40)
    
    java_root = Path("/Users/thomaskamsker/Documents/Atom/vron.one/playground/java")
    
    if java_root.exists():
        java_files = list(java_root.rglob("*.java"))
        xml_files = list(java_root.rglob("*.xml"))
        sql_files = list(java_root.rglob("*.sql"))
        
        logger.info(f"☕ Java files: {len(java_files)}")
        logger.info(f"📄 XML files: {len(xml_files)}")
        logger.info(f"🗃️ SQL files: {len(sql_files)}")
        
        # Estimate total size
        total_size = sum(f.stat().st_size for f in java_files if f.is_file())
        logger.info(f"💾 Total Java code size: {total_size / 1024 / 1024:.1f} MB")
    
    # Check if analysis is currently running
    import subprocess
    try:
        result = subprocess.run(['pgrep', '-f', 'python.*analysis'], capture_output=True, text=True)
        if result.returncode == 0:
            processes = result.stdout.strip().split('\n')
            logger.info(f"⚙️ Analysis processes running: {len(processes)}")
        else:
            logger.info("⚙️ No analysis processes currently running")
    except:
        pass

async def main():
    """Main function"""
    logger.info("🔍 Java Analysis Progress Checker")
    logger.info("=" * 50)
    
    # Check Ollama status
    await check_ollama_status()
    
    # Show repository stats
    show_quick_stats()
    
    # Show discovered Java files
    show_java_files_discovered()
    
    # Check analysis progress
    check_analysis_progress()
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Progress check complete!")
    
    # Instructions
    logger.info("\n💡 Next Steps:")
    logger.info("   • Wait for current analysis to complete (~5-10 more minutes)")
    logger.info("   • Or start a new analysis: python run_java_analysis_clean.py")
    logger.info("   • Check results in output/ directory")
    logger.info("   • Re-run this checker: python check_analysis_progress.py")

if __name__ == "__main__":
    asyncio.run(main())