#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

# Ensure project root on path
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]

TEMP_SRC_ROOT = PROJECT_ROOT / "data" / "build" / "middle_src"
LOGS_DIR = PROJECT_ROOT / "data" / "output" / "logs"


def find_java_files(root: Path, limit: int) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*.java"):
        files.append(p)
        if len(files) >= limit:
            break
    return files


def copy_files(files: List[Path], source_root: Path, dest_root: Path) -> None:
    for src in files:
        # Preserve relative structure if possible; fall back to flat copy
        try:
            rel = src.relative_to(source_root)
        except ValueError:
            rel = Path(src.name)
        dst = dest_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main():
    parser = argparse.ArgumentParser(description="Run a middle-size test: pick up to N Java files from two directories, then run the pipeline.")
    parser.add_argument("--dir1", required=True, help="First directory to sample Java files from")
    parser.add_argument("--dir2", required=True, help="Second directory to sample Java files from")
    parser.add_argument("--count", type=int, default=100, help="Total number of files to include (split evenly)")
    parser.add_argument("--log-level", default=os.environ.get("LOG_LEVEL", "INFO"), help="LOG_LEVEL for the run")
    parser.add_argument("--preview", type=int, default=5, help="Diagnosis preview count")
    parser.add_argument("--project", default=os.environ.get("PROJECT", ""), help="Optional project name to diagnose after run")
    args = parser.parse_args()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare temp source set
    if TEMP_SRC_ROOT.exists():
        shutil.rmtree(TEMP_SRC_ROOT)
    TEMP_SRC_ROOT.mkdir(parents=True, exist_ok=True)

    d1 = Path(args.dir1).resolve()
    d2 = Path(args.dir2).resolve()

    per_dir = max(1, args.count // 2)
    files1 = find_java_files(d1, per_dir)
    files2 = find_java_files(d2, args.count - len(files1))

    if not files1 and not files2:
        print("No Java files found in provided directories.")
        return 1

    # Attempt to use common ancestor as source_root to preserve structure
    try:
        common_root = Path(os.path.commonpath([str(d1), str(d2)]))
    except Exception:
        common_root = d1

    copy_files(files1, common_root, TEMP_SRC_ROOT)
    copy_files(files2, common_root, TEMP_SRC_ROOT)

    # Environment for run
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["FORCE_MULTIPROJECT_DISCOVERY"] = "true"
    env["JAVA_SOURCE_DIR"] = str(TEMP_SRC_ROOT)
    env["JAVA_INCLUDE_GLOBS"] = "**/*.java"
    env["JSP_INCLUDE_GLOBS"] = ""
    env["JS_INCLUDE_GLOBS"] = ""
    env["GWT_INCLUDE_GLOBS"] = ""
    env["HTML_INCLUDE_GLOBS"] = ""
    env["XML_INCLUDE_GLOBS"] = ""
    env["SQL_INCLUDE_GLOBS"] = ""
    env["LOG_LEVEL"] = args.log_level

    # Validate
    print("[run_middle] Validating setup...")
    subprocess.call([sys.executable, str(PROJECT_ROOT / "validate_setup.py")], env=env)

    # Run pipeline
    print("[run_middle] Running pipeline on sampled files...")
    with open(LOGS_DIR / "pipeline_middle.log", "w", encoding="utf-8") as f:
        proc = subprocess.Popen([sys.executable, str(PROJECT_ROOT / "main.py")], env=env, stdout=f, stderr=subprocess.STDOUT)
        proc.wait()
        print(f"[run_middle] Pipeline exit code: {proc.returncode}")

    # Optional diagnosis
    if args.project:
        print(f"[run_middle] Diagnosis for project: {args.project}")
        subprocess.call([sys.executable, str(PROJECT_ROOT / "scripts" / "diagnose_weaviate.py"), "--project", args.project, "--preview", str(args.preview)], env=env)

    print("[run_middle] Done. Logs at data/output/logs/pipeline_middle.log")
    return 0


if __name__ == "__main__":
    sys.exit(main())
