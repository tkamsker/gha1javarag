#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Ensure project root on path
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("rerun_full_cycle")


def run_cmd(args: list, env: dict | None = None) -> int:
    print(f"$ {' '.join(args)}")
    return subprocess.call(args, env=env or os.environ.copy())


def main():
    parser = argparse.ArgumentParser(description="Automate seeding, full pipeline run, and diagnosis for a project.")
    parser.add_argument("--project", default="cuco-ui-cct-common", help="Project to diagnose/seed")
    parser.add_argument("--seed", type=int, default=0, help="Number of seed objects to insert (0 to skip seeding)")
    parser.add_argument("--vectorizer", choices=["none", "text2vec-ollama"], default="none", help="Collection vectorizer for seeding")
    parser.add_argument("--recreate", action="store_true", help="If set, recreate collection before seeding")
    parser.add_argument("--embed", action="store_true", help="If set, generate embeddings for seed inserts (vectorizer=none)")
    parser.add_argument("--preview", type=int, default=5, help="Diagnosis preview count")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validate_setup step")
    parser.add_argument("--skip-pipeline", action="store_true", help="Skip pipeline run")
    args = parser.parse_args()

    # Ensure output/log dirs
    Config.ensure_output_dirs()
    logs_dir = Config.OUTPUT_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    full_log = logs_dir / "full_cycle.log"

    # Seeding (optional)
    if args.seed > 0:
        seed_cmd = [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "seed_weaviate.py"),
            "--project", args.project,
            "--count", str(args.seed),
            "--vectorizer", args.vectorizer,
        ]
        if args.recreate:
            seed_cmd.append("--recreate")
        if args.embed:
            seed_cmd.extend(["--embed", "--embed-text", "filePath extractedInfo"])
        code = run_cmd(seed_cmd)
        if code != 0:
            print("Seeding failed; aborting.")
            return code

    # Validate (optional)
    if not args.skip_validate:
        code = run_cmd([sys.executable, str(PROJECT_ROOT / "validate_setup.py")])
        if code != 0:
            print("Validation reported issues; continuing anyway.")

    # Pipeline run (optional)
    if not args.skip_pipeline:
        env = os.environ.copy()
        env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
        env.setdefault("FORCE_MULTIPROJECT_DISCOVERY", "true")
        env.setdefault("JAVA_INCLUDE_GLOBS", "**/*.java")
        env.setdefault("JSP_INCLUDE_GLOBS", "**/*.jsp,**/*.jspf")
        env.setdefault("JS_INCLUDE_GLOBS", "**/*.js")
        env.setdefault("GWT_INCLUDE_GLOBS", "**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java")
        env.setdefault("HTML_INCLUDE_GLOBS", "**/*.htm,**/*.html")
        env.setdefault("XML_INCLUDE_GLOBS", "**/*.xml,**/*.xhtml")
        env.setdefault("SQL_INCLUDE_GLOBS", "**/*.sql")
        env.setdefault("LOG_LEVEL", env.get("LOG_LEVEL", "INFO"))

        print("[rerun_full_cycle] Running pipeline (this may take a while)...")
        with open(full_log, "w", encoding="utf-8") as f:
            proc = subprocess.Popen([sys.executable, str(PROJECT_ROOT / "main.py")], env=env, stdout=f, stderr=subprocess.STDOUT)
            proc.wait()
            if proc.returncode != 0:
                print(f"Pipeline exited with code {proc.returncode}; see {full_log}")
            else:
                print(f"Pipeline completed. Logs at: {full_log}")

    # Diagnosis
    diag_cmd = [
        sys.executable, str(PROJECT_ROOT / "scripts" / "diagnose_weaviate.py"),
        "--project", args.project,
        "--preview", str(args.preview)
    ]
    run_cmd(diag_cmd)

    print("\n[rERUN SUMMARY]")
    print(f"  Logs: {full_log}")
    print(f"  Outputs: {Config.OUTPUT_DIR}/*/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
