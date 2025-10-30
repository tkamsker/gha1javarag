#!/usr/bin/env python3
"""Dry run of the pipeline - shows what will be processed without actually running"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.agents.step1_agents import SourceReaderTool
from src.utils.logger import setup_logger

logger = setup_logger("dry_run")


def main():
    """Run a dry run to see what files will be processed"""
    print("=" * 80)
    print("DRY RUN: Requirements Extraction Pipeline")
    print("=" * 80)
    print(f"\nSource Directory: {Config.JAVA_SOURCE_DIR}")
    print(f"Output Directory: {Config.OUTPUT_DIR}")
    print(f"Build Directory: {Config.BUILD_DIR}")
    
    print("\n" + "=" * 80)
    print("Step 1: Discovering source files...")
    print("=" * 80)
    
    source_reader = SourceReaderTool()
    discovery_result = source_reader._run(str(Config.JAVA_SOURCE_DIR))
    
    projects = discovery_result.get("projects", {})
    total_files = discovery_result.get("total_files", 0)
    
    print(f"\nFound {len(projects)} project(s) with {total_files} total file(s)\n")
    
    for project_name, files in projects.items():
        print(f"\nProject: {project_name}")
        print(f"  Files: {len(files)}")
        
        # Count by type
        file_types = {}
        for file_info in files:
            file_type = file_info.get("type", "unknown")
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        print("  Breakdown by type:")
        for file_type, count in sorted(file_types.items()):
            print(f"    {file_type}: {count}")
        
        # Show first few files as examples
        print(f"\n  Sample files (first 5):")
        for file_info in files[:5]:
            rel_path = file_info.get("relative_path", file_info.get("path", ""))
            print(f"    - {rel_path} ({file_info.get('type', 'unknown')})")
        
        if len(files) > 5:
            print(f"    ... and {len(files) - 5} more files")
    
    print("\n" + "=" * 80)

    # Write machine-readable check report
    try:
        from pathlib import Path
        import json
        Config.BUILD_DIR.mkdir(parents=True, exist_ok=True)
        check = {
            "sourceDir": str(Config.JAVA_SOURCE_DIR),
            "projectCount": len(projects),
            "totalFiles": total_files,
            "projects": {}
        }
        for project_name, files in projects.items():
            types = {}
            for f in files:
                t = f.get("type", "unknown")
                types[t] = types.get(t, 0) + 1
            check["projects"][project_name] = {
                "fileCount": len(files),
                "byType": types,
                "sample": files[:10]
            }
        (Config.BUILD_DIR / "source_check.json").write_text(json.dumps(check, indent=2), encoding='utf-8')
        print(f"Wrote discovery report to {Config.BUILD_DIR / 'source_check.json'}")
    except Exception as e:
        print(f"Could not write source_check.json: {e}")
    print("Estimated Processing Time")
    print("=" * 80)
    print("\nNote: This is a rough estimate. Actual time depends on:")
    print("  - File sizes (larger files take longer)")
    print("  - LLM processing speed")
    print("  - Network latency")
    print("\nRough estimates:")
    print(f"  Step 1 (Extraction): ~{total_files * 2}-{total_files * 10} seconds")
    print(f"  Step 2 (Analysis): ~{len(projects) * 30}-{len(projects) * 120} seconds")
    print(f"  Step 3 (Requirements): ~{len(projects) * 60}-{len(projects) * 180} seconds")
    print(f"\n  Total estimated: ~{(total_files * 5 + len(projects) * 90) / 60:.1f} minutes")
    
    print("\n" + "=" * 80)
    print("Output Structure Preview")
    print("=" * 80)
    print("\ndata/output/")
    for project_name in projects.keys():
        print(f"  {project_name}/")
        print(f"    requirements.md")
        print(f"    requirements_json.json")
        print(f"    mapping.md")
    print("  logs/")
    print("    pipeline.log")
    
    print("\n" + "=" * 80)
    print("Ready to run?")
    print("=" * 80)
    print("\nIf everything looks correct, run:")
    print("  python main.py")
    print("\nTo monitor progress:")
    print("  tail -f data/output/logs/pipeline.log")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDry run cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during dry run: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

